#!/usr/bin/env python3
"""
Magnificent Seven Stock Analysis - Retro Pastel GUI Application
Modern stock analysis with retro 90s styling
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import random
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not available. Icons will be disabled.")
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
    """Main GUI application for stock analysis and recommendations - Retro Pastel Edition!"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        self.create_styles()
        
        # Initialize all attributes FIRST before creating widgets
        self.recommendation_engine = RecommendationEngine(delay=1)
        self.stock_crawler = StockCrawler(delay=1)
        
        # Data storage
        self.current_stock_data = {}
        self.current_recommendations = {}
        
        # Animation variables
        self.animation_running = False
        
        # Pixel icons - initialize BEFORE create_widgets()
        self.pixel_icons = []
        self.icons = {}
        self.load_pixel_icons()
        
        # NOW create widgets after all attributes are initialized
        self.create_widgets()
        
        # Initialize effects
        self.setup_effects()
        
    def setup_main_window(self):
        """Configure the main window with retro pastel aesthetics"""
        self.root.title("×~☆𝑲𝒖𝒓𝒐𝒎𝒊☆~× Magnificent Seven Stock Analysis")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Center window on screen for better UX
        self.center_window()
        
        # Set theme background
        self.root.configure(bg='#1F144A')  # Deep navy purple
        
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
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_styles(self):
        """Create retro 90s-style pastel purple/pink theme"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Enhanced pastel purple/pink retro palette
        self.colors = {
            # base backgrounds
            'bg':           '#1F144A',  # Deep navy purple (main background)
            'panel':        '#2B1E6B',  # Panel/tab background
            'panel_alt':    '#3A2A86',  # Alternate panel color
            'panel_light':  '#4C3BAA',  # Lighter panel variant

            # purple pastels
            'lavender':     '#C4B5FD',  # Lavender
            'periwinkle':   '#A78BFA',  # Periwinkle purple
            'lilac':        '#DDD6FE',  # Light lilac
            'violet':       '#8B5CF6',  # Medium violet

            # pink pastels
            'pink':         '#FBCFE8',  # Soft pink
            'hotpink':      '#FDA4AF',  # Hot pink accent
            'rose':         '#F9A8D4',  # Rose pink
            'magenta':      '#E879F9',  # Bright magenta
            'blush':        '#FDF2F8',  # Very light blush

            # accent colors
            'mint':         '#A7F3D0',  # Mint accent
            'coral':        '#FCA5A5',  # Coral accent
            'peach':        '#FBBF24',  # Peach accent

            # text colors (no pure white)
            'text':         '#F3E8FF',  # Soft lavender white
            'text_muted':   '#DDD6FE',  # Muted lavender text
            'text_accent':  '#A78BFA',  # Accent text color

            # borders/shadows
            'border':       '#8B5CF6',  # Violet border
            'border_light': '#C4B5FD',  # Light border
            'shadow':       '#140E33',  # Shadow color
            'highlight':    '#F9A8D4'   # Pink highlight
        }
        
        # Set root background
        self.root.configure(bg=self.colors['bg'])
        
        # Font (try Korean font first, fallback to Arial)
        try:
            default_font = ('맑은 고딕', 9)
        except:
            default_font = ('Arial', 9)
        self.style.configure('.', font=default_font, foreground=self.colors['text'])
        
        # Common background styles (no white/gray)
        self.style.configure('TFrame', background=self.colors['panel'])
        self.style.configure('TLabel', background=self.colors['panel'], foreground=self.colors['text'])
        self.style.configure('TLabelFrame', background=self.colors['panel'], foreground=self.colors['rose'])
        self.style.configure('TLabelFrame.Label', background=self.colors['panel'], foreground=self.colors['rose'])
        
        # Accent label styles
        self.style.configure('Accent.TLabel', background=self.colors['panel'], foreground=self.colors['magenta'])
        self.style.configure('Highlight.TLabel', background=self.colors['panel'], foreground=self.colors['hotpink'])
        
        # Button styles (Primary / Secondary / Ghost)
        self.style.configure('Pastel.Primary.TButton',
            background=self.colors['periwinkle'], foreground='#1B1350',
            bordercolor=self.colors['border'], borderwidth=2, relief='ridge',
            padding=[10,6])
        self.style.map('Pastel.Primary.TButton',
            background=[('active', self.colors['lavender']), ('pressed', self.colors['pink'])])

        self.style.configure('Pastel.Secondary.TButton',
            background=self.colors['rose'], foreground='#1B1350',
            bordercolor=self.colors['highlight'], borderwidth=2, relief='ridge',
            padding=[10,6])
        self.style.map('Pastel.Secondary.TButton',
            background=[('active', self.colors['hotpink']), ('pressed', self.colors['magenta'])])

        self.style.configure('Pastel.Ghost.TButton',
            background=self.colors['panel_light'], foreground=self.colors['text'],
            bordercolor=self.colors['border_light'], borderwidth=2, relief='ridge',
            padding=[10,6])
        
        # Legacy button style mappings for backward compatibility
        self.style.configure('Kuromi.Primary.TButton',
            background=self.colors['periwinkle'], foreground='#1B1350',
            bordercolor=self.colors['border'], borderwidth=2, relief='ridge',
            padding=[10,6])
        self.style.map('Kuromi.Primary.TButton',
            background=[('active', self.colors['lavender']), ('pressed', self.colors['pink'])])
        
        self.style.configure('Kuromi.Black.TButton',
            background=self.colors['panel_alt'], foreground=self.colors['text'],
            bordercolor=self.colors['border'], borderwidth=2, relief='ridge',
            padding=[10,6])
        
        # Notebook tabs (retro window style)
        self.style.configure('TNotebook', background=self.colors['panel'], borderwidth=0)
        self.style.configure('TNotebook.Tab',
            background=self.colors['panel_alt'],
            foreground=self.colors['text'],
            padding=[14, 6],
            bordercolor=self.colors['border'],
            lightcolor=self.colors['periwinkle'],
            darkcolor=self.colors['shadow'],
            borderwidth=2, relief='ridge')
        self.style.map('TNotebook.Tab',
            background=[('selected', self.colors['periwinkle']), ('active', self.colors['lavender'])],
            foreground=[('selected', '#1B1350')])
        
        # Treeview (retro data grid style)
        self.style.configure('Pastel.Treeview',
            background=self.colors['panel_light'], fieldbackground=self.colors['panel_light'],
            foreground=self.colors['text'], borderwidth=2, relief='ridge')
        self.style.configure('Pastel.Treeview.Heading',
            background=self.colors['rose'], foreground='#1B1350', borderwidth=2, relief='ridge')
        self.style.map('Pastel.Treeview',
            background=[('selected', self.colors['magenta'])],
            foreground=[('selected', self.colors['text'])])
        
        # Legacy Treeview mapping
        self.style.configure('Kuromi.Treeview',
            background=self.colors['panel_alt'], fieldbackground=self.colors['panel_alt'],
            foreground=self.colors['text'], borderwidth=2, relief='ridge')
        self.style.configure('Kuromi.Treeview.Heading',
            background=self.colors['periwinkle'], foreground='#1B1350', borderwidth=2, relief='ridge')
        
        # Combobox (retro dropdown style)
        self.style.configure('Pastel.TCombobox',
            fieldbackground=self.colors['panel_light'], background=self.colors['rose'],
            foreground='#1B1350', bordercolor=self.colors['highlight'], borderwidth=2,
            arrowcolor='#1B1350')
        self.style.map('Pastel.TCombobox',
            fieldbackground=[('readonly', self.colors['panel_light'])],
            background=[('readonly', self.colors['hotpink'])])
        
        # Legacy Combobox mapping
        self.style.configure('Kuromi.TCombobox',
            fieldbackground=self.colors['panel_alt'], background=self.colors['periwinkle'],
            foreground='#1B1350', bordercolor=self.colors['border'], borderwidth=2)
        
        # Progress bar (retro style)
        self.style.configure('Pastel.Horizontal.TProgressbar',
            background=self.colors['periwinkle'], troughcolor=self.colors['panel_alt'],
            bordercolor=self.colors['border'], lightcolor=self.colors['lavender'],
            darkcolor=self.colors['shadow'], borderwidth=2)
        
        # Legacy progress bar mapping
        self.style.configure('Kuromi.Horizontal.TProgressbar',
            background=self.colors['periwinkle'], troughcolor=self.colors['panel_alt'],
            bordercolor=self.colors['border'], lightcolor=self.colors['lavender'],
            darkcolor=self.colors['shadow'], borderwidth=2)
        
        # Scrollbars (retro style)
        self.style.configure('Pastel.Vertical.TScrollbar',
            background=self.colors['panel_alt'], troughcolor=self.colors['panel'],
            arrowcolor=self.colors['text'])
        self.style.configure('Pastel.Horizontal.TScrollbar',
            background=self.colors['panel_alt'], troughcolor=self.colors['panel'],
            arrowcolor=self.colors['text'])
        
        # Legacy scrollbar mappings
        self.style.configure('Kuromi.Vertical.TScrollbar',
            background=self.colors['panel_alt'], troughcolor=self.colors['panel'],
            arrowcolor=self.colors['text'])
        self.style.configure('Kuromi.Horizontal.TScrollbar',
            background=self.colors['panel_alt'], troughcolor=self.colors['panel'],
            arrowcolor=self.colors['text'])
        
    def create_widgets(self):
        """Create all GUI widgets with retro styling"""
        # Create main frame with retro styling
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Retro title section
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
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_title_section(self, parent):
        """Create the title section with pixel decorations"""
        title_frame = ttk.Frame(parent)
        title_frame.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        title_frame.grid_columnconfigure(1, weight=1)
        
        # Left pixel decoration
        left_decoration = self.add_pixel_decoration(title_frame)
        if left_decoration:
            left_decoration.grid(row=0, column=0, rowspan=2, padx=(0, 15), pady=5)
        
        # Title and subtitle
        title_label = ttk.Label(title_frame, 
                              text="×~☆𝑲𝒖𝒓𝒐𝒎𝒊☆~× Magnificent Seven Stock Analysis",
                              font=('Arial', 18, 'bold'),
                              foreground=self.colors['lavender'])
        title_label.grid(row=0, column=1)
        
        # Pixel icon in title
        if hasattr(self, 'pixel_icons') and self.pixel_icons:
            title_icon = self.pixel_icons[0] if self.pixel_icons else None
            if title_icon:
                icon_label = ttk.Label(title_frame, image=title_icon, background=self.colors['panel'])
                icon_label.grid(row=1, column=1, pady=(5, 5))
        
        subtitle_label = ttk.Label(title_frame,
                                 text="✨ Kawaii stock analysis with rebellious attitude! ( ˶ˆᗜˆ˵ )",
                                 font=('Arial', 12, 'italic'),
                                 foreground=self.colors['periwinkle'])
        subtitle_label.grid(row=2, column=1, pady=(5, 0))
        
        # Right pixel decoration
        right_decoration = self.add_pixel_decoration(title_frame)
        if right_decoration:
            right_decoration.grid(row=0, column=2, rowspan=2, padx=(15, 0), pady=5)
        
    def create_status_bar(self, parent):
        """Create status bar"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to analyze the stock market. Let's find the best investment opportunities.")
        
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(15, 0))
        status_frame.grid_columnconfigure(0, weight=1)
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W,
                               background=self.colors['panel_light'], 
                               foreground=self.colors['text'])
        status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Progress indicator
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate',
                                       style='Kuromi.Horizontal.TProgressbar')
        self.progress.grid(row=0, column=1, padx=(10, 0))
        
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        self.root.update()
        
    def show_progress(self):
        """Show progress bar"""
        self.progress.start()
        
    def hide_progress(self):
        """Hide progress bar and stop animations"""
        self.progress.stop()
        self.animation_running = False
        
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
        
    def on_closing(self):
        """Handle application closing"""
        try:
            self.recommendation_engine.close()
            self.stock_crawler.close()
        except:
            pass
        self.root.destroy()
        
    def setup_effects(self):
        """Setup GUI effects and animations"""
        # Create animation variables
        self.animation_dots = 0
        self.status_messages = [
            "Analyzing market trends with advanced algorithms...",
            "Searching for the best investment opportunities...",
            "Processing stock data and performance metrics...",
            "Evaluating risk factors and potential returns...",
            "Generating personalized investment recommendations...",
            "Monitoring market volatility and price movements...",
            "Calculating optimal portfolio diversification...",
            "Studying fundamental and technical indicators...",
            "Ready to help you make informed investment decisions.",
            "Professional stock analysis at your fingertips."
        ]
        self.current_quote = 0
        
        # Start status message rotation
        self.root.after(5000, self.show_status_message)
        
    def show_status_message(self):
        """Show a rotating status message in status bar"""
        if not self.animation_running:  # Only show messages when not processing
            message = self.status_messages[self.current_quote]
            self.status_var.set(message)
            self.current_quote = (self.current_quote + 1) % len(self.status_messages)
        
        # Schedule next message change
        self.root.after(8000, self.show_status_message)
        
    def load_pixel_icons(self):
        """Load pixel-style icons for GUI decoration"""
        if not PIL_AVAILABLE:
            print("PIL not available, skipping icon loading")
            return
            
        # Icon mapping for different functions
        icon_mapping = {
            'analyze_advanced': 'bow.png',
            'analyze_quick':    'sparkle.png',
            'save':             'mail.png',
            'refresh':          'skull.png',
            'get_all':          'folder.png',
            'get_one':          'heart.png',
            'charts':           'glasses.png',
            'tab_data':         'add_1.png',
            'tab_recommend':    'add_2.png', 
            'tab_analysis':     'add_3.png',
            'tab_charts':       'add_4.png',
            'tab_settings':     'add_5.png',
            'decoration':       'heart.png'
        }
        
        icons_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'pixel_icons')
        if os.path.exists(icons_path):
            for key, filename in icon_mapping.items():
                icon_path = os.path.join(icons_path, filename)
                if os.path.exists(icon_path):
                    try:
                        # Load and resize icon with nearest neighbor for pixel perfect scaling
                        img = Image.open(icon_path)
                        img = img.resize((24, 24), Image.Resampling.NEAREST)  # Pixel feel
                        self.icons[key] = ImageTk.PhotoImage(img)
                    except Exception as e:
                        print(f"Failed to load icon {filename}: {e}")
        
        # Also load general pixel icons for decorations
        if os.path.exists(icons_path):
            for i, filename in enumerate(['sparkle.png', 'bow.png', 'heart.png']):
                icon_path = os.path.join(icons_path, filename)
                if os.path.exists(icon_path):
                    try:
                        img = Image.open(icon_path)
                        img = img.resize((32, 32), Image.Resampling.NEAREST)
                        photo = ImageTk.PhotoImage(img)
                        self.pixel_icons.append(photo)
                    except Exception as e:
                        print(f"Failed to load decoration icon {filename}: {e}")
        
        print(f"Loaded {len(self.icons)} functional icons and {len(self.pixel_icons)} decoration icons!")
        
    def get_random_pixel_icon(self):
        """Get a random pixel icon for decoration"""
        # Check if pixel_icons attribute exists and has items
        if hasattr(self, 'pixel_icons') and self.pixel_icons:
            import random
            return random.choice(self.pixel_icons)
        return None
        
    def get_pixel_icon(self, icon_key):
        """Get specific pixel icon by key"""
        if hasattr(self, 'icons') and icon_key in self.icons:
            return self.icons[icon_key]
        return None
    
    def add_pixel_decoration(self, parent):
        """Add random pixel icon decoration to a frame"""
        try:
            if hasattr(self, 'pixel_icons') and self.pixel_icons:
                import random
                icon = random.choice(self.pixel_icons)
                decoration_label = ttk.Label(parent, image=icon, background=self.colors['panel'])
                # Store reference to prevent garbage collection
                if not hasattr(self, 'decoration_refs'):
                    self.decoration_refs = []
                self.decoration_refs.append(icon)
                return decoration_label
        except Exception as e:
            print(f"Pixel decoration failed: {e}")
        
        # Simple fallback: Use decorative text patterns
        try:
            decorations = [
                "★",
                "♦", 
                "●",
                "◆"
            ]
            import random
            decoration_text = random.choice(decorations)
            decoration_label = ttk.Label(parent, text=decoration_text, 
                                       foreground=self.colors['lavender'],
                                       background=self.colors['panel'],
                                       font=('Arial', 12))
            return decoration_label
        except Exception as e:
            print(f"Text decoration failed: {e}")
            return None
    
    def icon_button(self, parent, key, text, command, style='Pastel.Primary.TButton'):
        """Create button with pixel icon"""
        btn = ttk.Button(parent, text=text, command=command, style=style)
        if hasattr(self, 'icons') and key in self.icons:
            btn.configure(image=self.icons[key], compound='left')
        return btn
        
    def add_icon_to_tab(self, tab_frame, icon_key, text):
        """Add icon to tab text if available"""
        if hasattr(self, 'icons') and icon_key in self.icons:
            # For tabs, we'll use text with icon reference
            return f"   {text}"  # Space for icon appearance
        return text
        
    def add_kuromi_icon_button(self, parent, text, command, icon_index=None):
        """Legacy method for backward compatibility - creates pixel icon button"""
        # Map old functionality to new pixel icon system
        if icon_index is not None and hasattr(self, 'pixel_icons') and icon_index < len(self.pixel_icons):
            icon = self.pixel_icons[icon_index]
            btn = ttk.Button(parent, text=text, command=command, 
                           style='Pastel.Primary.TButton', image=icon, compound='left')
            # Store reference to prevent garbage collection
            if not hasattr(self, 'icon_refs'):
                self.icon_refs = []
            self.icon_refs.append(icon)
            return btn
        else:
            # Fallback to regular button
            return ttk.Button(parent, text=text, command=command, style='Pastel.Primary.TButton')
        
    def run(self):
        """Run the GUI application with retro magic"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    """Main function to run the GUI application"""
    app = StockAnalysisGUI()
    app.run()


if __name__ == "__main__":
    main()