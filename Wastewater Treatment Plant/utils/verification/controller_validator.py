#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Controller Validation Tool for Wastewater Treatment Plant
--------------------------------------------------------
This utility simulates and validates controller behavior under various conditions
to ensure correct operation of control algorithms.
"""

import os
import sys
import configparser
import json
import time
import random
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


class PIDController:
    """Simple PID controller for simulation purposes."""
    
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, setpoint=0.0, min_output=None, max_output=None):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.min_output = min_output
        self.max_output = max_output
        
        self.integral = 0
        self.previous_error = 0
        self.last_update_time = time.time()
    
    def compute(self, process_value):
        """Compute PID output."""
        # Calculate time since last update
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Avoid division by zero or extreme values
        if delta_time <= 0:
            delta_time = 0.1
        
        # Calculate error
        error = self.setpoint - process_value
        
        # Proportional term
        p_term = self.kp * error
        
        # Integral term
        self.integral += error * delta_time
        i_term = self.ki * self.integral
        
        # Derivative term (avoid spikes by using filtered derivative)
        d_term = 0
        if delta_time > 0:
            d_term = self.kd * (error - self.previous_error) / delta_time
        
        # Remember error for next iteration
        self.previous_error = error
        
        # Sum the terms
        output = p_term + i_term + d_term
        
        # Apply limits if specified
        if self.min_output is not None:
            output = max(output, self.min_output)
        if self.max_output is not None:
            output = min(output, self.max_output)
        
        return output
    
    def reset(self):
        """Reset controller state."""
        self.integral = 0
        self.previous_error = 0


class ProcessModel:
    """Simple first-order process model with optional disturbance and dead time."""
    
    def __init__(self, gain=1.0, time_constant=60.0, dead_time=0.0, initial_value=0.0):
        self.gain = gain
        self.time_constant = time_constant
        self.dead_time = dead_time
        
        self.value = initial_value
        self.input_history = [(0, 0)] if dead_time > 0 else []
        self.last_update_time = time.time()
    
    def update(self, input_value, disturbance=0.0, elapsed_time=None):
        """Update the process model with a new input."""
        current_time = time.time()
        dt = elapsed_time if elapsed_time is not None else (current_time - self.last_update_time)
        self.last_update_time = current_time
        
        # Handle dead time by storing inputs
        if self.dead_time > 0:
            # Store current input with timestamp
            self.input_history.append((current_time, input_value))
            
            # Find the effective input considering dead time
            effective_time = current_time - self.dead_time
            effective_input = 0
            
            # Find the closest input before the effective time
            for i in range(len(self.input_history) - 1, -1, -1):
                if self.input_history[i][0] <= effective_time:
                    effective_input = self.input_history[i][1]
                    break
            
            # Clean up old input history (keep last 100 entries at most)
            if len(self.input_history) > 100:
                # Find entries older than twice the dead time
                cutoff_time = current_time - (2 * self.dead_time)
                new_history = [entry for entry in self.input_history if entry[0] >= cutoff_time]
                self.input_history = new_history
                
            input_value = effective_input
        
        # First order response calculation
        response_rate = dt / self.time_constant
        if response_rate > 1.0:
            response_rate = 1.0  # Limit to stable value
            
        target = self.gain * input_value
        self.value += response_rate * (target - self.value)
        
        # Add disturbance
        self.value += disturbance
        
        return self.value


class ControllerValidator:
    """Validates WWTP controllers under various simulated conditions."""
    
    def __init__(self, project_root):
        self.project_root = project_root
        self.config = {}
        self.results = {}
        self.plots_directory = os.path.join(project_root, 'diagrams', 'validation')
    
    def load_config(self):
        """Load configuration values from the system config files."""
        try:
            # Load PLC config for controller settings
            plc_config = configparser.ConfigParser()
            plc_config.read(os.path.join(self.project_root, 'config', 'plc_config.ini'))
            
            # Load WWTP config for process parameters
            wwtp_config = configparser.ConfigParser()
            wwtp_config.read(os.path.join(self.project_root, 'config', 'wwtp_config.ini'))
            
            # Load PID parameters
            if 'PID_Parameters' in wwtp_config:
                self.config['pid_params'] = dict(wwtp_config['PID_Parameters'])
            
            # Load process parameters
            if 'Process_Parameters' in wwtp_config:
                self.config['process_params'] = dict(wwtp_config['Process_Parameters'])
            
            # Load tank parameters
            if 'Tank_Configuration' in wwtp_config:
                self.config['tank_params'] = dict(wwtp_config['Tank_Configuration'])
            
            # Ensure plots directory exists
            os.makedirs(self.plots_directory, exist_ok=True)
            
            return True
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return False
    
    def validate_ph_control(self):
        """Validate pH control loop performance."""
        result = {
            'controller_name': 'pH Control',
            'status': 'running',
            'test_cases': []
        }
        
        try:
            # Extract PID parameters for pH control
            pid_params = self.config.get('pid_params', {})
            ph_p = float(pid_params.get('ph_p', 5.0))
            ph_i = float(pid_params.get('ph_i', 0.2))
            ph_d = float(pid_params.get('ph_d', 1.0))
            
            # Get process parameters
            process_params = self.config.get('process_params', {})
            min_ph = float(process_params.get('minph', 6.0))
            max_ph = float(process_params.get('maxph', 9.0))
            optimum_ph = float(process_params.get('optimumph', 7.0))
            
            # Create controller and process model
            ph_controller = PIDController(
                kp=ph_p, ki=ph_i, kd=ph_d,
                setpoint=optimum_ph,
                min_output=-100.0, max_output=100.0
            )
            
            # pH process model (gain, time_constant, dead_time, initial_value)
            # Typical pH process is nonlinear, but we'll approximate it linearly here
            ph_process = ProcessModel(gain=0.01, time_constant=120.0, dead_time=10.0, initial_value=7.5)
            
            # Test case 1: Standard setpoint tracking
            case1 = self._run_setpoint_tracking_test(
                ph_controller, ph_process, 
                [optimum_ph, optimum_ph - 0.5, optimum_ph + 0.5, optimum_ph],
                simulation_time=1800, # 30 minutes 
                step_interval=450,    # 7.5 minutes per step
                disturbances=[(600, 0.3), (1200, -0.2)],
                title="pH Control - Setpoint Tracking Test",
                y_label="pH",
                y_limits=(min_ph - 0.5, max_ph + 0.5)
            )
            result['test_cases'].append(case1)
            
            # Test case 2: Disturbance rejection
            ph_controller.reset()
            ph_process = ProcessModel(gain=0.01, time_constant=120.0, dead_time=10.0, initial_value=optimum_ph)
            
            case2 = self._run_disturbance_test(
                ph_controller, ph_process,
                simulation_time=1200,  # 20 minutes
                disturbances=[
                    (300, 0.5),   # pH increase at 5 min
                    (600, -1.0),  # pH decrease at 10 min
                    (900, 0.3)    # Small pH increase at 15 min
                ],
                title="pH Control - Disturbance Rejection Test",
                y_label="pH",
                y_limits=(min_ph - 0.5, max_ph + 0.5)
            )
            result['test_cases'].append(case2)
            
            # Assess overall performance
            overall_performance = self._assess_controller_performance(
                result['test_cases'], 
                max_steady_state_error=0.2,
                max_overshoot_percent=30.0
            )
            
            result.update(overall_performance)
            result['status'] = 'completed'
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        self.results['ph_control'] = result
        return result
    
    def validate_do_control(self):
        """Validate dissolved oxygen control loop performance."""
        result = {
            'controller_name': 'Dissolved Oxygen Control',
            'status': 'running',
            'test_cases': []
        }
        
        try:
            # Extract PID parameters for DO control
            pid_params = self.config.get('pid_params', {})
            do_p = float(pid_params.get('do_p', 10.0))
            do_i = float(pid_params.get('do_i', 0.1))
            do_d = float(pid_params.get('do_d', 1.0))
            
            # Get process parameters
            process_params = self.config.get('process_params', {})
            min_do = float(process_params.get('mindissolvedoxygen', 2.0))
            optimum_do = float(process_params.get('optimumdissolvedoxygen', 5.0))
            
            # Create controller and process model
            do_controller = PIDController(
                kp=do_p, ki=do_i, kd=do_d,
                setpoint=optimum_do,
                min_output=0.0, max_output=100.0
            )
            
            # DO process model
            # DO dynamics include relatively long time constants
            do_process = ProcessModel(gain=0.05, time_constant=300.0, dead_time=20.0, initial_value=min_do)
            
            # Test case 1: Setpoint tracking (startup to setpoint)
            case1 = self._run_setpoint_tracking_test(
                do_controller, do_process, 
                [optimum_do],
                simulation_time=2400,  # 40 minutes
                step_interval=2400,    # No step changes, just startup
                disturbances=[(1200, -0.5)],
                title="Dissolved Oxygen Control - Startup Test",
                y_label="DO (mg/L)",
                y_limits=(0, optimum_do * 1.5)
            )
            result['test_cases'].append(case1)
            
            # Test case 2: Load changes (simulates changing oxygen demand)
            do_controller.reset()
            do_process = ProcessModel(gain=0.05, time_constant=300.0, dead_time=20.0, initial_value=optimum_do)
            
            case2 = self._run_disturbance_test(
                do_controller, do_process,
                simulation_time=3600,  # 60 minutes
                disturbances=[
                    (600, -1.0),   # Increased oxygen demand (DO drop)
                    (1800, -1.5),  # Large oxygen demand (DO drop)
                    (2700, 1.0)    # Decreased oxygen demand (DO rise)
                ],
                title="Dissolved Oxygen Control - Load Change Test",
                y_label="DO (mg/L)",
                y_limits=(0, optimum_do * 1.5)
            )
            result['test_cases'].append(case2)
            
            # Assess overall performance
            overall_performance = self._assess_controller_performance(
                result['test_cases'], 
                max_steady_state_error=0.3,
                max_overshoot_percent=20.0
            )
            
            result.update(overall_performance)
            result['status'] = 'completed'
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        self.results['do_control'] = result
        return result
    
    def validate_flow_control(self):
        """Validate flow control loop performance."""
        result = {
            'controller_name': 'Flow Control',
            'status': 'running',
            'test_cases': []
        }
        
        try:
            # Extract PID parameters for flow control
            pid_params = self.config.get('pid_params', {})
            flow_p = float(pid_params.get('flow_p', 2.0))
            flow_i = float(pid_params.get('flow_i', 0.1))
            flow_d = float(pid_params.get('flow_d', 0.05))
            
            # Get process parameters
            process_params = self.config.get('process_params', {})
            max_flow_rate = float(process_params.get('maxflowrate', 600.0))
            
            # Create controller and process model
            setpoint_flow = max_flow_rate * 0.5  # 50% of max flow
            flow_controller = PIDController(
                kp=flow_p, ki=flow_i, kd=flow_d,
                setpoint=setpoint_flow,
                min_output=0.0, max_output=100.0
            )
            
            # Flow process model (fast dynamics)
            flow_process = ProcessModel(gain=max_flow_rate/100.0, time_constant=10.0, dead_time=2.0, initial_value=0.0)
            
            # Test case 1: Setpoint tracking (multiple flow rates)
            case1 = self._run_setpoint_tracking_test(
                flow_controller, flow_process, 
                [max_flow_rate * 0.5, max_flow_rate * 0.25, max_flow_rate * 0.75, max_flow_rate * 0.5],
                simulation_time=600,  # 10 minutes
                step_interval=150,    # 2.5 minutes per step
                disturbances=[],
                title="Flow Control - Setpoint Tracking Test",
                y_label="Flow Rate (m³/hr)",
                y_limits=(0, max_flow_rate * 1.2)
            )
            result['test_cases'].append(case1)
            
            # Test case 2: Pressure disturbance (simulates changes in inlet/outlet pressure)
            flow_controller.reset()
            flow_process = ProcessModel(gain=max_flow_rate/100.0, time_constant=10.0, dead_time=2.0, 
                                         initial_value=setpoint_flow)
            
            case2 = self._run_disturbance_test(
                flow_controller, flow_process,
                simulation_time=600,  # 10 minutes
                disturbances=[
                    (120, -max_flow_rate * 0.1),  # Pressure drop (flow drop)
                    (300, max_flow_rate * 0.15),  # Pressure increase (flow increase)
                    (450, -max_flow_rate * 0.05)  # Small pressure drop
                ],
                title="Flow Control - Pressure Disturbance Test",
                y_label="Flow Rate (m³/hr)",
                y_limits=(0, max_flow_rate * 1.2)
            )
            result['test_cases'].append(case2)
            
            # Assess overall performance
            overall_performance = self._assess_controller_performance(
                result['test_cases'], 
                max_steady_state_error=0.05,  # Tighter tolerance for flow control
                max_overshoot_percent=15.0
            )
            
            result.update(overall_performance)
            result['status'] = 'completed'
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        self.results['flow_control'] = result
        return result
    
    def _run_setpoint_tracking_test(self, controller, process, setpoints, simulation_time, step_interval, 
                                   disturbances=None, title="", y_label="", y_limits=None):
        """Run a setpoint tracking test and generate plots."""
        # Initialize results
        test_case = {
            'name': title,
            'type': 'setpoint_tracking',
            'duration_sec': simulation_time,
            'setpoints': setpoints,
            'disturbances': disturbances or [],
            'metrics': {}
        }
        
        # Data storage
        times = []
        setpoint_values = []
        process_values = []
        control_signals = []
        
        # Initial values
        current_time = 0
        current_setpoint_index = 0
        controller.setpoint = setpoints[0]
        setpoint_change_times = []
        
        # Disturbances dictionary for easy lookup
        disturbance_dict = {t: d for t, d in disturbances} if disturbances else {}
        
        # Simulation loop
        dt = 1.0  # 1 second time step
        while current_time <= simulation_time:
            # Check for setpoint change
            if (current_time > 0 and 
                current_time % step_interval == 0 and 
                current_setpoint_index < len(setpoints) - 1):
                current_setpoint_index += 1
                controller.setpoint = setpoints[current_setpoint_index]
                setpoint_change_times.append(current_time)
            
            # Calculate control signal
            control_signal = controller.compute(process.value)
            
            # Check for disturbance
            disturbance = disturbance_dict.get(current_time, 0.0)
            
            # Update process
            process_value = process.update(control_signal, disturbance, dt)
            
            # Store data
            times.append(current_time)
            setpoint_values.append(controller.setpoint)
            process_values.append(process_value)
            control_signals.append(control_signal)
            
            # Increment time
            current_time += dt
        
        # Calculate performance metrics
        metrics = {}
        
        # Calculate rise time, settling time, and overshoot for each setpoint change
        if setpoint_change_times:
            # Add the start time as a setpoint change
            all_change_times = [0] + setpoint_change_times
            
            for i, change_time in enumerate(all_change_times):
                # Define region of interest for this setpoint change
                next_change_idx = len(times)
                if i < len(all_change_times) - 1:
                    next_change_idx = times.index(all_change_times[i+1])
                
                region_times = times[times.index(change_time):next_change_idx]
                region_values = process_values[times.index(change_time):next_change_idx]
                region_setpoint = setpoints[i]
                
                if len(region_times) < 10:  # Need enough data points
                    continue
                
                # Get starting value
                initial_value = region_values[0]
                
                # Calculate setpoint change magnitude
                change_magnitude = abs(region_setpoint - initial_value)
                if change_magnitude < 0.001:  # Skip if negligible change
                    continue
                
                # Calculate rise time (10% to 90%)
                ten_percent_threshold = min(initial_value, region_setpoint) + 0.1 * change_magnitude
                ninety_percent_threshold = min(initial_value, region_setpoint) + 0.9 * change_magnitude
                
                # Find crossing times
                try:
                    if initial_value < region_setpoint:  # Increasing setpoint
                        time_10 = next((t for t, v in zip(region_times, region_values) 
                                     if v >= ten_percent_threshold), None)
                        time_90 = next((t for t, v in zip(region_times, region_values)
                                     if v >= ninety_percent_threshold), None)
                    else:  # Decreasing setpoint
                        time_10 = next((t for t, v in zip(region_times, region_values)
                                     if v <= ten_percent_threshold), None)
                        time_90 = next((t for t, v in zip(region_times, region_values)
                                     if v <= ninety_percent_threshold), None)
                    
                    rise_time = None if not (time_10 and time_90) else time_90 - time_10
                except:
                    rise_time = None
                
                # Calculate overshoot
                max_val = max(region_values) if initial_value < region_setpoint else min(region_values)
                overshoot = 0
                if initial_value < region_setpoint:
                    if max_val > region_setpoint:
                        overshoot = (max_val - region_setpoint) / change_magnitude * 100
                else:
                    if max_val < region_setpoint:
                        overshoot = (region_setpoint - max_val) / change_magnitude * 100
                
                # Calculate settling time (5% band)
                settling_band = 0.05 * change_magnitude
                settling_time = None
                
                try:
                    # Find the first index where the value is within the band and stays there
                    for j in range(len(region_values)):
                        if abs(region_values[j] - region_setpoint) <= settling_band:
                            # Check if it stays within band for the rest of the data
                            if all(abs(v - region_setpoint) <= settling_band for v in region_values[j:]):
                                settling_time = region_times[j] - change_time
                                break
                except:
                    settling_time = None
                
                # Calculate steady state error
                steady_state_error = None
                if len(region_values) > 10:
                    # Use the last 10% of values to determine steady state
                    steady_idx = int(len(region_values) * 0.9)
                    if steady_idx > 0:
                        steady_values = region_values[steady_idx:]
                        steady_state_value = sum(steady_values) / len(steady_values)
                        steady_state_error = abs(steady_state_value - region_setpoint)
                
                # Store metrics for this setpoint change
                setpoint_metrics = {
                    'setpoint': region_setpoint,
                    'rise_time_sec': rise_time,
                    'settling_time_sec': settling_time,
                    'overshoot_percent': overshoot,
                    'steady_state_error': steady_state_error
                }
                
                metrics[f'setpoint_change_{i+1}'] = setpoint_metrics
        
        # Store metrics in test case
        test_case['metrics'] = metrics
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
        
        # Process value and setpoint plot
        ax1.plot(times, process_values, 'b-', label='Process Value')
        ax1.plot(times, setpoint_values, 'r--', label='Setpoint')
        ax1.set_xlabel('Time (sec)')
        ax1.set_ylabel(y_label)
        ax1.set_title(title)
        ax1.grid(True)
        ax1.legend()
        
        # Mark disturbances
        if disturbances:
            for dist_time, _ in disturbances:
                ax1.axvline(x=dist_time, color='g', linestyle=':', alpha=0.5)
                ax1.text(dist_time, ax1.get_ylim()[0], 'Dist', 
                        rotation=90, va='bottom', ha='right', alpha=0.7)
        
        # Set y limits if provided
        if y_limits:
            ax1.set_ylim(y_limits)
        
        # Control signal plot
        ax2.plot(times, control_signals, 'k-', label='Control Signal')
        ax2.set_xlabel('Time (sec)')
        ax2.set_ylabel('Control Signal (%)')
        ax2.grid(True)
        ax2.set_ylim([-10, 110])  # Standard range for control signal
        
        # Save plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title.replace(' ', '_').lower()}_{timestamp}.png"
        filepath = os.path.join(self.plots_directory, filename)
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close(fig)
        
        test_case['plot_path'] = filepath
        
        return test_case
    
    def _run_disturbance_test(self, controller, process, simulation_time, disturbances, 
                             title="", y_label="", y_limits=None):
        """Run a disturbance rejection test and generate plots."""
        # Initialize results
        test_case = {
            'name': title,
            'type': 'disturbance_rejection',
            'duration_sec': simulation_time,
            'setpoint': controller.setpoint,
            'disturbances': disturbances,
            'metrics': {}
        }
        
        # Data storage
        times = []
        setpoint_values = []
        process_values = []
        control_signals = []
        
        # Disturbances dictionary for easy lookup
        disturbance_dict = {t: d for t, d in disturbances}
        
        # Simulation loop
        current_time = 0
        dt = 1.0  # 1 second time step
        
        while current_time <= simulation_time:
            # Calculate control signal
            control_signal = controller.compute(process.value)
            
            # Check for disturbance
            disturbance = disturbance_dict.get(current_time, 0.0)
            
            # Update process
            process_value = process.update(control_signal, disturbance, dt)
            
            # Store data
            times.append(current_time)
            setpoint_values.append(controller.setpoint)
            process_values.append(process_value)
            control_signals.append(control_signal)
            
            # Increment time
            current_time += dt
        
        # Calculate performance metrics for each disturbance
        metrics = {}
        
        for i, (dist_time, dist_value) in enumerate(disturbances):
            # Find the index for this disturbance
            try:
                dist_idx = times.index(dist_time)
                
                # Define region of interest after disturbance
                region_end_idx = len(times)
                if i < len(disturbances) - 1:
                    next_dist_time = disturbances[i+1][0]
                    region_end_idx = times.index(next_dist_time)
                
                region_times = times[dist_idx:region_end_idx]
                region_values = process_values[dist_idx:region_end_idx]
                
                if len(region_values) < 10:  # Need enough data points
                    continue
                
                # Calculate maximum deviation from setpoint
                max_deviation = max((abs(v - controller.setpoint) for v in region_values), default=0)
                
                # Calculate recovery time (when process value returns within 5% of setpoint)
                recovery_band = 0.05 * abs(controller.setpoint)
                recovery_time = None
                
                for j, v in enumerate(region_values[1:], start=1):
                    if abs(v - controller.setpoint) <= recovery_band:
                        # Check if it stays within band for at least 10 more values or to the end
                        future_vals = region_values[j:min(j+10, len(region_values))]
                        if all(abs(fv - controller.setpoint) <= recovery_band for fv in future_vals):
                            recovery_time = region_times[j] - dist_time
                            break
                
                # Integral of Absolute Error (IAE) after disturbance
                iae = sum(abs(v - controller.setpoint) for v in region_values)
                
                # Store metrics for this disturbance
                disturbance_metrics = {
                    'time_sec': dist_time,
                    'magnitude': dist_value,
                    'max_deviation': max_deviation,
                    'recovery_time_sec': recovery_time,
                    'IAE': iae
                }
                
                metrics[f'disturbance_{i+1}'] = disturbance_metrics
            except:
                # If there's an error calculating metrics for this disturbance, skip it
                continue
        
        # Store metrics in test case
        test_case['metrics'] = metrics
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
        
        # Process value and setpoint plot
        ax1.plot(times, process_values, 'b-', label='Process Value')
        ax1.plot(times, setpoint_values, 'r--', label='Setpoint')
        ax1.set_xlabel('Time (sec)')
        ax1.set_ylabel(y_label)
        ax1.set_title(title)
        ax1.grid(True)
        ax1.legend()
        
        # Mark disturbances
        for dist_time, dist_value in disturbances:
            ax1.axvline(x=dist_time, color='g', linestyle=':', alpha=0.5)
            direction = "+" if dist_value > 0 else "-"
            ax1.text(dist_time, ax1.get_ylim()[0], f'Dist{direction}', 
                    rotation=90, va='bottom', ha='right', alpha=0.7)
        
        # Set y limits if provided
        if y_limits:
            ax1.set_ylim(y_limits)
        
        # Control signal plot
        ax2.plot(times, control_signals, 'k-', label='Control Signal')
        ax2.set_xlabel('Time (sec)')
        ax2.set_ylabel('Control Signal (%)')
        ax2.grid(True)
        ax2.set_ylim([-10, 110])  # Standard range for control signal
        
        # Save plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title.replace(' ', '_').lower()}_{timestamp}.png"
        filepath = os.path.join(self.plots_directory, filename)
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close(fig)
        
        test_case['plot_path'] = filepath
        
        return test_case
    
    def _assess_controller_performance(self, test_cases, max_steady_state_error=0.1, max_overshoot_percent=20.0):
        """Assess controller performance based on test metrics."""
        assessment = {
            'passed': True,
            'performance_rating': 'Good',
            'issues': []
        }
        
        # Collect all metrics across test cases
        all_metrics = {}
        
        for test_case in test_cases:
            metrics = test_case.get('metrics', {})
            
            for key, value in metrics.items():
                # Split metrics by setpoint changes and disturbances
                if 'setpoint_change' in key:
                    if 'setpoint_changes' not in all_metrics:
                        all_metrics['setpoint_changes'] = []
                    all_metrics['setpoint_changes'].append(value)
                elif 'disturbance' in key:
                    if 'disturbances' not in all_metrics:
                        all_metrics['disturbances'] = []
                    all_metrics['disturbances'].append(value)
        
        # Assess setpoint tracking performance
        if 'setpoint_changes' in all_metrics:
            # Check steady state error
            errors = [m.get('steady_state_error') for m in all_metrics['setpoint_changes'] if m.get('steady_state_error') is not None]
            if errors:
                avg_error = sum(errors) / len(errors)
                if avg_error > max_steady_state_error:
                    assessment['passed'] = False
                    assessment['issues'].append(f"High steady state error: {avg_error:.3f}")
                
                # Good/Fair categorization
                if avg_error <= max_steady_state_error / 2:
                    assessment['steady_state_error_rating'] = 'Good'
                else:
                    assessment['steady_state_error_rating'] = 'Fair'
                
                # Record the metric
                assessment['avg_steady_state_error'] = avg_error
            
            # Check overshoot
            overshoots = [m.get('overshoot_percent') for m in all_metrics['setpoint_changes'] if m.get('overshoot_percent') is not None]
            if overshoots:
                max_overshoot = max(overshoots)
                if max_overshoot > max_overshoot_percent:
                    assessment['passed'] = False
                    assessment['issues'].append(f"High overshoot: {max_overshoot:.2f}%")
                
                # Good/Fair categorization
                if max_overshoot <= max_overshoot_percent / 2:
                    assessment['overshoot_rating'] = 'Good'
                else:
                    assessment['overshoot_rating'] = 'Fair'
                
                # Record the metric
                assessment['max_overshoot_percent'] = max_overshoot
        
        # Assess disturbance rejection
        if 'disturbances' in all_metrics:
            # Check recovery time
            recovery_times = [m.get('recovery_time_sec') for m in all_metrics['disturbances'] if m.get('recovery_time_sec') is not None]
            if recovery_times:
                avg_recovery = sum(recovery_times) / len(recovery_times)
                
                # Record the metric
                assessment['avg_recovery_time_sec'] = avg_recovery
                
                # Good/Fair categorization - this is subjective based on process dynamics
                if avg_recovery < 120:  # Assuming 2 minutes is good recovery
                    assessment['recovery_time_rating'] = 'Good'
                elif avg_recovery < 300:  # 5 minutes is fair
                    assessment['recovery_time_rating'] = 'Fair'
                else:
                    assessment['recovery_time_rating'] = 'Poor'
                    assessment['issues'].append(f"Slow disturbance recovery: {avg_recovery:.1f} seconds")
            
            # Check maximum deviations
            max_devs = [m.get('max_deviation') for m in all_metrics['disturbances'] if m.get('max_deviation') is not None]
            if max_devs:
                avg_max_dev = sum(max_devs) / len(max_devs)
                
                # Record the metric
                assessment['avg_max_deviation'] = avg_max_dev
        
        # Overall performance rating
        if assessment['passed'] and not assessment['issues']:
            assessment['performance_rating'] = 'Excellent'
        elif not assessment['passed'] and len(assessment['issues']) > 2:
            assessment['performance_rating'] = 'Poor'
        
        return assessment
    
    def run_all_validations(self):
        """Run all controller validations."""
        if not self.load_config():
            return {'error': 'Failed to load configuration'}
        
        self.validate_ph_control()
        self.validate_do_control()
        self.validate_flow_control()
        
        # Check overall results
        all_passed = True
        for controller_name, result in self.results.items():
            if result.get('status') != 'completed' or not result.get('passed', True):
                all_passed = False
                break
        
        # Generate summary
        summary = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'overall_status': 'passed' if all_passed else 'failed',
            'controllers_tested': len(self.results),
            'controllers_passed': sum(1 for r in self.results.values() if r.get('passed', True)),
            'details': self.results
        }
        
        return summary


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate WWTP controllers')
    parser.add_argument('--project-root', '-p', type=str, 
                       default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')),
                       help='Path to project root directory')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output file path for validation results')
    parser.add_argument('--controllers', '-c', type=str, default='all',
                       help='Comma-separated list of controllers to validate (ph,do,flow or all)')
    
    args = parser.parse_args()
    
    validator = ControllerValidator(args.project_root)
    
    # Determine which controllers to validate
    controllers = args.controllers.lower().split(',')
    if 'all' in controllers:
        results = validator.run_all_validations()
    else:
        validator.load_config()
        results = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        if 'ph' in controllers:
            results['ph_control'] = validator.validate_ph_control()
        
        if 'do' in controllers:
            results['do_control'] = validator.validate_do_control()
        
        if 'flow' in controllers:
            results['flow_control'] = validator.validate_flow_control()
    
    # Print summary
    print("\nController Validation Results:")
    print("=" * 40)
    
    if 'error' in results:
        print(f"Error: {results['error']}")
    else:
        print(f"Timestamp: {results.get('timestamp', 'Unknown')}")
        print(f"Overall Status: {results.get('overall_status', 'Unknown').upper()}")
        print(f"Controllers Tested: {results.get('controllers_tested', 'Unknown')}")
        print(f"Controllers Passed: {results.get('controllers_passed', 'Unknown')}")
        
        # Details for each controller
        for controller_name, result in results.get('details', {}).items():
            if controller_name.startswith('_'):  # Skip private fields
                continue
                
            print(f"\n{controller_name.replace('_', ' ').title()}:")
            print(f"  Status: {result.get('status', 'Unknown').upper()}")
            
            if 'performance_rating' in result:
                print(f"  Performance Rating: {result.get('performance_rating', 'Unknown')}")
            
            if 'issues' in result and result['issues']:
                print(f"  Issues:")
                for issue in result['issues']:
                    print(f"    - {issue}")
            
            if 'plot_path' in result:
                print(f"  Plot: {result.get('plot_path', 'Not generated')}")
    
    # Save results to file if requested
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {args.output}")
        except Exception as e:
            print(f"\nError saving results: {str(e)}")
            sys.exit(1)
