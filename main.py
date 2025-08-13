#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for the Magnificent Seven Stock Analysis System
くるみ様の優雅なる株式分析システム 🌹⏰
"""

import sys
import os

# Add the project root to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function - launch the GUI application"""
    try:
        from scripts.run_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"(˃̵ᴗ˂) Failed to import GUI components: {e}")
        print("( ˶ˆᗜˆ˵ ) Trying CLI fallback...")
        try:
            from scripts.cli import StockAnalysisCLI
            cli = StockAnalysisCLI()
            cli.run()
        except Exception as cli_e:
            print(f"(˃̵ᴗ˂) CLI fallback also failed: {cli_e}")
            print("\n( ˶ˆ꒳ˆ˵ ) Please install missing dependencies:")
            print("   pip install -r requirements.txt")
            sys.exit(1)

if __name__ == "__main__":
    main()