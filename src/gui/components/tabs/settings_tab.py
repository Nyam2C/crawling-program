#!/usr/bin/env python3
"""Settings Tab Component - Cute Kuromi Style"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.analysis.recommendation_engine import RecommendationEngine
from src.data.stock_crawler import StockCrawler


class SettingsTab:
    def __init__(self, notebook, main_app):
        self.notebook = notebook
        self.main_app = main_app
        self.colors = main_app.colors
        self.setup_tab()
        
    def setup_tab(self):
        """Create the settings tab with scrollable content"""
        # Main frame for the tab
        self.main_frame = ttk.Frame(self.notebook, padding="5")
        icon = self.main_app.icon_manager.get_icon('tab_settings')
        if icon:
            self.notebook.add(self.main_frame, text='Settings', image=icon, compound='left')
        else:
            self.notebook.add(self.main_frame, text='Settings')
        
        # Create scrollable frame
        self.create_scrollable_frame()
        
        # App info
        self.create_app_info()
        
        # Settings controls
        self.create_settings_controls()
        
    def create_scrollable_frame(self):
        """Create a scrollable frame for the settings content"""
        # Create canvas and scrollbar with background color
        self.canvas = tk.Canvas(self.main_frame, highlightthickness=0, bg=self.colors['panel'])
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, padding="15")
        
        # Configure scrollable frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create canvas window
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Set the frame reference for content creation
        self.frame = self.scrollable_frame
        
    def create_app_info(self):
        """Create app information section"""
        info_frame = ttk.LabelFrame(self.frame, text="About This App", padding="15")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        info_text = """Stock Analysis Platform

Version: 4.0.0 - Professional Trading Simulation Edition
Style: Modern Interface with Professional Aesthetics  
Purpose: Educational Stock Analysis & Virtual Trading

This platform provides comprehensive stock market education 
tools for risk-free learning:

✧ Real-time stock data analysis and AI recommendations
✧ Virtual trading simulation with $100,000 virtual cash
✧ Investment personality analysis and skill assessment
✧ Educational market tools designed for safe learning
✧ Comprehensive recommendation reports
✧ Professional interface with intuitive design

"Knowledge is the best investment you can make."

DISCLAIMER: This tool is for educational purposes only.
   Not investment advice. Always do your own research!"""
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT, 
                              foreground=self.colors['text'])
        info_label.grid(row=0, column=0, sticky=(tk.W, tk.N))
        
    def create_settings_controls(self):
        """Create settings control panel"""
        controls_frame = ttk.LabelFrame(self.frame, text="Configuration", padding="15")
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Request delay setting
        ttk.Label(controls_frame, text="Request Delay (seconds):").grid(row=0, column=0, padx=(0, 15), sticky=tk.W)
        self.delay_var = tk.StringVar(value="2")
        delay_spinbox = ttk.Spinbox(controls_frame, from_=1, to=10, textvariable=self.delay_var, 
                                   width=10)
        delay_spinbox.grid(row=0, column=1, padx=(0, 15), sticky=tk.W)
        
        ttk.Label(controls_frame, text="(Higher values are more respectful to servers)",
                 font=('Arial', 9), foreground=self.colors['pink']).grid(row=0, column=2, sticky=tk.W)
        
        # Save button with icon
        self.main_app.icon_button(controls_frame, 'save', 'Save Settings',
                                  self.save_settings,
                                  style='Pastel.Secondary.TButton').grid(row=1, column=0, pady=(15, 0), sticky=tk.W)
        
        # Theme info
        theme_frame = ttk.LabelFrame(self.frame, text="Theme Information", padding="15")
        theme_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        theme_text = """Current Theme: Professional Retro Style

Color Palette:
Background: Deep Navy Purple (#1F144A)
Panel: Medium Purple (#2B1E6B)  
Lavender: Dreamy Lavender (#C4B5FD)
Periwinkle: Soft Purple (#A78BFA)
Pink: Accent Pink (#FBCFE8)
Text: Ghost White (#F8F8FF)

This theme combines professional aesthetics 
with pleasant pastel colors and retro styling!"""
        
        theme_label = ttk.Label(theme_frame, text=theme_text, justify=tk.LEFT,
                               foreground=self.colors['text'])
        theme_label.grid(row=0, column=0, sticky=(tk.W, tk.N))
        
    def save_settings(self):
        """Save application settings"""
        try:
            delay = int(self.delay_var.get())
            
            # Update engines with new delay
            self.main_app.recommendation_engine.close()
            self.main_app.stock_crawler.close()
            
            self.main_app.recommendation_engine = RecommendationEngine(delay=delay)
            self.main_app.stock_crawler = StockCrawler(delay=delay)
            
            try:
                from src.gui.components.dialogs import show_success
                show_success(self.main_app.root, "Success", f"Settings saved successfully!\n\nNew request delay: {delay} seconds")
            except ImportError:
                messagebox.showinfo("Success", f"Settings saved successfully!\n\nNew request delay: {delay} seconds")
            self.main_app.update_status(f"Settings updated - Request delay: {delay}s")
            
        except ValueError:
            try:
                from src.gui.components.dialogs import show_error
                show_error(self.main_app.root, "Error", "Please enter a valid delay value (1-10 seconds)!")
            except ImportError:
                messagebox.showerror("Error", "Please enter a valid delay value (1-10 seconds)!")