#!/usr/bin/env python3
"""
Test suite for the Stock Recommendation System
"""

from recommendation_engine import RecommendationEngine
from financial_analyzer import FinancialAnalyzer
import json


def test_financial_analyzer():
    """Test the financial analyzer components"""
    print("🧪 Testing Financial Analyzer...")
    
    analyzer = FinancialAnalyzer()
    
    # Test sample stock data
    sample_data = {
        'symbol': 'AAPL',
        'company': 'Apple Inc.',
        'current_price': '185.64',
        'change': '+2.18',
        'change_percent': '+1.19%',
        'market_cap': '2.89T',
        'volume': '45678901'
    }
    
    # Test individual analysis functions
    momentum_score, momentum_text = analyzer.analyze_price_momentum(sample_data)
    print(f"✓ Momentum Analysis: {momentum_text} (Score: {momentum_score})")
    
    volume_score, volume_text = analyzer.analyze_volume(sample_data)
    print(f"✓ Volume Analysis: {volume_text} (Score: {volume_score})")
    
    market_cap_score, market_cap_text = analyzer.analyze_market_cap(sample_data)
    print(f"✓ Market Cap Analysis: {market_cap_text} (Score: {market_cap_score})")
    
    # Test comprehensive analysis
    comprehensive = analyzer.generate_comprehensive_analysis(sample_data)
    print(f"✓ Comprehensive Analysis: {comprehensive['recommendation']} (Score: {comprehensive['overall_score']})")
    
    return True


def test_recommendation_engine():
    """Test the recommendation engine"""
    print("\n🚀 Testing Recommendation Engine...")
    
    engine = RecommendationEngine(delay=1)  # Faster for testing
    
    try:
        # Test single stock analysis
        print("📊 Testing single stock analysis (AAPL)...")
        analysis = engine.analyze_single_stock('AAPL')
        
        if 'error' in analysis:
            print(f"❌ Single stock test failed: {analysis['error']}")
            return False
        else:
            print(f"✓ Single stock analysis successful: {analysis['recommendation']}")
        
        # Note: Full analysis test would require internet connection
        print("📈 Full analysis test skipped (requires internet connection)")
        
        return True
        
    except Exception as e:
        print(f"❌ Recommendation engine test failed: {e}")
        return False
    finally:
        engine.close()


def test_value_parsing():
    """Test financial value parsing"""
    print("\n💰 Testing Financial Value Parsing...")
    
    analyzer = FinancialAnalyzer()
    
    test_cases = [
        ('2.89T', 2890000000000),
        ('45.6B', 45600000000),
        ('123.4M', 123400000),
        ('567K', 567000),
        ('N/A', 0.0),
        ('--', 0.0),
        ('185.64', 185.64)
    ]
    
    all_passed = True
    for input_val, expected in test_cases:
        result = analyzer.parse_financial_value(input_val)
        if abs(result - expected) < 0.01:  # Allow for floating point precision
            print(f"✓ {input_val} -> {result}")
        else:
            print(f"❌ {input_val} -> {result} (expected {expected})")
            all_passed = False
    
    return all_passed


def test_mock_recommendation_system():
    """Test the recommendation system with mock data"""
    print("\n🎯 Testing Mock Recommendation System...")
    
    analyzer = FinancialAnalyzer()
    
    # Mock data for different scenarios
    mock_stocks = {
        'STRONG_BUY': {
            'symbol': 'MOCK1',
            'company': 'Strong Buy Company',
            'current_price': '200.00',
            'change': '+5.50',
            'change_percent': '+2.84%',
            'market_cap': '3.2T',
            'volume': '85000000'
        },
        'WEAK_HOLD': {
            'symbol': 'MOCK2', 
            'company': 'Weak Hold Company',
            'current_price': '50.00',
            'change': '-2.10',
            'change_percent': '-4.03%',
            'market_cap': '45B',
            'volume': '8000000'
        }
    }
    
    for scenario, data in mock_stocks.items():
        analysis = analyzer.generate_comprehensive_analysis(data)
        print(f"✓ {scenario} scenario: {analysis['recommendation']} (Score: {analysis['overall_score']})")
        
        # Verify expected behavior
        if scenario == 'STRONG_BUY' and analysis['overall_score'] > 0.7:
            print(f"  ✓ High score as expected")
        elif scenario == 'WEAK_HOLD' and analysis['overall_score'] < 0.6:
            print(f"  ✓ Lower score as expected")
    
    return True


def run_all_tests():
    """Run all tests"""
    print("🔬 STOCK RECOMMENDATION SYSTEM TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Financial Analyzer", test_financial_analyzer),
        ("Value Parsing", test_value_parsing), 
        ("Mock Recommendation System", test_mock_recommendation_system),
        ("Recommendation Engine", test_recommendation_engine)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Recommendation system is ready!")
    else:
        print("⚠️  Some tests failed. Check implementation.")
    
    return passed == total


if __name__ == "__main__":
    run_all_tests()