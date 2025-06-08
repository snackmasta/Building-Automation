#!/usr/bin/env python3
"""
HVAC System - Test Report Summary Generator
Analyzes all test reports and creates a comprehensive summary

Author: System Engineer
Date: June 8, 2025
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class TestReportAnalyzer:
    """Analyzes and summarizes all test reports"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.reports_dir = self.project_root / "tests" / "reports"
        self.summary = {
            'analysis_timestamp': datetime.now().isoformat(),
            'total_reports': 0,
            'categories': {
                'final_verification': {'count': 0, 'latest_success_rate': 0},
                'restructuring': {'count': 0, 'latest_success_rate': 0},
                'archived': {'count': 0, 'latest_success_rate': 0}
            },
            'latest_results': {},
            'trend_analysis': {}
        }
    
    def analyze_final_verification_reports(self):
        """Analyze final verification reports"""
        reports_path = self.reports_dir / "final_verification"
        if not reports_path.exists():
            return
        
        reports = sorted(reports_path.glob("*.json"))
        self.summary['categories']['final_verification']['count'] = len(reports)
        
        if reports:
            # Get latest report
            latest_report_path = reports[-1]
            with open(latest_report_path, 'r', encoding='utf-8') as f:
                latest_data = json.load(f)
            
            self.summary['latest_results']['final_verification'] = {
                'file': latest_report_path.name,
                'timestamp': latest_data.get('timestamp'),
                'success_rate': latest_data.get('success_rate', '0%'),
                'status': latest_data.get('status', 'Unknown'),
                'total_tests': latest_data.get('total_tests', 0),
                'passed_tests': latest_data.get('passed_tests', 0)
            }
            
            # Extract numeric success rate
            success_rate_str = latest_data.get('success_rate', '0%')
            success_rate = float(success_rate_str.replace('%', ''))
            self.summary['categories']['final_verification']['latest_success_rate'] = success_rate
    
    def analyze_restructuring_reports(self):
        """Analyze restructuring verification reports"""
        reports_path = self.reports_dir / "restructuring"
        if not reports_path.exists():
            return
        
        reports = sorted(reports_path.glob("*.json"))
        self.summary['categories']['restructuring']['count'] = len(reports)
        
        if reports:
            # Get latest report
            latest_report_path = reports[-1]
            with open(latest_report_path, 'r', encoding='utf-8') as f:
                latest_data = json.load(f)
            
            self.summary['latest_results']['restructuring'] = {
                'file': latest_report_path.name,
                'timestamp': latest_data.get('timestamp'),
                'success': latest_data.get('success', False),
                'verification_type': latest_data.get('verification_type', 'Unknown')
            }
            
            # Convert success to percentage
            success_rate = 100.0 if latest_data.get('success', False) else 0.0
            self.summary['categories']['restructuring']['latest_success_rate'] = success_rate
    
    def analyze_archived_reports(self):
        """Analyze archived reports"""
        reports_path = self.reports_dir / "archived"
        if not reports_path.exists():
            return
        
        reports = sorted(reports_path.glob("*.json"))
        self.summary['categories']['archived']['count'] = len(reports)
        
        if reports:
            # Get latest report
            latest_report_path = reports[-1]
            with open(latest_report_path, 'r', encoding='utf-8') as f:
                latest_data = json.load(f)
            
            self.summary['latest_results']['archived'] = {
                'file': latest_report_path.name,
                'timestamp': latest_data.get('timestamp'),
                'summary': latest_data.get('summary', {})
            }
    
    def calculate_trends(self):
        """Calculate trend analysis across reports"""
        # Analyze final verification trends
        reports_path = self.reports_dir / "final_verification"
        if reports_path.exists():
            reports = sorted(reports_path.glob("*.json"))
            success_rates = []
            
            for report_path in reports[-5:]:  # Last 5 reports
                try:
                    with open(report_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    success_rate_str = data.get('success_rate', '0%')
                    success_rate = float(success_rate_str.replace('%', ''))
                    success_rates.append(success_rate)
                except:
                    continue
            
            if success_rates:
                self.summary['trend_analysis']['final_verification'] = {
                    'recent_success_rates': success_rates,
                    'average_success_rate': sum(success_rates) / len(success_rates),
                    'trend': 'improving' if len(success_rates) > 1 and success_rates[-1] > success_rates[0] else 'stable'
                }
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("🔍 HVAC System - Test Report Analysis Summary")
        print("=" * 60)
        print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 Reports Directory: {self.reports_dir}")
        print()
        
        # Category overview
        print("📊 Report Categories Overview:")
        print("-" * 40)
        for category, data in self.summary['categories'].items():
            count = data['count']
            success_rate = data['latest_success_rate']
            status_icon = "✅" if success_rate >= 90 else "⚠️" if success_rate >= 70 else "❌"
            print(f"{status_icon} {category.replace('_', ' ').title():<20} {count:>3} reports (Latest: {success_rate:.1f}%)")
        
        print()
        
        # Latest results
        print("🎯 Latest Test Results:")
        print("-" * 40)
        
        if 'final_verification' in self.summary['latest_results']:
            fv = self.summary['latest_results']['final_verification']
            status_icon = "✅" if fv['status'] == 'COMPLETE SUCCESS' else "⚠️"
            print(f"{status_icon} Final Verification: {fv['passed_tests']}/{fv['total_tests']} tests passed ({fv['success_rate']})")
            print(f"   Status: {fv['status']}")
            print(f"   Report: {fv['file']}")
        
        if 'restructuring' in self.summary['latest_results']:
            rs = self.summary['latest_results']['restructuring']
            status_icon = "✅" if rs['success'] else "❌"
            print(f"{status_icon} Restructuring: {'Completed Successfully' if rs['success'] else 'Issues Found'}")
            print(f"   Report: {rs['file']}")
        
        print()
        
        # Trend analysis
        if 'final_verification' in self.summary['trend_analysis']:
            trend = self.summary['trend_analysis']['final_verification']
            trend_icon = "📈" if trend['trend'] == 'improving' else "📊"
            print(f"{trend_icon} Trend Analysis:")
            print(f"   Average Success Rate: {trend['average_success_rate']:.1f}%")
            print(f"   Recent Trend: {trend['trend'].title()}")
            print(f"   Recent Success Rates: {trend['recent_success_rates']}")
        
        print()
        
        # Overall system status
        overall_success = self.summary['categories']['final_verification']['latest_success_rate']
        if overall_success >= 90:
            print("🎉 OVERALL STATUS: EXCELLENT - System fully operational!")
        elif overall_success >= 70:
            print("✅ OVERALL STATUS: GOOD - System mostly operational")
        else:
            print("⚠️ OVERALL STATUS: NEEDS ATTENTION - Issues require resolution")
        
        print()
        
        return self.summary
    
    def save_summary_report(self):
        """Save the summary report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = self.reports_dir / f"SUMMARY_REPORT_{timestamp}.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.summary, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Summary report saved to: {summary_file}")
        return summary_file
    
    def run_analysis(self):
        """Run complete analysis"""
        self.analyze_final_verification_reports()
        self.analyze_restructuring_reports() 
        self.analyze_archived_reports()
        self.calculate_trends()
        
        self.summary['total_reports'] = sum(cat['count'] for cat in self.summary['categories'].values())
        
        # Generate and save report
        self.generate_summary_report()
        return self.save_summary_report()

def main():
    """Main function"""
    analyzer = TestReportAnalyzer()
    summary_file = analyzer.run_analysis()
    return 0

if __name__ == "__main__":
    sys.exit(main())
