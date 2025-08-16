#!/usr/bin/env python3
"""Test icon path resolution"""

import os
from src.gui.components.ui_core.icon_manager import IconManager

# Test current directory structure
icon_manager_path = "/workspace/claude/src/gui/components/ui_core/icon_manager.py"
print(f"Icon manager location: {icon_manager_path}")

# Calculate expected path
expected_path = os.path.join(os.path.dirname(icon_manager_path), '..', '..', '..', '..', 'assets', 'pixel_icons')
resolved_path = os.path.abspath(expected_path)
print(f"Expected assets path: {resolved_path}")
print(f"Assets path exists: {os.path.exists(resolved_path)}")

if os.path.exists(resolved_path):
    files = os.listdir(resolved_path)
    print(f"Icon files found: {files}")
    
# Test icon manager
try:
    icon_manager = IconManager()
    icon_manager.load_icons()
    print(f"Icons loaded: {list(icon_manager.icons.keys())}")
except Exception as e:
    print(f"Error loading icons: {e}")