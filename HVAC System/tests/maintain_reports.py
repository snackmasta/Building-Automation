#!/usr/bin/env python3
"""
HVAC System - Test Reports Maintenance
Utility for managing and maintaining test report organization

Author: System Engineer
Date: June 8, 2025
Version: 1.0.0
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import json

class TestReportsMaintenanceTool:
    """Tool for maintaining organized test reports"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.reports_dir = self.project_root / "tests" / "reports"
        self.archive_days = 30  # Archive reports older than 30 days
    
    def organize_loose_reports(self):
        """Move any loose report files to appropriate directories"""
        moved_count = 0
        
        # Check for loose reports in project root
        for pattern in ["final_verification_report_*.json", "verification_report_restructuring_*.json", "verification_report_*.json"]:
            for file_path in self.project_root.glob(pattern):
                if "restructuring" in file_path.name:
                    target_dir = self.reports_dir / "restructuring"
                elif "final_verification" in file_path.name:
                    target_dir = self.reports_dir / "final_verification"
                else:
                    target_dir = self.reports_dir / "archived"
                
                target_dir.mkdir(parents=True, exist_ok=True)
                target_path = target_dir / file_path.name
                
                if not target_path.exists():
                    shutil.move(str(file_path), str(target_path))
                    print(f"📦 Moved: {file_path.name} → {target_dir.name}/")
                    moved_count += 1
        
        return moved_count
    
    def clean_old_reports(self, dry_run=True):
        """Archive old reports (older than archive_days)"""
        cutoff_date = datetime.now() - timedelta(days=self.archive_days)
        archived_count = 0
        
        for category_dir in ["final_verification", "restructuring"]:
            category_path = self.reports_dir / category_dir
            if not category_path.exists():
                continue
            
            for report_file in category_path.glob("*.json"):
                # Extract date from filename (format: *_YYYYMMDD_HHMMSS.json)
                try:
                    parts = report_file.stem.split('_')
                    date_part = parts[-2]  # YYYYMMDD
                    time_part = parts[-1]  # HHMMSS
                    
                    file_date = datetime.strptime(f"{date_part}_{time_part}", "%Y%m%d_%H%M%S")
                    
                    if file_date < cutoff_date:
                        archive_dir = self.reports_dir / "archived" / category_dir
                        archive_dir.mkdir(parents=True, exist_ok=True)
                        target_path = archive_dir / report_file.name
                        
                        if dry_run:
                            print(f"🗂️  Would archive: {report_file.name} (age: {(datetime.now() - file_date).days} days)")
                        else:
                            shutil.move(str(report_file), str(target_path))
                            print(f"🗂️  Archived: {report_file.name} → archived/{category_dir}/")
                            archived_count += 1
                            
                except (ValueError, IndexError):
                    print(f"⚠️  Cannot parse date from: {report_file.name}")
        
        return archived_count
    
    def generate_directory_report(self):
        """Generate a report on the current directory organization"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'directories': {},
            'total_files': 0,
            'disk_usage': {}
        }
        
        print("📁 HVAC Test Reports Directory Structure")
        print("=" * 50)
        
        for category in ["final_verification", "restructuring", "archived"]:
            category_path = self.reports_dir / category
            if category_path.exists():
                files = list(category_path.glob("*.json"))
                total_size = sum(f.stat().st_size for f in files if f.is_file())
                
                report['directories'][category] = {
                    'count': len(files),
                    'size_bytes': total_size,
                    'size_mb': round(total_size / (1024 * 1024), 2)
                }
                
                print(f"📂 {category.replace('_', ' ').title():<20} {len(files):>3} files ({total_size:,} bytes)")
                
                if files:
                    oldest = min(files, key=lambda f: f.stat().st_mtime)
                    newest = max(files, key=lambda f: f.stat().st_mtime)
                    
                    oldest_date = datetime.fromtimestamp(oldest.stat().st_mtime)
                    newest_date = datetime.fromtimestamp(newest.stat().st_mtime)
                    
                    print(f"   📅 Date Range: {oldest_date.strftime('%Y-%m-%d')} to {newest_date.strftime('%Y-%m-%d')}")
                
                report['total_files'] += len(files)
        
        # Check for summary reports
        summary_files = list(self.reports_dir.glob("SUMMARY_REPORT_*.json"))
        if summary_files:
            print(f"📊 Summary Reports           {len(summary_files):>3} files")
            report['directories']['summary_reports'] = {
                'count': len(summary_files),
                'latest': max(summary_files, key=lambda f: f.stat().st_mtime).name
            }
        
        print(f"\n📈 Total Report Files: {report['total_files']}")
        
        return report
    
    def cleanup_duplicates(self, dry_run=True):
        """Remove duplicate report files based on content"""
        removed_count = 0
        
        for category_dir in ["final_verification", "restructuring", "archived"]:
            category_path = self.reports_dir / category_dir
            if not category_path.exists():
                continue
            
            files = list(category_path.glob("*.json"))
            content_hashes = {}
            
            for file_path in files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    content_hash = hash(content)
                    
                    if content_hash in content_hashes:
                        # Duplicate found
                        original_file = content_hashes[content_hash]
                        if dry_run:
                            print(f"🔄 Would remove duplicate: {file_path.name} (same as {original_file.name})")
                        else:
                            file_path.unlink()
                            print(f"🔄 Removed duplicate: {file_path.name}")
                            removed_count += 1
                    else:
                        content_hashes[content_hash] = file_path
                        
                except Exception as e:
                    print(f"⚠️  Error processing {file_path.name}: {e}")
        
        return removed_count
    
    def run_maintenance(self, archive_old=False, remove_duplicates=False):
        """Run comprehensive maintenance"""
        print("🔧 HVAC Test Reports Maintenance Tool")
        print("=" * 50)
        print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 1. Organize loose reports
        print("1️⃣ Organizing loose reports...")
        moved = self.organize_loose_reports()
        print(f"   ✅ Moved {moved} files to organized directories")
        print()
        
        # 2. Generate directory report
        print("2️⃣ Analyzing directory structure...")
        self.generate_directory_report()
        print()
        
        # 3. Check for old reports
        print("3️⃣ Checking for old reports...")
        old_count = self.clean_old_reports(dry_run=True)
        if archive_old and old_count > 0:
            print(f"   🗂️  Archiving {old_count} old reports...")
            self.clean_old_reports(dry_run=False)
        elif old_count > 0:
            print(f"   📝 Found {old_count} reports that could be archived (use --archive flag)")
        else:
            print("   ✅ No old reports found")
        print()
        
        # 4. Check for duplicates
        print("4️⃣ Checking for duplicate reports...")
        dup_count = self.cleanup_duplicates(dry_run=True)
        if remove_duplicates and dup_count > 0:
            print(f"   🔄 Removing {dup_count} duplicate reports...")
            self.cleanup_duplicates(dry_run=False)
        elif dup_count > 0:
            print(f"   📝 Found {dup_count} duplicate reports (use --remove-duplicates flag)")
        else:
            print("   ✅ No duplicate reports found")
        
        print()
        print("🎯 Maintenance completed successfully!")

def main():
    """Main function"""
    tool = TestReportsMaintenanceTool()
    
    # Parse command line arguments
    archive_old = "--archive" in sys.argv
    remove_duplicates = "--remove-duplicates" in sys.argv
    
    tool.run_maintenance(archive_old=archive_old, remove_duplicates=remove_duplicates)
    return 0

if __name__ == "__main__":
    sys.exit(main())
