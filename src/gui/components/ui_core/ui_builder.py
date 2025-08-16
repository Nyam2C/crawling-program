#!/usr/bin/env python3
"""UI Builder - Creates common UI elements and layouts"""

import tkinter as tk
from tkinter import ttk
import random


class UIBuilder:
    """Builds common UI elements for the GUI application"""
    
    def __init__(self, main_app, icon_manager, theme_manager):
        self.main_app = main_app
        self.icon_manager = icon_manager
        self.theme_manager = theme_manager
        
    def create_icon_button(self, parent, key, text, command, style='Pastel.Primary.TButton', spacing=None):
        """Create button with pixel icon"""
        # Add minimal extra spacing if requested (reduced from 2 spaces to 1)
        display_text = f" {text}" if spacing else text
        btn = ttk.Button(parent, text=display_text, command=command, style=style)
        if self.icon_manager.has_icon(key):
            btn.configure(image=self.icon_manager.get_icon(key), compound='left')
        return btn
        
    def add_icon_to_tab(self, tab_frame, icon_key, text):
        """Add icon to tab text if available"""
        if self.icon_manager.has_icon(icon_key):
            # For tabs, we'll use text with icon reference
            return f"   {text}"  # Space for icon appearance
        return text
        
    def create_pixel_decoration(self, parent):
        """Create pixel decoration element"""
        try:
            if not self.icon_manager.pixel_icons:
                return None
                
            # Pick a random decoration icon
            icon = random.choice(self.icon_manager.pixel_icons)
            decoration_label = ttk.Label(parent, image=icon, 
                                       background=self.theme_manager.colors['panel'])
            
            # Keep reference to prevent garbage collection
            if not hasattr(self.main_app, 'decoration_refs'):
                self.main_app.decoration_refs = []
            self.main_app.decoration_refs.append(icon)
            
            return decoration_label
        except Exception as e:
            print(f"Decoration creation failed: {e}")
            return None
            
    def create_text_decoration(self, parent):
        """Create text-based decoration"""
        try:
            decorations = ["✧*:･ﾟ✧", "⋆｡‧˚ʚ♡ɞ˚‧｡⋆", "♡⃗*ೃ༄", "✧･ﾟ: *✧･ﾟ:*", 
                         "⋆୨୧˚", "˚₊‧꒰ა ♡ ໒꒱‧₊˚"]
            decoration_text = random.choice(decorations)
            decoration_label = ttk.Label(parent, text=decoration_text,
                                       font=('Arial', 12),
                                       foreground=self.theme_manager.colors['periwinkle'],
                                       background=self.theme_manager.colors['panel'])
            return decoration_label
        except Exception as e:
            print(f"Text decoration failed: {e}")
            return None
            
    def create_title_section(self, parent):
        """Create the title section with pixel decorations"""
        title_frame = ttk.Frame(parent)
        title_frame.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        title_frame.grid_columnconfigure(1, weight=1)
        
        # Left pixel decoration
        left_decoration = self.create_pixel_decoration(title_frame)
        if left_decoration:
            left_decoration.grid(row=0, column=0, rowspan=2, padx=(0, 15), pady=5)
        
        # Title and subtitle
        title_label = ttk.Label(title_frame, 
                              text="Kawaii StockEdu Platform",
                              font=('Arial', 18, 'bold'),
                              foreground=self.theme_manager.colors['lavender'])
        title_label.grid(row=0, column=1)
        
        # Pixel icon in title
        title_icon = self.icon_manager.get_decoration_icon(0)
        if title_icon:
            icon_label = ttk.Label(title_frame, image=title_icon, 
                                 background=self.theme_manager.colors['panel'])
            icon_label.grid(row=1, column=1, pady=(5, 5))
        
        subtitle_label = ttk.Label(title_frame,
                                 text="Educational stock trading simulation platform!",
                                 font=('Arial', 12, 'italic'),
                                 foreground=self.theme_manager.colors['periwinkle'])
        subtitle_label.grid(row=2, column=1, pady=(5, 0))
        
        # Right pixel decoration
        right_decoration = self.create_pixel_decoration(title_frame)
        if right_decoration:
            right_decoration.grid(row=0, column=2, rowspan=2, padx=(15, 0), pady=5)
            
        return title_frame
        
    def create_status_bar(self, parent, status_var):
        """Create status bar with progress indicator"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(15, 0))
        status_frame.grid_columnconfigure(0, weight=1)
        
        status_label = ttk.Label(status_frame, textvariable=status_var, 
                               relief=tk.SUNKEN, anchor=tk.W,
                               background=self.theme_manager.colors['panel_light'], 
                               foreground=self.theme_manager.colors['text'])
        status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Progress bar
        progress = ttk.Progressbar(status_frame, mode='indeterminate', 
                                 style='Pastel.Horizontal.TProgressbar', length=150)
        progress.grid(row=0, column=1, padx=(10, 0))
        
        return status_frame, progress
        
    def create_legacy_icon_button(self, parent, text, command, icon_index=None):
        """Legacy method for backward compatibility - creates pixel icon button"""
        # Map old functionality to new pixel icon system
        icon = self.icon_manager.get_decoration_icon(icon_index) if icon_index is not None else None
        if icon:
            btn = ttk.Button(parent, text=text, command=command, 
                           style='Pastel.Primary.TButton', image=icon, compound='left')
            # Store reference to prevent garbage collection
            if not hasattr(self.main_app, 'icon_refs'):
                self.main_app.icon_refs = []
            self.main_app.icon_refs.append(icon)
            return btn
        else:
            # Fallback to regular button
            return ttk.Button(parent, text=text, command=command, style='Pastel.Primary.TButton')
            
    def place_background_stickers(self, parent, count=6):
        """Place add_* icons as background stickers across the screen"""
        # add_* loader fills pixel_icons 
        if not self.icon_manager.pixel_icons:
            return
        
        HINTS = [(0.10,0.05),(0.90,0.05),(0.10,0.25),(0.90,0.30),(0.10,0.85),(0.90,0.88)]
        for i in range(min(count, len(HINTS))):
            icon = random.choice(self.icon_manager.pixel_icons)
            lbl = ttk.Label(parent, image=icon,
                            background=self.theme_manager.colors['panel'])
            # Keep reference
            if not hasattr(self.main_app, 'decoration_refs'):
                self.main_app.decoration_refs = []
            self.main_app.decoration_refs.append(icon)
            # Place based on screen ratios
            x, y = HINTS[i]
            lbl.place(relx=x, rely=y, anchor='center')