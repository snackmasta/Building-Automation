#!/usr/bin/env python3
"""
PLC Program Simulator
====================
This simulator mimics PLC execution for testing the Structured Text program.
It provides a simple console interface to simulate inputs and monitor outputs.
"""

import time
import threading
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any
import json

@dataclass
class PLCVariables:
    """Data class to hold all PLC variables"""
    # Inputs
    StartButton: bool = False
    StopButton: bool = False
    EmergencyStop: bool = False
    LevelSensor: bool = True  # Assume tank has liquid
    TempSensor: float = 20.0
    PressureSensor: float = 1.0
    
    # Outputs
    Pump: bool = False
    Heater: bool = False
    Valve1: bool = False
    Valve2: bool = False
    AlarmLight: bool = False
    StatusLight: bool = False
    
    # Internal variables
    SystemRunning: bool = False
    SystemReady: bool = False
    AlarmActive: bool = False
    CycleCount: int = 0
    
    # Setpoints
    SetTemperature: float = 75.0
    MaxPressure: float = 5.0
    TempTolerance: float = 2.0
    
    # Timers (simplified as counters)
    StartupTimer: int = 0
    HeatingTimer: int = 0
    PumpTimer: int = 0
    AlarmTimer: int = 0

class PLCSimulator:
    """Main PLC Simulator class"""
    
    def __init__(self):
        self.vars = PLCVariables()
        self.cycle_time = 0.1  # 100ms cycle time
        self.running = False
        self.cycle_count = 0
        
    def start_simulation(self):
        """Start the PLC simulation"""
        self.running = True
        print("=" * 50)
        print("PLC SIMULATOR STARTED")
        print("=" * 50)
        print("Cycle time: 100ms")
        print("Type 'help' for available commands")
        print("Type 'quit' to exit")
        print()
        
        # Start PLC scan thread
        plc_thread = threading.Thread(target=self._plc_scan_loop, daemon=True)
        plc_thread.start()
        
        # Start user interface
        self._user_interface()
    
    def _plc_scan_loop(self):
        """Main PLC scan loop - executes the control logic"""
        while self.running:
            start_time = time.time()
            
            # Execute main program logic
            self._execute_main_program()
            
            # Simulate physical process
            self._simulate_process()
            
            self.cycle_count += 1
            
            # Maintain cycle time
            elapsed = time.time() - start_time
            sleep_time = max(0, self.cycle_time - elapsed)
            time.sleep(sleep_time)
    
    def _execute_main_program(self):
        """Execute the main PLC program logic"""
        v = self.vars  # Shorthand reference
        
        # System safety checks
        v.SystemReady = (not v.EmergencyStop and 
                        v.LevelSensor and 
                        (v.PressureSensor < v.MaxPressure) and
                        not v.AlarmActive)
        
        # Start/Stop logic
        if v.StartButton and v.SystemReady and not v.SystemRunning:
            v.SystemRunning = True
            v.CycleCount += 1
            v.StartupTimer = 0  # Reset timer
            print(f"[{self._timestamp()}] SYSTEM STARTED - Cycle #{v.CycleCount}")
        
        if v.StopButton or v.EmergencyStop or v.AlarmActive:
            if v.SystemRunning:
                print(f"[{self._timestamp()}] SYSTEM STOPPED")
            v.SystemRunning = False
            v.StartButton = False  # Reset start button
        
        # Process control logic
        if v.SystemRunning:
            # Startup sequence
            v.StartupTimer += 1
            if v.StartupTimer >= 20:  # 2 seconds at 100ms cycle
                v.Valve1 = True
                
                # Start pump after valve opens
                v.PumpTimer += 1
                if v.PumpTimer >= 10:  # 1 second delay
                    v.Pump = True
                
                # Temperature control
                if v.TempSensor < (v.SetTemperature - v.TempTolerance):
                    v.Heater = True
                    v.HeatingTimer += 1
                elif v.TempSensor > (v.SetTemperature + v.TempTolerance):
                    v.Heater = False
                    v.HeatingTimer = 0
                
                # Process completion check
                if (v.TempSensor >= v.SetTemperature and 
                    v.HeatingTimer >= 300):  # 30 seconds heating
                    v.Valve2 = True
        else:
            # System stopped - reset outputs
            v.StartupTimer = 0
            v.PumpTimer = 0
            v.HeatingTimer = 0
            v.Pump = False
            v.Heater = False
            v.Valve1 = False
            v.Valve2 = False
        
        # Alarm logic
        alarm_conditions = (v.PressureSensor > v.MaxPressure or
                           v.TempSensor > 100.0 or
                           (v.SystemRunning and not v.LevelSensor))
        
        if alarm_conditions:
            v.AlarmTimer += 1
            if v.AlarmTimer >= 5:  # 500ms delay
                v.AlarmActive = True
                v.AlarmLight = True
                if v.SystemRunning:
                    print(f"[{self._timestamp()}] ALARM ACTIVATED - Emergency shutdown!")
        else:
            v.AlarmTimer = 0
            v.AlarmLight = False
        
        # Status indicators
        v.StatusLight = v.SystemReady and v.SystemRunning
        
        # Reset alarm when conditions clear and system stopped
        if not alarm_conditions and not v.SystemRunning:
            v.AlarmActive = False
        
        # Reset stop button
        v.StopButton = False
    
    def _simulate_process(self):
        """Simulate the physical process"""
        v = self.vars
        
        # Temperature simulation
        if v.Heater:
            # Heat up when heater is on
            v.TempSensor += 0.5
        else:
            # Cool down naturally
            if v.TempSensor > 20.0:
                v.TempSensor -= 0.2
        
        # Pressure simulation
        if v.Pump:
            # Pressure increases when pump runs
            if v.PressureSensor < 3.0:
                v.PressureSensor += 0.1
        else:
            # Pressure decreases when pump stops
            if v.PressureSensor > 0.5:
                v.PressureSensor -= 0.05
    
    def _user_interface(self):
        """Command line user interface"""
        while self.running:
            try:
                command = input("PLC> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    self.running = False
                    break
                elif command == 'help':
                    self._show_help()
                elif command == 'status':
                    self._show_status()
                elif command == 'inputs':
                    self._show_inputs()
                elif command == 'outputs':
                    self._show_outputs()
                elif command == 'start':
                    self.vars.StartButton = True
                elif command == 'stop':
                    self.vars.StopButton = True
                elif command == 'emergency':
                    self.vars.EmergencyStop = not self.vars.EmergencyStop
                    state = "ACTIVATED" if self.vars.EmergencyStop else "RESET"
                    print(f"Emergency stop {state}")
                elif command.startswith('temp '):
                    try:
                        temp = float(command.split()[1])
                        self.vars.TempSensor = temp
                        print(f"Temperature set to {temp}°C")
                    except (ValueError, IndexError):
                        print("Invalid temperature value")
                elif command.startswith('pressure '):
                    try:
                        pressure = float(command.split()[1])
                        self.vars.PressureSensor = pressure
                        print(f"Pressure set to {pressure} bar")
                    except (ValueError, IndexError):
                        print("Invalid pressure value")
                elif command == 'level':
                    self.vars.LevelSensor = not self.vars.LevelSensor
                    state = "HIGH" if self.vars.LevelSensor else "LOW"
                    print(f"Level sensor: {state}")
                elif command == '':
                    continue
                else:
                    print(f"Unknown command: {command}")
                    
            except KeyboardInterrupt:
                self.running = False
                break
            except EOFError:
                self.running = False
                break
    
    def _show_help(self):
        """Show available commands"""
        print("""
Available Commands:
==================
start           - Press start button
stop            - Press stop button  
emergency       - Toggle emergency stop
temp <value>    - Set temperature sensor value
pressure <value>- Set pressure sensor value
level           - Toggle level sensor
status          - Show system status
inputs          - Show all input values
outputs         - Show all output values
help            - Show this help
quit/exit       - Exit simulator
        """)
    
    def _show_status(self):
        """Show current system status"""
        v = self.vars
        print(f"""
System Status:
=============
Cycle Count: {self.cycle_count}
System Running: {v.SystemRunning}
System Ready: {v.SystemReady}
Alarm Active: {v.AlarmActive}
Production Cycles: {v.CycleCount}

Process Values:
Temperature: {v.TempSensor:.1f}°C (SP: {v.SetTemperature}°C)
Pressure: {v.PressureSensor:.1f} bar
Level Sensor: {'HIGH' if v.LevelSensor else 'LOW'}
        """)
    
    def _show_inputs(self):
        """Show all input values"""
        v = self.vars
        print(f"""
Input Status:
============
Start Button: {v.StartButton}
Stop Button: {v.StopButton}
Emergency Stop: {v.EmergencyStop}
Level Sensor: {v.LevelSensor}
Temperature: {v.TempSensor:.1f}°C
Pressure: {v.PressureSensor:.1f} bar
        """)
    
    def _show_outputs(self):
        """Show all output values"""
        v = self.vars
        print(f"""
Output Status:
=============
Pump: {v.Pump}
Heater: {v.Heater}
Valve 1 (Inlet): {v.Valve1}
Valve 2 (Outlet): {v.Valve2}
Alarm Light: {v.AlarmLight}
Status Light: {v.StatusLight}
        """)
    
    def _timestamp(self):
        """Get current timestamp"""
        return datetime.now().strftime("%H:%M:%S")

if __name__ == "__main__":
    simulator = PLCSimulator()
    try:
        simulator.start_simulation()
    except KeyboardInterrupt:
        pass
    finally:
        print("\nPLC Simulator stopped.")
