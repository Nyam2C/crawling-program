#!/usr/bin/env python3
"""Test icon loading after path fix"""

import sys
import os

# Add project root to path
sys.path.insert(0, '/workspace/claude')

try:
    from src.gui.components.ui_core.icon_manager import IconManager
    
    print("🔍 Testing icon loading...")
    icon_manager = IconManager()
    icon_manager.load_icons()
    
    # Check what icons were loaded
    loaded_icons = list(icon_manager.icons.keys())
    print(f"📋 Loaded icons: {loaded_icons}")
    
    # Test specific tab icons
    tab_icons = ['tab_data', 'tab_recommend', 'tab_analysis', 'tab_trading', 'tab_settings']
    for icon_key in tab_icons:
        icon = icon_manager.get_icon(icon_key)
        status = "✅" if icon else "❌"
        print(f"{status} {icon_key}: {'Available' if icon else 'Missing'}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()