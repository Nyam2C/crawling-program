#!/usr/bin/env python3

from stock_crawler import StockCrawler
import json

def test_single_stock():
    crawler = StockCrawler(delay=2)
    
    print("Testing Apple (AAPL) stock data extraction...")
    result = crawler.get_stock_data('AAPL')
    
    if result:
        print("Success! Retrieved data:")
        print(json.dumps(result, indent=2))
    else:
        print("Failed to retrieve stock data")
    
    crawler.close()

def test_all_stocks():
    crawler = StockCrawler(delay=2)
    
    print("Testing all Magnificent Seven stocks...")
    results = crawler.get_all_stocks_data()
    
    print(f"Retrieved data for {len(results)} stocks:")
    print(json.dumps(results, indent=2))
    
    crawler.close()

def test_general_crawling():
    crawler = StockCrawler(delay=1)
    
    print("Testing general web crawling...")
    test_url = "https://httpbin.org/html"
    result = crawler.crawl_general_url(test_url)
    
    if result:
        print("Success! General crawling works:")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"Status: {result.get('status_code', 'N/A')}")
        print(f"Links found: {len(result.get('links', []))}")
    else:
        print("Failed to perform general crawling")
    
    crawler.close()

if __name__ == "__main__":
    print("Stock Crawler Modular Test")
    print("=" * 40)
    test_single_stock()
    print("\n" + "=" * 40)
    test_all_stocks()
    print("\n" + "=" * 40)
    test_general_crawling()