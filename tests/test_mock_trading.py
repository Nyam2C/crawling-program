#!/usr/bin/env python3
"""
Test script for mock trading functionality
모의투자 기능 테스트 스크립트
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.trading.trading_engine import TradingEngine
from src.trading.models import OrderRequest, TransactionType, OrderType


def test_trading_engine():
    """Test the trading engine functionality"""
    print("=== Mock Trading Engine Test ===\n")
    
    # Initialize trading engine
    engine = TradingEngine()
    print(f"Initial portfolio: {engine.get_portfolio_summary()}\n")
    
    # Add some test stock prices
    test_stocks = {
        'AAPL': 150.00,
        'GOOGL': 2500.00,
        'TSLA': 800.00,
        'MSFT': 300.00
    }
    
    for symbol, price in test_stocks.items():
        engine.update_stock_price(symbol, price, f"{symbol} Inc.")
        print(f"Added {symbol}: ${price:.2f}")
    
    print("\n=== Testing Buy Orders ===")
    
    # Test buy order
    buy_order = OrderRequest(
        symbol='AAPL',
        transaction_type=TransactionType.BUY,
        order_type=OrderType.MARKET,
        quantity=10
    )
    
    success, message, transaction = engine.execute_order(buy_order)
    print(f"Buy order result: {success}")
    print(f"Message: {message}")
    if transaction:
        print(f"Transaction: {transaction.symbol} {transaction.quantity} shares at ${transaction.price:.2f}")
        print(f"Commission: ₩{transaction.commission:.0f}, Tax: ₩{transaction.tax:.0f}")
    
    print(f"\nPortfolio after buy: {engine.get_portfolio_summary()}")
    print(f"Positions: {engine.get_positions_summary()}")
    
    print("\n=== Testing Limit Order ===")
    
    # Test limit buy order
    limit_order = OrderRequest(
        symbol='GOOGL',
        transaction_type=TransactionType.BUY,
        order_type=OrderType.LIMIT,
        quantity=2,
        price=2400.00
    )
    
    success, message, transaction = engine.execute_order(limit_order)
    print(f"Limit order result: {success}")
    print(f"Message: {message}")
    
    print(f"\nPortfolio after limit buy: {engine.get_portfolio_summary()}")
    
    print("\n=== Testing Sell Order ===")
    
    # Test sell order
    sell_order = OrderRequest(
        symbol='AAPL',
        transaction_type=TransactionType.SELL,
        order_type=OrderType.MARKET,
        quantity=5
    )
    
    success, message, transaction = engine.execute_order(sell_order)
    print(f"Sell order result: {success}")
    print(f"Message: {message}")
    if transaction:
        print(f"Transaction: {transaction.symbol} {transaction.quantity} shares at ${transaction.price:.2f}")
        print(f"Commission: ₩{transaction.commission:.0f}, Tax: ₩{transaction.tax:.0f}")
    
    print(f"\nFinal portfolio: {engine.get_portfolio_summary()}")
    print(f"Final positions: {engine.get_positions_summary()}")
    
    print("\n=== Transaction History ===")
    transactions = engine.get_recent_transactions()
    for i, trans in enumerate(transactions, 1):
        print(f"{i}. {trans.timestamp.strftime('%Y-%m-%d %H:%M')} - "
              f"{trans.transaction_type.value.upper()} {trans.quantity} {trans.symbol} "
              f"at ${trans.price:.2f} (Total: ₩{trans.total_amount:.0f})")
    
    print("\n=== Test Error Cases ===")
    
    # Test insufficient funds
    expensive_order = OrderRequest(
        symbol='GOOGL',
        transaction_type=TransactionType.BUY,
        order_type=OrderType.MARKET,
        quantity=1000  # This should exceed available funds
    )
    
    success, message, _ = engine.execute_order(expensive_order)
    print(f"Expensive order (should fail): {success} - {message}")
    
    # Test selling more than owned
    oversell_order = OrderRequest(
        symbol='AAPL',
        transaction_type=TransactionType.SELL,
        order_type=OrderType.MARKET,
        quantity=100  # More than we own
    )
    
    success, message, _ = engine.execute_order(oversell_order)
    print(f"Oversell order (should fail): {success} - {message}")
    
    print("\n=== Test Complete ===")


def test_data_manager():
    """Test the data manager functionality"""
    print("\n=== Data Manager Test ===\n")
    
    from src.trading.data_manager import TradingDataManager
    
    # Create data manager
    dm = TradingDataManager("test_trading_data.json")
    
    # Add some watched stocks
    dm.add_watched_stock('AAPL')
    dm.add_watched_stock('GOOGL')
    
    print(f"Watched stocks: {dm.get_watched_stocks()}")
    
    # Test stock search
    print("\nTesting stock search...")
    try:
        stock_info = dm.search_stock('AAPL')
        if stock_info:
            print(f"Found: {stock_info}")
        else:
            print("Stock not found")
    except Exception as e:
        print(f"Search error: {e}")
    
    # Test trading engine access
    engine = dm.get_trading_engine()
    summary = engine.get_portfolio_summary()
    print(f"\nPortfolio summary: {summary}")
    
    # Save and cleanup
    dm.save_data()
    dm.close()
    
    print("Data manager test complete")


if __name__ == "__main__":
    test_trading_engine()
    test_data_manager()