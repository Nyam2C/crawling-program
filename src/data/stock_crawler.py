"""
Main stock crawler implementation
"""

import logging
from typing import List
from src.core.config import MAGNIFICENT_SEVEN, YAHOO_FINANCE_BASE_URL, DEFAULT_DELAY, STOCK_CATEGORIES

# Try to import yfinance, fallback to old method if not available
try:
    from src.data.yfinance_data_source import YFinanceDataSource
    YFINANCE_AVAILABLE = True
except ImportError:
    print("yfinance not available. Install with: pip install yfinance")
    # Fallback imports
    from src.core.http_client import HTTPClient
    from src.data.data_extractors import HTMLExtractor, YahooFinanceExtractor
    from src.utils.stock_validator import StockValidator
    YFINANCE_AVAILABLE = False


class StockCrawler:
    """Universal stock information crawler for any stock symbol"""
    
    def __init__(self, delay=DEFAULT_DELAY):
        self.delay = delay
        
        if YFINANCE_AVAILABLE:
            # Use yfinance data source (preferred)
            self.data_source = YFinanceDataSource(delay)
            self.use_yfinance = True
            print("Using YFinance data source (⊃｡•́‿•̀｡)⊃━☆ﾟ.*・｡ﾟ")
        else:
            # Fallback to old web scraping method
            self.http_client = HTTPClient(delay)
            self.html_extractor = HTMLExtractor()
            self.yahoo_extractor = YahooFinanceExtractor()
            self.validator = StockValidator()
            self.use_yfinance = False
            print("Using web scraping fallback method (,,>﹏<,,)")
            print("Note: For better data quality, install yfinance: pip install yfinance")
        
    def get_stock_data(self, symbol):
        """
        Get stock data for any stock symbol
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'MSFT', etc.)
            
        Returns:
            dict: Stock data or error info
        """
        if not symbol:
            logging.error("Empty symbol provided")
            return {
                'error': 'Empty symbol provided',
                'symbol': '',
                'valid': False
            }
            
        symbol = symbol.upper().strip()
        
        if self.use_yfinance:
            # Use yfinance data source
            return self.data_source.get_stock_data(symbol)
        else:
            # Use legacy web scraping method
            return self._get_stock_data_legacy(symbol)
    
    def _get_stock_data_legacy(self, symbol):
        """Legacy web scraping method with simplified validation"""
        # Skip external validation due to blocking, use basic format check only
        if not self._is_valid_symbol_format(symbol):
            return {
                'error': f'Invalid symbol format: {symbol}',
                'symbol': symbol,
                'valid': False
            }
            
        url = f"{YAHOO_FINANCE_BASE_URL}{symbol}"
        response = self.http_client.get(url)
        
        if not response:
            return {
                'error': f'Failed to fetch data for {symbol} - network error',
                'symbol': symbol,
                'valid': False
            }
            
        # Use fallback company name
        company_name = self._get_company_name_fallback(symbol)
        
        # Try to extract data, but provide fallback if extraction fails
        try:
            extracted_data = self.yahoo_extractor.extract_stock_data(
                response.text, symbol, company_name, url
            )
            
            # If extraction failed or returned minimal data, provide basic fallback
            if not extracted_data or extracted_data.get('current_price') == 'N/A':
                return self._create_fallback_stock_data(symbol, company_name)
            
            return extracted_data
            
        except Exception as e:
            logging.error(f"Data extraction failed for {symbol}: {str(e)}")
            return self._create_fallback_stock_data(symbol, company_name)
    
    def _create_fallback_stock_data(self, symbol: str, company_name: str) -> dict:
        """Create basic fallback stock data when extraction fails"""
        return {
            'symbol': symbol,
            'company': company_name,
            'current_price': 'Data unavailable',
            'change': 'N/A',
            'change_percent': 'N/A', 
            'market_cap': 'N/A',
            'volume': 'N/A',
            'high': 'N/A',
            'low': 'N/A',
            'valid': True,  # Symbol format is valid, just no data
            'source': 'fallback',
            'note': 'Limited data - install yfinance for full data'
        }
    
    def _is_valid_symbol_format(self, symbol: str) -> bool:
        """Basic symbol format validation"""
        if not symbol or len(symbol) < 1 or len(symbol) > 5:
            return False
        # Allow letters and dots for symbols like BRK.A
        return symbol.replace('.', '').replace('-', '').isalpha()
    
    def get_multiple_stocks_data(self, symbols: List[str]):
        """
        Get stock data for multiple symbols (portfolio/watchlist)
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            dict: Dictionary with symbol as key and stock data as value
        """
        if self.use_yfinance:
            # Use yfinance bulk method (more efficient)
            return self.data_source.get_multiple_stocks_data(symbols)
        else:
            # Use legacy method
            all_stocks = {}
            
            for symbol in symbols:
                if symbol:
                    print(f"Crawling {symbol}...")
                    stock_data = self.get_stock_data(symbol)
                    
                    if stock_data and 'error' not in stock_data:
                        all_stocks[symbol] = stock_data
                    else:
                        print(f"Failed to get data for {symbol}")
                        if stock_data:
                            all_stocks[symbol] = stock_data  # Include error info
                    
            return all_stocks
    
    def get_category_stocks_data(self, category_key: str):
        """
        Get stock data for a predefined category
        
        Args:
            category_key: Key from STOCK_CATEGORIES
            
        Returns:
            dict: Dictionary with symbol as key and stock data as value
        """
        if category_key not in STOCK_CATEGORIES:
            return {'error': f'Category {category_key} not found'}
            
        category = STOCK_CATEGORIES[category_key]
        symbols = list(category['stocks'].keys())
        
        print(f"Analyzing {category['name']} category...")
        return self.get_multiple_stocks_data(symbols)
    
    def get_all_stocks_data(self):
        """
        Legacy method: Get stock data for Magnificent Seven (for backward compatibility)
        
        Returns:
            dict: Dictionary with symbol as key and stock data as value
        """
        return self.get_category_stocks_data('magnificent_seven')
    
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
    
    def _get_company_name_fallback(self, symbol: str) -> str:
        """
        Get company name fallback when validator doesn't provide one
        
        Args:
            symbol: Stock symbol
            
        Returns:
            str: Company name or symbol with Inc.
        """
        # Check if it's in our predefined categories
        for category in STOCK_CATEGORIES.values():
            if symbol in category['stocks']:
                return category['stocks'][symbol]
        
        # Fallback to symbol + Inc.
        return f"{symbol} Inc."
    
    def get_stock_suggestions(self, partial_symbol: str, limit: int = 5) -> List[str]:
        """
        Get stock symbol suggestions based on partial input
        
        Args:
            partial_symbol: Partial symbol input
            limit: Maximum suggestions to return
            
        Returns:
            list: List of suggested symbols
        """
        if self.use_yfinance:
            return self.data_source.get_stock_suggestions(partial_symbol, limit)
        else:
            return self.validator.get_suggestions(partial_symbol, limit)
    
    def validate_symbol(self, symbol: str):
        """
        Validate a stock symbol
        
        Args:
            symbol: Symbol to validate
            
        Returns:
            tuple: (is_valid, company_name, error_message)
        """
        if self.use_yfinance:
            return self.data_source.validate_symbol(symbol)
        else:
            # Use simplified validation for web scraping
            if not symbol:
                return False, None, "Empty symbol"
            
            symbol = symbol.upper().strip()
            if self._is_valid_symbol_format(symbol):
                company_name = self._get_company_name_fallback(symbol)
                return True, company_name, None
            else:
                return False, None, f"Invalid symbol format: {symbol}"
    
    def close(self):
        """Clean up resources"""
        if self.use_yfinance:
            self.data_source.close()
        else:
            self.http_client.close()
            if hasattr(self.validator, 'session'):
                self.validator.session.close()