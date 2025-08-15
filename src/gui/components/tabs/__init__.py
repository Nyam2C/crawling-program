#!/usr/bin/env python3
"""
GUI Tabs Package - All tab components for the main interface
"""

from .stock_data_tab import StockDataTab
from .analysis_tab import IndividualAnalysisTab
from .recommendations_tab import RecommendationsTab
from .scoreboard_tab import ScoreboardTab
from .settings_tab import SettingsTab
from .investment_analysis_tab import InvestmentAnalysisTab

__all__ = [
    'StockDataTab',
    'IndividualAnalysisTab', 
    'RecommendationsTab',
    'ScoreboardTab',
    'SettingsTab',
    'InvestmentAnalysisTab'
]