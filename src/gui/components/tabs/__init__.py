#!/usr/bin/env python3
"""
GUI Tabs Package - All tab components for the main interface
"""

from .stock_data_tab import StockDataTab
from .analysis_tab import IndividualAnalysisTab
from .recommendations_tab import RecommendationsTab
from .settings_tab import SettingsTab

__all__ = [
    'StockDataTab',
    'IndividualAnalysisTab', 
    'RecommendationsTab',
    'SettingsTab'
]