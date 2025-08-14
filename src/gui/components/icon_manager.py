#!/usr/bin/env python3
"""Icon Manager for GUI - Handles loading and managing pixel icons"""

import os
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class IconManager:
    """Manages pixel icons for the GUI application"""
    
    def __init__(self):
        self.icons = {}
        self.pixel_icons = []
        self.icon_refs = []
        
    def load_icons(self):
        """Load all pixel icons"""
        if not PIL_AVAILABLE:
            print("PIL not available, skipping icon loading")
            return
            
        # Icon mapping for different functions - Using add_ icons more actively
        icon_mapping = {
            'analyze_advanced': 'bow.png',
            'analyze_quick':    'add_1.png',     # Changed to add_1 for sparkle-like effect
            'save':             'add_2.png',     # Changed to add_2 for save functionality
            'refresh':          'add_3.png',     # Changed to add_3 for refresh functionality
            'get_all':          'folder.png',
            'get_one':          'add_4.png',     # Changed to add_4 for single item retrieval
            'export':           'add_5.png',     # New export functionality with add_5
            'tab_data':         'sparkle.png',   # Swapped with analyze_quick
            'tab_recommend':    'heart.png',     # Changed to heart for recommendations
            'tab_analysis':     'glasses.png',   # Changed to glasses for analysis
            'tab_settings':     'skull.png',     # Changed to skull for settings
            'decoration':       'mail.png'       # Changed decoration to mail
        }
        
        icons_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'pixel_icons')
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
                        # Store reference
                        if not hasattr(self, 'icon_refs'):
                            self.icon_refs = []
                        self.icon_refs.append(photo)
                    except Exception as e:
                        print(f"Failed to load decoration icon {filename}: {e}")
        
        print(f"Loaded {len(self.icons)} functional icons and {len(self.pixel_icons)} decoration icons")
        
    def get_icon(self, key):
        """Get icon by key"""
        return self.icons.get(key)
        
    def get_decoration_icon(self, index):
        """Get decoration icon by index"""
        if 0 <= index < len(self.pixel_icons):
            return self.pixel_icons[index]
        return None
        
    def has_icon(self, key):
        """Check if icon exists"""
        return key in self.icons