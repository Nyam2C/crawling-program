#!/usr/bin/env python3
"""
Magnificent Seven Stock Analysis - Retro Pastel GUI Application (Refactored)
Modern stock analysis with retro 90s styling
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import random

from src.analysis.recommendation_engine import RecommendationEngine
from src.data.stock_crawler import StockCrawler
from src.gui.components import (
    StockDataTab, RecommendationsTab, IndividualAnalysisTab, ScoreboardTab, SettingsTab, InvestmentAnalysisTab,
    MockTradingTab, NewsSentimentTab, ThemeManager, IconManager, UIBuilder
)
from src.gui.components.ui_core.keyboard_manager import KeyboardManager
from src.gui.components.ui_core.action_manager import ActionManager


class StockAnalysisGUI:
    """Main GUI application for stock analysis and recommendations - Retro Pastel Edition!"""
    
    def __init__(self):
        self.root = tk.Tk()
        
        # Show splash screen first
        self.show_kawaii_splash()
        
        self.setup_main_window()
        
        # Initialize component managers
        self.theme_manager = ThemeManager(self.root)
        self.icon_manager = IconManager()
        self.ui_builder = UIBuilder(self, self.icon_manager, self.theme_manager)
        
        # Initialize UX enhancement managers
        self.action_manager = ActionManager(max_history=50)
        self.action_manager.set_main_app(self)
        self.keyboard_manager = KeyboardManager(self.root, self)
        
        # Apply theme and load icons
        self.theme_manager.apply_styles()
        self.icon_manager.load_icons()
        
        # Initialize engines
        self.recommendation_engine = RecommendationEngine(delay=1)
        self.stock_crawler = StockCrawler(delay=1)
        
        # Data storage
        self.current_stock_data = {}
        self.current_recommendations = {}
        
        # Animation variables
        self.animation_running = False
        
        # Create widgets
        self.create_widgets()
        
        # Initialize effects
        self.setup_effects()
        
    def setup_main_window(self):
        """Configure the main window with retro pastel aesthetics"""
        self.root.title("Professional Stock Analysis Platform")
        self.root.geometry("1250x800")
        self.root.minsize(1050, 600)
        
        # Center window on screen for better UX
        self.center_window()
        
        # Add colorful window border
        try:
            self.root.configure(highlightbackground='#6B5CD6', highlightthickness=3)
        except:
            pass  # In case the option is not supported
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
            
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Set window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center the window on screen for better UX"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """Create all GUI widgets with retro styling"""
        # Create main frame with retro styling
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Retro title section
        self.ui_builder.create_title_section(main_frame)
        
        # Place background stickers using add_* icons
        self.ui_builder.place_background_stickers(main_frame, count=6)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tab components
        self.stock_data_tab = StockDataTab(self.notebook, self)
        self.recommendations_tab = RecommendationsTab(self.notebook, self)
        self.analysis_tab = IndividualAnalysisTab(self.notebook, self)
        self.news_sentiment_tab = NewsSentimentTab(self.notebook, self.icon_manager, self.theme_manager, self)
        self.mock_trading_tab = MockTradingTab(self.notebook, self)
        self.scoreboard_tab = ScoreboardTab(self.notebook, self)
        self.investment_analysis_tab = InvestmentAnalysisTab(self.notebook, self)
        self.settings_tab = SettingsTab(self.notebook, self)
        
        # Comprehensive evaluation area moved to investment analysis tab
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to analyze the stock market. Let's find the best investment opportunities!")
        status_frame, self.progress = self.ui_builder.create_status_bar(main_frame, self.status_var)
        
    def setup_effects(self):
        """Initialize visual effects"""
        # Add subtle animation to title (optional)
        self.animate_title()
        
    def animate_title(self):
        """Subtle title animation"""
        if not self.animation_running:
            self.animation_running = True
            # Simple color cycling for the title
            colors = [self.theme_manager.colors['lavender'], 
                     self.theme_manager.colors['periwinkle'],
                     self.theme_manager.colors['pink']]
            self.title_color_index = 0
            
            def cycle_colors():
                try:
                    if hasattr(self, 'title_label'):
                        current_color = colors[self.title_color_index % len(colors)]
                        self.title_label.configure(foreground=current_color)
                        self.title_color_index += 1
                        self.root.after(3000, cycle_colors)  # Change every 3 seconds
                except:
                    self.animation_running = False
            
            cycle_colors()
    
    # Evaluation area methods moved to investment analysis tab
        
    # Delegation methods for backward compatibility
    def icon_button(self, parent, key, text, command, style='Pastel.Primary.TButton', spacing=None):
        """Create button with pixel icon - delegates to ui_builder"""
        return self.ui_builder.create_icon_button(parent, key, text, command, style, spacing)
        
    def add_icon_to_tab(self, tab_frame, icon_key, text):
        """Add icon to tab text - delegates to ui_builder"""
        return self.ui_builder.add_icon_to_tab(tab_frame, icon_key, text)
        
    def add_kuromi_icon_button(self, parent, text, command, icon_index=None):
        """Legacy icon button - delegates to ui_builder"""
        return self.ui_builder.create_legacy_icon_button(parent, text, command, icon_index)
        
    @property
    def colors(self):
        """Access to theme colors"""
        return self.theme_manager.colors
        
    # Utility methods
    def show_progress(self):
        """Show progress indicator"""
        self.progress.start(10)
        
    def hide_progress(self):
        """Hide progress indicator"""
        self.progress.stop()
        
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        
    def show_error(self, message):
        """Show error dialog with styled theme"""
        try:
            from src.gui.components.dialogs import show_error
            show_error(self.root, "Error", message)
        except ImportError:
            # Fallback to standard messagebox
            messagebox.showerror("Error", message)
        
    def on_closing(self):
        """Handle window closing event"""
        try:
            self.recommendation_engine.close()
            self.stock_crawler.close()
        except:
            pass
        finally:
            self.root.destroy()
    
    def show_kawaii_splash(self):
        """Show kawaii splash screen with ASCII art"""
        # Hide main window initially
        self.root.withdraw()
        
        # Create splash window
        splash = tk.Toplevel()
        splash.title("Loading...")
        splash.configure(bg='#1F144A')  # Dark navy purple
        splash.resizable(False, False)
        splash.overrideredirect(True)  # Remove window borders
        
        # Center splash on screen  
        splash.update_idletasks()
        width = 600
        height = 450
        x = (splash.winfo_screenwidth() // 2) - (width // 2)
        y = (splash.winfo_screenheight() // 2) - (height // 2)
        splash.geometry(f"{width}x{height}+{x}+{y}")
        
        # Compact ASCII art
        kawaii_art = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠛⠛⠛⠒⠒⠶⢤⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⠤⠴⠶⠒⠒⠲⠶⠦⢤⣼⡃⠀⠀⠀⠀⠀⠀⠀⠈⠙⠳⣴⠛⠻⡆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⠀⠀⢀⣠⠶⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢶⣄⠀⠀⠀⠀⠀⠀⠀⣠⠿⢦⡴⠇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠟⠉⠈⠉⠻⣦⠟⠁⠀⠀⠀⠀⠀⢀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣆⠀⠀⠀⢠⡾⠁⠀⠀⠀⠀⠀⠀
⠀⢀⣀⠀⢀⣠⠶⠋⠁⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⠤⠴⠋⠀⠀⠀⠀⠀⠀⠀⠀
⢰⡏⠈⢳⣟⠁⠀⠀⠀⠀⠀⠀⠀⢰⡇⠀⠀⠀⠀⠀⠀⢸⡟⠉⣿⣿⣧⣨⠇⢀⣀⣀⡀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠛⠚⠋⠉⠳⢦⡀⠀⠀⠀⠀⠀⡾⠀⠀⠀⠀⠀⠀⠀⢀⠙⠿⢿⣿⣿⣯⠞⠋⠁⠈⠉⠳⢦⡄⠀⠀⢠⡇⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⢷⣄⠀⠀⢀⡇⠀⠀⠀⠀⠀⣤⠞⠉⠉⠙⠛⠛⠋⠀⠀⠀⠀⠀⠀⢠⡀⠙⣦⠀⣸⠃⠀⢰⠋⠉⠳⠋⠉⠙⡆⠀
⠀⠀⠀⠀⢀⠤⠤⣄⡀⠈⠛⠚⠋⣷⠀⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡶⢛⣿⣁⠀⢸⣦⡟⠀⠀⠸⣆⠀⠀⠀⠀⡼⠃⠀
⠀⠀⠀⠀⡏⠀⠀⠀⠵⠒⠲⢤⠀⠹⡆⠀⠀⢸⠇⢀⣤⡤⠤⣄⠀⠀⢠⠄⣄⠀⠀⢰⣿⠿⣿⣀⣸⡟⠀⠀⠀⠀⠈⠓⢤⡴⠊⠀⠀⠀
⠀⠀⠀⠀⢳⡀⠀⠀⠀⠀⠀⢨⠇⠀⠙⢦⡀⢸⡄⠀⣻⣴⣶⡶⠀⠀⣬⠭⠅⡆⠀⠈⣴⠟⠉⠉⢻⣦⡶⢲⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠳⡄⠀⣀⡤⠖⠉⠀⠀⠀⠀⠙⢦⣿⣤⣛⣿⠿⢧⣄⠀⠈⠒⣒⣡⡤⢾⡇⠀⢠⣴⣟⣯⡛⠛⠃⠀⠀⠀⢠⡏⠉⠳⠖⠲
⠀⠀⠀⣀⣀⡀⠹⠋⠁⠀⠀⠀⠀⠀⠀⠀⢀⣀⣈⣽⠿⣇⠀⠀⠹⡗⠚⣋⡭⠤⠤⣤⣷⡀⠀⢻⢿⣄⡿⠀⠀⠀⠀⠀⠀⠳⡀⠀⢀⡠
⡴⠚⠻⠇⠀⣹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣅⣿⠋⢉⣛⣿⠀⠀⢹⠟⠉⠀⠀⠀⠀⠈⠳⣶⠟⠀⠀⠀⡰⠒⠓⢆⠀⠀⠀⠘⠒⠉⠀
⠹⢄⣀⠀⡰⠃⠀⠀⠀⠀⠀⠀⠀⢸⡗⠒⠲⣶⠀⠀⠺⣥⣽⣦⡴⠟⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⢰⡇⠀⠀⢨⡧⣄⡀⠀⠀⠀⠀
⠀⠀⠈⠉⠁⠀⠀⣀⣀⡞⠉⠙⡆⠀⣧⣴⣄⠹⣦⣀⣀⣸⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡾⠃⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⠙⡆⠀⠀⠀
⠀⠀⠀⠀⠀⢠⠏⠁⠈⠀⠀⠀⡀⠀⠈⠀⠙⠳⠦⣬⣭⣽⣿⣆⠀⠀⠀⠀⠀⣤⠀⠀⣹⡇⠀⠀⠀⠀⠀⣇⣀⣀⣀⣀⣀⡼⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠈⢧⣄⣀⣀⠀⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀⡟⠀⠁⠀⠀⠀⠀⣰⠏⠀⠀⠻⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠛⣉⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⢦⣀⣀⣤⠞⠛⠶⠤⠴⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    
██╗░░██╗░█████╗░░██╗░░░░░░░██╗░█████╗░██╗██╗
██║░██╔╝██╔══██╗░██║░░██╗░░██║██╔══██╗██║██║
█████═╝░███████║░╚██╗████╗██╔╝███████║██║██║
██╔═██╗░██╔══██║░░████╔═████║░██╔══██║██║██║
██║░╚██╗██║░░██║░░╚██╔╝░╚██╔╝░██║░░██║██║██║
╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝╚═╝"""
        
        # Create main frame
        main_frame = tk.Frame(splash, bg='#1F144A')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ASCII art label
        art_label = tk.Label(main_frame, text=kawaii_art, 
                           font=('Courier', 8), 
                           fg='#C4B5FD',  # Lavender
                           bg='#1F144A',
                           justify=tk.CENTER)
        art_label.pack(pady=(5, 15))
        
        # Title
        title_label = tk.Label(main_frame, 
                             text="✧✿: *✧✿:* Kawaii StockEdu Platform *:✿✧*:✿✧",
                             font=('Arial', 14, 'bold'),
                             fg='#A78BFA',  # Periwinkle
                             bg='#1F144A')
        title_label.pack(pady=(0, 20))
        
        # Loading text
        loading_label = tk.Label(main_frame, 
                               text="Loading cute analytics... ♡",
                               font=('Arial', 12),
                               fg='#F9A8D4',  # Rose pink
                               bg='#1F144A')
        loading_label.pack(pady=(0, 10))
        
        # Progress bar
        progress = ttk.Progressbar(main_frame, mode='indeterminate', length=300)
        progress.pack(pady=(0, 20))
        progress.start()
        
        # Auto-close splash after 3 seconds
        def close_splash():
            progress.stop()
            splash.destroy()
            self.root.deiconify()  # Show main window
        
        splash.after(3000, close_splash)  # 3 seconds
        splash.update()

    def on_closing(self):
        """Handle application closing - cleanup resources"""
        try:
            # Cleanup mock trading tab resources
            if hasattr(self, 'mock_trading_tab'):
                self.mock_trading_tab.cleanup()
            
            # Cleanup other resources
            if hasattr(self, 'recommendation_engine'):
                self.recommendation_engine.close()
            if hasattr(self, 'stock_crawler'):
                self.stock_crawler.close()
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            self.root.destroy()

    def run(self):
        """Run the GUI application with retro magic"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    """Main entry point for the GUI application"""
    try:
        app = StockAnalysisGUI()
        app.run()
    except Exception as e:
        print(f"Application startup error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()