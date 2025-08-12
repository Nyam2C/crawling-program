#!/usr/bin/env python3
"""
Launcher script for the Magnificent Seven Stock Analysis GUI
"""

import sys
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []
    
    try:
        import requests
    except ImportError:
        missing_deps.append("requests")
        
    try:
        import bs4
    except ImportError:
        missing_deps.append("beautifulsoup4")
        
    try:
        import lxml
    except ImportError:
        missing_deps.append("lxml")
        
    return missing_deps

def show_welcome_message():
    """Show welcome message with instructions"""
    welcome_text = """
🚀 Welcome to Magnificent Seven Stock Analysis System!

This application provides:
• Real-time stock data for the Magnificent Seven
• AI-powered buy/sell recommendations  
• Interactive charts and visualizations
• Comprehensive investment reports

Getting Started:
1. Click on different tabs to explore features
2. Start by fetching stock data in the 'Stock Data' tab
3. Generate AI recommendations in the 'Recommendations' tab
4. View individual analysis in the 'Individual Analysis' tab
5. Explore charts in the 'Charts' tab (if matplotlib is installed)

⚠️  DISCLAIMER: This tool is for educational purposes only.
   Not financial advice. Always do your own research!

Click OK to continue...
    """
    
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    messagebox.showinfo("Welcome", welcome_text)
    root.destroy()

def main():
    """Main function to launch the GUI"""
    print("🚀 Starting Magnificent Seven Stock Analysis GUI...")
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("📦 Please install missing packages:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    try:
        # Show welcome message
        show_welcome_message()
        
        # Import and run the main GUI
        from gui_app import StockAnalysisGUI
        
        print("✅ Dependencies verified")
        print("🎉 Launching GUI application...")
        
        app = StockAnalysisGUI()
        app.run()
        
    except ImportError as e:
        print(f"❌ Failed to import GUI components: {e}")
        print("📝 Make sure all files are in the same directory")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()