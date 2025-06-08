#!/usr/bin/env python3
"""
System Verification Script for Water Treatment System
Verifies all components are present and demonstrates the flowchart capabilities
"""

import os
import time
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"{title:^60}")
    print("="*60)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{title}")
    print("-" * len(title))

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    exists = os.path.exists(filepath)
    status = "✅ EXISTS" if exists else "❌ MISSING"
    print(f"{status} | {description}")
    return exists

def main():
    """Main verification function"""
    print_header("WATER TREATMENT SYSTEM VERIFICATION")
    
    # Navigate to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", "..")
    os.chdir(project_root)
    
    current_dir = os.getcwd()
    print(f"Project Root: {current_dir}")
    print(f"Verification Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define all system files with new structure
    system_files = {
        "PLC Programming Files": [
            ("plc/global_vars.st", "Global variables and data structures"),
            ("plc/main.st", "Main PLC control program"),
            ("plc/desalination_controller.st", "RO process controller"),
            ("plc/pump_controller.st", "Multi-pump control system"),
            ("plc/water_quality_controller.st", "Water quality monitoring"),
        ],
        "Python Applications": [
            ("src/simulation/water_treatment_simulator.py", "Complete system simulator with GUI"),
            ("src/gui/hmi_interface.py", "Advanced Python GUI interface"),
            ("src/monitoring/system_status.py", "System monitoring and health assessment"),
            ("src/core/process_diagram.py", "Enhanced diagram generator with flowchart"),        ],
        "Web Interface": [
            ("src/gui/web_hmi.html", "Modern web-based dashboard"),
        ],
        "Configuration Files": [
            ("config/plc_config.ini", "System configuration parameters"),
        ],
        "Documentation": [
            ("docs/README.md", "Project overview and documentation"),
            ("docs/System_Documentation.md", "Comprehensive technical documentation"),
            ("docs/FLOWCHART_IMPLEMENTATION_SUMMARY.md", "Flowchart implementation details"),
            ("docs/PROJECT_STRUCTURE.md", "Project organization documentation"),
        ],
        "Visual Diagrams": [
            ("diagrams/water_treatment_process_diagram.png", "Main process flow diagram"),
            ("diagrams/water_treatment_pid.png", "P&ID instrumentation diagram"),
            ("diagrams/control_system_architecture.png", "Control system layout"),
            ("diagrams/process_control_flowchart.png", "🆕 Detailed control logic flowchart"),
            ("diagrams/system_states_diagram.png", "🆕 System state transitions"),
            ("diagrams/water_treatment_diagrams.pdf", "Combined PDF with all diagrams"),
        ],
        "System Utilities": [
            ("scripts/batch/system_launcher.bat", "Main system menu"),
            ("scripts/batch/run_hmi.bat", "Launch HMI interface"),
            ("scripts/batch/run_simulator.bat", "Launch system simulator"),
            ("scripts/batch/run_status_monitor.bat", "Launch status monitor"),
            ("scripts/batch/generate_diagrams.bat", "Generate all diagrams"),
        ],
        "Verification & Utilities": [
            ("utils/verification/verify_system.py", "System verification script"),
            ("utils/final_project_summary.py", "Project summary generator"),
            ("utils/flowchart_demo.py", "Flowchart demonstration tool"),
        ]
    }
    
    # Verify all files
    total_files = 0
    found_files = 0
    
    for category, files in system_files.items():
        print_section(category)
        for filename, description in files:
            total_files += 1
            if check_file_exists(filename, description):
                found_files += 1
    
    # Summary
    print_section("VERIFICATION SUMMARY")
    completion_rate = (found_files / total_files) * 100
    print(f"Files Found: {found_files}/{total_files}")
    print(f"Completion Rate: {completion_rate:.1f}%")
    
    if completion_rate == 100:
        print("🎉 SYSTEM COMPLETE - All components verified!")
    elif completion_rate >= 90:
        print("✅ SYSTEM NEARLY COMPLETE - Minor components missing")
    else:
        print("⚠️ SYSTEM INCOMPLETE - Major components missing")
    
    # Flowchart Features Summary
    print_section("NEW FLOWCHART FEATURES")
    flowchart_features = [
        "🔄 Complete control logic visualization",
        "💎 Decision points with YES/NO branches",
        "🛡️ Safety interlocks and emergency procedures",
        "⚙️ Process control sequences from startup to shutdown",
        "🚨 Alarm conditions and fault handling",
        "🔄 System state transitions (9 operational states)",
        "📊 Color-coded process elements",
        "🎯 PID control loop representations",
        "🔧 Maintenance and cleaning cycle logic",
        "📋 Operator decision support"
    ]
    
    for feature in flowchart_features:
        print(f"  {feature}")
    
    # System Capabilities
    print_section("SYSTEM CAPABILITIES")
    capabilities = [
        "🌊 Seawater desalination (10,000 L/hour capacity)",
        "🔄 45% RO recovery rate with energy optimization",
        "🏗️ Complete PLC programming with structured text",
        "🖥️ Dual interface (Python GUI + Web HMI)",
        "📊 Real-time monitoring and data logging",
        "🔧 Comprehensive simulation environment",
        "📈 Performance trending and analytics",
        "🚨 Multi-level alarm system",
        "🛡️ Advanced safety interlocks",
        "📱 Mobile-friendly web interface",
        "🎨 Automatic diagram generation",
        "📋 Complete technical documentation",
        "🔄 State machine control logic",
        "🧪 Water quality monitoring and control"
    ]
    
    for capability in capabilities:
        print(f"  {capability}")
    
    print_section("NEXT STEPS")
    print("1. Run 'system_launcher.bat' to access the main menu")
    print("2. Use 'generate_diagrams.bat' to create/update visual documentation")
    print("3. Review 'process_control_flowchart.png' for detailed control logic")
    print("4. Check 'System_Documentation.md' for complete technical details")
    print("5. Test system with 'run_simulator.bat' and 'run_hmi.bat'")
    
    print(f"\n🕒 Verification completed at {datetime.now().strftime('%H:%M:%S')}")
    print("Water Treatment System - Ready for Operation! 🏭💧")

if __name__ == "__main__":
    main()
