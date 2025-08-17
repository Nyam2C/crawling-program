#!/usr/bin/env python3
"""
GUI Components Package - All GUI components for the main interface
Organized into logical groups: tabs, dialogs, ui_core, and trading
"""

# Import from organized subpackages
from .tabs import StockDataTab, IndividualAnalysisTab, RecommendationsTab, ScoreboardTab, SettingsTab, InvestmentAnalysisTab, NewsSentimentTab
from .dialogs import KawaiiMessageBox, KawaiiInputDialog, TradingHelpDialog
from .ui_core import ThemeManager, IconManager, UIBuilder, KeyboardManager, ActionManager
from .trading import MockTradingTab

__all__ = [
    # Tab components
    'StockDataTab',
    'IndividualAnalysisTab', 
    'RecommendationsTab',
    'ScoreboardTab',
    'SettingsTab',
    'InvestmentAnalysisTab',
    'NewsSentimentTab',
    
    # Dialog components
    'KawaiiMessageBox',
    'KawaiiInputDialog',
    'TradingHelpDialog',
    
    # UI Core components
    'ThemeManager',
    'IconManager',
    'UIBuilder',
    'KeyboardManager',
    'ActionManager',
    
    # Trading components
    'MockTradingTab'
]