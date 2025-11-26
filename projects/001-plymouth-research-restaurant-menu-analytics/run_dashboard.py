#!/usr/bin/env python3
"""
Dashboard Entry Point
=====================

Launch the Streamlit dashboard.

Usage:
    python run_dashboard.py
    # OR
    streamlit run dashboard/app.py

Author: Plymouth Research Team
Date: 2025-11-26
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the Streamlit dashboard."""
    dashboard_path = Path(__file__).parent / "dashboard" / "app.py"

    if not dashboard_path.exists():
        print(f"❌ Dashboard not found at: {dashboard_path}")
        sys.exit(1)

    print("🚀 Launching Plymouth Research Dashboard...")
    print(f"   Path: {dashboard_path}")
    print("   Press Ctrl+C to stop")
    print()

    try:
        subprocess.run(
            ["streamlit", "run", str(dashboard_path)],
            check=True
        )
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")
    except FileNotFoundError:
        print("❌ Streamlit not found. Install with: pip install streamlit")
        sys.exit(1)


if __name__ == "__main__":
    main()
