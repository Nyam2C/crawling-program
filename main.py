#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Analysis Platform
Main entry point for Stock Analysis Platform
Professional stock analysis and virtual trading platform
"""

import sys
import os

# Add the project root to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function - Launch the stock analysis platform GUI"""
    # Check Python version compatibility first
    try:
        from src.core.version_check import check_python_version
        compatible, error = check_python_version()
        if not compatible:
            print("="*60)
            print("PYTHON VERSION ERROR")
            print("="*60)
            print(f"Error: {error}")
            print("\nThis application requires Python 3.7 or higher.")
            print("Please upgrade your Python installation.")
            sys.exit(1)
    except ImportError:
        # If version check module can't be imported, try to continue
        pass
    
    try:
        from scripts.run_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Failed to import GUI components: {e}")
        print("\nPlease install missing dependencies:")
        print("   pip install -r requirements.txt")
        print("\nNote: This platform only supports GUI mode.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        print("\nIf you're getting a 'type object is not subscriptable' error,")
        print("this usually means you're using an older Python version.")
        print("Please upgrade to Python 3.9+ for best compatibility.")
        sys.exit(1)

if __name__ == "__main__":
    main()