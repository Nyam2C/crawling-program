"""
Main stock crawler implementation
"""

import logging
from src.core.http_client import HTTPClient
from src.data.data_extractors import HTMLExtractor, YahooFinanceExtractor
from src.core.config import MAGNIFICENT_SEVEN, YAHOO_FINANCE_BASE_URL, DEFAULT_DELAY


class StockCrawler:
    """Stock information crawler for the Magnificent Seven"""
    
    def __init__(self, delay=DEFAULT_DELAY):
        self.http_client = HTTPClient(delay)
        self.html_extractor = HTMLExtractor()
        self.yahoo_extractor = YahooFinanceExtractor()
        
    def get_stock_data(self, symbol):
        """
        Get stock data for a specific symbol
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL')
            
        Returns:
            dict or None: Stock data or None if failed
        """
        if symbol not in MAGNIFICENT_SEVEN:
            logging.warning(f"Symbol {symbol} not in Magnificent Seven")
            return None
            
        url = f"{YAHOO_FINANCE_BASE_URL}{symbol}"
        response = self.http_client.get(url)
        
        if not response:
            return None
            
        company_name = MAGNIFICENT_SEVEN[symbol]
        return self.yahoo_extractor.extract_stock_data(
            response.text, symbol, company_name, url
        )
    
    def get_all_stocks_data(self):
        """
        Get stock data for all Magnificent Seven stocks
        
        Returns:
            dict: Dictionary with symbol as key and stock data as value
        """
        all_stocks = {}
        
        for symbol in MAGNIFICENT_SEVEN.keys():
            print(f"Crawling {symbol}...")
            stock_data = self.get_stock_data(symbol)
            
            if stock_data:
                all_stocks[symbol] = stock_data
            else:
                print(f"Failed to get data for {symbol}")
                
        return all_stocks
    
    def crawl_general_url(self, url):
        """
        General web crawling functionality
        
        Args:
            url (str): URL to crawl
            
        Returns:
            dict or None: Extracted data or None if failed
        """
        response = self.http_client.get(url)
        
        if not response:
            return None
            
        data = {
            'url': url,
            'status_code': response.status_code,
            'title': self.html_extractor.extract_title(response.text),
            'text': self.html_extractor.extract_text(response.text),
            'links': self.html_extractor.extract_links(response.text, url)
        }
        
        return data
    
    def close(self):
        """Clean up resources"""
        self.http_client.close()