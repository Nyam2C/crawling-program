"""
YFinance-based data source for reliable stock data retrieval
"""

import yfinance as yf
from typing import Dict, Optional, List, Tuple
import logging
from datetime import datetime

class YFinanceDataSource:
    """YFinance-based stock data source - reliable and fast"""
    
    def __init__(self, delay=0.1):  # Much faster than web scraping
        self.delay = delay
        self._cache = {}
        
    def get_stock_data(self, symbol: str) -> Dict:
        """
        Get comprehensive stock data for a symbol
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            dict: Stock data or error info
        """
        if not symbol:
            return {'error': 'Empty symbol provided', 'symbol': symbol, 'valid': False}
            
        symbol = symbol.upper().strip()
        
        try:
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Get basic info
            info = ticker.info
            
            # Validate if ticker exists
            if not info or info.get('regularMarketPrice') is None:
                return {
                    'error': f'Symbol "{symbol}" not found or has no market data',
                    'symbol': symbol,
                    'valid': False
                }
            
            # Get current price data
            hist = ticker.history(period='1d', interval='1m')
            if hist.empty:
                # Fallback to daily data
                hist = ticker.history(period='5d')
                
            current_price = info.get('regularMarketPrice', 0)
            if current_price == 0 and not hist.empty:
                current_price = hist['Close'].iloc[-1]
                
            # Calculate change
            previous_close = info.get('regularMarketPreviousClose', current_price)
            change = current_price - previous_close
            change_percent = (change / previous_close * 100) if previous_close != 0 else 0
            
            # Format data to match existing interface
            stock_data = {
                'symbol': symbol,
                'company': info.get('longName', info.get('shortName', f'{symbol} Inc.')),
                'current_price': f"${current_price:.2f}" if current_price else 'N/A',
                'change': f"{change:+.2f}" if change else 'N/A',
                'change_percent': f"({change_percent:+.2f}%)" if change_percent else 'N/A',
                'market_cap': self._format_market_cap(info.get('marketCap', 0)),
                'volume': self._format_volume(info.get('regularMarketVolume', 0)),
                'high': info.get('regularMarketDayHigh', 0),
                'low': info.get('regularMarketDayLow', 0),
                'pe_ratio': info.get('forwardPE', info.get('trailingPE', 'N/A')),
                'dividend_yield': info.get('dividendYield', 0),
                'valid': True,
                'source': 'yfinance',
                'timestamp': datetime.now().isoformat()
            }
            
            return stock_data
            
        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {str(e)}")
            return {
                'error': f'Failed to fetch data for {symbol}: {str(e)}',
                'symbol': symbol,
                'valid': False
            }
    
    def validate_symbol(self, symbol: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate if a stock symbol exists
        
        Args:
            symbol: Stock symbol to validate
            
        Returns:
            tuple: (is_valid, company_name, error_message)
        """
        if not symbol:
            return False, None, "Empty symbol"
        
        symbol = symbol.upper().strip()
        
        # Basic format validation
        if not symbol.replace('.', '').replace('-', '').isalnum() or len(symbol) > 10:
            return False, None, f"Invalid symbol format: '{symbol}'"
        
        # Check cache first
        if symbol in self._cache:
            cached = self._cache[symbol]
            return cached['valid'], cached.get('company'), cached.get('error')
        
        try:
            # Quick validation using yfinance
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Check if symbol has market data
            if not info or info.get('regularMarketPrice') is None:
                error_msg = f"Symbol '{symbol}' not found or has no market data"
                self._cache[symbol] = {'valid': False, 'company': None, 'error': error_msg}
                return False, None, error_msg
            
            # Extract company name
            company_name = info.get('longName', info.get('shortName', f'{symbol} Inc.'))
            
            self._cache[symbol] = {'valid': True, 'company': company_name, 'error': None}
            return True, company_name, None
            
        except Exception as e:
            error_msg = f"Error validating '{symbol}': {str(e)}"
            self._cache[symbol] = {'valid': False, 'company': None, 'error': error_msg}
            return False, None, error_msg
    
    def get_multiple_stocks_data(self, symbols: List[str]) -> Dict[str, Dict]:
        """
        Get data for multiple stocks efficiently
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            dict: Symbol -> stock data mapping
        """
        results = {}
        
        # Use yfinance's download method for efficiency
        try:
            valid_symbols = [s.upper().strip() for s in symbols if s.strip()]
            
            for symbol in valid_symbols:
                print(f"Fetching {symbol}...")
                stock_data = self.get_stock_data(symbol)
                results[symbol] = stock_data
                
                # Small delay to be respectful
                if self.delay > 0:
                    import time
                    time.sleep(self.delay)
            
        except Exception as e:
            logging.error(f"Error in bulk fetch: {str(e)}")
            
        return results
    
    def get_stock_suggestions(self, partial_symbol: str, limit: int = 5) -> List[str]:
        """
        Get stock symbol suggestions - simplified for yfinance
        
        Args:
            partial_symbol: Partial symbol input
            limit: Maximum suggestions to return
            
        Returns:
            list: List of suggested symbols
        """
        if not partial_symbol:
            return []
        
        partial = partial_symbol.upper()
        suggestions = []
        
        # Get suggestions from predefined categories (as before)
        from src.core.config import STOCK_CATEGORIES
        
        for category in STOCK_CATEGORIES.values():
            for symbol, company in category['stocks'].items():
                if symbol.startswith(partial) or partial in symbol:
                    suggestions.append(symbol)
                if len(suggestions) >= limit:
                    break
            if len(suggestions) >= limit:
                break
        
        return suggestions[:limit]
    
    def _format_market_cap(self, market_cap: float) -> str:
        """Format market cap for display"""
        if not market_cap or market_cap <= 0:
            return 'N/A'
            
        if market_cap >= 1e12:
            return f"${market_cap/1e12:.2f}T"
        elif market_cap >= 1e9:
            return f"${market_cap/1e9:.2f}B"
        elif market_cap >= 1e6:
            return f"${market_cap/1e6:.2f}M"
        else:
            return f"${market_cap:.0f}"
    
    def _format_volume(self, volume: int) -> str:
        """Format volume for display"""
        if not volume or volume <= 0:
            return 'N/A'
            
        if volume >= 1e9:
            return f"{volume/1e9:.2f}B"
        elif volume >= 1e6:
            return f"{volume/1e6:.2f}M"
        elif volume >= 1e3:
            return f"{volume/1e3:.2f}K"
        else:
            return f"{volume:,}"
    
    def clear_cache(self):
        """Clear the validation cache"""
        self._cache.clear()
    
    def close(self):
        """Clean up resources - not needed for yfinance"""
        pass