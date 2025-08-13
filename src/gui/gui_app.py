#!/usr/bin/env python3
"""
Magnificent Seven Stock Analysis - Cool Kuromi GUI Application
Powered by Kuromi's rebellious cuteness! 🖤💗
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import random
from PIL import Image, ImageTk
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
    """Main GUI application for stock analysis and recommendations - Cool Kuromi Edition! 🖤💗"""
    
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
        
        # Kuromi stickers
        self.kuromi_stickers = []
        self.load_kuromi_stickers()
        
        # Initialize cool effects
        self.setup_cool_effects()
        
    def setup_main_window(self):
        """Configure the main window with cool Kuromi aesthetics 🖤💗"""
        self.root.title("×~☆𝑲𝒖𝒓𝒐𝒎𝒊☆~× Magnificent Seven Stock Analysis ×~☆𝑲𝒖𝒓𝒐𝒎𝒊☆~×")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Cool Kuromi dark theme background
        self.root.configure(bg='#1A1A1A')  # Deep black
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
            
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_styles(self):
        """Create cool Kuromi-inspired custom styles 🎨"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cool Kuromi color palette 🖤💗
        self.colors = {
            'kuromi_primary': '#FF69B4',    # Hot pink
            'kuromi_secondary': '#FF1493',  # Deep pink  
            'kuromi_accent': '#FF91A4',     # Light pink
            'kuromi_black': '#000000',      # Pure black
            'kuromi_dark': '#1A1A1A',       # Dark grey-black
            'kuromi_light': '#2D2D2D',      # Light grey-black
            'kuromi_text': '#FFFFFF',       # White
            'kuromi_purple': '#8B008B'      # Dark magenta
        }
        
        # Configure cool root theme
        self.style.configure('TFrame', background=self.colors['kuromi_dark'])
        self.style.configure('TLabel', background=self.colors['kuromi_dark'], 
                           foreground=self.colors['kuromi_text'])
        self.style.configure('TLabelFrame', background=self.colors['kuromi_dark'],
                           foreground=self.colors['kuromi_primary'])
        self.style.configure('TLabelFrame.Label', background=self.colors['kuromi_dark'],
                           foreground=self.colors['kuromi_primary'])
        
        # Cool Kuromi button styles 🖤💗
        self.style.configure('Kuromi.Primary.TButton',
                           background=self.colors['kuromi_primary'],
                           foreground=self.colors['kuromi_black'],
                           borderwidth=2,
                           relief='raised',
                           focuscolor=self.colors['kuromi_accent'])
        
        self.style.map('Kuromi.Primary.TButton',
                      background=[('active', self.colors['kuromi_accent']),
                                ('pressed', self.colors['kuromi_secondary'])])
        
        self.style.configure('Kuromi.Black.TButton',
                           background=self.colors['kuromi_black'], 
                           foreground=self.colors['kuromi_primary'],
                           borderwidth=2,
                           relief='raised',
                           focuscolor=self.colors['kuromi_accent'])
        
        self.style.map('Kuromi.Black.TButton',
                      background=[('active', self.colors['kuromi_light']),
                                ('pressed', self.colors['kuromi_dark'])])
        
        # Cool notebook (tabs) styling
        self.style.configure('TNotebook', background=self.colors['kuromi_dark'],
                           borderwidth=0)
        self.style.configure('TNotebook.Tab', 
                           background=self.colors['kuromi_light'],
                           foreground=self.colors['kuromi_text'],
                           padding=[20, 10],
                           borderwidth=1)
        self.style.map('TNotebook.Tab',
                      background=[('selected', self.colors['kuromi_primary']),
                                ('active', self.colors['kuromi_accent'])])
        
        # Cool treeview styling
        self.style.configure('Kuromi.Treeview',
                           background=self.colors['kuromi_light'],
                           foreground=self.colors['kuromi_text'],
                           fieldbackground=self.colors['kuromi_light'],
                           borderwidth=1,
                           relief='solid')
        self.style.configure('Kuromi.Treeview.Heading',
                           background=self.colors['kuromi_primary'],
                           foreground=self.colors['kuromi_black'],
                           relief='raised',
                           borderwidth=1)
        
        # Cool combobox styling  
        self.style.configure('Kuromi.TCombobox',
                           fieldbackground=self.colors['kuromi_light'],
                           background=self.colors['kuromi_primary'],
                           foreground=self.colors['kuromi_black'])
        
        # Cool progress bar styling
        self.style.configure('Kuromi.Horizontal.TProgressbar',
                           background=self.colors['kuromi_primary'],
                           troughcolor=self.colors['kuromi_light'],
                           borderwidth=1,
                           lightcolor=self.colors['kuromi_accent'],
                           darkcolor=self.colors['kuromi_secondary'])
        
        # Cool scrollbar styling
        self.style.configure('Kuromi.Vertical.TScrollbar',
                           background=self.colors['kuromi_light'],
                           troughcolor=self.colors['kuromi_dark'],
                           borderwidth=1,
                           arrowcolor=self.colors['kuromi_text'])
        self.style.configure('Kuromi.Horizontal.TScrollbar',
                           background=self.colors['kuromi_light'],
                           troughcolor=self.colors['kuromi_dark'],
                           borderwidth=1,
                           arrowcolor=self.colors['kuromi_text'])
        
    def create_widgets(self):
        """Create all GUI widgets with cool styling 🖤💗"""
        # Create main frame with cool Kuromi styling
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Cool Kuromi title with rebellious styling
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
        
        # Cool status bar
        self.create_status_bar(main_frame)
        
    def create_title_section(self, parent):
        """Create the cool title section with Kuromi decorations 🖤💗"""
        title_frame = ttk.Frame(parent)
        title_frame.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        title_frame.grid_columnconfigure(1, weight=1)
        
        # Left Kuromi sticker
        left_sticker = self.add_kuromi_decoration(title_frame)
        if left_sticker:
            left_sticker.grid(row=0, column=0, rowspan=2, padx=(0, 15), pady=5)
        
        # Title and subtitle
        title_label = ttk.Label(title_frame, 
                              text="×~☆𝑲𝒖𝒓𝒐𝒎𝒊☆~× Magnificent Seven Analysis ×~☆𝑲𝒖𝒓𝒐𝒎𝒊☆~×",
                              font=('Arial', 20, 'bold'),
                              foreground=self.colors['kuromi_primary'])
        title_label.grid(row=0, column=1)
        
        # ASCII Art
        kuromi_ascii = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣦⣤⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⡿⢋⣾⣿⣿⡇⠀⠀
⠀⠀⣾⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣏⣠⣿⣿⣿⣿⣿⠀⠀
⠀⠀⠉⠉⢿⣯⡛⠻⠿⣿⣶⣶⣶⡄⠀⠀⢀⣀⣀⣤⣼⣿⣿⣿⣭⣿⣿⣿⣿⡇⠀
⠀⠀⠀⠀⠸⣿⣿⣦⣤⣴⣿⣿⣿⣧⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠁⠀
⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠉⢉⣉⢻⣿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢖⣟⢈⣩⣾⣿⠟⠛⠿⢿⣿⣿⣧⠀
⠀⠀⠀⠀⠀⠀⠈⠛⠛⣿⣿⣿⡿⠛⢉⣭⠽⠤⠿⢿⡿⠛⠁⠀⢀⣴⡆⠙⣿⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣷⣾⠋⣀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⣹⡏⠀
⠀⠀⠀⣀⠤⠠⡀⠀⠀⢿⣿⣿⣿⠇⠀⢻⣿⣿⡄⠀⢠⢤⡄⠀⠈⠉⠐⣤⡟⠁⠀
⢠⢎⡉⠁⠀⠀⡗⠀⠀⠈⢿⣿⣿⣇⠀⠈⠿⠋⠀⠀⢰⣿⣆⣀⡀⣠⡼⠋⠀⠀⠀
⠀⠓⠤⣀⣀⡜⠁⠀⡠⢄⠀⠙⢻⣿⣷⢿⡿⠒⠒⠉⢹⣿⣯⠀⠹⣧⡤⢤⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡠⠚⠀⠀⡇⠀⡇⠹⣿⣃⣾⡶⣺⣻⣼⣿⣿⣀⣰⣷⣝⠉⣴⣿⡄
⠀⠀⠀⠀⠀⠀⠣⠤⠤⠴⠇⠀⠈⠒⠻⣍⣙⣛⢺⣾⣯⡿⣿⣿⣿⣿⣿⣯⣹⣿⠛
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠈⠙⠛⡟⠛⣉⠄⢠⠈⠉⠉⢸⠿⠟⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡀⠀⢠⣧⡈⠀⢀⡄⠀⣀⡠⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀
        """
        
        # ASCII Art Label
        ascii_label = ttk.Label(title_frame,
                               text=kuromi_ascii,
                               font=('Consolas', 8),
                               foreground=self.colors['kuromi_primary'])
        ascii_label.grid(row=1, column=1, pady=(5, 0))
        
        subtitle_label = ttk.Label(title_frame,
                                 text="Stocks are as rebellious as me... let's tame them! ˃̵ᴗ˂",
                                 font=('Arial', 12, 'italic'),
                                 foreground=self.colors['kuromi_accent'])
        subtitle_label.grid(row=2, column=1, pady=(5, 0))
        
        # Right Kuromi sticker
        right_sticker = self.add_kuromi_decoration(title_frame)
        if right_sticker:
            right_sticker.grid(row=0, column=2, rowspan=2, padx=(15, 0), pady=5)
        
    def create_status_bar(self, parent):
        """Create cool status bar 🖤💗"""
        self.status_var = tk.StringVar()
        self.status_var.set("˚ǚ⁀˝ 𝑐𝑜�𝒊𝐼 𝐫̵ 𝑜 ˝⁀̵ Ready to rock the market with Kuromi's style! Let's make some rebellious investments! ∿ ₁ ᵗ⁷")
        
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(15, 0))
        status_frame.grid_columnconfigure(0, weight=1)
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Cool progress indicator
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate',
                                       style='Kuromi.Horizontal.TProgressbar')
        self.progress.grid(row=0, column=1, padx=(10, 0))
        
    def update_status(self, message):
        """Update status bar message with cool flair 🖤💗"""
        self.status_var.set(message)
        self.root.update()
        
    def show_progress(self):
        """Show cool progress bar 😈"""
        self.progress.start()
        
    def hide_progress(self):
        """Hide progress bar and stop cool animations 🖤💗"""
        self.progress.stop()
        self.animation_running = False
        
    def show_error(self, message):
        """Show cool error message 😠"""
        messagebox.showerror("˃̵ᴗ˂ Hmph!", f"₅⃒⃑*ˊᵀ⁵ᵀˊ*⃒⃐ₔ {message}")
        
    def on_closing(self):
        """Handle application closing with cool goodbye 🖤💗"""
        try:
            self.recommendation_engine.close()
            self.stock_crawler.close()
        except:
            pass
        self.root.destroy()
        
    def setup_cool_effects(self):
        """Setup cool Kuromi-style effects and animations 🖤💗"""
        # Create cool animation variables
        self.animation_dots = 0
        self.cool_quotes = [
            "( ˆᶤⁱ ˆ⁷ ) Markets are just like me... unpredictable but totally worth it! ˃̵ᴗ˂",
            "“₉ₕ₈ₑ ˆ•␡•ˆ ₈ₑₕ₁ Don't underestimate me! I'll find the best stocks for you! ׳˚ﾊ(ˊ*ˊﾀ˓*ﾀ)˚׳",
            "( ˆⁱ̵˓ˆ⁷ ) Even rebels need smart investments... let's be rebelliously rich! ₉(ˊᶤˋ*)و̵",
            "׳˚(ˊˊᶤ̃אﾀᶤ̃ˊ)₁ₐ* ˈ♡‧₊˚ Hmph! These market trends can't fool Kuromi's sharp eyes!",
            "׵²•✼•²׵ My Devil's tail knows which way the market will swing! °ǚ(ˊ*ˊ͐₃ﾀ*ﾀ)ɪ°",
            "₈₁ₕ₈ₑ₇*ᵃˊᶤⁿˊˋ)₂ₙₗ* ‪₈♡‧₊˚ Being cute AND profitable? That's my specialty!",
            "₊‧°𝐿♡♡𝑂°‧₊ Pink and black, just like profits and losses... I prefer pink!",
            "₅⃒⃑*ˊᵀ⁵ᵀˊ*⃒⃐ₔ Those boring analysts don't know real style! Let me show you!",
            "°ǚ(ˊ*ˊ͐₃ﾀ*ﾀ)ɪ° Kuromi's investment magic is way cooler than anyone else's!",
            "˃̵ᴗ˂ Rebellious stocks for a rebellious investor... perfect match! ( ˆⁱ̵˓ˆ⁷ )"
        ]
        self.current_quote = 0
        
        # Start cool quote rotation
        self.root.after(5000, self.show_cool_quote)
        
    def show_cool_quote(self):
        """Show a rotating cool quote in status bar 🖤💗"""
        if not self.animation_running:  # Only show quotes when not processing
            quote = self.cool_quotes[self.current_quote]
            self.status_var.set(quote)
            self.current_quote = (self.current_quote + 1) % len(self.cool_quotes)
        
        # Schedule next quote change
        self.root.after(8000, self.show_cool_quote)
        
    def load_kuromi_stickers(self):
        """Load Kuromi sticker images for GUI decoration 🖤💗"""
        stickers_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'kuromi_stickers')
        if os.path.exists(stickers_path):
            for i in range(1, 26):  # 01.png to 25.png
                sticker_file = f"{i:02d}.png"
                sticker_path = os.path.join(stickers_path, sticker_file)
                if os.path.exists(sticker_path):
                    try:
                        # Load and resize sticker
                        img = Image.open(sticker_path)
                        img = img.resize((50, 50), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        self.kuromi_stickers.append(photo)
                    except Exception as e:
                        print(f"Failed to load sticker {sticker_file}: {e}")
        print(f"Loaded {len(self.kuromi_stickers)} Kuromi stickers! 🖤💗")
        
    def get_random_kuromi_sticker(self):
        """Get a random Kuromi sticker for decoration 🎲"""
        if self.kuromi_stickers:
            return random.choice(self.kuromi_stickers)
        return None
        
    def add_kuromi_decoration(self, parent):
        """Add random Kuromi sticker decoration to a frame 😈💗"""
        sticker = self.get_random_kuromi_sticker()
        if sticker:
            decoration_label = ttk.Label(parent, image=sticker, background=self.colors['kuromi_dark'])
            return decoration_label
        return None
        
    def run(self):
        """Run the GUI application with cool Kuromi magic 🖤💗"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    """Main function to run the cool GUI application 🖤💗"""
    app = StockAnalysisGUI()
    app.run()


if __name__ == "__main__":
    main()