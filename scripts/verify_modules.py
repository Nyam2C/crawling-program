#!/usr/bin/env python3
"""
Quick verification script to test modular structure
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported without errors"""
    try:
        print("Testing imports...")
        
        from src.core.config import MAGNIFICENT_SEVEN, DEFAULT_DELAY
        print(f"✓ Config imported: {len(MAGNIFICENT_SEVEN)} stocks defined")
        
        from src.core.http_client import HTTPClient
        print("✓ HTTPClient imported")
        
        from src.data.data_extractors import HTMLExtractor, YahooFinanceExtractor
        print("✓ Data extractors imported")
        
        from src.data.stock_crawler import StockCrawler
        print("✓ StockCrawler imported")
        
        from scripts.cli import StockAnalysisCLI
        print("✓ CLI imported")
        
        print("\nAll modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without external requests"""
    try:
        print("\nTesting basic functionality...")
        
        from src.data.stock_crawler import StockCrawler
        from src.core.config import MAGNIFICENT_SEVEN
        
        # Create crawler instance
        crawler = StockCrawler(delay=1)
        print("✓ StockCrawler instantiated")
        
        # Test configuration access
        if 'AAPL' in MAGNIFICENT_SEVEN:
            print("✓ Configuration accessible")
        
        # Clean up
        crawler.close()
        print("✓ Crawler closed properly")
        
        print("Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("Modular Structure Verification")
    print("=" * 40)
    
    import_success = test_imports()
    functionality_success = test_basic_functionality()
    
    print("\n" + "=" * 40)
    if import_success and functionality_success:
        print("✓ ALL TESTS PASSED - Modular structure is working!")
    else:
        print("✗ Some tests failed - Check module structure")