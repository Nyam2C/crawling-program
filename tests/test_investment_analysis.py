#!/usr/bin/env python3
"""Test script for Investment Analysis integration"""

def test_imports():
    """Test that all required modules can be imported"""
    try:
        # Test core analysis imports
        from src.analysis.investment_personality_analyzer import InvestmentPersonalityAnalyzer, PersonalityMetrics
        from src.trading.scoreboard_manager import ScoreboardManager
        print("✓ Core analysis modules imported successfully")
        
        # Test GUI components
        from src.gui.components.tabs.investment_analysis_tab import InvestmentAnalysisTab
        print("✓ Investment Analysis Tab imported successfully")
        
        # Test GUI integration
        from src.gui.components import InvestmentAnalysisTab as ComponentsTab
        print("✓ Investment Analysis Tab accessible from components package")
        
        # Test main GUI integration
        from src.gui.gui_app import StockAnalysisGUI
        print("✓ Main GUI app imports successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_analyzer():
    """Test the investment personality analyzer"""
    try:
        from src.analysis.investment_personality_analyzer import InvestmentPersonalityAnalyzer
        from src.trading.scoreboard_models import ScoreRecord, ScoreboardResult
        from datetime import datetime
        
        analyzer = InvestmentPersonalityAnalyzer()
        
        # Create test data
        test_record = ScoreRecord(
            nickname="TestTrader",
            date=datetime.now(),
            initial_balance=100000.0,
            final_balance=110000.0,
            return_rate=10.0,
            holding_period_days=30,
            best_stock="NVDA",
            best_stock_return=25.0,
            total_trades=5,
            result_type=ScoreboardResult.MANUAL_SAVE
        )
        
        # Test analysis
        metrics = analyzer.analyze_personality([test_record])
        print(f"✓ Analysis completed: {metrics.risk_tolerance.value} investor")
        
        return True
        
    except Exception as e:
        print(f"✗ Analyzer test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Investment Analysis Integration...")
    print("=" * 50)
    
    import_success = test_imports()
    analyzer_success = test_analyzer()
    
    print("=" * 50)
    if import_success and analyzer_success:
        print("✓ All tests passed! Investment Analysis is ready to use.")
    else:
        print("✗ Some tests failed. Check the errors above.")