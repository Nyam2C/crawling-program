#!/usr/bin/env python3
"""
Launcher script for the Magnificent Seven Stock Analysis GUI
"""

import sys
import platform
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_tkinter():
    """Check if tkinter is available and provide installation instructions if not"""
    try:
        import tkinter as tk
        return True, None
    except ImportError:
        os_name = platform.system().lower()
        
        if os_name == 'linux':
            # Check distribution
            try:
                with open('/etc/os-release') as f:
                    content = f.read().lower()
                if 'ubuntu' in content or 'debian' in content:
                    install_cmd = "sudo apt-get update && sudo apt-get install python3-tk"
                elif 'centos' in content or 'rhel' in content or 'fedora' in content:
                    install_cmd = "sudo dnf install python3-tkinter  # or: sudo yum install tkinter"
                else:
                    install_cmd = "sudo apt-get install python3-tk  # (or equivalent for your distribution)"
            except:
                install_cmd = "sudo apt-get install python3-tk  # (or equivalent for your distribution)"
                
        elif os_name == 'darwin':  # macOS
            install_cmd = "tkinter should be included with Python. Try: brew install python-tk"
        elif os_name == 'windows':
            install_cmd = "tkinter should be included with Python. Reinstall Python with 'Add to PATH' option."
        else:
            install_cmd = "Install tkinter package for your operating system"
            
        error_msg = f"""
❌ tkinter is not available!

tkinter is required for the GUI application. Please install it:

{install_cmd}

Alternative options:
1. Use the CLI version instead: python main.py
2. Install tkinter as shown above, then run: python run_gui.py
3. Use the web-based version (if available)

Operating System: {platform.system()} {platform.release()}
Python Version: {sys.version}
"""
        return False, error_msg

def check_other_dependencies():
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
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        welcome_text = """🚀 Welcome to Magnificent Seven Stock Analysis System!

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

Click OK to continue..."""
        
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        messagebox.showinfo("Welcome", welcome_text)
        root.destroy()
        
    except ImportError:
        print("📝 Welcome to Magnificent Seven Stock Analysis System!")

def main():
    """Main function to launch the GUI"""
    print("🚀 Starting Magnificent Seven Stock Analysis GUI...")
    
    # Check tkinter first
    tkinter_available, tkinter_error = check_tkinter()
    if not tkinter_available:
        print(tkinter_error)
        print("\n" + "="*60)
        print("🔄 FALLBACK: Launching CLI version instead...")
        print("="*60)
        try:
            from scripts.cli import StockAnalysisCLI
            cli = StockAnalysisCLI()
            cli.run()
        except Exception as e:
            print(f"❌ CLI fallback also failed: {e}")
            print("\n📦 Please install missing dependencies:")
            print("   pip install -r requirements.txt")
        return
    
    # Check other dependencies
    missing = check_other_dependencies()
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("📦 Please install missing packages:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    try:
        # Show welcome message
        show_welcome_message()
        
        # Import and run the main GUI
        from src.gui.gui_app import StockAnalysisGUI
        
        print("✅ Dependencies verified")
        print("🎉 Launching GUI application...")
        
        app = StockAnalysisGUI()
        app.run()
        
    except ImportError as e:
        print(f"❌ Failed to import GUI components: {e}")
        print("📝 Make sure all files are in the same directory")
        print("\n🔄 Trying CLI fallback...")
        try:
            from scripts.cli import StockAnalysisCLI
            cli = StockAnalysisCLI()
            cli.run()
        except:
            print("❌ CLI fallback also failed")
            sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()