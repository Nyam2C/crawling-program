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
from src.gui.components.stock_data_tab import StockDataTab
from src.gui.components.recommendations_tab import RecommendationsTab
from src.gui.components.analysis_tab import IndividualAnalysisTab
from src.gui.components.settings_tab import SettingsTab
from src.gui.components.theme_manager import ThemeManager
from src.gui.components.icon_manager import IconManager
from src.gui.components.ui_builder import UIBuilder


class StockAnalysisGUI:
    """Main GUI application for stock analysis and recommendations - Retro Pastel Edition!"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        
        # Initialize component managers
        self.theme_manager = ThemeManager(self.root)
        self.icon_manager = IconManager()
        self.ui_builder = UIBuilder(self, self.icon_manager, self.theme_manager)
        
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
        self.root.title("Kuromi's Magnificent Seven Stock Analysis")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
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
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tab components
        self.stock_data_tab = StockDataTab(self.notebook, self)
        self.recommendations_tab = RecommendationsTab(self.notebook, self)
        self.analysis_tab = IndividualAnalysisTab(self.notebook, self)
        self.settings_tab = SettingsTab(self.notebook, self)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to analyze the stock market. Let's find the best investment opportunities.")
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
        
    # Delegation methods for backward compatibility
    def icon_button(self, parent, key, text, command, style='Pastel.Primary.TButton'):
        """Create button with pixel icon - delegates to ui_builder"""
        return self.ui_builder.create_icon_button(parent, key, text, command, style)
        
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
        """Show error dialog"""
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