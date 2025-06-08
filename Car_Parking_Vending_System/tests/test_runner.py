"""
Test Runner for Car Parking Vending System
Executes all unit and integration tests with detailed reporting
"""

import unittest
import sys
import os
import time
import json
from datetime import datetime
from io import StringIO

# Add source paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class TestRunner:
    """Enhanced test runner with detailed reporting and coverage"""
    
    def __init__(self):
        self.test_results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'execution_time': 0,
            'coverage': {},
            'detailed_results': []
        }
        
    def discover_tests(self):
        """Discover all test modules"""
        test_directories = [
            os.path.join(os.path.dirname(__file__), 'unit'),
            os.path.join(os.path.dirname(__file__), 'integration')
        ]
        
        test_suites = []
        for test_dir in test_directories:
            if os.path.exists(test_dir):
                loader = unittest.TestLoader()
                suite = loader.discover(test_dir, pattern='test_*.py')
                test_suites.append(suite)
                
        return unittest.TestSuite(test_suites)
        
    def run_tests(self, verbosity=2):
        """Run all discovered tests with detailed reporting"""
        print("=" * 70)
        print("CAR PARKING VENDING SYSTEM - TEST EXECUTION")
        print("=" * 70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Discover tests
        test_suite = self.discover_tests()
        
        # Create custom test result class for detailed tracking
        class DetailedTestResult(unittest.TextTestResult):
            def __init__(self, stream, descriptions, verbosity, test_runner):
                super().__init__(stream, descriptions, verbosity)
                self.test_runner = test_runner
                
            def addSuccess(self, test):
                super().addSuccess(test)
                self.test_runner.test_results['passed'] += 1
                self.test_runner.test_results['detailed_results'].append({
                    'test': str(test),
                    'status': 'PASSED',
                    'message': '',
                    'execution_time': getattr(test, '_execution_time', 0)
                })
                
            def addError(self, test, err):
                super().addError(test, err)
                self.test_runner.test_results['errors'] += 1
                self.test_runner.test_results['detailed_results'].append({
                    'test': str(test),
                    'status': 'ERROR',
                    'message': str(err[1]),
                    'execution_time': getattr(test, '_execution_time', 0)
                })
                
            def addFailure(self, test, err):
                super().addFailure(test, err)
                self.test_runner.test_results['failed'] += 1
                self.test_runner.test_results['detailed_results'].append({
                    'test': str(test),
                    'status': 'FAILED',
                    'message': str(err[1]),
                    'execution_time': getattr(test, '_execution_time', 0)
                })
                
            def addSkip(self, test, reason):
                super().addSkip(test, reason)
                self.test_runner.test_results['skipped'] += 1
                self.test_runner.test_results['detailed_results'].append({
                    'test': str(test),
                    'status': 'SKIPPED',
                    'message': reason,
                    'execution_time': 0
                })
        
        # Run tests with timing
        start_time = time.time()
        
        stream = StringIO()
        runner = unittest.TextTestRunner(
            stream=stream,
            verbosity=verbosity,
            resultclass=lambda s, d, v: DetailedTestResult(s, d, v, self)
        )
        
        result = runner.run(test_suite)
        
        end_time = time.time()
        self.test_results['execution_time'] = end_time - start_time
        self.test_results['total_tests'] = result.testsRun
        
        # Print results
        self._print_summary(result)
        self._generate_reports()
        
        return result.wasSuccessful()
        
    def _print_summary(self, result):
        """Print test execution summary"""
        print("\n" + "=" * 70)
        print("TEST EXECUTION SUMMARY")
        print("=" * 70)
        
        print(f"Total Tests Run: {self.test_results['total_tests']}")
        print(f"Passed: {self.test_results['passed']}")
        print(f"Failed: {self.test_results['failed']}")
        print(f"Errors: {self.test_results['errors']}")
        print(f"Skipped: {self.test_results['skipped']}")
        print(f"Execution Time: {self.test_results['execution_time']:.2f} seconds")
        
        if self.test_results['total_tests'] > 0:
            success_rate = (self.test_results['passed'] / self.test_results['total_tests']) * 100
            print(f"Success Rate: {success_rate:.1f}%")
            
        print("\n" + "-" * 70)
        
        # Print failed/error tests
        if self.test_results['failed'] > 0 or self.test_results['errors'] > 0:
            print("FAILED/ERROR TESTS:")
            print("-" * 30)
            for test_result in self.test_results['detailed_results']:
                if test_result['status'] in ['FAILED', 'ERROR']:
                    print(f"❌ {test_result['test']}")
                    print(f"   Status: {test_result['status']}")
                    if test_result['message']:
                        # Print first line of error message
                        first_line = test_result['message'].split('\n')[0]
                        print(f"   Error: {first_line}")
                    print()
                    
        # Print component coverage
        self._print_component_coverage()
        
    def _print_component_coverage(self):
        """Print test coverage by system component"""
        print("COMPONENT TEST COVERAGE:")
        print("-" * 30)
        
        components = {
            'Database': 0,
            'Communication': 0,
            'Simulation': 0,
            'Integration': 0,
            'Utilities': 0
        }
        
        for test_result in self.test_results['detailed_results']:
            test_name = test_result['test'].lower()
            if 'database' in test_name:
                components['Database'] += 1
            elif 'communication' in test_name:
                components['Communication'] += 1
            elif 'simulation' in test_name or 'parking' in test_name:
                components['Simulation'] += 1
            elif 'integration' in test_name:
                components['Integration'] += 1
            elif 'utilities' in test_name or 'system' in test_name:
                components['Utilities'] += 1
                
        for component, count in components.items():
            if count > 0:
                print(f"✓ {component}: {count} tests")
            else:
                print(f"⚠ {component}: No tests found")
                
    def _generate_reports(self):
        """Generate detailed test reports"""
        # Create reports directory
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate JSON report
        json_report_path = os.path.join(reports_dir, 'test_results.json')
        with open(json_report_path, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
            
        # Generate HTML report
        html_report_path = os.path.join(reports_dir, 'test_report.html')
        self._generate_html_report(html_report_path)
        
        print(f"\nReports generated:")
        print(f"  JSON: {json_report_path}")
        print(f"  HTML: {html_report_path}")
        
    def _generate_html_report(self, filepath):
        """Generate HTML test report"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Car Parking System - Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ background-color: #ecf0f1; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .test-result {{ margin: 10px 0; padding: 10px; border-left: 4px solid #ccc; }}
        .passed {{ border-left-color: #27ae60; background-color: #d5f4e6; }}
        .failed {{ border-left-color: #e74c3c; background-color: #fdf2f2; }}
        .error {{ border-left-color: #f39c12; background-color: #fef9e7; }}
        .skipped {{ border-left-color: #95a5a6; background-color: #f8f9fa; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .metric {{ background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Car Parking Vending System - Test Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>Test Execution Summary</h2>
        <div class="metrics">
            <div class="metric">
                <h3>Total Tests</h3>
                <h2>{self.test_results['total_tests']}</h2>
            </div>
            <div class="metric">
                <h3>Passed</h3>
                <h2 style="color: #27ae60">{self.test_results['passed']}</h2>
            </div>
            <div class="metric">
                <h3>Failed</h3>
                <h2 style="color: #e74c3c">{self.test_results['failed']}</h2>
            </div>
            <div class="metric">
                <h3>Errors</h3>
                <h2 style="color: #f39c12">{self.test_results['errors']}</h2>
            </div>
            <div class="metric">
                <h3>Execution Time</h3>
                <h2>{self.test_results['execution_time']:.2f}s</h2>
            </div>
        </div>
    </div>
    
    <h2>Detailed Test Results</h2>
"""
        
        for test_result in self.test_results['detailed_results']:
            status_class = test_result['status'].lower()
            html_content += f"""
    <div class="test-result {status_class}">
        <h4>{test_result['test']}</h4>
        <p><strong>Status:</strong> {test_result['status']}</p>
        <p><strong>Execution Time:</strong> {test_result['execution_time']:.3f}s</p>
"""
            if test_result['message']:
                html_content += f"""
        <p><strong>Message:</strong></p>
        <pre>{test_result['message']}</pre>
"""
            html_content += "    </div>\n"
            
        html_content += """
</body>
</html>
"""
        
        with open(filepath, 'w') as f:
            f.write(html_content)

def main():
    """Main test execution function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print("Usage: python test_runner.py [options]")
            print("Options:")
            print("  --unit      Run only unit tests")
            print("  --integration Run only integration tests")
            print("  --verbose   Increase verbosity")
            print("  --quiet     Reduce verbosity")
            print("  --help      Show this help message")
            return
            
    runner = TestRunner()
    
    # Parse command line arguments
    verbosity = 2
    if '--verbose' in sys.argv:
        verbosity = 3
    elif '--quiet' in sys.argv:
        verbosity = 1
        
    # Run tests
    success = runner.run_tests(verbosity=verbosity)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
