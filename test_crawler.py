#!/usr/bin/env python3

from crawler import StockCrawler
import json

def test_single_stock():
    crawler = StockCrawler(delay=2)
    
    print("Testing Apple (AAPL) stock data extraction...")
    result = crawler.extract_stock_data_yahoo('AAPL')
    
    if result:
        print("Success! Retrieved data:")
        print(json.dumps(result, indent=2))
    else:
        print("Failed to retrieve stock data")

def test_all_stocks():
    crawler = StockCrawler(delay=2)
    
    print("Testing all Magnificent Seven stocks...")
    results = crawler.crawl_all_magnificent_seven()
    
    print(f"Retrieved data for {len(results)} stocks:")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    print("Stock Crawler Test")
    print("=" * 30)
    test_single_stock()
    print("\n" + "=" * 30)
    test_all_stocks()