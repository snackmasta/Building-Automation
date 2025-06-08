#!/usr/bin/env python3
# Wastewater Treatment Plant - System Verification
# Checks the system integrity and validates components

import os
import sys
import time
import json
import subprocess
import configparser
from pathlib import Path

# Project root directory
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class SystemVerifier:
    def __init__(self):
        self.verification_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_status": "Unknown",
            "components": {},
            "errors": [],
            "warnings": []
        }
    
    def verify_file_exists(self, filepath, component, critical=True):
        """Verify that a file exists"""
        full_path = ROOT_DIR / filepath
        exists = full_path.exists()
        
        if not component in self.verification_results["components"]:
            self.verification_results["components"][component] = {
                "status": "Pass",
                "checks": []
            }
        
        result = {
            "check": f"File exists: {filepath}",
            "result": "Pass" if exists else "Fail",
            "critical": critical
        }
        
        self.verification_results["components"][component]["checks"].append(result)
        
        if not exists:
            if critical:
                self.verification_results["components"][component]["status"] = "Fail"
                self.verification_results["errors"].append(f"Missing critical file: {filepath}")
            else:
                self.verification_results["warnings"].append(f"Missing file: {filepath}")
        
        return exists
    
    def verify_directory_exists(self, dirpath, component, critical=True):
        """Verify that a directory exists"""
        full_path = ROOT_DIR / dirpath
        exists = full_path.is_dir()
        
        if not component in self.verification_results["components"]:
            self.verification_results["components"][component] = {
                "status": "Pass",
                "checks": []
            }
        
        result = {
            "check": f"Directory exists: {dirpath}",
            "result": "Pass" if exists else "Fail",
            "critical": critical
        }
        
        self.verification_results["components"][component]["checks"].append(result)
        
        if not exists:
            if critical:
                self.verification_results["components"][component]["status"] = "Fail"
                self.verification_results["errors"].append(f"Missing critical directory: {dirpath}")
            else:
                self.verification_results["warnings"].append(f"Missing directory: {dirpath}")
        
        return exists
    
    def verify_config_valid(self, config_path, component):
        """Verify that a configuration file is valid"""
        full_path = ROOT_DIR / config_path
        
        if not component in self.verification_results["components"]:
            self.verification_results["components"][component] = {
                "status": "Pass",
                "checks": []
            }
        
        if not full_path.exists():
            result = {
                "check": f"Config valid: {config_path}",
                "result": "Fail",
                "critical": True,
                "message": "File does not exist"
            }
            self.verification_results["components"][component]["checks"].append(result)
            self.verification_results["components"][component]["status"] = "Fail"
            self.verification_results["errors"].append(f"Missing config file: {config_path}")
            return False
        
        # Try to parse the config
        try:
            config = configparser.ConfigParser()
            config.read(full_path)
            result = {
                "check": f"Config valid: {config_path}",
                "result": "Pass",
                "critical": True
            }
            self.verification_results["components"][component]["checks"].append(result)
            return True
        except Exception as e:
            result = {
                "check": f"Config valid: {config_path}",
                "result": "Fail",
                "critical": True,
                "message": str(e)
            }
            self.verification_results["components"][component]["checks"].append(result)
            self.verification_results["components"][component]["status"] = "Fail"
            self.verification_results["errors"].append(f"Invalid config file {config_path}: {e}")
            return False
    
    def verify_python_imports(self, component, required_modules):
        """Verify that required Python modules can be imported"""
        if not component in self.verification_results["components"]:
            self.verification_results["components"][component] = {
                "status": "Pass",
                "checks": []
            }
        
        for module in required_modules:
            try:
                # Try importing the module
                subprocess.check_call(
                    [sys.executable, "-c", f"import {module}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                result = {
                    "check": f"Python module: {module}",
                    "result": "Pass",
                    "critical": True
                }
                self.verification_results["components"][component]["checks"].append(result)
            except subprocess.CalledProcessError:
                result = {
                    "check": f"Python module: {module}",
                    "result": "Fail",
                    "critical": True,
                    "message": f"Module {module} not installed or has errors"
                }
                self.verification_results["components"][component]["checks"].append(result)
                self.verification_results["components"][component]["status"] = "Fail"
                self.verification_results["errors"].append(f"Missing Python module: {module}")
    
    def verify_system_structure(self):
        """Verify the overall system structure"""
        # Verify critical directories
        self.verify_directory_exists("plc", "System Structure")
        self.verify_directory_exists("src", "System Structure")
        self.verify_directory_exists("config", "System Structure")
        self.verify_directory_exists("diagrams", "System Structure", critical=False)
        self.verify_directory_exists("docs", "System Structure", critical=False)
        self.verify_directory_exists("scripts", "System Structure")
        
        # Verify key files
        self.verify_file_exists("README.md", "Documentation", critical=False)
        self.verify_file_exists("plc/global_vars.st", "PLC Program")
        self.verify_file_exists("plc/main.st", "PLC Program")
        self.verify_file_exists("config/plc_config.ini", "Configuration")
        self.verify_file_exists("config/wwtp_config.ini", "Configuration")
    
    def verify_plc_program(self):
        """Verify the PLC program components"""
        # Verify PLC program files
        plc_files = [
            "global_vars.st",
            "main.st",
            "intake_controller.st",
            "treatment_controller.st",
            "dosing_controller.st",
            "aeration_controller.st",
            "monitoring_controller.st"
        ]
        
        for file in plc_files:
            self.verify_file_exists(f"plc/{file}", "PLC Program")
    
    def verify_configurations(self):
        """Verify configuration files"""
        self.verify_config_valid("config/plc_config.ini", "Configuration")
        self.verify_config_valid("config/wwtp_config.ini", "Configuration")
    
    def verify_hmi_components(self):
        """Verify HMI components"""
        self.verify_file_exists("src/gui/hmi_interface.py", "HMI Interface")
        self.verify_python_imports("HMI Interface", ["tkinter", "matplotlib", "configparser"])
    
    def verify_system_scripts(self):
        """Verify system scripts"""
        script_files = [
            "batch/system_launcher.bat",
            "batch/run_hmi.bat",
            "batch/run_simulator.bat",
            "batch/run_status_monitor.bat",
            "batch/generate_diagrams.bat"
        ]
        
        for file in script_files:
            self.verify_file_exists(f"scripts/{file}", "System Scripts")
    
    def verify_diagrams(self):
        """Verify system diagrams"""
        diagram_files = [
            "treatment_control_flowchart.png",
            "system_layout_diagram.png",
            "p_id_diagram.png",
            "electrical_schematic.png",
            "wwtp_system_diagrams.pdf"
        ]
        
        for file in diagram_files:
            self.verify_file_exists(f"diagrams/{file}", "System Diagrams", critical=False)
    
    def run_verification(self):
        """Run all verification checks"""
        print("Running system verification...")
        
        # Run all verification methods
        self.verify_system_structure()
        self.verify_plc_program()
        self.verify_configurations()
        self.verify_hmi_components()
        self.verify_system_scripts()
        self.verify_diagrams()
        
        # Determine overall system status
        component_statuses = [comp["status"] for comp in self.verification_results["components"].values()]
        if "Fail" in component_statuses:
            self.verification_results["system_status"] = "Fail"
        else:
            self.verification_results["system_status"] = "Pass"
        
        return self.verification_results
    
    def save_results(self, format="both"):
        """Save verification results to file"""
        # Create output directory if it doesn't exist
        output_dir = ROOT_DIR / "utils" / "verification"
        output_dir.mkdir(exist_ok=True)
        
        # Save as JSON
        if format in ["json", "both"]:
            json_path = output_dir / "verification_results.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.verification_results, f, indent=2)
            print(f"Saved verification results to {json_path}")
        
        # Save as text
        if format in ["text", "both"]:
            txt_path = output_dir / "verification_results.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                # Write header
                f.write("=" * 80 + "\n")
                f.write("WASTEWATER TREATMENT PLANT - SYSTEM VERIFICATION RESULTS\n")
                f.write("=" * 80 + "\n\n")
                
                # Write timestamp and overall status
                f.write(f"Timestamp: {self.verification_results['timestamp']}\n")
                status = self.verification_results["system_status"]
                status_symbol = "✓" if status == "Pass" else "✗"
                f.write(f"Overall Status: {status_symbol} {status}\n\n")
                
                # Write component results
                f.write("-" * 80 + "\n")
                f.write("COMPONENT VERIFICATION RESULTS:\n")
                f.write("-" * 80 + "\n")
                
                for component, data in self.verification_results["components"].items():
                    comp_status = data["status"]
                    comp_symbol = "✓" if comp_status == "Pass" else "✗"
                    f.write(f"\n{component}: {comp_symbol} {comp_status}\n")
                    
                    # Write individual checks
                    for check in data["checks"]:
                        check_status = check["result"]
                        check_symbol = "✓" if check_status == "Pass" else "✗"
                        f.write(f"  {check_symbol} {check['check']}\n")
                        if check_status == "Fail" and "message" in check:
                            f.write(f"      Error: {check['message']}\n")
                
                # Write errors and warnings
                if self.verification_results["errors"]:
                    f.write("\n" + "-" * 80 + "\n")
                    f.write("ERRORS:\n")
                    f.write("-" * 80 + "\n")
                    for error in self.verification_results["errors"]:
                        f.write(f"✗ {error}\n")
                
                if self.verification_results["warnings"]:
                    f.write("\n" + "-" * 80 + "\n")
                    f.write("WARNINGS:\n")
                    f.write("-" * 80 + "\n")
                    for warning in self.verification_results["warnings"]:
                        f.write(f"! {warning}\n")
                
            print(f"Saved verification results to {txt_path}")

def main():
    """Main function"""
    verifier = SystemVerifier()
    verifier.run_verification()
    verifier.save_results()
    
    # Print summary to console
    print("\nVerification Summary:")
    print(f"Status: {verifier.verification_results['system_status']}")
    print(f"Errors: {len(verifier.verification_results['errors'])}")
    print(f"Warnings: {len(verifier.verification_results['warnings'])}")
    
    if verifier.verification_results["system_status"] == "Fail":
        print("\nErrors:")
        for error in verifier.verification_results["errors"]:
            print(f"- {error}")
    
    if verifier.verification_results["warnings"]:
        print("\nWarnings:")
        for warning in verifier.verification_results["warnings"]:
            print(f"- {warning}")

if __name__ == "__main__":
    main()
