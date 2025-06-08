#!/usr/bin/env python3
# Wastewater Treatment Plant - Project Summary Generator
# Generates a comprehensive project summary

import os
import sys
import time
import json
from datetime import datetime

# Project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_file_count_by_type():
    """Count files by type in the project"""
    file_counts = {}
    total_files = 0
    total_lines = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            # Skip .git and __pycache__ directories
            if "/.git/" in root or "/__pycache__/" in root:
                continue
                
            # Get file extension
            _, ext = os.path.splitext(file)
            if ext:
                ext = ext.lower()
            else:
                ext = "no_extension"
                
            # Count file
            if ext in file_counts:
                file_counts[ext]["count"] += 1
            else:
                file_counts[ext] = {"count": 1, "lines": 0}
                
            total_files += 1
            
            # Count lines in text files
            text_extensions = ['.py', '.st', '.txt', '.md', '.ini', '.html', '.css', '.js', '.bat']
            if ext in text_extensions:
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        line_count = sum(1 for _ in f)
                        file_counts[ext]["lines"] += line_count
                        total_lines += line_count
                except Exception as e:
                    print(f"Error counting lines in {file_path}: {e}")
    
    return file_counts, total_files, total_lines

def get_folder_structure(max_depth=3):
    """Generate a simplified folder structure"""
    structure = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip .git and __pycache__ directories
        if "/.git/" in root or "/__pycache__/" in root:
            continue
            
        # Calculate depth
        rel_path = os.path.relpath(root, ROOT_DIR)
        if rel_path == ".":
            depth = 0
        else:
            depth = rel_path.count(os.sep) + 1
            
        # Skip if beyond max depth
        if depth > max_depth:
            continue
            
        # Add to structure
        structure.append({
            "path": rel_path,
            "depth": depth,
            "dirs": len(dirs),
            "files": len(files)
        })
    
    return structure

def check_implementation_status():
    """Check implementation status of different components"""
    component_paths = {
        "PLC Programs": os.path.join(ROOT_DIR, "plc"),
        "HMI Interface": os.path.join(ROOT_DIR, "src", "gui"),
        "Documentation": os.path.join(ROOT_DIR, "docs"),
        "Diagrams": os.path.join(ROOT_DIR, "diagrams"),
        "Simulation": os.path.join(ROOT_DIR, "src", "simulation"),
        "Configuration": os.path.join(ROOT_DIR, "config"),
        "Test Cases": os.path.join(ROOT_DIR, "tests"),
        "System Scripts": os.path.join(ROOT_DIR, "scripts")
    }
    
    status = {}
    
    for component, path in component_paths.items():
        if os.path.exists(path):
            # Check if directory has files
            files = os.listdir(path)
            if files:
                if component == "Diagrams" and len(files) >= 4:
                    status[component] = "Complete"
                elif component == "PLC Programs" and len(files) >= 6:
                    status[component] = "Complete"
                else:
                    status[component] = "Partial"
            else:
                status[component] = "Empty"
        else:
            status[component] = "Not Started"
    
    # Overall status
    completed = sum(1 for s in status.values() if s == "Complete")
    partial = sum(1 for s in status.values() if s == "Partial")
    
    if completed == len(status):
        overall = "Complete"
    elif completed + partial == len(status):
        overall = "Functional"
    elif completed + partial > len(status) / 2:
        overall = "Partial"
    else:
        overall = "Initial"
        
    status["Overall"] = overall
    
    return status

def generate_summary():
    """Generate project summary"""
    summary = {
        "project_name": "Wastewater Treatment Plant",
        "description": "Automated wastewater treatment plant control system",
        "generation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0"
    }
    
    # Get file statistics
    file_counts, total_files, total_lines = get_file_count_by_type()
    summary["file_statistics"] = {
        "total_files": total_files,
        "total_lines": total_lines,
        "by_type": file_counts
    }
    
    # Get folder structure
    summary["folder_structure"] = get_folder_structure()
    
    # Check implementation status
    summary["implementation_status"] = check_implementation_status()
    
    # Additional information
    summary["additional_info"] = {
        "development_start": "May 2025",
        "projected_completion": "July 2025",
        "project_type": "Industrial Automation",
        "complexity": "High"
    }
    
    return summary

def save_summary(summary, output_format="both"):
    """Save summary to file in specified format"""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(ROOT_DIR, "utils")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save as JSON
    if output_format in ["json", "both"]:
        json_path = os.path.join(output_dir, "project_summary.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        print(f"Saved JSON summary to {json_path}")
    
    # Save as text
    if output_format in ["text", "both"]:
        txt_path = os.path.join(output_dir, "project_summary.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            # Project header
            f.write("=" * 80 + "\n")
            f.write(f"{summary['project_name']} - Project Summary\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Description: {summary['description']}\n")
            f.write(f"Version: {summary['version']}\n")
            f.write(f"Generated: {summary['generation_time']}\n\n")
            
            # Implementation status
            f.write("-" * 80 + "\n")
            f.write("IMPLEMENTATION STATUS:\n")
            f.write("-" * 80 + "\n")
            status = summary['implementation_status']
            overall = status.pop("Overall", "Unknown")
            for component, state in status.items():
                f.write(f"{component}: {state}\n")
            f.write(f"\nOverall Status: {overall}\n\n")
            
            # File statistics
            f.write("-" * 80 + "\n")
            f.write("FILE STATISTICS:\n")
            f.write("-" * 80 + "\n")
            stats = summary['file_statistics']
            f.write(f"Total Files: {stats['total_files']}\n")
            f.write(f"Total Lines of Code: {stats['total_lines']}\n\n")
            
            f.write("Files by Type:\n")
            file_types = [(ext, data["count"], data["lines"]) 
                         for ext, data in stats['by_type'].items()]
            file_types.sort(key=lambda x: x[1], reverse=True)
            
            for ext, count, lines in file_types:
                if lines > 0:
                    f.write(f"  {ext:<10} {count:>5} files  {lines:>8} lines\n")
                else:
                    f.write(f"  {ext:<10} {count:>5} files\n")
            
            # Folder structure
            f.write("\n" + "-" * 80 + "\n")
            f.write("FOLDER STRUCTURE:\n")
            f.write("-" * 80 + "\n")
            
            for folder in summary['folder_structure']:
                depth = folder['depth']
                indent = "  " * depth
                name = os.path.basename(folder['path']) if folder['path'] != "." else "ROOT"
                files = folder['files']
                dirs = folder['dirs']
                
                if depth == 0:
                    f.write(f"{name} ({files} files, {dirs} directories)\n")
                else:
                    f.write(f"{indent}|- {name} ({files} files, {dirs} dirs)\n")
            
            # Additional information
            f.write("\n" + "-" * 80 + "\n")
            f.write("ADDITIONAL INFORMATION:\n")
            f.write("-" * 80 + "\n")
            for key, value in summary['additional_info'].items():
                formatted_key = " ".join(word.capitalize() for word in key.split("_"))
                f.write(f"{formatted_key}: {value}\n")
                
        print(f"Saved text summary to {txt_path}")

def main():
    """Main function"""
    print("Generating project summary...")
    summary = generate_summary()
    save_summary(summary)
    print("Project summary generation complete!")

if __name__ == "__main__":
    main()
