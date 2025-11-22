#!/usr/bin/env python3
"""
Documentation & Logs Organization Script
Organizes all documentation and log files into proper directory structure:
- docs/guides/ - Setup guides and how-tos
- docs/reports/ - Analysis reports and summaries
- docs/governance/ - Architecture governance (existing)
- logs/ - All log files
- Keep README.md and CLAUDE.md in root

Author: Claude Code
Date: 2025-11-22
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def organize_docs_and_logs():
    """Organize all documentation and log files into proper directory structure."""

    base_dir = Path("/workspaces/arckit-test-project-v13-plymouth-research/projects/001-plymouth-research-restaurant-menu-analytics")
    docs_dir = base_dir / "docs"
    logs_dir = base_dir / "logs"

    # Define directory structure
    directories = {
        'guides': docs_dir / 'guides',
        'reports': docs_dir / 'reports',
        'governance': docs_dir / 'governance',  # Already exists
        'logs': logs_dir
    }

    # Create directories
    print("=" * 80)
    print("DOCUMENTATION & LOGS ORGANIZATION - CREATING DIRECTORY STRUCTURE")
    print("=" * 80)
    for name, path in directories.items():
        path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {path}")

    print()

    # Files to keep in root (critical project documentation)
    keep_in_root = [
        'README.md',
        'CLAUDE.md',
        'organize_data.py',
        'organize_code.py',
        'organize_docs.py',  # This script
    ]

    # Categorize files
    file_categories = {
        'guides': [
            # Setup and integration guides
            'HYGIENE_RATINGS_GUIDE.md',
            'TRUSTPILOT_INTEGRATION_GUIDE.md',
            'GOOGLE_REVIEWS_SETUP.md',
            'COMPANIES_HOUSE_GUIDE.md',
            'INTERACTIVE_MATCHER_GUIDE.md',
            'LICENSING_SCRAPER_GUIDE.md',
            'LICENSING_DASHBOARD_INTEGRATION.md',
        ],

        'reports': [
            # Summary and analysis reports
            'DATA_ORGANIZATION_SUMMARY.md',
            'CODE_ORGANIZATION_SUMMARY.md',
            'BALANCE_SHEET_RESULTS.md',
            'FINANCIAL_DATA_POC_SUMMARY.md',
            'FINANCIAL_PERFORMANCE_SUMMARY.md',
            'SCRAPING_RESULTS.md',
            'PERFORMANCE_OPTIMIZATIONS.md',
            'data-consistency-report.md',
            'data-model-erd.md',
            'gold-standard-progress-report.md',
            'option-a-licensing-completion-report.md',
            'option-b-results-summary.md',
        ],

        'logs': [
            # All log files
            'discovery_log.txt',
            'fetch_balance_sheets_update.log',
            'fetch_balance_sheets_v2_run2.log',
            'fetch_google_all.log',
            'fetch_google_enhanced.log',
            'google_without_fsa.txt',
            'scrape_all_full.log',
            'scrape_test_10.log',
            'scraper_fixed_output.log',
            'scraper_full_output.log',
            'scraper_output.log',
            'scraper_restart_output.log',
            'requirements-scraping.txt',  # Old requirements (more like notes/log)
            'requirements.txt',  # Python requirements (should stay in root actually)
        ],
    }

    # Track moved files
    moved = defaultdict(list)
    kept = []

    # Move files
    print("=" * 80)
    print("MOVING FILES")
    print("=" * 80)

    for category, files in file_categories.items():
        dest_dir = directories[category]
        print(f"\n{category.upper()} → {dest_dir}")
        print("-" * 80)

        for filename in files:
            src = base_dir / filename
            dest = dest_dir / filename

            # Special handling for requirements.txt - keep in root
            if filename == 'requirements.txt':
                print(f"  ⊙ {filename} (keeping in root - Python dependencies)")
                continue

            if src.exists():
                shutil.move(str(src), str(dest))
                moved[category].append(filename)
                print(f"  ✓ {filename}")
            else:
                print(f"  ⚠ Not found: {filename}")

    # Move any remaining .pdf files to reports
    pdf_files = list(base_dir.glob("*.pdf"))
    if pdf_files:
        print(f"\nPDF FILES → {directories['reports']}")
        print("-" * 80)
        for pdf_file in pdf_files:
            dest = directories['reports'] / pdf_file.name
            shutil.move(str(pdf_file), str(dest))
            moved['reports'].append(pdf_file.name)
            print(f"  ✓ {pdf_file.name}")

    # Report files kept in root
    print(f"\nKEPT IN ROOT (critical project documentation)")
    print("-" * 80)
    for filename in keep_in_root:
        src = base_dir / filename
        if src.exists():
            kept.append(filename)
            print(f"  ✓ {filename}")
        elif filename not in ['organize_data.py', 'organize_code.py', 'organize_docs.py']:
            print(f"  ⚠ Not found: {filename}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total = 0
    for category, files in moved.items():
        count = len(files)
        total += count
        print(f"{category:20s}: {count:3d} files")
    print(f"{'kept in root':20s}: {len(kept):3d} files")
    print(f"{'TOTAL organized':20s}: {total:3d} files")

    # Create README files
    create_readmes(directories)

    # Create .gitignore for logs
    create_logs_gitignore(logs_dir)

    print("\n" + "=" * 80)
    print("DOCUMENTATION & LOGS ORGANIZATION COMPLETE")
    print("=" * 80)
    print("\n✅ All documentation organized into:")
    for name, path in directories.items():
        print(f"   - {path}")
    print(f"\n✅ Critical files kept in root:")
    for filename in keep_in_root:
        print(f"   - {filename}")
    print("\n" + "=" * 80)

def create_readmes(directories):
    """Create README files for each documentation category."""

    readmes = {
        'guides': """# Guides

Setup guides, integration guides, and how-to documentation.

## Integration Guides

- **HYGIENE_RATINGS_GUIDE.md** - FSA Food Hygiene Rating Scheme integration guide
- **TRUSTPILOT_INTEGRATION_GUIDE.md** - Trustpilot reviews scraping and integration
- **GOOGLE_REVIEWS_SETUP.md** - Google Places API reviews setup
- **COMPANIES_HOUSE_GUIDE.md** - Companies House API integration
- **LICENSING_SCRAPER_GUIDE.md** - Plymouth licensing data scraper guide
- **LICENSING_DASHBOARD_INTEGRATION.md** - Dashboard licensing integration

## Tools Guides

- **INTERACTIVE_MATCHER_GUIDE.md** - Interactive data matcher usage guide

## Usage

These guides provide step-by-step instructions for setting up and using various integrations and tools.
""",

        'reports': """# Reports

Analysis reports, summaries, and project documentation.

## Organization Reports

- **DATA_ORGANIZATION_SUMMARY.md** - Complete data organization details (125 files)
- **CODE_ORGANIZATION_SUMMARY.md** - Complete code organization details (39 files)

## Analysis Reports

- **BALANCE_SHEET_RESULTS.md** - Financial data analysis results
- **FINANCIAL_DATA_POC_SUMMARY.md** - Financial data proof of concept
- **FINANCIAL_PERFORMANCE_SUMMARY.md** - Restaurant financial performance analysis
- **SCRAPING_RESULTS.md** - Menu scraping results and statistics
- **PERFORMANCE_OPTIMIZATIONS.md** - Database and application optimizations
- **data-consistency-report.md** - Address consistency analysis
- **data-model-erd.md** - Entity relationship diagram

## Progress Reports

- **gold-standard-progress-report.md** - Data quality progress
- **option-a-licensing-completion-report.md** - Licensing integration completion
- **option-b-results-summary.md** - Alternative approach results

## PDF Documents

Contains exported financial documents and reports.
""",

        'governance': """# Governance

Enterprise architecture governance artifacts.

## Existing Documents

- **requirements.md** - Business and technical requirements (105 KB)
- **stakeholder-drivers.md** - Stakeholder analysis and drivers (101 KB)
- **backlog.md** - Product backlog and user stories (71 KB)
- **data-model.md** - Comprehensive data model (92 KB)
- **dpia.md** - Data Protection Impact Assessment (30 KB)
- **risk-register.md** - Risk register and mitigations (99 KB)
- **SPRINT2_RESEARCH_FINDINGS.md** - Sprint 2 research findings (10 KB)

## Purpose

These documents provide enterprise architecture governance for the Plymouth Research project,
following UK Government and enterprise best practices.

**Total**: ~500 KB of governance documentation
""",

        'logs': """# Logs

Application logs, scraping logs, and execution traces.

## Fetcher Logs

- `fetch_balance_sheets_update.log` - Balance sheet fetcher log
- `fetch_balance_sheets_v2_run2.log` - Balance sheet fetcher v2 log
- `fetch_google_all.log` - Google Places fetcher log
- `fetch_google_enhanced.log` - Enhanced Google Places log

## Scraper Logs

- `scraper_output.log` - Menu scraper output
- `scraper_fixed_output.log` - Fixed scraper output
- `scraper_full_output.log` - Full scraper run
- `scraper_restart_output.log` - Scraper restart log
- `scrape_all_full.log` - Complete scrape log
- `scrape_test_10.log` - Test scrape (10 restaurants)

## Discovery Logs

- `discovery_log.txt` - Restaurant discovery log
- `google_without_fsa.txt` - Google Places without FSA data

## Notes

- Logs are excluded from git (see .gitignore)
- Old logs can be archived or deleted as needed
- Active logs help with debugging and monitoring
"""
    }

    # Write README files
    for category, content in readmes.items():
        readme_path = directories[category] / 'README.md'
        with open(readme_path, 'w') as f:
            f.write(content)
        print(f"✓ Created: {readme_path}")

def create_logs_gitignore(logs_dir):
    """Create .gitignore for logs directory."""
    gitignore_path = logs_dir / '.gitignore'
    content = """# Exclude all logs from git
*.log
*.txt

# But keep README
!README.md
"""
    with open(gitignore_path, 'w') as f:
        f.write(content)
    print(f"✓ Created: {gitignore_path}")

if __name__ == "__main__":
    organize_docs_and_logs()
