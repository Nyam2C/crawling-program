"""
Enhanced Data Source with Multi-Source Support
다중 데이터 소스를 지원하는 향상된 데이터 소스
"""

import yfinance as yf
from typing import Dict, Optional, List, Tuple
import logging
from datetime import datetime
from .multi_data_source import MultiDataSourceManager, DataSourceType

class YFinanceDataSource:
    """Enhanced stock data source with multi-source support"""
    
    def __init__(self, delay=0.1):
        self.delay = delay
        self._cache = {}
        self.multi_data_manager = MultiDataSourceManager()
        self.logger = logging.getLogger(__name__)
        
    def get_stock_data(self, symbol: str) -> Dict:
        """
        Get comprehensive stock data using multi-source approach
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            dict: Stock data or error info
        """
        if not symbol:
            return {'error': 'Empty symbol provided', 'symbol': symbol, 'valid': False}
            
        symbol = symbol.upper().strip()
        
        try:
            # Try multi-source data first
            multi_result = self.multi_data_manager.get_stock_data_sync(symbol)
            
            if multi_result:
                # Convert to legacy format for compatibility
                stock_data = {
                    'symbol': symbol,
                    'company': f"{symbol} Corp.",  # Will be enhanced with company data
                    'current_price': f"${multi_result.price:.2f}",
                    'change': f"{multi_result.change:+.2f}",
                    'change_percent': f"({multi_result.change_percent:+.2f}%)",
                    'market_cap': self._format_market_cap(multi_result.market_cap or 0),
                    'volume': self._format_volume(multi_result.volume),
                    'high': multi_result.fifty_two_week_high or 0,
                    'low': multi_result.fifty_two_week_low or 0,
                    'pe_ratio': multi_result.pe_ratio or 'N/A',
                    'dividend_yield': multi_result.dividend_yield or 0,
                    'valid': True,
                    'source': multi_result.data_source,
                    'timestamp': multi_result.timestamp.isoformat(),
                    'raw_data': multi_result  # Store raw data for advanced analysis
                }
                
                return stock_data
            
            # Fallback to original yfinance method
            return self._get_yfinance_data_legacy(symbol)
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return {
                'error': f'Failed to fetch data for {symbol}: {str(e)}',
                'symbol': symbol,
                'valid': False
            }
    
    def _get_yfinance_data_legacy(self, symbol: str) -> Dict:
        """Legacy yfinance data retrieval method"""
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
                'source': 'yfinance (fallback)',
                'timestamp': datetime.now().isoformat()
            }
            
            return stock_data
            
        except Exception as e:
            raise e
    
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
    
    def configure_data_source(self, source_type: str, api_key: str = None, enabled: bool = True):
        """
        Configure additional data sources
        
        Args:
            source_type: Type of data source (alpha_vantage, finnhub, twelve_data)
            api_key: API key for the service
            enabled: Whether to enable this source
        """
        try:
            if source_type == "alpha_vantage":
                self.multi_data_manager.configure_data_source(
                    DataSourceType.ALPHA_VANTAGE, api_key, enabled
                )
            elif source_type == "finnhub":
                self.multi_data_manager.configure_data_source(
                    DataSourceType.FINNHUB, api_key, enabled
                )
            elif source_type == "twelve_data":
                self.multi_data_manager.configure_data_source(
                    DataSourceType.TWELVE_DATA, api_key, enabled
                )
            else:
                raise ValueError(f"Unsupported data source type: {source_type}")
                
            self.logger.info(f"Configured {source_type} with enabled={enabled}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure {source_type}: {e}")
            return False
    
    def get_data_source_status(self) -> Dict:
        """Get status of all configured data sources"""
        return self.multi_data_manager.get_data_source_status()
    
    def test_data_sources(self, test_symbol: str = "AAPL") -> Dict[str, bool]:
        """Test all configured data sources"""
        return self.multi_data_manager.test_data_sources(test_symbol)
    
    def get_multiple_stocks_data_enhanced(self, symbols: List[str]) -> Dict[str, Dict]:
        """
        Enhanced bulk data retrieval using multi-source approach
        """
        results = {}
        
        try:
            # Try to get data for all symbols using multi-source
            for symbol in symbols:
                print(f"Fetching {symbol}...")
                stock_data = self.get_stock_data(symbol)
                results[symbol] = stock_data
                
                # Respect rate limiting
                if self.delay > 0:
                    import time
                    time.sleep(self.delay)
                    
        except Exception as e:
            self.logger.error(f"Error in enhanced bulk fetch: {str(e)}")
            
        return results
    
    def close(self):
        """Clean up resources"""
        try:
            # Close multi-data manager if needed
            if hasattr(self.multi_data_manager, 'close'):
                self.multi_data_manager.close()
        except Exception as e:
            self.logger.error(f"Error closing resources: {e}")