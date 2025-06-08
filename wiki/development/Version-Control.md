# Version Control Guide

## Overview

This guide establishes version control standards and practices for all PLC projects in the repository. Proper version control is essential for managing industrial automation systems safely and maintaining comprehensive change history.

## Version Control Strategy

### Branching Model
We use GitFlow workflow adapted for industrial automation projects:

```
main (production)
├── develop (integration)
│   ├── feature/hvac-energy-optimization
│   ├── feature/water-treatment-efficiency
│   └── feature/hmi-alarm-enhancement
├── release/v2.1.0
├── hotfix/emergency-safety-fix
└── support/v1.x-maintenance
```

### Branch Types
- **main**: Production-ready releases only
- **develop**: Integration branch for new features
- **feature/**: New functionality development
- **release/**: Preparation for production release
- **hotfix/**: Emergency fixes for production
- **support/**: Long-term maintenance branches

## Repository Structure

### Project Organization
```
repository/
├── .git/                    # Git metadata
├── .gitignore              # Ignore patterns
├── .gitattributes          # File handling rules
├── README.md               # Main repository documentation
├── CHANGELOG.md            # Version history
├── VERSION                 # Current version number
├── docs/                   # Global documentation
├── scripts/                # Build and deployment scripts
├── tools/                  # Development utilities
├── Project Example/        # Educational project
├── HVAC System/           # HVAC automation project
├── Water Treatment System/ # Water treatment project
└── wiki/                  # Comprehensive documentation
```

### File Organization Standards
```
Project/
├── README.md              # Project overview
├── CHANGELOG.md           # Project-specific changes
├── config/                # Configuration files
│   ├── plc_config.ini    # PLC parameters
│   └── hmi_config.ini    # HMI settings
├── plc/                   # PLC source code
│   ├── main.st           # Main program
│   ├── global_vars.st    # Global variables
│   └── modules/          # Function blocks
├── src/                   # Application source
│   ├── simulation/       # Process simulation
│   ├── gui/             # User interface
│   └── monitoring/      # Data acquisition
├── tests/                 # Test suites
├── docs/                  # Project documentation
├── diagrams/             # System diagrams
└── scripts/              # Build/deployment scripts
```

## Commit Standards

### Commit Message Format
```
<type>(<scope>): <description>

<body>

<footer>
```

#### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code formatting
- **refactor**: Code restructuring
- **test**: Test additions/modifications
- **chore**: Maintenance tasks
- **safety**: Safety-related changes

#### Examples
```bash
feat(hvac): add energy optimization algorithm

Implement advanced energy optimization using machine learning
to reduce HVAC energy consumption by 15-20%.

- Add predictive control algorithm
- Integrate weather forecast data
- Update HMI energy dashboard
- Add performance monitoring

Closes #123
Tested-by: QA Team
Safety-review: Safety Engineer
```

```bash
fix(water-treatment): resolve membrane pressure alarm

Critical fix for false alarms during normal operation.
Adjusted alarm threshold from 85 psi to 90 psi based
on field testing and manufacturer recommendations.

Fixes #456
Tested-by: Operations Team
Emergency-approval: Plant Manager
```

### Commit Guidelines
1. **Atomic Commits**: One logical change per commit
2. **Descriptive Messages**: Clear, concise descriptions
3. **Safety Documentation**: Note safety-critical changes
4. **Testing Reference**: Include test validation
5. **Issue Tracking**: Link to issue numbers

## Tagging Strategy

### Version Numbering
We use Semantic Versioning (SemVer) adapted for industrial systems:

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
v1.0.0          # Initial release
v1.1.0          # New features
v1.1.1          # Bug fixes
v2.0.0          # Breaking changes
v2.0.0-rc.1     # Release candidate
v2.0.0+20250608 # Build metadata
```

### Tag Categories
- **Release Tags**: `v1.0.0`, `v1.1.0`, `v2.0.0`
- **Pre-release**: `v1.0.0-alpha.1`, `v1.0.0-beta.2`, `v1.0.0-rc.1`
- **Hotfix Tags**: `v1.0.1-hotfix.1`
- **Milestone Tags**: `milestone-commissioning`, `milestone-validation`

### Tagging Process
```bash
# Create annotated tag with detailed information
git tag -a v1.2.0 -m "Release v1.2.0: Enhanced HVAC Control

Features:
- Advanced PID tuning algorithms
- Energy optimization module
- Enhanced safety interlocks

Testing:
- Full system integration tests passed
- Safety validation completed
- Performance benchmarks verified

Approvals:
- Engineering: John Smith
- Safety: Mary Johnson  
- Operations: Mike Davis"

# Push tags to remote
git push origin v1.2.0
git push origin --tags
```

## File Management

### .gitignore Configuration
```gitignore
# PLC Development Files
*.bak
*.tmp
*.log
*_backup.*

# Compiled Files
*.obj
*.lib
*.bin
*.hex

# IDE Files
.vscode/settings.json
*.suo
*.user

# Simulation Data
simulation_data/
historical_logs/
*.csv
*.sqlite

# Configuration - Local Only
**/config/local_*
**/config/development_*

# Test Results
test_results/
coverage_reports/
performance_data/

# Documentation Generation
docs_build/
*.pdf
diagrams/*.png
!diagrams/reference_*.png

# Operating System
.DS_Store
Thumbs.db
desktop.ini

# Temporary Files
temp/
cache/
*.pid
```

### .gitattributes Configuration
```gitattributes
# Text files
*.md text eol=lf
*.txt text eol=lf
*.ini text eol=lf
*.json text eol=lf
*.xml text eol=lf
*.yml text eol=lf
*.yaml text eol=lf

# PLC source files
*.st text eol=lf
*.scl text eol=lf
*.awl text eol=lf

# Scripts
*.py text eol=lf
*.sh text eol=lf
*.bat text eol=crlf
*.ps1 text eol=crlf

# Binary files
*.png binary
*.jpg binary
*.pdf binary
*.zip binary
*.bin binary

# Large files (use Git LFS)
*.pdf filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
simulation_data/*.csv filter=lfs diff=lfs merge=lfs -text
```

## Development Workflow

### Feature Development
```bash
# 1. Start from latest develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/water-treatment-optimization

# 3. Develop and commit
git add .
git commit -m "feat(water-treatment): implement flow optimization"

# 4. Regular updates from develop
git checkout develop
git pull origin develop
git checkout feature/water-treatment-optimization
git rebase develop

# 5. Push feature branch
git push origin feature/water-treatment-optimization

# 6. Create pull request
# Use GitHub/GitLab interface

# 7. Merge after review
git checkout develop
git merge --no-ff feature/water-treatment-optimization
git push origin develop

# 8. Clean up
git branch -d feature/water-treatment-optimization
git push origin --delete feature/water-treatment-optimization
```

### Release Process
```bash
# 1. Create release branch
git checkout develop
git checkout -b release/v1.2.0

# 2. Update version numbers
echo "1.2.0" > VERSION
# Update version in configuration files
# Update CHANGELOG.md

# 3. Final testing and bug fixes
git commit -am "chore: prepare release v1.2.0"

# 4. Merge to main
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"

# 5. Back-merge to develop
git checkout develop
git merge --no-ff release/v1.2.0

# 6. Push everything
git push origin main
git push origin develop
git push origin v1.2.0

# 7. Clean up
git branch -d release/v1.2.0
```

### Hotfix Process
```bash
# 1. Create hotfix from main
git checkout main
git checkout -b hotfix/critical-safety-fix

# 2. Implement fix
git commit -am "fix(safety): resolve emergency stop delay"

# 3. Update version
echo "1.1.1" > VERSION
git commit -am "chore: bump version to 1.1.1"

# 4. Merge to main and develop
git checkout main
git merge --no-ff hotfix/critical-safety-fix
git tag -a v1.1.1 -m "Hotfix v1.1.1: Critical safety fix"

git checkout develop
git merge --no-ff hotfix/critical-safety-fix

# 5. Push and clean up
git push origin main
git push origin develop
git push origin v1.1.1
git branch -d hotfix/critical-safety-fix
```

## Code Review Process

### Pull Request Template
```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to change)
- [ ] Documentation update
- [ ] Safety-critical change

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] System tests pass
- [ ] Performance tests (if applicable)
- [ ] Safety validation (if required)

## Safety Review
- [ ] No safety implications
- [ ] Safety review completed by: _______________
- [ ] Safety documentation updated

## Checklist
- [ ] Code follows project coding standards
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version number updated (if applicable)

## Test Evidence
Attach test results, screenshots, or logs demonstrating functionality.

## Deployment Notes
Special considerations for deployment or commissioning.
```

### Review Criteria
1. **Functionality**: Code works as intended
2. **Safety**: No safety risks introduced
3. **Performance**: Meets response time requirements
4. **Maintainability**: Code is readable and documented
5. **Standards**: Follows coding conventions
6. **Testing**: Adequate test coverage

## Configuration Management

### Environment-Specific Configurations
```ini
# config/production.ini
[system]
environment = production
debug_mode = false
log_level = INFO
safety_override = false

[network]
plc_ip = 192.168.1.100
hmi_ip = 192.168.1.101
historian_ip = 192.168.1.102

[safety]
enable_interlocks = true
emergency_stop_enabled = true
watchdog_timeout = 5000
```

```ini
# config/development.ini
[system]
environment = development
debug_mode = true
log_level = DEBUG
safety_override = true

[network]
plc_ip = 127.0.0.1
hmi_ip = 127.0.0.1
historian_ip = 127.0.0.1

[safety]
enable_interlocks = false
emergency_stop_enabled = false
watchdog_timeout = 10000
```

### Secrets Management
```bash
# Use environment variables for sensitive data
export PLC_PASSWORD="secure_password"
export DATABASE_CONNECTION="encrypted_string"
export API_KEY="api_key_value"

# Never commit secrets to repository
echo "config/secrets.ini" >> .gitignore
```

## Backup and Recovery

### Repository Backup Strategy
```bash
# Daily automated backup
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR="/backup/plc_repository"

# Create full backup
git clone --mirror origin $BACKUP_DIR/repo_$DATE.git

# Archive and compress
tar -czf $BACKUP_DIR/repo_$DATE.tar.gz $BACKUP_DIR/repo_$DATE.git
rm -rf $BACKUP_DIR/repo_$DATE.git

# Keep 30 days of backups
find $BACKUP_DIR -name "repo_*.tar.gz" -mtime +30 -delete
```

### Disaster Recovery
```bash
# Restore from backup
tar -xzf repo_20250608.tar.gz
git clone repo_20250608.git restored_repository
cd restored_repository
git remote set-url origin <new_remote_url>
git push --mirror origin
```

## Best Practices

### Daily Operations
1. **Start of Day**: Pull latest changes
2. **Before Commits**: Run tests and checks
3. **Regular Pushes**: Don't hoard changes locally
4. **End of Day**: Push work in progress branches
5. **Weekly**: Review and clean up branches

### Safety Considerations
1. **Critical Changes**: Require dual approval
2. **Production Branches**: Protect main and release branches
3. **Change Documentation**: Detail safety implications
4. **Rollback Plan**: Always have rollback strategy
5. **Testing Requirements**: Mandatory safety testing

### Team Collaboration
1. **Communication**: Use descriptive commit messages
2. **Documentation**: Keep README files current
3. **Issue Tracking**: Link commits to issues
4. **Code Review**: Mandatory for all changes
5. **Knowledge Sharing**: Regular team sync meetings

## Tools and Integration

### Git Hooks
```bash
# pre-commit hook
#!/bin/sh
# Run tests before allowing commit
python -m pytest tests/unit/
if [ $? -ne 0 ]; then
    echo "Unit tests failed. Commit aborted."
    exit 1
fi

# Check for safety-critical files
git diff --cached --name-only | grep -E "(safety|emergency|interlock)" > /dev/null
if [ $? -eq 0 ]; then
    echo "Safety-critical files modified. Additional review required."
fi
```

### Continuous Integration
```yaml
# .github/workflows/ci.yml
name: CI Pipeline
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run Tests
      run: |
        python -m pytest
        python scripts/safety_check.py
    - name: Generate Report
      run: python scripts/test_report.py
```

## Troubleshooting

### Common Issues
1. **Merge Conflicts**: Use git mergetool
2. **Large Files**: Migrate to Git LFS
3. **Corrupted Repository**: Use git fsck
4. **Missing History**: Check reflog
5. **Performance Issues**: Use git gc

### Recovery Commands
```bash
# Undo last commit (keep changes)
git reset HEAD~1

# Discard all local changes
git reset --hard HEAD

# Recover deleted branch
git reflog
git checkout -b recovered_branch <commit_hash>

# Find lost commits
git fsck --lost-found
```

## See Also

- [Code Standards](Code-Standards.md)
- [Testing Procedures](Testing-Procedures.md)
- [Development Guide](Development-Guide.md)
- [System Architecture](../technical/System-Architecture.md)

---

*Version Control Guide - Part of Industrial PLC Control Systems Repository*
