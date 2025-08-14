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
        """Create the settings tab"""
        self.frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.frame, text="₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ Settings")
        
        # App info
        self.create_app_info()
        
        # Settings controls
        self.create_settings_controls()
        
    def create_app_info(self):
        """Create app information section"""
        info_frame = ttk.LabelFrame(self.frame, text="˚‧꒰ა 𓂋 ໒꒱ ‧˚ About This App", padding="15")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        info_text = """₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ Kuromi's Magnificent Seven Stock Analysis System ˚‧꒰ა 𓂋 ໒꒱ ‧˚

⸜(｡˃ ᵕ ˂ )⸝♡ Version: 2.0.0 - Kawaii Pastel Edition
₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ Style: Adorable Pastel Purple/Pink with Retro Windows Aesthetics  
⸜(｡˃ ᵕ ˂ )⸝♡ Magic Level: Maximum Kawaii Cuteness!

This application provides advanced analysis and recommendations 
for the seven greatest technology stocks:

₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ AAPL - Apple Inc. (The Apple Empire)
(@_@) MSFT - Microsoft Corporation (The Microsoft Kingdom) 
(@_@) GOOGL - Alphabet Inc. (The Google Realm)
(@_@) AMZN - Amazon.com Inc. (The Amazon Empire)
₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ NVDA - NVIDIA Corporation (The NVIDIA Universe)
(>_<) TSLA - Tesla Inc. (The Tesla Electric Kingdom)
₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ META - Meta Platforms Inc. (The Meta Social Dimension)

"Time reveals all truths... including market movements!" (@_@)

(>_<) DISCLAIMER: This tool is for educational purposes only.
   Not investment advice. Always do your own research! ˚‧꒰ა 𓂋 ໒꒱ ‧˚"""
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT, 
                              foreground=self.colors['text'])
        info_label.grid(row=0, column=0, sticky=(tk.W, tk.N))
        
    def create_settings_controls(self):
        """Create settings control panel"""
        controls_frame = ttk.LabelFrame(self.frame, text="₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ Configuration", padding="15")
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Request delay setting
        ttk.Label(controls_frame, text="Request Delay (seconds):").grid(row=0, column=0, padx=(0, 15), sticky=tk.W)
        self.delay_var = tk.StringVar(value="2")
        delay_spinbox = ttk.Spinbox(controls_frame, from_=1, to=10, textvariable=self.delay_var, 
                                   width=10)
        delay_spinbox.grid(row=0, column=1, padx=(0, 15), sticky=tk.W)
        
        ttk.Label(controls_frame, text="(Higher values are more respectful to servers)",
                 font=('Arial', 9), foreground=self.colors['pink']).grid(row=0, column=2, sticky=tk.W)
        
        # Save button
        ttk.Button(controls_frame, text="(@_@) Save Settings",
                  command=self.save_settings,
                  style='Pastel.Primary.TButton').grid(row=1, column=0, pady=(15, 0), sticky=tk.W)
        
        # Theme info
        theme_frame = ttk.LabelFrame(self.frame, text="₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ Theme Information", padding="15")
        theme_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        theme_text = """₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ Current Theme: Kawaii Pastel Retro Style

Color Palette:
˚‧꒰ა 𓂋 ໒꒱ ‧˚ Background: Deep Navy Purple (#1F144A)
⸜(｡˃ ᵕ ˂ )⸝♡ Panel: Medium Purple (#2B1E6B)  
(*o*) Lavender: Dreamy Lavender (#C4B5FD)
(-_-) Periwinkle: Soft Purple (#A78BFA)
⸜(｡˃ ᵕ ˂ )⸝♡ Pink: Kawaii Pink (#FBCFE8)
₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ Text: Ghost White (#F8F8FF)

This theme combines Kuromi's rebellious kawaii personality 
with dreamy pastel colors and retro Windows 95/98 styling! ˚‧꒰ა 𓂋 ໒꒱ ‧˚"""
        
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
            
            messagebox.showinfo("Success", f"₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ Settings saved successfully! ˚‧꒰ა 𓂋 ໒꒱ ‧˚\n\nNew request delay: {delay} seconds")
            self.main_app.update_status(f"₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ Settings updated - Request delay: {delay}s")
            
        except ValueError:
            messagebox.showerror("Error", "(>_<) Please enter a valid delay value (1-10 seconds)! (T_T)")