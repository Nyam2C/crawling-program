#!/usr/bin/env python3
"""Theme Manager for Retro Pastel GUI - Manages colors and styles"""

import tkinter as tk
from tkinter import ttk


class ThemeManager:
    """Manages theme colors and styles for the GUI application"""
    
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.setup_colors()
        
    def setup_colors(self):
        """Setup color palette"""
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
        
    def apply_styles(self):
        """Apply all theme styles"""
        # Font (try Korean font first, fallback to Arial)
        try:
            default_font = ('맑은 고딕', 9)
        except:
            default_font = ('Arial', 9)
        self.style.configure('.', font=default_font, foreground=self.colors['text'])
        
        # Common background styles (no white/gray)
        self.style.configure('TFrame', background=self.colors['panel'])
        self.style.configure('TLabel', background=self.colors['panel'], foreground=self.colors['text'])
        self.style.configure('TLabelFrame', background=self.colors['panel'], foreground=self.colors['lavender'])
        self.style.configure('TLabelFrame.Label', background=self.colors['panel'], foreground=self.colors['lavender'])
        
        # Entry and text widget styles
        self.style.configure('TEntry',
            background=self.colors['panel_light'], foreground=self.colors['text'],
            bordercolor=self.colors['border'], insertcolor=self.colors['periwinkle'])
        
        # Combobox style (retro dropdown)
        self.style.configure('Pastel.TCombobox',
            background=self.colors['panel_light'], foreground=self.colors['text'],
            bordercolor=self.colors['border'], arrowcolor=self.colors['periwinkle'])
        self.style.map('Pastel.TCombobox',
            fieldbackground=[('readonly', self.colors['panel_light'])])
        
        # Accent label styles
        self.style.configure('Accent.TLabel', background=self.colors['panel'], foreground=self.colors['magenta'])
        self.style.configure('Highlight.TLabel', background=self.colors['panel'], foreground=self.colors['hotpink'])
        
        self._apply_button_styles()
        self._apply_notebook_styles()
        self._apply_treeview_styles()
        self._apply_progress_styles()
        self._apply_scrollbar_styles()
        
    def _apply_button_styles(self):
        """Apply button styles"""
        # Button styles (Primary / Secondary / Ghost)
        self.style.configure('Pastel.Primary.TButton',
            background=self.colors['periwinkle'], foreground='#1B1350',
            bordercolor=self.colors['border'], borderwidth=2, relief='ridge',
            padding=[10,6], anchor='w')
        self.style.map('Pastel.Primary.TButton',
            background=[('active', self.colors['lavender']), ('pressed', self.colors['pink'])])

        self.style.configure('Pastel.Secondary.TButton',
            background=self.colors['rose'], foreground='#1B1350',
            bordercolor=self.colors['highlight'], borderwidth=2, relief='ridge',
            padding=[10,6], anchor='w')
        self.style.map('Pastel.Secondary.TButton',
            background=[('active', self.colors['hotpink']), ('pressed', self.colors['magenta'])])

        self.style.configure('Pastel.Ghost.TButton',
            background=self.colors['panel_light'], foreground=self.colors['text'],
            bordercolor=self.colors['border_light'], borderwidth=2, relief='ridge',
            padding=[10,6], anchor='w')
        
        # Legacy button style mappings for backward compatibility
        self.style.configure('Kuromi.Primary.TButton',
            background=self.colors['periwinkle'], foreground='#1B1350',
            bordercolor=self.colors['border'], borderwidth=2, relief='ridge',
            padding=[10,6], anchor='w')
        self.style.map('Kuromi.Primary.TButton',
            background=[('active', self.colors['lavender']), ('pressed', self.colors['pink'])])
        
        self.style.configure('Kuromi.Black.TButton',
            background=self.colors['panel_alt'], foreground=self.colors['text'],
            bordercolor=self.colors['border'], borderwidth=2, relief='ridge',
            padding=[10,6], anchor='w')
        
    def _apply_notebook_styles(self):
        """Apply notebook and tab styles"""
        # Notebook tabs (retro window style)
        self.style.configure('TNotebook', background=self.colors['panel'], borderwidth=0)
        self.style.configure('TNotebook.Tab',
            background=self.colors['panel_alt'], foreground=self.colors['text'],
            bordercolor=self.colors['border'], borderwidth=1, padding=[10,5])
        self.style.map('TNotebook.Tab',
            background=[('selected', self.colors['lavender']), ('active', self.colors['periwinkle'])],
            foreground=[('selected', '#1B1350')])
        
    def _apply_treeview_styles(self):
        """Apply treeview styles"""
        # Treeview (data table) style
        self.style.configure('Pastel.Treeview',
            background=self.colors['panel_light'], foreground=self.colors['text'],
            fieldbackground=self.colors['panel_light'], bordercolor=self.colors['border'])
        self.style.configure('Pastel.Treeview.Heading',
            background=self.colors['periwinkle'], foreground='#1B1350',
            bordercolor=self.colors['border'], relief='ridge')
        self.style.map('Pastel.Treeview.Heading',
            background=[('active', self.colors['lavender'])])
        self.style.map('Pastel.Treeview',
            background=[('selected', self.colors['lavender'])],
            foreground=[('selected', '#1B1350')])
        
    def _apply_progress_styles(self):
        """Apply progress bar styles"""
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
        
    def _apply_scrollbar_styles(self):
        """Apply scrollbar styles"""
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