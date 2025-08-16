#!/usr/bin/env python3
"""Test script to verify the reorganized GUI components imports work correctly"""

try:
    # Test main package import
    from src.gui.components import (
        StockDataTab, RecommendationsTab, IndividualAnalysisTab, SettingsTab,
        MockTradingTab, ThemeManager, IconManager, UIBuilder,
        KawaiiMessageBox, KawaiiInputDialog, TradingHelpDialog
    )
    
    # Test subpackage imports
    from src.gui.components.tabs import StockDataTab as StockDataTab2
    from src.gui.components.dialogs import KawaiiMessageBox as KawaiiMessageBox2
    from src.gui.components.ui_core import ThemeManager as ThemeManager2
    from src.gui.components.trading import MockTradingTab as MockTradingTab2
    
    print("✅ All imports successful!")
    print("✅ Main package imports: OK")
    print("✅ Subpackage imports: OK")
    print("✅ GUI components restructure completed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)