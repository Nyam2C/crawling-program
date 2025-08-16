#!/usr/bin/env python3
"""
Test script to verify all the fixes are working correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    
    try:
        from src.gui.components.dialogs import show_info, show_error, show_success
        print("✅ Styled dialogs import successful")
    except ImportError as e:
        print(f"❌ Styled dialogs import failed: {e}")
    
    try:
        from src.gui.components.ui_core.keyboard_manager import KeyboardManager
        print("✅ Keyboard manager import successful")
    except ImportError as e:
        print(f"❌ Keyboard manager import failed: {e}")
    
    try:
        from src.gui.components.tabs.settings_tab import SettingsTab
        print("✅ Settings tab import successful")
    except ImportError as e:
        print(f"❌ Settings tab import failed: {e}")

def test_no_korean_text():
    """Test that Korean text has been removed"""
    print("\nChecking for Korean text and emojis...")
    
    import re
    korean_pattern = re.compile(r'[가-힣]')
    emoji_pattern = re.compile(r'[😊🎮⭐✨💫🌟🎨💎🦄🌸🎀💖✧✿♡🔥💰📈📊🤖🚀💡⚡🎯📋✅❌⚠️💻📱🎵🌈🎪🎭🎨🖥️📺🎬🎤🎧🎮🕹️🎲🃏🎯🎨🎪🎭🎬🎤🎧🎸🎹🥁🎺🎻📻📱📞📟📠💻🖥️⌨️🖱️💾💿📀💽💾💿📀🖲️💳💰💸💵💴💶💷💳💎⚖️🔧🔨⚒️🛠️⛏️🔩⚙️🧰🔫🏹🛡️🔪⚔️💣🧨🔮📿💈⚗️🔬🔭📡💉💊🩹🩺🚪🪑🛏️🛋️🚿🛁🚽🧻🧽🧴🧷🧹🧺🔥🧯🛒🚬⚰️⚱️🗿]')
    
    # Check key files
    files_to_check = [
        'src/gui/components/ui_core/keyboard_manager.py',
        'src/gui/components/tabs/settings_tab.py',
        'src/gui/gui_app.py'
    ]
    
    korean_found = False
    emoji_found = False
    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if korean_pattern.search(content):
                    print(f"❌ Korean text found in {file_path}")
                    korean_found = True
                else:
                    print(f"✅ No Korean text in {file_path}")
                
                if emoji_pattern.search(content):
                    print(f"❌ Emojis found in {file_path}")
                    emoji_found = True
                else:
                    print(f"✅ No problematic emojis in {file_path}")
        except FileNotFoundError:
            print(f"⚠️ File not found: {file_path}")
    
    if not korean_found and not emoji_found:
        print("✅ All Korean text and emojis successfully removed")

def test_education_removal():
    """Test that education module has been removed"""
    print("\nChecking education module removal...")
    
    if not os.path.exists('src/education'):
        print("✅ Education module successfully removed")
    else:
        print("❌ Education module still exists")

def test_styled_dialogs():
    """Test that styled dialogs are properly implemented"""
    print("\nChecking styled dialogs...")
    
    try:
        from src.gui.components.dialogs import show_scrollable_info, show_error, show_success
        print("✅ Styled dialogs import successful")
        
        # Check if the scrollable dialog exists
        if os.path.exists('src/gui/components/dialogs/styled_dialogs.py'):
            print("✅ Styled dialogs file exists")
        else:
            print("❌ Styled dialogs file missing")
            
    except ImportError as e:
        print(f"❌ Styled dialogs import failed: {e}")

def main():
    """Run all tests"""
    print("Running fix verification tests...\n")
    
    test_imports()
    test_no_korean_text()
    test_education_removal()
    test_styled_dialogs()
    
    print("\nAll verification tests completed!")

if __name__ == "__main__":
    main()