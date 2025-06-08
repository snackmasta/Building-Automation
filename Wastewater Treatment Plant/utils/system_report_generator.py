#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
System Report Generator for Wastewater Treatment Plant
-----------------------------------------------------
This utility combines the outputs of all verification tools into a
comprehensive system report in HTML format for easy review.
"""

import os
import sys
import json
import argparse
from datetime import datetime
import glob


class SystemReportGenerator:
    """Generates a comprehensive system report from all validation outputs."""
    
    def __init__(self, project_root, reports_dir=None):
        self.project_root = project_root
        self.reports_dir = reports_dir or os.path.join(project_root, 'reports')
        self.report_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'config_validation': None,
            'connectivity_check': None,
            'io_validation': None,
            'controller_validation': None,
            'project_summary': None
        }
    
    def load_report_files(self):
        """Load the most recent report files of each type."""
        try:
            # Create reports directory if it doesn't exist
            os.makedirs(self.reports_dir, exist_ok=True)
            
            # Load configuration validation report
            config_files = glob.glob(os.path.join(self.reports_dir, 'config_validation_*.json'))
            if config_files:
                latest_file = max(config_files, key=os.path.getmtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    self.report_data['config_validation'] = json.load(f)
                    self.report_data['config_validation']['source_file'] = os.path.basename(latest_file)
            
            # Load connectivity check report
            conn_files = glob.glob(os.path.join(self.reports_dir, 'connectivity_check_*.json'))
            if conn_files:
                latest_file = max(conn_files, key=os.path.getmtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    self.report_data['connectivity_check'] = json.load(f)
                    self.report_data['connectivity_check']['source_file'] = os.path.basename(latest_file)
            
            # Load IO validation report
            io_files = glob.glob(os.path.join(self.reports_dir, 'io_validation_*.json'))
            if io_files:
                latest_file = max(io_files, key=os.path.getmtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    self.report_data['io_validation'] = json.load(f)
                    self.report_data['io_validation']['source_file'] = os.path.basename(latest_file)
            
            # Load controller validation report
            controller_files = glob.glob(os.path.join(self.reports_dir, 'controller_validation_*.json'))
            if controller_files:
                latest_file = max(controller_files, key=os.path.getmtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    self.report_data['controller_validation'] = json.load(f)
                    self.report_data['controller_validation']['source_file'] = os.path.basename(latest_file)
            
            # Project summary is typically HTML, but try to load both formats
            project_summary_html = glob.glob(os.path.join(self.reports_dir, 'project_summary_*.html'))
            project_summary_json = glob.glob(os.path.join(self.reports_dir, 'project_summary_*.json'))
            
            if project_summary_json:
                latest_file = max(project_summary_json, key=os.path.getmtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    self.report_data['project_summary'] = json.load(f)
                    self.report_data['project_summary']['source_file'] = os.path.basename(latest_file)
                    self.report_data['project_summary']['type'] = 'json'
            
            if project_summary_html:
                latest_file = max(project_summary_html, key=os.path.getmtime)
                self.report_data['project_summary_html'] = latest_file
                self.report_data['project_summary_html_file'] = os.path.basename(latest_file)
            
            return True
        except Exception as e:
            print(f"Error loading report files: {str(e)}")
            return False
    
    def generate_html_report(self):
        """Generate a comprehensive HTML report from all loaded data."""
        html = []
        
        # HTML header
        html.append("<!DOCTYPE html>")
        html.append('<html lang="en">')
        html.append('<head>')
        html.append('  <meta charset="UTF-8">')
        html.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html.append('  <title>WWTP System Verification Report</title>')
        html.append('  <style>')
        html.append('    body { font-family: Arial, sans-serif; margin: 20px; color: #333; }')
        html.append('    h1, h2, h3 { color: #0066cc; }')
        html.append('    .header { background-color: #0066cc; color: white; padding: 20px; border-radius: 4px; }')
        html.append('    .section { margin: 20px 0; border: 1px solid #ddd; padding: 20px; border-radius: 4px; }')
        html.append('    .summary { background-color: #f5f5f5; padding: 15px; border-left: 4px solid #0066cc; }')
        html.append('    .pass { color: #008800; font-weight: bold; }')
        html.append('    .fail { color: #cc0000; font-weight: bold; }')
        html.append('    .warning { color: #ff9900; font-weight: bold; }')
        html.append('    .error-list { background-color: #fff0f0; border-left: 4px solid #cc0000; padding: 10px; }')
        html.append('    .warning-list { background-color: #fffbe6; border-left: 4px solid #ff9900; padding: 10px; }')
        html.append('    table { border-collapse: collapse; width: 100%; margin: 15px 0; }')
        html.append('    th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }')
        html.append('    th { background-color: #f2f2f2; }')
        html.append('    .details-container { margin-top: 15px; }')
        html.append('    .details-toggle { cursor: pointer; padding: 10px; background-color: #f2f2f2; border: none; ')
        html.append('                      width: 100%; text-align: left; font-weight: bold; }')
        html.append('    .details-content { display: none; padding: 10px; border: 1px solid #ddd; }')
        html.append('    .tab { overflow: hidden; border: 1px solid #ccc; background-color: #f1f1f1; }')
        html.append('    .tab button { background-color: inherit; float: left; border: none; outline: none;')
        html.append('                  cursor: pointer; padding: 14px 16px; transition: 0.3s; }')
        html.append('    .tab button:hover { background-color: #ddd; }')
        html.append('    .tab button.active { background-color: #ccc; }')
        html.append('    .tabcontent { display: none; padding: 6px 12px; border: 1px solid #ccc; border-top: none; }')
        html.append('    iframe { border: none; width: 100%; height: 600px; }')
        html.append('  </style>')
        html.append('</head>')
        html.append('<body>')
        
        # Report header
        html.append('  <div class="header">')
        html.append('    <h1>Wastewater Treatment Plant - System Verification Report</h1>')
        html.append(f'    <p>Generated: {self.report_data["timestamp"]}</p>')
        html.append('  </div>')
        
        # Overall summary
        html.append('  <div class="section summary">')
        html.append('    <h2>Verification Summary</h2>')
        
        # Determine overall status
        config_status = self._get_status(self.report_data['config_validation'], 'status')
        conn_status = self._get_status(self.report_data['connectivity_check'], 'overall_status')
        io_status = self._get_status(self.report_data['io_validation'], 'validation.status')
        controller_status = self._get_status(self.report_data['controller_validation'], 'overall_status')
        
        overall_status = 'passed'
        if any(s == 'failed' for s in [config_status, conn_status, io_status, controller_status]):
            overall_status = 'failed'
        elif any(s == 'warning' for s in [config_status, conn_status, io_status, controller_status]):
            overall_status = 'warning'
        
        status_class = 'pass' if overall_status == 'passed' else ('warning' if overall_status == 'warning' else 'fail')
        html.append(f'    <h3>Overall Status: <span class="{status_class}">{overall_status.upper()}</span></h3>')
        
        html.append('    <table>')
        html.append('      <tr><th>Verification Component</th><th>Status</th><th>Source</th></tr>')
        
        # Configuration validation status
        status_class = 'pass' if config_status == 'passed' else ('warning' if config_status == 'warning' else 'fail')
        source_file = self.report_data['config_validation'].get('source_file', 'N/A') if self.report_data['config_validation'] else 'N/A'
        html.append(f'      <tr><td>Configuration Validation</td><td class="{status_class}">{config_status.upper()}</td><td>{source_file}</td></tr>')
        
        # Connectivity check status
        status_class = 'pass' if conn_status == 'passed' else ('warning' if conn_status == 'warning' else 'fail')
        source_file = self.report_data['connectivity_check'].get('source_file', 'N/A') if self.report_data['connectivity_check'] else 'N/A'
        html.append(f'      <tr><td>Connectivity Check</td><td class="{status_class}">{conn_status.upper()}</td><td>{source_file}</td></tr>')
        
        # I/O validation status
        status_class = 'pass' if io_status == 'passed' else ('warning' if io_status == 'warning' else 'fail')
        source_file = self.report_data['io_validation'].get('source_file', 'N/A') if self.report_data['io_validation'] else 'N/A'
        html.append(f'      <tr><td>I/O Configuration Validation</td><td class="{status_class}">{io_status.upper()}</td><td>{source_file}</td></tr>')
        
        # Controller validation status
        status_class = 'pass' if controller_status == 'passed' else ('warning' if controller_status == 'warning' else 'fail')
        source_file = self.report_data['controller_validation'].get('source_file', 'N/A') if self.report_data['controller_validation'] else 'N/A'
        html.append(f'      <tr><td>Controller Validation</td><td class="{status_class}">{controller_status.upper()}</td><td>{source_file}</td></tr>')
        
        html.append('    </table>')
        
        # Add aggregated errors and warnings
        html.append('    <div class="details-container">')
        html.append('      <button class="details-toggle" onclick="toggleDetails(\'aggregated-errors\')">► Show All Errors</button>')
        html.append('      <div id="aggregated-errors" class="details-content error-list">')
        
        # Collect all errors
        all_errors = []
        if self.report_data['config_validation'] and 'errors' in self.report_data['config_validation']:
            for error in self.report_data['config_validation']['errors']:
                all_errors.append(f"[Config] {error}")
        
        if self.report_data['io_validation'] and 'validation' in self.report_data['io_validation'] and 'errors' in self.report_data['io_validation']['validation']:
            for error in self.report_data['io_validation']['validation']['errors']:
                all_errors.append(f"[I/O] {error}")
        
        if all_errors:
            html.append('        <ul>')
            for error in all_errors:
                html.append(f'          <li>{error}</li>')
            html.append('        </ul>')
        else:
            html.append('        <p>No errors found.</p>')
        
        html.append('      </div>')
        html.append('    </div>')
        
        # Add warnings container
        html.append('    <div class="details-container">')
        html.append('      <button class="details-toggle" onclick="toggleDetails(\'aggregated-warnings\')">► Show All Warnings</button>')
        html.append('      <div id="aggregated-warnings" class="details-content warning-list">')
        
        # Collect all warnings
        all_warnings = []
        if self.report_data['config_validation'] and 'warnings' in self.report_data['config_validation']:
            for warning in self.report_data['config_validation']['warnings']:
                all_warnings.append(f"[Config] {warning}")
        
        if self.report_data['io_validation'] and 'validation' in self.report_data['io_validation'] and 'warnings' in self.report_data['io_validation']['validation']:
            for warning in self.report_data['io_validation']['validation']['warnings']:
                all_warnings.append(f"[I/O] {warning}")
        
        if all_warnings:
            html.append('        <ul>')
            for warning in all_warnings:
                html.append(f'          <li>{warning}</li>')
            html.append('        </ul>')
        else:
            html.append('        <p>No warnings found.</p>')
        
        html.append('      </div>')
        html.append('    </div>')
        
        html.append('  </div>')  # End of summary section
        
        # Detailed reports in tabs
        html.append('  <div class="section">')
        html.append('    <h2>Detailed Reports</h2>')
        
        # Create tabs
        html.append('    <div class="tab">')
        html.append('      <button class="tablinks" onclick="openTab(event, \'ConfigTab\')" id="defaultOpen">Configuration</button>')
        html.append('      <button class="tablinks" onclick="openTab(event, \'ConnectivityTab\')">Connectivity</button>')
        html.append('      <button class="tablinks" onclick="openTab(event, \'IOTab\')">I/O Configuration</button>')
        html.append('      <button class="tablinks" onclick="openTab(event, \'ControllerTab\')">Controllers</button>')
        html.append('      <button class="tablinks" onclick="openTab(event, \'SummaryTab\')">Project Summary</button>')
        html.append('    </div>')
        
        # Configuration Validation Tab
        html.append('    <div id="ConfigTab" class="tabcontent">')
        html.append('      <h3>Configuration Validation</h3>')
        if self.report_data['config_validation']:
            html.append(self._format_config_validation(self.report_data['config_validation']))
        else:
            html.append('      <p>No configuration validation data available.</p>')
        html.append('    </div>')
        
        # Connectivity Check Tab
        html.append('    <div id="ConnectivityTab" class="tabcontent">')
        html.append('      <h3>Connectivity Check</h3>')
        if self.report_data['connectivity_check']:
            html.append(self._format_connectivity_check(self.report_data['connectivity_check']))
        else:
            html.append('      <p>No connectivity check data available.</p>')
        html.append('    </div>')
        
        # I/O Configuration Tab
        html.append('    <div id="IOTab" class="tabcontent">')
        html.append('      <h3>I/O Configuration Validation</h3>')
        if self.report_data['io_validation']:
            html.append(self._format_io_validation(self.report_data['io_validation']))
        else:
            html.append('      <p>No I/O validation data available.</p>')
        html.append('    </div>')
        
        # Controller Validation Tab
        html.append('    <div id="ControllerTab" class="tabcontent">')
        html.append('      <h3>Controller Validation</h3>')
        if self.report_data['controller_validation']:
            html.append(self._format_controller_validation(self.report_data['controller_validation']))
        else:
            html.append('      <p>No controller validation data available.</p>')
        html.append('    </div>')
        
        # Project Summary Tab
        html.append('    <div id="SummaryTab" class="tabcontent">')
        html.append('      <h3>Project Summary</h3>')
        
        if 'project_summary_html' in self.report_data:
            # If we have an HTML summary, embed it
            relative_path = os.path.relpath(self.report_data['project_summary_html'], os.path.dirname(self.reports_dir))
            html.append(f'      <p>Project summary available: <a href="{relative_path}" target="_blank">{self.report_data["project_summary_html_file"]}</a></p>')
            html.append(f'      <iframe src="{relative_path}"></iframe>')
        elif self.report_data['project_summary']:
            # If we have JSON data, format it
            html.append(self._format_project_summary(self.report_data['project_summary']))
        else:
            html.append('      <p>No project summary data available.</p>')
        
        html.append('    </div>')
        
        html.append('  </div>')  # End of detailed reports section
        
        # JavaScript functions
        html.append('  <script>')
        html.append('    function toggleDetails(id) {')
        html.append('      var content = document.getElementById(id);')
        html.append('      var button = content.previousElementSibling;')
        html.append('      if (content.style.display === "block") {')
        html.append('        content.style.display = "none";')
        html.append('        button.innerHTML = "► " + button.innerHTML.substring(2);')
        html.append('      } else {')
        html.append('        content.style.display = "block";')
        html.append('        button.innerHTML = "▼ " + button.innerHTML.substring(2);')
        html.append('      }')
        html.append('    }')
        
        html.append('    function openTab(evt, tabName) {')
        html.append('      var i, tabcontent, tablinks;')
        html.append('      tabcontent = document.getElementsByClassName("tabcontent");')
        html.append('      for (i = 0; i < tabcontent.length; i++) {')
        html.append('        tabcontent[i].style.display = "none";')
        html.append('      }')
        html.append('      tablinks = document.getElementsByClassName("tablinks");')
        html.append('      for (i = 0; i < tablinks.length; i++) {')
        html.append('        tablinks[i].className = tablinks[i].className.replace(" active", "");')
        html.append('      }')
        html.append('      document.getElementById(tabName).style.display = "block";')
        html.append('      evt.currentTarget.className += " active";')
        html.append('    }')
        
        html.append('    // Get the element with id="defaultOpen" and click on it')
        html.append('    document.getElementById("defaultOpen").click();')
        html.append('  </script>')
        
        html.append('</body>')
        html.append('</html>')
        
        return "\n".join(html)
    
    def _format_config_validation(self, config_data):
        """Format configuration validation data for HTML display."""
        output = []
        
        # Remove source_file from display
        if 'source_file' in config_data:
            del config_data['source_file']
        
        # Overall status
        status = config_data.get('status', 'unknown')
        status_class = 'pass' if status == 'passed' else ('warning' if status == 'warning' else 'fail')
        output.append(f'<p>Status: <span class="{status_class}">{status.upper()}</span></p>')
        
        # Errors and warnings
        if 'errors' in config_data and config_data['errors']:
            output.append('<div class="error-list">')
            output.append('<h4>Errors:</h4>')
            output.append('<ul>')
            for error in config_data['errors']:
                output.append(f'<li>{error}</li>')
            output.append('</ul>')
            output.append('</div>')
        
        if 'warnings' in config_data and config_data['warnings']:
            output.append('<div class="warning-list">')
            output.append('<h4>Warnings:</h4>')
            output.append('<ul>')
            for warning in config_data['warnings']:
                output.append(f'<li>{warning}</li>')
            output.append('</ul>')
            output.append('</div>')
        
        # Detailed validation results
        if 'details' in config_data and config_data['details']:
            output.append('<div class="details-container">')
            output.append('<button class="details-toggle" onclick="toggleDetails(\'config-details\')">► Show Validation Details</button>')
            output.append('<div id="config-details" class="details-content">')
            
            for category, details in config_data['details'].items():
                output.append(f'<h4>{category.replace("_", " ").title()}</h4>')
                output.append(f'<p>Status: <span class="{details["status"]}">{details["status"].upper()}</span></p>')
                
                if 'errors' in details and details['errors']:
                    output.append('<h5>Errors:</h5>')
                    output.append('<ul>')
                    for error in details['errors']:
                        output.append(f'<li>{error}</li>')
                    output.append('</ul>')
                
                if 'warnings' in details and details['warnings']:
                    output.append('<h5>Warnings:</h5>')
                    output.append('<ul>')
                    for warning in details['warnings']:
                        output.append(f'<li>{warning}</li>')
                    output.append('</ul>')
            
            output.append('</div>')
            output.append('</div>')
        
        return "\n".join(output)
    
    def _format_connectivity_check(self, conn_data):
        """Format connectivity check data for HTML display."""
        output = []
        
        # Remove source_file from display
        if 'source_file' in conn_data:
            del conn_data['source_file']
        
        # System information
        output.append('<div class="summary">')
        output.append(f'<p>System: {conn_data.get("system", "Unknown")} ({conn_data.get("hostname", "Unknown")})</p>')
        output.append(f'<p>Timestamp: {conn_data.get("timestamp", "Unknown")}</p>')
        
        # Overall status
        status = conn_data.get('overall_status', 'unknown')
        status_class = 'pass' if status == 'passed' else ('warning' if status == 'warning' else 'fail')
        output.append(f'<p>Status: <span class="{status_class}">{status.upper()}</span></p>')
        output.append('</div>')
        
        # Test results
        if 'tests' in conn_data:
            output.append('<h4>Test Results</h4>')
            output.append('<table>')
            output.append('<tr><th>Test</th><th>Status</th><th>Details</th></tr>')
            
            for test_name, test_result in conn_data['tests'].items():
                if isinstance(test_result, dict) and 'status' in test_result:
                    test_status = test_result['status']
                    status_class = 'pass' if test_status == 'passed' else ('warning' if test_status in ['timeout', 'skipped'] else 'fail')
                    details = test_result.get('details', '')
                    
                    output.append(f'<tr>')
                    output.append(f'<td>{test_name.replace("_", " ").title()}</td>')
                    output.append(f'<td class="{status_class}">{test_status.upper()}</td>')
                    output.append(f'<td>{details}</td>')
                    output.append('</tr>')
            
            output.append('</table>')
        
        return "\n".join(output)
    
    def _format_io_validation(self, io_data):
        """Format I/O validation data for HTML display."""
        output = []
        
        # Remove source_file from display
        if 'source_file' in io_data:
            del io_data['source_file']
        
        # Get validation section
        validation = io_data.get('validation', {})
        
        # Overall status
        status = validation.get('status', 'unknown')
        status_class = 'pass' if status == 'passed' else ('warning' if status == 'warning' else 'fail')
        output.append(f'<p>Status: <span class="{status_class}">{status.upper()}</span></p>')
        
        # Errors and warnings
        if 'errors' in validation and validation['errors']:
            output.append('<div class="error-list">')
            output.append('<h4>Errors:</h4>')
            output.append('<ul>')
            for error in validation['errors']:
                output.append(f'<li>{error}</li>')
            output.append('</ul>')
            output.append('</div>')
        
        if 'warnings' in validation and validation['warnings']:
            output.append('<div class="warning-list">')
            output.append('<h4>Warnings:</h4>')
            output.append('<ul>')
            for warning in validation['warnings']:
                output.append(f'<li>{warning}</li>')
            output.append('</ul>')
            output.append('</div>')
        
        # I/O Point Summary
        if 'details' in validation and 'hardware' in validation['details'] and 'required' in validation['details']:
            hw = validation['details']['hardware']
            req = validation['details']['required']
            
            output.append('<h4>I/O Point Summary</h4>')
            output.append('<table>')
            output.append('<tr><th>I/O Type</th><th>Required</th><th>Available</th><th>Status</th></tr>')
            
            io_types = [
                ('Digital Inputs', 'di', 'digital_inputs'),
                ('Digital Outputs', 'do', 'digital_outputs'),
                ('Analog Inputs', 'ai', 'analog_inputs'),
                ('Analog Outputs', 'ao', 'analog_outputs')
            ]
            
            for label, req_key, hw_key in io_types:
                req_count = req.get(req_key, 0)
                hw_count = hw.get(hw_key, 0)
                status_class = 'pass' if hw_count >= req_count else 'fail'
                status_text = 'OK' if hw_count >= req_count else 'Insufficient'
                
                output.append('<tr>')
                output.append(f'<td>{label}</td>')
                output.append(f'<td>{req_count}</td>')
                output.append(f'<td>{hw_count}</td>')
                output.append(f'<td class="{status_class}">{status_text}</td>')
                output.append('</tr>')
            
            output.append('</table>')
        
        # Missing I/O details
        if 'details' in validation and 'missing_io' in validation['details']:
            missing_io = validation['details']['missing_io']
            
            output.append('<div class="details-container">')
            output.append('<button class="details-toggle" onclick="toggleDetails(\'missing-io\')">► Show Missing I/O Details</button>')
            output.append('<div id="missing-io" class="details-content">')
            
            output.append('<h4>Missing I/O Tags</h4>')
            
            for component, missing_tags in missing_io.items():
                output.append(f'<h5>{component.replace("_", " ").title()}</h5>')
                if missing_tags:
                    output.append('<ul>')
                    for tag in missing_tags:
                        output.append(f'<li>{tag}</li>')
                    output.append('</ul>')
                else:
                    output.append('<p>No missing tags</p>')
            
            output.append('</div>')
            output.append('</div>')
        
        # I/O configuration
        if 'io_configuration' in io_data:
            output.append('<div class="details-container">')
            output.append('<button class="details-toggle" onclick="toggleDetails(\'io-config\')">► Show I/O Configuration</button>')
            output.append('<div id="io-config" class="details-content">')
            
            output.append('<h4>I/O Configuration</h4>')
            
            for controller, config in io_data['io_configuration'].items():
                output.append(f'<h5>{controller.replace("_", " ").title()} Controller</h5>')
                
                for io_type in ['di', 'do', 'ai', 'ao']:
                    if io_type in config:
                        output.append(f'<p>{io_type.upper()}:</p>')
                        output.append('<ul>')
                        for tag in config[io_type]:
                            output.append(f'<li>{tag}</li>')
                        output.append('</ul>')
            
            output.append('</div>')
            output.append('</div>')
        
        return "\n".join(output)
    
    def _format_controller_validation(self, controller_data):
        """Format controller validation data for HTML display."""
        output = []
        
        # Remove source_file from display
        if 'source_file' in controller_data:
            del controller_data['source_file']
        
        # Overall information
        output.append('<div class="summary">')
        output.append(f'<p>Timestamp: {controller_data.get("timestamp", "Unknown")}</p>')
        
        # Overall status
        status = controller_data.get('overall_status', 'unknown')
        status_class = 'pass' if status == 'passed' else ('warning' if status == 'warning' else 'fail')
        output.append(f'<p>Status: <span class="{status_class}">{status.upper()}</span></p>')
        
        output.append(f'<p>Controllers Tested: {controller_data.get("controllers_tested", 0)}</p>')
        output.append(f'<p>Controllers Passed: {controller_data.get("controllers_passed", 0)}</p>')
        output.append('</div>')
        
        # Controller details
        if 'details' in controller_data:
            for controller_name, result in controller_data['details'].items():
                if controller_name.startswith('_'):  # Skip private fields
                    continue
                
                output.append('<div class="section">')
                output.append(f'<h4>{controller_name.replace("_", " ").title()}</h4>')
                
                # Status
                status = result.get('status', 'unknown')
                status_class = 'pass' if status == 'completed' and result.get('passed', False) else 'fail'
                output.append(f'<p>Status: <span class="{status_class}">{status.upper()}</span></p>')
                
                # Performance rating
                if 'performance_rating' in result:
                    rating = result['performance_rating']
                    rating_class = 'pass' if rating in ['Excellent', 'Good'] else ('warning' if rating == 'Fair' else 'fail')
                    output.append(f'<p>Performance Rating: <span class="{rating_class}">{rating}</span></p>')
                
                # Issues
                if 'issues' in result and result['issues']:
                    output.append('<div class="warning-list">')
                    output.append('<h5>Issues:</h5>')
                    output.append('<ul>')
                    for issue in result['issues']:
                        output.append(f'<li>{issue}</li>')
                    output.append('</ul>')
                    output.append('</div>')
                
                # Performance metrics
                metrics = {}
                for key, value in result.items():
                    if key.startswith('avg_') or key.startswith('max_'):
                        metrics[key] = value
                
                if metrics:
                    output.append('<h5>Performance Metrics:</h5>')
                    output.append('<table>')
                    output.append('<tr><th>Metric</th><th>Value</th></tr>')
                    
                    for key, value in metrics.items():
                        output.append('<tr>')
                        output.append(f'<td>{key.replace("_", " ").title()}</td>')
                        output.append(f'<td>{value}</td>')
                        output.append('</tr>')
                    
                    output.append('</table>')
                
                # Test cases
                if 'test_cases' in result:
                    output.append('<div class="details-container">')
                    output.append(f'<button class="details-toggle" onclick="toggleDetails(\'{controller_name}-tests\')">► Show Test Cases</button>')
                    output.append(f'<div id="{controller_name}-tests" class="details-content">')
                    
                    for i, test_case in enumerate(result['test_cases']):
                        output.append(f'<h5>Test {i+1}: {test_case["name"]}</h5>')
                        output.append(f'<p>Type: {test_case["type"]}</p>')
                        output.append(f'<p>Duration: {test_case["duration_sec"]} seconds</p>')
                        
                        # If there's a plot path, show the image
                        if 'plot_path' in test_case:
                            plot_rel_path = os.path.relpath(test_case['plot_path'], os.path.dirname(self.reports_dir))
                            output.append(f'<img src="{plot_rel_path}" alt="Test Plot" style="max-width: 100%;">')
                    
                    output.append('</div>')
                    output.append('</div>')
                
                output.append('</div>')
        
        return "\n".join(output)
    
    def _format_project_summary(self, summary_data):
        """Format project summary data for HTML display when HTML version is not available."""
        output = []
        
        # Remove source_file from display
        if 'source_file' in summary_data:
            del summary_data['source_file']
        
        # Basic project information
        output.append('<div class="summary">')
        output.append(f'<p>Project Name: {summary_data.get("project_name", "Unknown")}</p>')
        output.append(f'<p>Generated: {summary_data.get("generated_timestamp", "Unknown")}</p>')
        output.append(f'<p>System Capacity: {summary_data.get("system_capacity", "Unknown")}</p>')
        output.append(f'<p>System Version: {summary_data.get("system_version", "Unknown")}</p>')
        output.append('</div>')
        
        # Source code statistics
        if 'statistics' in summary_data and 'source_code' in summary_data['statistics']:
            stats = summary_data['statistics']['source_code']
            
            output.append('<h4>Code Statistics</h4>')
            output.append('<table>')
            
            # PLC code stats
            if 'plc' in stats:
                output.append('<tr><th colspan="2">PLC Code</th></tr>')
                output.append(f'<tr><td>Files</td><td>{stats["plc"].get("files", 0)}</td></tr>')
                output.append(f'<tr><td>Lines of Code</td><td>{stats["plc"].get("lines_of_code", 0)}</td></tr>')
                output.append(f'<tr><td>Function Blocks</td><td>{stats["plc"].get("function_blocks", 0)}</td></tr>')
            
            # Python code stats
            if 'python' in stats:
                output.append('<tr><th colspan="2">Python Code</th></tr>')
                output.append(f'<tr><td>Files</td><td>{stats["python"].get("files", 0)}</td></tr>')
                output.append(f'<tr><td>Lines of Code</td><td>{stats["python"].get("lines_of_code", 0)}</td></tr>')
                output.append(f'<tr><td>Classes</td><td>{stats["python"].get("classes", 0)}</td></tr>')
                output.append(f'<tr><td>Functions</td><td>{stats["python"].get("functions", 0)}</td></tr>')
            
            # Other code stats
            output.append('<tr><th colspan="2">Other</th></tr>')
            output.append(f'<tr><td>Web Files</td><td>{stats.get("web", {}).get("files", 0)}</td></tr>')
            output.append(f'<tr><td>Batch Scripts</td><td>{stats.get("batch", {}).get("files", 0)}</td></tr>')
            
            output.append('</table>')
        
        # Components
        if 'components' in summary_data:
            output.append('<div class="details-container">')
            output.append('<button class="details-toggle" onclick="toggleDetails(\'components\')">► Show System Components</button>')
            output.append('<div id="components" class="details-content">')
            
            output.append('<h4>System Components</h4>')
            
            # Group components by type
            component_types = {}
            for component in summary_data['components']:
                comp_type = component.get('type', 'other')
                if comp_type not in component_types:
                    component_types[comp_type] = []
                component_types[comp_type].append(component)
            
            for comp_type, components in component_types.items():
                output.append(f'<h5>{comp_type.replace("_", " ").title()} ({len(components)})</h5>')
                output.append('<ul>')
                for component in components:
                    output.append(f'<li>{component["name"]}</li>')
                output.append('</ul>')
            
            output.append('</div>')
            output.append('</div>')
        
        # Documentation status
        if 'documentation' in summary_data:
            docs = summary_data['documentation']
            
            output.append('<h4>Documentation Status</h4>')
            output.append(f'<p>Total Documentation Files: {docs.get("total_files", 0)}</p>')
            
            output.append('<table>')
            output.append('<tr><th>Document</th><th>Status</th><th>Words</th><th>Sections</th><th>Last Modified</th></tr>')
            
            for doc_name, status in docs.items():
                if doc_name == 'total_files':
                    continue
                
                if status.get('exists', False):
                    status_class = 'pass'
                    status_text = 'Present'
                    word_count = status.get('word_count', 0)
                    sections = status.get('sections', 0)
                    last_modified = status.get('last_modified', 'Unknown')
                else:
                    status_class = 'fail'
                    status_text = 'Missing'
                    word_count = '-'
                    sections = '-'
                    last_modified = '-'
                
                output.append('<tr>')
                output.append(f'<td>{doc_name}</td>')
                output.append(f'<td class="{status_class}">{status_text}</td>')
                output.append(f'<td>{word_count}</td>')
                output.append(f'<td>{sections}</td>')
                output.append(f'<td>{last_modified}</td>')
                output.append('</tr>')
            
            output.append('</table>')
        
        return "\n".join(output)
    
    def _get_status(self, data, path):
        """Extract status from nested JSON data using a dot path notation."""
        if not data:
            return 'unknown'
        
        path_parts = path.split('.')
        current = data
        
        for part in path_parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return 'unknown'
        
        if isinstance(current, str):
            if current.lower() in ['passed', 'pass', 'ok', 'success', 'completed']:
                return 'passed'
            elif current.lower() in ['failed', 'fail', 'error']:
                return 'failed'
            elif current.lower() in ['warning', 'warnings']:
                return 'warning'
            else:
                return current.lower()
        
        return 'unknown'
    
    def save_report(self, output_file):
        """Save the generated report to a file."""
        try:
            html_content = self.generate_html_report()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return True
        except Exception as e:
            print(f"Error saving report: {str(e)}")
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate comprehensive system verification report')
    parser.add_argument('--project-root', '-p', type=str,
                       default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')),
                       help='Path to project root directory')
    parser.add_argument('--reports-dir', '-r', type=str, default=None,
                       help='Path to reports directory (defaults to PROJECT_ROOT/reports)')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output HTML report file path')
    
    args = parser.parse_args()
    
    # Determine output file path
    if not args.output:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        reports_dir = args.reports_dir or os.path.join(args.project_root, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        output_file = os.path.join(reports_dir, f'system_verification_report_{timestamp}.html')
    else:
        output_file = args.output
    
    # Generate the report
    generator = SystemReportGenerator(args.project_root, args.reports_dir)
    
    if generator.load_report_files():
        if generator.save_report(output_file):
            print(f"System verification report generated successfully: {output_file}")
            
            # Try to open the report in the default browser
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(output_file)
                else:  # macOS or Linux
                    import subprocess
                    subprocess.call(['xdg-open', output_file])
            except:
                print("Note: Could not open the report automatically. Please open it manually.")
            
            sys.exit(0)
        else:
            print("Failed to save report")
            sys.exit(1)
    else:
        print("Failed to load report files")
        sys.exit(1)
