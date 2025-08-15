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

        icons_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'pixel_icons')
        if not os.path.exists(icons_path):
            return

        # 1) Button/tab icons (named files only)
        button_map = {
            'analyze_advanced': 'bow.png',
            'analyze_quick':    'sparkle.png',
            'save':             'mail.png',
            'refresh':          'glasses.png',
            'get_all':          'folder.png',
            'get_one':          'heart.png',
            'export':           'skull.png',
            'tab_data':         'sparkle.png',
            'tab_recommend':    'heart.png',
            'tab_analysis':     'glasses.png',
            'tab_trading':      'folder.png',  # Mock trading tab
            'tab_settings':     'skull.png',
            # Trading specific icons
            'search':           'glasses.png',
            'trade':            'heart.png',
            'remove':           'skull.png',
            'reset':            'bow.png',
            'help':             'glasses.png',  # Help guide icon
        }
        for key, filename in button_map.items():
            icon_path = os.path.join(icons_path, filename)
            if os.path.exists(icon_path):
                try:
                    img = Image.open(icon_path).resize((24, 24), Image.Resampling.NEAREST)
                    self.icons[key] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Button icon load fail {filename}: {e}")

        # 2) Decoration icons (add_* files only)
        for fname in os.listdir(icons_path):
            if fname.startswith('add_') and fname.endswith('.png'):
                icon_path = os.path.join(icons_path, fname)
                try:
                    img = Image.open(icon_path).resize((32, 32), Image.Resampling.NEAREST)
                    ph = ImageTk.PhotoImage(img)
                    self.pixel_icons.append(ph)
                    self.icon_refs.append(ph)
                except Exception as e:
                    print(f"Decor load fail {fname}: {e}")

        print(f"Loaded {len(self.icons)} button/tab icons and {len(self.pixel_icons)} decorations (⊃｡•́‿•̀｡)⊃━☆ﾟ.*・｡ﾟ")
        
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