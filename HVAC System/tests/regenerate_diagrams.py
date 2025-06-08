#!/usr/bin/env python3
"""
HVAC System - Diagram Regeneration Tool
Utility for regenerating all system diagrams

Author: System Engineer
Date: June 8, 2025
Version: 1.0.0
"""

import sys
import os
from pathlib import Path
from datetime import datetime

def regenerate_diagrams():
    """Regenerate all HVAC system diagrams"""
    print("🎨 HVAC Diagram Regeneration Tool")
    print("=" * 50)
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    diagram_script = project_root / "utils" / "hvac_diagram_new.py"
    
    if not diagram_script.exists():
        print("❌ Error: Diagram generation script not found")
        print(f"   Expected: {diagram_script}")
        return False
    
    print("🔧 Checking dependencies...")
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        print("✅ matplotlib and numpy are available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install matplotlib numpy")
        return False
    
    print()
    print("🎨 Regenerating diagrams...")
    
    # Import and run the diagram generator
    try:
        sys.path.insert(0, str(project_root))
        from utils.hvac_diagram_new import HVACDiagramGenerator
        
        generator = HVACDiagramGenerator()
        success = generator.generate_all_diagrams()
        
        if success:
            print("✅ All diagrams regenerated successfully!")
            diagrams_dir = project_root / "diagrams"
            print(f"📁 Diagrams location: {diagrams_dir}")
            print(f"🌐 View diagrams: {diagrams_dir / 'index.html'}")
        else:
            print("❌ Some diagrams failed to generate")
            
        return success
        
    except Exception as e:
        print(f"❌ Error during diagram generation: {e}")
        return False

def verify_diagrams():
    """Verify that all diagram files exist and are not empty"""
    print("🔍 Verifying diagram files...")
    
    project_root = Path(__file__).parent.parent
    diagrams_dir = project_root / "diagrams"
    
    expected_diagrams = [
        "system_overview.png",
        "zone_layout.png", 
        "piping_schematic.png",
        "electrical_diagram.png",
        "control_flow.png",
        "air_flow_diagram.png",
        "energy_flow_diagram.png",
        "sensor_network.png",
        "safety_systems.png",
        "maintenance_diagram.png"
    ]
    
    all_good = True
    
    for diagram in expected_diagrams:
        diagram_path = diagrams_dir / diagram
        if not diagram_path.exists():
            print(f"❌ Missing: {diagram}")
            all_good = False
        else:
            size = diagram_path.stat().st_size
            if size < 1000:  # Less than 1KB probably indicates an empty/corrupted file
                print(f"⚠️  Suspiciously small: {diagram} ({size} bytes)")
                all_good = False
            else:
                print(f"✅ OK: {diagram} ({size:,} bytes)")
    
    # Check index.html
    index_path = diagrams_dir / "index.html"
    if index_path.exists():
        print(f"✅ OK: index.html ({index_path.stat().st_size:,} bytes)")
    else:
        print("❌ Missing: index.html")
        all_good = False
    
    return all_good

def main():
    """Main function"""
    if "--verify-only" in sys.argv:
        # Just verify existing diagrams
        success = verify_diagrams()
    else:
        # Regenerate and verify
        print("1️⃣ Regenerating diagrams...")
        regen_success = regenerate_diagrams()
        
        print()
        print("2️⃣ Verifying diagrams...")
        verify_success = verify_diagrams()
        
        success = regen_success and verify_success
    
    print()
    if success:
        print("🎉 All diagrams are ready!")
    else:
        print("⚠️  Some issues were found - see output above")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
