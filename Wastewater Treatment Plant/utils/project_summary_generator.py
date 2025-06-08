#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project Summary Generator for Wastewater Treatment Plant
-------------------------------------------------------
This utility script generates comprehensive project summaries by analyzing
configuration files, source code, and project documentation.
"""

import os
import sys
import configparser
import json
import datetime
import glob
import re
from collections import Counter, defaultdict

class ProjectSummaryGenerator:
    """Generates detailed project summaries for the Wastewater Treatment Plant system."""
    
    def __init__(self, project_root):
        self.project_root = project_root
        self.config = {}
        self.source_stats = {}
        self.component_list = []
        self.documentation_status = {}
        self.timestamp = datetime.datetime.now()
    
    def load_configs(self):
        """Load system configuration files."""
        try:
            # Load PLC configuration
            plc_config = configparser.ConfigParser()
            plc_config.read(os.path.join(self.project_root, 'config', 'plc_config.ini'))
            
            # Load WWTP configuration
            wwtp_config = configparser.ConfigParser()
            wwtp_config.read(os.path.join(self.project_root, 'config', 'wwtp_config.ini'))
            
            self.config = {
                'plc': {s: dict(plc_config[s]) for s in plc_config.sections()},
                'wwtp': {s: dict(wwtp_config[s]) for s in wwtp_config.sections()}
            }
            
            print("Configuration files loaded successfully")
        except Exception as e:
            print(f"Error loading configuration files: {str(e)}")
            self.config = {'error': str(e)}
    
    def analyze_source_code(self):
        """Analyze source code files to gather statistics."""
        try:
            stats = defaultdict(Counter)
            
            # Analyze PLC code (.st files)
            plc_files = glob.glob(os.path.join(self.project_root, 'plc', '*.st'))
            stats['plc']['files'] = len(plc_files)
            
            # Count lines of code, variables, and function blocks
            total_loc = 0
            total_vars = 0
            total_fbs = 0
            
            for file in plc_files:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    total_loc += len(lines)
                    
                    # Count variables (simple heuristic)
                    var_matches = re.findall(r'VAR\s+.*?\s+END_VAR', content, re.DOTALL)
                    for match in var_matches:
                        var_lines = match.split('\n')
                        total_vars += len(var_lines) - 2  # Subtract VAR and END_VAR lines
                    
                    # Count function blocks
                    fb_matches = re.findall(r'FUNCTION_BLOCK\s+(\w+)', content)
                    total_fbs += len(fb_matches)
            
            stats['plc']['lines_of_code'] = total_loc
            stats['plc']['variables'] = total_vars
            stats['plc']['function_blocks'] = total_fbs
            
            # Analyze Python files
            py_files = []
            for root, _, files in os.walk(self.project_root):
                for file in files:
                    if file.endswith('.py'):
                        py_files.append(os.path.join(root, file))
            
            stats['python']['files'] = len(py_files)
            
            py_loc = 0
            py_classes = 0
            py_functions = 0
            
            for file in py_files:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    py_loc += len(lines)
                    
                    # Count classes and functions
                    class_matches = re.findall(r'^\s*class\s+\w+', content, re.MULTILINE)
                    py_classes += len(class_matches)
                    
                    func_matches = re.findall(r'^\s*def\s+\w+', content, re.MULTILINE)
                    py_functions += len(func_matches)
            
            stats['python']['lines_of_code'] = py_loc
            stats['python']['classes'] = py_classes
            stats['python']['functions'] = py_functions
            
            # Analyze HTML/JavaScript files for HMI
            web_files = glob.glob(os.path.join(self.project_root, 'src', 'gui', 'web', '*.*'))
            stats['web']['files'] = len(web_files)
            
            # Count batch scripts
            batch_files = glob.glob(os.path.join(self.project_root, 'scripts', 'batch', '*.bat'))
            stats['batch']['files'] = len(batch_files)
            
            self.source_stats = dict(stats)
            print("Source code analysis completed")
        except Exception as e:
            print(f"Error analyzing source code: {str(e)}")
            self.source_stats = {'error': str(e)}
    
    def identify_components(self):
        """Identify system components from directories and config files."""
        try:
            components = []
            
            # Add main components from directory structure
            main_dirs = [d for d in os.listdir(self.project_root) 
                       if os.path.isdir(os.path.join(self.project_root, d))]
            
            for dir_name in main_dirs:
                if dir_name.startswith('.'):
                    continue
                    
                component = {
                    'name': dir_name.replace('_', ' ').title(),
                    'type': 'directory',
                    'path': os.path.join(self.project_root, dir_name)
                }
                components.append(component)
            
            # Add PLC components from config
            if 'plc' in self.config and 'Modules' in self.config['plc']:
                for key, value in self.config['plc']['Modules'].items():
                    components.append({
                        'name': value,
                        'type': 'plc_module',
                    })
            
            # Add controller components from PLC files
            plc_files = glob.glob(os.path.join(self.project_root, 'plc', '*_controller.st'))
            for file in plc_files:
                controller_name = os.path.basename(file).replace('.st', '').replace('_', ' ').title()
                components.append({
                    'name': controller_name,
                    'type': 'controller',
                    'file': os.path.basename(file)
                })
            
            # Add process components from WWTP config
            if 'wwtp' in self.config:
                # Add tanks
                if 'Tank_Configuration' in self.config['wwtp']:
                    for key, value in self.config['wwtp']['Tank_Configuration'].items():
                        if key.endswith('capacity'):
                            tank_name = key.replace('capacity', '').replace('_', ' ').title()
                            components.append({
                                'name': tank_name,
                                'type': 'process_equipment',
                                'capacity': value
                            })
                
                # Add chemical dosing components
                if 'Chemical_Dosing' in self.config['wwtp']:
                    for key, value in self.config['wwtp']['Chemical_Dosing'].items():
                        if key.endswith('type'):
                            chemical_name = key.replace('type', '').replace('_', ' ').title()
                            components.append({
                                'name': f"{value} ({chemical_name})",
                                'type': 'chemical_system'
                            })
            
            self.component_list = components
            print(f"Identified {len(components)} system components")
        except Exception as e:
            print(f"Error identifying components: {str(e)}")
            self.component_list = []
    
    def check_documentation_status(self):
        """Check status of project documentation."""
        try:
            docs_dir = os.path.join(self.project_root, 'docs')
            
            # Get documentation files
            user_docs = glob.glob(os.path.join(docs_dir, 'user', '*.md'))
            technical_docs = glob.glob(os.path.join(docs_dir, 'technical', '*.md'))
            
            # Check for required documentation
            required_docs = [
                ('operating_procedures.md', 'user'),
                ('troubleshooting_guide.md', 'user'),
                ('system_documentation.md', 'technical')
            ]
            
            doc_status = {}
            
            for doc_name, doc_type in required_docs:
                doc_path = os.path.join(docs_dir, doc_type, doc_name)
                if os.path.exists(doc_path):
                    with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        word_count = len(content.split())
                        section_count = len(re.findall(r'^#+\s+', content, re.MULTILINE))
                        
                        doc_status[doc_name] = {
                            'exists': True,
                            'word_count': word_count,
                            'sections': section_count,
                            'last_modified': datetime.datetime.fromtimestamp(
                                os.path.getmtime(doc_path)
                            ).strftime('%Y-%m-%d %H:%M:%S')
                        }
                else:
                    doc_status[doc_name] = {'exists': False}
            
            # Count total documentation files
            doc_status['total_files'] = len(user_docs) + len(technical_docs)
            
            self.documentation_status = doc_status
            print("Documentation status checked")
        except Exception as e:
            print(f"Error checking documentation status: {str(e)}")
            self.documentation_status = {'error': str(e)}
    
    def generate_summary(self, output_format='json'):
        """Generate the final project summary."""
        try:
            # Build the summary dictionary
            summary = {
                'project_name': self.config.get('plc', {}).get('System', {}).get('name', 'Wastewater Treatment Plant'),
                'generated_timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'system_capacity': self.config.get('wwtp', {}).get('System', {}).get('capacity', 'Unknown'),
                'system_version': self.config.get('plc', {}).get('System', {}).get('version', 'Unknown'),
                'configuration': self.config,
                'statistics': {
                    'source_code': self.source_stats,
                    'component_count': len(self.component_list)
                },
                'components': self.component_list,
                'documentation': self.documentation_status
            }
            
            # Generate output based on format
            if output_format.lower() == 'json':
                return json.dumps(summary, indent=2, default=str)
            elif output_format.lower() == 'text':
                return self._format_text_summary(summary)
            elif output_format.lower() == 'html':
                return self._format_html_summary(summary)
            else:
                return json.dumps(summary, indent=2, default=str)
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return json.dumps({
                'error': f"Failed to generate summary: {str(e)}",
                'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }, indent=2)
    
    def _format_text_summary(self, summary):
        """Format the summary as plain text."""
        lines = []
        
        lines.append("=" * 80)
        lines.append(f"WASTEWATER TREATMENT PLANT PROJECT SUMMARY")
        lines.append("=" * 80)
        lines.append(f"Generated: {summary['generated_timestamp']}")
        lines.append(f"System Name: {summary['project_name']}")
        lines.append(f"System Version: {summary['system_version']}")
        lines.append(f"Treatment Capacity: {summary['system_capacity']} m³/hr")
        lines.append("=" * 80)
        
        lines.append("\nCODE STATISTICS:")
        lines.append("-" * 40)
        stats = summary['statistics']['source_code']
        
        if 'plc' in stats:
            lines.append(f"PLC Code Files:       {stats['plc'].get('files', 0)}")
            lines.append(f"PLC Lines of Code:    {stats['plc'].get('lines_of_code', 0)}")
            lines.append(f"PLC Function Blocks:  {stats['plc'].get('function_blocks', 0)}")
        
        if 'python' in stats:
            lines.append(f"Python Files:         {stats['python'].get('files', 0)}")
            lines.append(f"Python Lines of Code: {stats['python'].get('lines_of_code', 0)}")
            lines.append(f"Python Classes:       {stats['python'].get('classes', 0)}")
            lines.append(f"Python Functions:     {stats['python'].get('functions', 0)}")
        
        lines.append(f"Web Files:            {stats.get('web', {}).get('files', 0)}")
        lines.append(f"Batch Scripts:        {stats.get('batch', {}).get('files', 0)}")
        
        lines.append("\nSYSTEM COMPONENTS:")
        lines.append("-" * 40)
        
        component_types = defaultdict(list)
        for component in summary['components']:
            component_types[component.get('type', 'other')].append(component['name'])
        
        for comp_type, components in component_types.items():
            lines.append(f"{comp_type.replace('_', ' ').title()} ({len(components)}):")
            for component in components:
                lines.append(f"  - {component}")
        
        lines.append("\nDOCUMENTATION STATUS:")
        lines.append("-" * 40)
        
        docs = summary['documentation']
        lines.append(f"Total Documentation Files: {docs.get('total_files', 0)}")
        
        for doc_name, status in docs.items():
            if doc_name == 'total_files':
                continue
                
            if status.get('exists', False):
                lines.append(f"{doc_name}:")
                lines.append(f"  - Words: {status.get('word_count', 0)}")
                lines.append(f"  - Sections: {status.get('sections', 0)}")
                lines.append(f"  - Last Modified: {status.get('last_modified', 'Unknown')}")
            else:
                lines.append(f"{doc_name}: Missing")
        
        return "\n".join(lines)
    
    def _format_html_summary(self, summary):
        """Format the summary as HTML."""
        html = []
        
        html.append("<!DOCTYPE html>")
        html.append('<html lang="en">')
        html.append('<head>')
        html.append('  <meta charset="UTF-8">')
        html.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html.append('  <title>WWTP Project Summary</title>')
        html.append('  <style>')
        html.append('    body { font-family: Arial, sans-serif; margin: 20px; color: #333; }')
        html.append('    h1, h2, h3 { color: #0066cc; }')
        html.append('    table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }')
        html.append('    th, td { text-align: left; padding: 12px; border-bottom: 1px solid #ddd; }')
        html.append('    th { background-color: #f2f2f2; }')
        html.append('    .card { border: 1px solid #ddd; border-radius: 4px; padding: 15px; margin-bottom: 20px; }')
        html.append('    .header { background-color: #0066cc; color: white; padding: 20px; border-radius: 4px; }')
        html.append('    .missing { color: #cc0000; }')
        html.append('    .present { color: #007700; }')
        html.append('  </style>')
        html.append('</head>')
        html.append('<body>')
        
        # Header
        html.append('  <div class="header">')
        html.append(f'    <h1>Wastewater Treatment Plant Project Summary</h1>')
        html.append(f'    <p>Generated: {summary["generated_timestamp"]}</p>')
        html.append('  </div>')
        
        # System Information
        html.append('  <div class="card">')
        html.append('    <h2>System Information</h2>')
        html.append('    <table>')
        html.append('      <tr><th>Property</th><th>Value</th></tr>')
        html.append(f'      <tr><td>System Name</td><td>{summary["project_name"]}</td></tr>')
        html.append(f'      <tr><td>System Version</td><td>{summary["system_version"]}</td></tr>')
        html.append(f'      <tr><td>Treatment Capacity</td><td>{summary["system_capacity"]} m³/hr</td></tr>')
        html.append('    </table>')
        html.append('  </div>')
        
        # Code Statistics
        html.append('  <div class="card">')
        html.append('    <h2>Code Statistics</h2>')
        html.append('    <table>')
        html.append('      <tr><th>Metric</th><th>Value</th></tr>')
        
        stats = summary['statistics']['source_code']
        
        if 'plc' in stats:
            html.append(f'      <tr><td>PLC Code Files</td><td>{stats["plc"].get("files", 0)}</td></tr>')
            html.append(f'      <tr><td>PLC Lines of Code</td><td>{stats["plc"].get("lines_of_code", 0)}</td></tr>')
            html.append(f'      <tr><td>PLC Function Blocks</td><td>{stats["plc"].get("function_blocks", 0)}</td></tr>')
        
        if 'python' in stats:
            html.append(f'      <tr><td>Python Files</td><td>{stats["python"].get("files", 0)}</td></tr>')
            html.append(f'      <tr><td>Python Lines of Code</td><td>{stats["python"].get("lines_of_code", 0)}</td></tr>')
            html.append(f'      <tr><td>Python Classes</td><td>{stats["python"].get("classes", 0)}</td></tr>')
            html.append(f'      <tr><td>Python Functions</td><td>{stats["python"].get("functions", 0)}</td></tr>')
        
        html.append(f'      <tr><td>Web Files</td><td>{stats.get("web", {}).get("files", 0)}</td></tr>')
        html.append(f'      <tr><td>Batch Scripts</td><td>{stats.get("batch", {}).get("files", 0)}</td></tr>')
        
        html.append('    </table>')
        html.append('  </div>')
        
        # System Components
        html.append('  <div class="card">')
        html.append('    <h2>System Components</h2>')
        
        component_types = defaultdict(list)
        for component in summary['components']:
            component_types[component.get('type', 'other')].append(component)
        
        for comp_type, components in component_types.items():
            html.append(f'    <h3>{comp_type.replace("_", " ").title()} ({len(components)})</h3>')
            html.append('    <ul>')
            for component in components:
                name = component['name']
                html.append(f'      <li>{name}</li>')
            html.append('    </ul>')
        
        html.append('  </div>')
        
        # Documentation Status
        html.append('  <div class="card">')
        html.append('    <h2>Documentation Status</h2>')
        
        docs = summary['documentation']
        html.append(f'    <p>Total Documentation Files: {docs.get("total_files", 0)}</p>')
        html.append('    <table>')
        html.append('      <tr><th>Document</th><th>Status</th><th>Words</th><th>Sections</th><th>Last Modified</th></tr>')
        
        for doc_name, status in docs.items():
            if doc_name == 'total_files':
                continue
                
            if status.get('exists', False):
                html.append(f'      <tr>')
                html.append(f'        <td>{doc_name}</td>')
                html.append(f'        <td class="present">Present</td>')
                html.append(f'        <td>{status.get("word_count", 0)}</td>')
                html.append(f'        <td>{status.get("sections", 0)}</td>')
                html.append(f'        <td>{status.get("last_modified", "Unknown")}</td>')
                html.append(f'      </tr>')
            else:
                html.append(f'      <tr>')
                html.append(f'        <td>{doc_name}</td>')
                html.append(f'        <td class="missing">Missing</td>')
                html.append(f'        <td>-</td>')
                html.append(f'        <td>-</td>')
                html.append(f'        <td>-</td>')
                html.append(f'      </tr>')
        
        html.append('    </table>')
        html.append('  </div>')
        
        html.append('</body>')
        html.append('</html>')
        
        return "\n".join(html)
    
    def save_summary(self, output_path, output_format='json'):
        """Save the summary to file."""
        try:
            summary = self.generate_summary(output_format)
            
            extension = output_format.lower()
            if extension == 'text':
                extension = 'txt'
                
            with open(f"{output_path}.{extension}", 'w', encoding='utf-8') as f:
                f.write(summary)
            
            print(f"Summary saved to {output_path}.{extension}")
            return True
        except Exception as e:
            print(f"Error saving summary: {str(e)}")
            return False
    
    def run(self, output_path=None, output_format='json'):
        """Execute the full summary generation process."""
        print(f"Starting project summary generation for {self.project_root}")
        
        self.load_configs()
        self.analyze_source_code()
        self.identify_components()
        self.check_documentation_status()
        
        if output_path:
            return self.save_summary(output_path, output_format)
        else:
            timestamp = self.timestamp.strftime('%Y%m%d_%H%M%S')
            default_path = os.path.join(self.project_root, f"project_summary_{timestamp}")
            return self.save_summary(default_path, output_format)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a project summary for the WWTP system')
    parser.add_argument('--project-root', '-p', type=str, default=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
                      help='Path to project root directory')
    parser.add_argument('--output', '-o', type=str, default=None,
                      help='Output file path (without extension)')
    parser.add_argument('--format', '-f', type=str, choices=['json', 'text', 'html'], default='json',
                      help='Output format')
    
    args = parser.parse_args()
    
    generator = ProjectSummaryGenerator(args.project_root)
    success = generator.run(args.output, args.format)
    
    if success:
        print("Project summary generation completed successfully")
    else:
        print("Project summary generation failed")
        sys.exit(1)
