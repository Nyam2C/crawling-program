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
            print("PIL not available, loading icons with tkinter PhotoImage")
            self._load_icons_without_pil()
            return

        # Get project root directory (more reliable)
        current_file = os.path.abspath(__file__)
        # Navigate up from src/gui/components/ui_core/icon_manager.py to project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file)))))
        icons_path = os.path.join(project_root, 'assets', 'pixel_icons')
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
            'tab_individual':   'glasses.png',  # Individual Analysis tab
            'tab_analysis':     'rainbow.png',  # Investment Analysis tab
            'tab_trading':      'folder.png',   # Mock trading tab
            'tab_scoreboard':   'bow.png',      # Scoreboard tab
            'tab_settings':     'skull.png',
            # Trading specific icons
            'search':           'glasses.png',
            'trade':            'heart.png',
            'remove':           'skull.png',
            'reset':            'bow.png',
            'help':             'glasses.png',  # Help guide icon
            'rainbow':          'rainbow.png',  # Rainbow button icon
            # Additional icon aliases
            'glasses':          'glasses.png',  # Direct glasses icon
            'heart':            'heart.png',    # Direct heart icon
            # Level icons
            'level_1':          'level_1.png',
            'level_2':          'level_2.png',
            'level_3':          'level_3.png',
            'level_4':          'level_4.png',
            'level_5':          'level_5.png',
        }
        for key, filename in button_map.items():
            icon_path = os.path.join(icons_path, filename)
            if os.path.exists(icon_path):
                try:
                    img = Image.open(icon_path).resize((24, 24), Image.Resampling.NEAREST)
                    self.icons[key] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"❌ Button icon load fail {filename}: {e}")
        
        # 2) Decoration icons (add_* files only)
        for fname in os.listdir(icons_path):
            if fname.startswith('add_') and fname.endswith('.png'):
                icon_path = os.path.join(icons_path, fname)
                try:
                    img = Image.open(icon_path).resize((64, 64), Image.Resampling.NEAREST)
                    ph = ImageTk.PhotoImage(img)
                    self.pixel_icons.append(ph)
                    self.icon_refs.append(ph)
                except Exception as e:
                    print(f"Decor load fail {fname}: {e}")

        # Icons loaded successfully (silent loading)
        
    def get_icon(self, key):
        """Get icon by key"""
        return self.icons.get(key)
        
    def get_decoration_icon(self, index):
        """Get decoration icon by index"""
        if 0 <= index < len(self.pixel_icons):
            return self.pixel_icons[index]
        return None
        
    def _load_icons_without_pil(self):
        """Load icons using tkinter PhotoImage when PIL is not available"""
        try:
            import tkinter as tk
        except ImportError:
            print("❌ tkinter not available")
            return

        # Get project root directory (same logic as main load_icons)
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file)))))
        icons_path = os.path.join(project_root, 'assets', 'pixel_icons')
        
        if not os.path.exists(icons_path):
            print(f"❌ Icons path not found: {icons_path}")
            return

        # 1) Button/tab icons (named files only) - same mapping as PIL version
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
            'tab_individual':   'glasses.png',
            'tab_analysis':     'rainbow.png',
            'tab_trading':      'folder.png',
            'tab_scoreboard':   'bow.png',
            'tab_settings':     'skull.png',
            'search':           'glasses.png',
            'trade':            'heart.png',
            'remove':           'skull.png',
            'reset':            'bow.png',
            'help':             'glasses.png',
            'rainbow':          'rainbow.png',
            'glasses':          'glasses.png',
            'heart':            'heart.png',
            'level_1':          'level_1.png',
            'level_2':          'level_2.png',
            'level_3':          'level_3.png',
            'level_4':          'level_4.png',
            'level_5':          'level_5.png',
        }
        
        for key, filename in button_map.items():
            icon_path = os.path.join(icons_path, filename)
            if os.path.exists(icon_path):
                try:
                    # Load with tkinter PhotoImage (supports PNG)
                    photo_image = tk.PhotoImage(file=icon_path)
                    # Note: tkinter PhotoImage doesn't have subsample method for resizing like PIL
                    # We'll keep original size for compatibility
                    self.icons[key] = photo_image
                    print(f"✓ Loaded icon: {key} -> {filename}")
                except Exception as e:
                    print(f"❌ Failed to load icon {filename}: {e}")
        
        # 2) Decoration icons (add_* files only)
        try:
            for fname in os.listdir(icons_path):
                if fname.startswith('add_') and fname.endswith('.png'):
                    icon_path = os.path.join(icons_path, fname)
                    try:
                        photo_image = tk.PhotoImage(file=icon_path)
                        self.pixel_icons.append(photo_image)
                        self.icon_refs.append(photo_image)
                        print(f"✓ Loaded decoration icon: {fname}")
                    except Exception as e:
                        print(f"❌ Failed to load decoration icon {fname}: {e}")
        except Exception as e:
            print(f"❌ Error listing decoration icons: {e}")

        print(f"📦 Loaded {len(self.icons)} button icons and {len(self.pixel_icons)} decoration icons without PIL")

    def has_icon(self, key):
        """Check if icon exists"""
        return key in self.icons