"""
Command line interface for the Stock Crawler
"""

import json
from stock_crawler import StockCrawler
from config import MAGNIFICENT_SEVEN


class StockCrawlerCLI:
    """Command line interface for stock crawler"""
    
    def __init__(self):
        self.crawler = StockCrawler()
        
    def show_menu(self):
        """Display the main menu"""
        print("Stock Information Crawler for the Magnificent Seven")
        print("=" * 50)
        print("Choose option:")
        print("1. Crawl all Magnificent Seven stocks")
        print("2. Crawl specific stock")
        print("3. General web crawling")
        
    def get_user_choice(self):
        """Get user menu choice"""
        return input("Enter choice (1-3): ").strip()
        
    def crawl_all_stocks(self):
        """Handle crawling all stocks"""
        print("\nCrawling all Magnificent Seven stocks...")
        results = self.crawler.get_all_stocks_data()
        print(json.dumps(results, indent=2))
        
    def crawl_specific_stock(self):
        """Handle crawling a specific stock"""
        print(f"\nAvailable stocks: {', '.join(MAGNIFICENT_SEVEN.keys())}")
        symbol = input("Enter stock symbol: ").upper().strip()
        
        if symbol in MAGNIFICENT_SEVEN:
            result = self.crawler.get_stock_data(symbol)
            if result:
                print(json.dumps(result, indent=2))
            else:
                print(f"Failed to get data for {symbol}")
        else:
            print("Invalid symbol. Please choose from the Magnificent Seven.")
            
    def crawl_general_url(self):
        """Handle general web crawling"""
        url = input("Enter URL to crawl: ").strip()
        result = self.crawler.crawl_general_url(url)
        
        if result:
            print(json.dumps(result, indent=2))
        else:
            print("Failed to crawl the URL")
            
    def run(self):
        """Run the CLI application"""
        try:
            self.show_menu()
            choice = self.get_user_choice()
            
            if choice == "1":
                self.crawl_all_stocks()
            elif choice == "2":
                self.crawl_specific_stock()
            elif choice == "3":
                self.crawl_general_url()
            else:
                print("Invalid choice.")
                
        finally:
            self.crawler.close()