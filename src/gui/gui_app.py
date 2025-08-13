#!/usr/bin/env python3
"""
Magnificent Seven Stock Analysis - Cute Kurumi GUI Application
Powered by Kurumi's magical cuteness! 💖✨
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from src.analysis.recommendation_engine import RecommendationEngine
from src.data.stock_crawler import StockCrawler
from src.gui.components.stock_data_tab import StockDataTab
from src.gui.components.recommendations_tab import RecommendationsTab
from src.gui.components.analysis_tab import IndividualAnalysisTab
from src.gui.components.settings_tab import SettingsTab

# Try to import charts module
try:
    from src.gui.gui_charts import StockChartsFrame
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False
    print("Charts module not available. Install matplotlib for chart functionality.")


class StockAnalysisGUI:
    """Main GUI application for stock analysis and recommendations - Cute Kurumi Edition! 💖"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        self.create_styles()
        self.create_widgets()
        
        # Initialize engines
        self.recommendation_engine = RecommendationEngine(delay=1)
        self.stock_crawler = StockCrawler(delay=1)
        
        # Data storage
        self.current_stock_data = {}
        self.current_recommendations = {}
        
        # Animation variables
        self.animation_running = False
        
        # Initialize cute effects
        self.setup_cute_effects()
        
    def setup_main_window(self):
        """Configure the main window with cute Kurumi aesthetics 💖"""
        self.root.title("💖 Kurumi's Magnificent Seven Stock Analysis 💖")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Cute Kurumi dark theme background
        self.root.configure(bg='#0D0B1F')  # Deep dark purple-black
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
            
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_styles(self):
        """Create cute Kurumi-inspired custom styles 🎨"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cute Kurumi color palette 💖
        self.colors = {
            'kurumi_primary': '#8B0000',    # Deep crimson red
            'kurumi_secondary': '#4B0000',  # Darker red  
            'kurumi_accent': '#FF6B6B',     # Soft pink-red
            'kurumi_gold': '#FFD700',       # Elegant gold
            'kurumi_dark': '#0D0B1F',       # Deep dark purple-black
            'kurumi_light': '#1A1A2E',      # Dark blue-purple
            'kurumi_text': '#F8F8FF',       # Ghost white
            'kurumi_shadow': '#2E0016'      # Dark shadow
        }
        
        # Configure cute root theme
        self.style.configure('TFrame', background=self.colors['kurumi_dark'])
        self.style.configure('TLabel', background=self.colors['kurumi_dark'], 
                           foreground=self.colors['kurumi_text'])
        self.style.configure('TLabelFrame', background=self.colors['kurumi_dark'],
                           foreground=self.colors['kurumi_gold'])
        self.style.configure('TLabelFrame.Label', background=self.colors['kurumi_dark'],
                           foreground=self.colors['kurumi_gold'])
        
        # Cute Kurumi button styles 💖
        self.style.configure('Kurumi.Primary.TButton',
                           background=self.colors['kurumi_primary'],
                           foreground=self.colors['kurumi_text'],
                           borderwidth=2,
                           relief='raised',
                           focuscolor=self.colors['kurumi_accent'])
        
        self.style.map('Kurumi.Primary.TButton',
                      background=[('active', self.colors['kurumi_accent']),
                                ('pressed', self.colors['kurumi_secondary'])])
        
        self.style.configure('Kurumi.Gold.TButton',
                           background=self.colors['kurumi_gold'], 
                           foreground=self.colors['kurumi_dark'],
                           borderwidth=2,
                           relief='raised',
                           focuscolor=self.colors['kurumi_accent'])
        
        self.style.map('Kurumi.Gold.TButton',
                      background=[('active', '#FFFF99'),
                                ('pressed', '#B8860B')])
        
        # Cute notebook (tabs) styling
        self.style.configure('TNotebook', background=self.colors['kurumi_dark'],
                           borderwidth=0)
        self.style.configure('TNotebook.Tab', 
                           background=self.colors['kurumi_light'],
                           foreground=self.colors['kurumi_text'],
                           padding=[20, 10],
                           borderwidth=1)
        self.style.map('TNotebook.Tab',
                      background=[('selected', self.colors['kurumi_primary']),
                                ('active', self.colors['kurumi_accent'])])
        
        # Cute treeview styling
        self.style.configure('Kurumi.Treeview',
                           background=self.colors['kurumi_light'],
                           foreground=self.colors['kurumi_text'],
                           fieldbackground=self.colors['kurumi_light'],
                           borderwidth=1,
                           relief='solid')
        self.style.configure('Kurumi.Treeview.Heading',
                           background=self.colors['kurumi_primary'],
                           foreground=self.colors['kurumi_text'],
                           relief='raised',
                           borderwidth=1)
        
        # Cute combobox styling  
        self.style.configure('Kurumi.TCombobox',
                           fieldbackground=self.colors['kurumi_light'],
                           background=self.colors['kurumi_primary'],
                           foreground=self.colors['kurumi_text'])
        
        # Cute progress bar styling
        self.style.configure('Kurumi.Horizontal.TProgressbar',
                           background=self.colors['kurumi_primary'],
                           troughcolor=self.colors['kurumi_light'],
                           borderwidth=1,
                           lightcolor=self.colors['kurumi_accent'],
                           darkcolor=self.colors['kurumi_secondary'])
        
        # Cute scrollbar styling
        self.style.configure('Kurumi.Vertical.TScrollbar',
                           background=self.colors['kurumi_light'],
                           troughcolor=self.colors['kurumi_dark'],
                           borderwidth=1,
                           arrowcolor=self.colors['kurumi_text'])
        self.style.configure('Kurumi.Horizontal.TScrollbar',
                           background=self.colors['kurumi_light'],
                           troughcolor=self.colors['kurumi_dark'],
                           borderwidth=1,
                           arrowcolor=self.colors['kurumi_text'])
        
    def create_widgets(self):
        """Create all GUI widgets with cute styling 💖"""
        # Create main frame with cute Kurumi styling
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Cute Kurumi title with adorable styling
        self.create_title_section(main_frame)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tab components
        self.stock_data_tab = StockDataTab(self.notebook, self)
        self.recommendations_tab = RecommendationsTab(self.notebook, self)
        self.analysis_tab = IndividualAnalysisTab(self.notebook, self)
        
        # Add charts tab if available
        self.charts_frame = None
        if CHARTS_AVAILABLE:
            self.charts_frame = StockChartsFrame(self.notebook)
        
        self.settings_tab = SettingsTab(self.notebook, self)
        
        # Cute status bar
        self.create_status_bar(main_frame)
        
    def create_title_section(self, parent):
        """Create the cute title section"""
        title_frame = ttk.Frame(parent)
        title_frame.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(title_frame, 
                              text="💖 Kurumi's Magnificent Seven Analysis 💖",
                              font=('Arial', 20, 'bold'),
                              foreground=self.colors['kurumi_gold'])
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(title_frame,
                                 text="Time and stocks... both are precious! ✨",
                                 font=('Arial', 12, 'italic'),
                                 foreground=self.colors['kurumi_accent'])
        subtitle_label.grid(row=1, column=0, pady=(5, 0))
        
    def create_status_bar(self, parent):
        """Create cute status bar 💖"""
        self.status_var = tk.StringVar()
        self.status_var.set("💖 Ready to analyze with Kurumi's magic! Let's make some great investments! ✨")
        
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(15, 0))
        status_frame.grid_columnconfigure(0, weight=1)
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Cute progress indicator
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate',
                                       style='Kurumi.Horizontal.TProgressbar')
        self.progress.grid(row=0, column=1, padx=(10, 0))
        
    def update_status(self, message):
        """Update status bar message with cute flair 💖"""
        self.status_var.set(message)
        self.root.update()
        
    def show_progress(self):
        """Show cute progress bar ✨"""
        self.progress.start()
        
    def hide_progress(self):
        """Hide progress bar and stop cute animations 💖"""
        self.progress.stop()
        self.animation_running = False
        
    def show_error(self, message):
        """Show cute error message 😢"""
        messagebox.showerror("😢 Oops!", f"💔 {message}")
        
    def on_closing(self):
        """Handle application closing with cute goodbye 💖"""
        try:
            self.recommendation_engine.close()
            self.stock_crawler.close()
        except:
            pass
        self.root.destroy()
        
    def setup_cute_effects(self):
        """Setup cute Kurumi-style effects and animations 💖"""
        # Create cute animation variables
        self.animation_dots = 0
        self.cute_quotes = [
            "💖 Time reveals all market secrets... let's analyze together! ✨",
            "🌙 The best investment opportunities are found in careful analysis! 📊",
            "🌹 Elegant investing blooms with patience and wisdom! 🌸",
            "✨ Market rhythms echo through time... just like my heartbeat! 💖",
            "💎 Even spirits need good portfolio advice sometimes! 😊",
            "🌙 Let me give you the best investment advice... ara ara ara! 💖",
            "🕰️ Time spirit Kurumi will protect your wealth! ✨",
            "💃 Market dances are beautiful... but my dance is more beautiful! 🌹",
            "⏳ Seeking short-term profits is foolish... time is the true treasure! 💰",
            "😏 Fufu... seeing these results, you'll be amazed by my power! 🌹"
        ]
        self.current_quote = 0
        
        # Start cute quote rotation
        self.root.after(5000, self.show_cute_quote)
        
    def show_cute_quote(self):
        """Show a rotating cute quote in status bar 💖"""
        if not self.animation_running:  # Only show quotes when not processing
            quote = self.cute_quotes[self.current_quote]
            self.status_var.set(quote)
            self.current_quote = (self.current_quote + 1) % len(self.cute_quotes)
        
        # Schedule next quote change
        self.root.after(8000, self.show_cute_quote)
        
    def run(self):
        """Run the GUI application with cute Kurumi magic 💖"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    """Main function to run the cute GUI application 💖"""
    app = StockAnalysisGUI()
    app.run()


if __name__ == "__main__":
    main()