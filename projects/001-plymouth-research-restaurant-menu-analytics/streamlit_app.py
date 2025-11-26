#!/usr/bin/env python3
"""
Plymouth Research Restaurant Menu Analytics Dashboard
=====================================================

Streamlit Cloud Entry Point

This is the main entry point for Streamlit Cloud deployment.
It runs the modular dashboard from dashboard/app.py.

For local development, you can also run:
    streamlit run dashboard/app.py

Author: Plymouth Research Team
Date: 2025-11-26
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import and run the modular dashboard
from dashboard.app import main

if __name__ == "__main__":
    main()
else:
    # When imported by Streamlit, run main directly
    main()
