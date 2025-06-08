#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Connectivity Checker for Wastewater Treatment Plant
--------------------------------------------------
This utility verifies network connectivity with system components
and validates communication settings.
"""

import os
import sys
import configparser
import socket
import subprocess
import time
import json
import re
import platform
from datetime import datetime


class ConnectivityChecker:
    """Checks network connectivity and communication settings for WWTP components."""
    
    def __init__(self, project_root):
        self.project_root = project_root
        self.plc_config = None
        self.results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'system': platform.system(),
            'hostname': socket.gethostname(),
            'tests': {}
        }
        self.devices = {}
        self.all_passed = True
    
    def load_plc_config(self):
        """Load PLC configuration information."""
        try:
            config = configparser.ConfigParser()
            config.read(os.path.join(self.project_root, 'config', 'plc_config.ini'))
            self.plc_config = config
            
            # Extract device information
            if 'PLC' in config:
                plc_section = config['PLC']
                self.devices['main_plc'] = {
                    'ip': plc_section.get('ip', ''),
                    'type': plc_section.get('type', 'Unknown PLC'),
                    'rack': plc_section.get('rack', '0'),
                    'slot': plc_section.get('slot', '0')
                }
            
            # Check for other networked devices
            if 'HMI' in config:
                hmi_section = config['HMI']
                if 'server' in hmi_section and 'port' in hmi_section:
                    self.devices['hmi_server'] = {
                        'server': hmi_section.get('server', ''),
                        'port': hmi_section.get('port', '4840')
                    }
            
            return True
        except Exception as e:
            self.results['error'] = f"Failed to load PLC config: {str(e)}"
            return False
    
    def test_ping(self, ip_address, device_name):
        """Test ping connectivity to a device."""
        result = {
            'device': device_name,
            'ip': ip_address,
            'status': 'failed',
            'latency_ms': None,
            'packet_loss': None,
            'details': ''
        }
        
        try:
            # Determine ping command parameters based on OS
            if platform.system().lower() == "windows":
                # Windows ping with 4 packets, 1 second timeout
                cmd = ['ping', '-n', '4', '-w', '1000', ip_address]
            else:
                # Linux/Unix ping with 4 packets, 1 second timeout
                cmd = ['ping', '-c', '4', '-W', '1', ip_address]
            
            # Execute ping command
            ping_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
            
            # Check if ping was successful
            if "TTL=" in ping_output or "ttl=" in ping_output:
                result['status'] = 'passed'
                
                # Try to extract ping statistics (this is OS-dependent)
                # Extract latency
                latency_match = re.search(r'Average\s*=\s*(\d+)ms|min/avg/max.*\s=\s[\d.]+/([\d.]+)/[\d.]+', ping_output)
                if latency_match:
                    result['latency_ms'] = float(latency_match.group(1) if latency_match.group(1) else latency_match.group(2))
                
                # Extract packet loss
                loss_match = re.search(r'(\d+)%\s+packet\s+loss', ping_output)
                if loss_match:
                    result['packet_loss'] = int(loss_match.group(1))
                    if result['packet_loss'] > 0:
                        result['details'] = f"Warning: {result['packet_loss']}% packet loss detected"
            else:
                result['status'] = 'failed'
                result['details'] = "No response received"
                
            result['raw_output'] = ping_output
        except subprocess.CalledProcessError:
            result['status'] = 'failed'
            result['details'] = "Ping request failed"
        except Exception as e:
            result['status'] = 'error'
            result['details'] = str(e)
        
        return result
    
    def test_port(self, ip_address, port, device_name, service_name=""):
        """Test TCP connectivity to a specific port."""
        result = {
            'device': device_name,
            'ip': ip_address,
            'port': port,
            'service': service_name,
            'status': 'failed',
            'response_time_ms': None,
            'details': ''
        }
        
        try:
            # Try to connect to the port
            start_time = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)  # 2 second timeout
            
            conn_result = s.connect_ex((ip_address, int(port)))
            end_time = time.time()
            
            # Check result
            if conn_result == 0:
                result['status'] = 'passed'
                result['response_time_ms'] = round((end_time - start_time) * 1000, 2)
                result['details'] = "Port is open"
            else:
                result['status'] = 'failed'
                result['details'] = f"Port is closed (Error: {conn_result})"
            
            s.close()
        except socket.gaierror:
            result['status'] = 'error'
            result['details'] = "Address resolution failed"
        except socket.timeout:
            result['status'] = 'timeout'
            result['details'] = "Connection timed out"
        except Exception as e:
            result['status'] = 'error'
            result['details'] = str(e)
        
        return result
    
    def check_main_plc(self):
        """Check connectivity to the main PLC."""
        if 'main_plc' not in self.devices or not self.devices['main_plc']['ip']:
            self.results['tests']['main_plc'] = {
                'status': 'skipped',
                'details': "PLC IP address not specified in configuration"
            }
            return False
        
        plc = self.devices['main_plc']
        plc_ip = plc['ip']
        plc_type = plc['type']
        
        # Perform ping test
        ping_result = self.test_ping(plc_ip, f"Main PLC ({plc_type})")
        self.results['tests']['main_plc_ping'] = ping_result
        
        # Set main test result based on ping
        plc_connected = ping_result['status'] == 'passed'
        
        # If ping succeeds, check commonly used PLC ports
        if plc_connected:
            # Port tests to run based on PLC type
            port_tests = []
            
            # Common PLC ports by type
            if 'siemens' in plc_type.lower():
                # Siemens S7 Communication
                port_tests.append((102, "S7 Communication"))
                
                # OPC UA if specified
                if 'hmi_server' in self.devices and self.devices['hmi_server']['server'].lower() == 'opc ua':
                    port_tests.append((4840, "OPC UA"))
                    
            elif 'allen' in plc_type.lower() or 'bradley' in plc_type.lower():
                # Allen-Bradley EtherNet/IP
                port_tests.append((44818, "EtherNet/IP"))
                
            elif 'modbus' in plc_type.lower():
                # Modbus TCP
                port_tests.append((502, "Modbus TCP"))
                
            elif 'bacnet' in plc_type.lower():
                # BACnet/IP
                port_tests.append((47808, "BACnet/IP"))
                
            else:
                # Generic tests for unknown PLC types
                port_tests.extend([
                    (80, "HTTP"),
                    (443, "HTTPS"),
                    (502, "Modbus TCP"),
                    (4840, "OPC UA")
                ])
            
            # Run port tests
            port_results = []
            for port, service in port_tests:
                port_result = self.test_port(plc_ip, port, f"Main PLC ({plc_type})", service)
                port_results.append(port_result)
                test_key = f"main_plc_port_{port}"
                self.results['tests'][test_key] = port_result
                
            # Check if any port tests passed
            any_ports_open = any(r['status'] == 'passed' for r in port_results)
            
            if not any_ports_open and port_tests:
                ping_result['details'] += " (Warning: Device pingable but no tested ports are open)"
        
        # Update all_passed flag
        if not plc_connected:
            self.all_passed = False
            
        return plc_connected
    
    def check_hmi_server(self):
        """Check connectivity to the HMI server if configured."""
        if 'hmi_server' not in self.devices:
            return True  # Not a failure if HMI isn't defined
        
        hmi = self.devices['hmi_server']
        server_type = hmi.get('server', 'Unknown')
        port = hmi.get('port', '4840')
        
        # Handle different HMI server types
        if server_type.lower() == 'opc ua':
            # For OPC UA, check if we can connect to the PLC's OPC UA port
            if 'main_plc' in self.devices and self.devices['main_plc']['ip']:
                plc_ip = self.devices['main_plc']['ip']
                port_result = self.test_port(plc_ip, port, "HMI Server", "OPC UA")
                self.results['tests']['hmi_server'] = port_result
                
                if port_result['status'] != 'passed':
                    self.all_passed = False
                    
                return port_result['status'] == 'passed'
            else:
                self.results['tests']['hmi_server'] = {
                    'status': 'skipped',
                    'details': "OPC UA server check requires PLC IP address"
                }
                return True  # Not a failure
        else:
            # For other server types, just note that we can't test them
            self.results['tests']['hmi_server'] = {
                'status': 'skipped',
                'details': f"Testing for {server_type} server not implemented"
            }
            return True  # Not a failure
    
    def check_network_config(self):
        """Check if the network configuration is consistent."""
        result = {
            'status': 'passed',
            'issues': []
        }
        
        try:
            # Get our network information
            if platform.system().lower() == "windows":
                cmd = ['ipconfig', '/all']
            else:
                cmd = ['ifconfig', '-a']
                
            net_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
            
            # Check if PLC is on same subnet as any of our network interfaces
            if 'main_plc' in self.devices and self.devices['main_plc']['ip']:
                plc_ip = self.devices['main_plc']['ip']
                plc_subnet = self.devices['main_plc'].get('subnet', '')
                
                # Very basic check - see if our output contains the same subnet
                if plc_subnet and plc_subnet not in net_output:
                    result['status'] = 'warning'
                    result['issues'].append(f"PLC subnet ({plc_subnet}) not found in local network configuration")
                
                # Check if gateway is pingable
                gateway = self.devices['main_plc'].get('gateway', '')
                if gateway:
                    gateway_ping = self.test_ping(gateway, "Network Gateway")
                    self.results['tests']['gateway_ping'] = gateway_ping
                    
                    if gateway_ping['status'] != 'passed':
                        result['status'] = 'warning'
                        result['issues'].append("Cannot reach network gateway")
        except Exception as e:
            result['status'] = 'error'
            result['issues'].append(str(e))
        
        self.results['tests']['network_config'] = result
        return result['status'] == 'passed'
    
    def run_checks(self):
        """Run all connectivity checks."""
        self.load_plc_config()
        
        # Run connectivity tests
        self.check_main_plc()
        self.check_hmi_server()
        self.check_network_config()
        
        # Set overall status
        self.results['overall_status'] = 'passed' if self.all_passed else 'failed'
        
        return self.results
    
    def save_report(self, output_file):
        """Save results to a JSON report file."""
        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error saving report: {str(e)}")
            return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Check network connectivity for WWTP system')
    parser.add_argument('--project-root', '-p', type=str, default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')),
                        help='Path to project root directory')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='Output file path for JSON report')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print detailed test results')
    
    args = parser.parse_args()
    
    checker = ConnectivityChecker(args.project_root)
    results = checker.run_checks()
    
    # Print results
    print(f"\nConnectivity Check Results: {results['overall_status'].upper()}")
    print(f"System: {results['system']} ({results['hostname']})")
    print(f"Timestamp: {results['timestamp']}")
    print("-" * 50)
    
    # Print test results
    if args.verbose:
        for test_name, test_result in results['tests'].items():
            print(f"\n{test_name.replace('_', ' ').title()}:")
            
            if isinstance(test_result, dict) and 'status' in test_result:
                print(f"  Status: {test_result['status'].upper()}")
                
                for key, value in test_result.items():
                    if key not in ['status', 'raw_output']:
                        print(f"  {key.replace('_', ' ').title()}: {value}")
            else:
                print(f"  {test_result}")
    else:
        # Simple summary
        test_results = [r['status'] for r in results['tests'].values() if isinstance(r, dict) and 'status' in r]
        passed = test_results.count('passed')
        failed = test_results.count('failed')
        skipped = test_results.count('skipped')
        error = test_results.count('error')
        
        print(f"Tests: {len(test_results)} total, {passed} passed, {failed} failed, {error} errors, {skipped} skipped")
        
        # Show failed tests
        if failed > 0 or error > 0:
            print("\nFailed Tests:")
            for test_name, test_result in results['tests'].items():
                if isinstance(test_result, dict) and 'status' in test_result and test_result['status'] in ['failed', 'error']:
                    print(f"  - {test_name.replace('_', ' ').title()}: {test_result.get('details', '')}")
    
    # Save report if requested
    if args.output:
        if checker.save_report(args.output):
            print(f"\nReport saved to {args.output}")
        else:
            print(f"\nFailed to save report to {args.output}")
    
    # Exit with status code
    sys.exit(0 if results['overall_status'] == 'passed' else 1)
