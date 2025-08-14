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
    """Show welcome message with custom kawaii design"""
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # Create custom welcome dialog
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        welcome = tk.Toplevel()
        welcome.title("Welcome to Kawaii Stock Analysis Platform")
        welcome.configure(bg='#1F144A')  # Dark navy purple
        welcome.resizable(False, False)
        welcome.grab_set()  # Make modal
        
        # Center dialog
        welcome.update_idletasks()
        width = 600
        height = 500
        x = (welcome.winfo_screenwidth() // 2) - (width // 2)
        y = (welcome.winfo_screenheight() // 2) - (height // 2)
        welcome.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(welcome, bg='#1F144A')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, 
                             text="✧･ﾟ: *✧･ﾟ:* Welcome *:･ﾟ✧*:･ﾟ✧",
                             font=('Arial', 18, 'bold'),
                             fg='#A78BFA',  # Periwinkle
                             bg='#1F144A')
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(main_frame,
                                text="Kawaii Stock Analysis Platform",
                                font=('Arial', 14),
                                fg='#C4B5FD',  # Lavender
                                bg='#1F144A')
        subtitle_label.pack(pady=(0, 20))
        
        # Features section
        features_text = """This application provides:

✧ Universal stock symbol support (not limited to M7)
✧ Real-time data fetching with yfinance integration  
✧ AI-powered buy/sell recommendations
✧ Advanced multi-criteria investment analysis
✧ Individual stock portfolio management
✧ Comprehensive investment reports

Getting Started:
1. Add stocks in the 'Stock Data' tab
2. Generate recommendations in the 'Recommendations' tab
3. View detailed analysis in the 'Individual Analysis' tab
4. Customize settings in the 'Settings' tab"""
        
        features_label = tk.Label(main_frame, text=features_text,
                                font=('Arial', 11),
                                fg='#F3E8FF',  # Soft lavender white
                                bg='#1F144A',
                                justify=tk.LEFT)
        features_label.pack(pady=(0, 20))
        
        # Disclaimer
        disclaimer_label = tk.Label(main_frame,
                                  text="⚠️  DISCLAIMER: For educational purposes only.\nNot financial advice. Always do your own research!",
                                  font=('Arial', 10, 'italic'),
                                  fg='#F9A8D4',  # Rose pink
                                  bg='#1F144A',
                                  justify=tk.CENTER)
        disclaimer_label.pack(pady=(0, 20))
        
        # OK button
        def close_welcome():
            welcome.destroy()
            root.destroy()
        
        ok_button = tk.Button(main_frame, text="Let's Start! ♡",
                            font=('Arial', 12, 'bold'),
                            bg='#A78BFA',  # Periwinkle
                            fg='#1B1350',  # Dark purple
                            activebackground='#C4B5FD',  # Lavender
                            activeforeground='#1B1350',
                            relief='raised',
                            borderwidth=2,
                            padx=20, pady=8,
                            command=close_welcome)
        ok_button.pack()
        
        # Bind Enter key
        welcome.bind('<Return>', lambda e: close_welcome())
        ok_button.focus_set()
        
        welcome.wait_window()
        
    except ImportError:
        print("📝 Welcome to Kawaii Stock Analysis Platform!")

def show_kawaii_ascii():
    """Show kawaii ASCII art at startup"""
    kawaii_art = """
⠀⠀⠀⠀⠀⠀⠀⢀⣶⣾⣲⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣯⣳⡄
⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣟⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣽⣾⣿⣿⠇
⠀⠀⠀⠀⠀⠀⠀⠀⢈⡟⠉⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠚⠉⠀⢸⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣼⠁⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠞⠋⠁⠀⠀⢀⠀⣼⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⠇⠀⠀⠀⠀⠈⠻⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣀⠀⠀⣀⣤⠶⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⠀⠈⢷⡄⠀⠀⠀⠀⠀⠀⠀⣠⠞⠡⡀⠉⠳⣞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⢀⡼⠃⠈⠢⣌⠲⡄⠈⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀
⠀⠀⠀⠀⠀⣸⠃⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⡬⠿⠶⠶⢶⡾⠡⡉⠢⢄⡀⠑⢌⠢⡈⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀
⠀⠀⠀⠀⢠⡏⠀⠀⠀⠀⠀⠀⣠⡴⠞⠫⠉⠀⠀⠀⠀⢀⡞⠡⣀⠈⠑⠢⢍⠒⣄⡳⡌⢸⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀
⠀⠀⠀⠀⢾⠀⠀⠀⠀⢀⣴⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠂⠤⣉⡒⠤⢄⣹⡟⠿⣾⠋⠉⠛⣶⠒⠛⠋⠉⠉⠙⠛⠲⠧⣤⡀⠀
⠀⠀⠀⠀⠈⠳⣄⠀⣰⣿⠃⠀⢒⣠⠤⠤⠤⠤⣄⡀⠀⠸⠷⣤⣀⣀⠉⠁⠒⠢⠍⢰⡇⠀⠀⣠⣟⣀⡭⠭⠍⣁⡒⠒⠤⢄⣀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣻⠿⠃⠀⡴⠋⠀⠀⠀⠀⠀⠀⠙⢦⠐⠀⠀⠉⠉⠙⠛⠛⠛⠻⠋⠛⢶⡶⠋⣐⠮⢟⡒⠤⣀⠈⠉⠒⠄⡾⠀⠀
⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⣴⠃⢀⣤⡄⠀⠀⢠⣤⡀⠘⣇⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡘⠮⡓⢄⡈⠑⠠⣍⠒⠤⣼⠃⠀⠀
⠀⣄⡀⠀⠀⢰⠇⠀⠀⠀⠘⣇⢸⣿⠇⠀⠀⠸⣿⡗⣸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣄⠉⠢⣉⠢⢄⡀⠉⣾⠃⠀⠀⠀
⠀⠈⠙⠀⠀⣾⠀⠈⢀⡴⠶⣿⣷⣦⠀⡄⢠⠀⣴⣾⡷⠖⠓⠲⢶⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣄⠈⠑⠦⢉⡾⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡇⠀⣾⡋⠀⠀⠀⠙⠿⣟⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠉⠛⢦⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢶⠶⠋⢀⣀⡄⠀⠀⠀
⠉⠉⠁⠀⠀⡇⣸⠃⣟⣦⣄⡀⠀⠀⠈⠙⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠀⠀⠉⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢿⡿⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣴⣶⠄⠀⠀⠈⢿⡄⠀⠀⠀⠀⠀⠀⣸⠃⠀⢀⣀⡀⠀⠀⠀⠀
⠐⠚⠋⠀⠀⠘⣧⠀⠸⣿⣿⡿⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠋⠁⠀⠀⠁⠀⠀⠀⠀⠀⢿⠀⠀⠀⠀⢠⡾⠁⠀⠀⠀⠉⠙⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⢷⡀⠈⠉⠀⠀⠀⠻⠿⠇⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠇⠀⣠⡴⠋⠀⠀⠀⢤⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⢳⡤⠤⣴⠲⡽⣖⣚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣣⡴⠛⠁⠀⠀⠀⠀⠀⠀⠙⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢰⠏⠀⠀⢨⣾⠁⣀⡉⠙⠓⢦⣀⣀⣀⣀⣀⣀⣤⣤⣴⣶⣿⣿⣿⣝⣷⠛⢳⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⣀⣀⣠⣾⣷⡿⣛⡻⣷⠄⣼⠭⡽⣿⣿⣅⡀⠀⣿⡟⠛⠻⣏⠉⠉⠙⠛⠋⠀⠀⣀⣴⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣏⠁⡞⣿⣟⠴⢜⣿⠷⠳⢾⣅⠀⠉⠛⣿⡷⣿⠿⣄⠀⠙⢦⡀⠀⠀⠀⠀⠸⢿⣿⣿⣿⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠳⢬⣟⣯⢿⡃⠀⠀⠀⢩⣠⡴⠞⠁⠀⠻⣤⡽⠀⠀⠀⠙⢦⡀⠀⠀⢀⣼⣿⡿⠙⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⢧⣀⠀⣀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣬⣷⣤⣴⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢻⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠿⢿⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

██╗░░██╗░█████╗░░██╗░░░░░░░██╗░█████╗░██╗██╗
██║░██╔╝██╔══██╗░██║░░██╗░░██║██╔══██╗██║██║
█████═╝░███████║░╚██╗████╗██╔╝███████║██║██║
██╔═██╗░██╔══██║░░████╔═████║░██╔══██║██║██║
██║░╚██╗██║░░██║░░╚██╔╝░╚██╔╝░██║░░██║██║██║
╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝╚═╝

    ✧･ﾟ: *✧･ﾟ:* Kawaii Stock Analysis Platform *:･ﾟ✧*:･ﾟ✧
"""
    print(kawaii_art)

def main():
    """Main function to launch the GUI"""
    show_kawaii_ascii()
    print("🚀 Starting Kawaii Stock Analysis Platform...")
    
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
        
        print("Dependencies verified (⊃｡•́‿•̀｡)⊃━☆ﾟ.*・｡ﾟ")
        print("Launching GUI application...")
        
        app = StockAnalysisGUI()
        app.run()
        
    except ImportError as e:
        print(f"Failed to import GUI components: {e}")
        print("Make sure all files are in the same directory")
        print("\nTrying CLI fallback...")
        try:
            from scripts.cli import StockAnalysisCLI
            cli = StockAnalysisCLI()
            cli.run()
        except:
            print("CLI fallback also failed")
            sys.exit(1)
        
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()