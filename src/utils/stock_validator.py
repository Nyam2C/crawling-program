"""
Stock symbol validation utilities
"""

import re
import requests
from typing import Tuple, Optional
from src.core.config import VALID_SYMBOL_PATTERN, YAHOO_FINANCE_BASE_URL, USER_AGENT

class StockValidator:
    """Validates stock symbols and checks if they exist on Yahoo Finance"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        self._cache = {}  # Cache for validated symbols
    
    def is_valid_format(self, symbol: str) -> bool:
        """
        Check if symbol has valid format (1-5 uppercase letters)
        
        Args:
            symbol: Stock symbol to validate
            
        Returns:
            bool: True if format is valid
        """
        if not symbol:
            return False
        return bool(re.match(VALID_SYMBOL_PATTERN, symbol.upper()))
    
    def validate_symbol(self, symbol: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate stock symbol by checking Yahoo Finance
        
        Args:
            symbol: Stock symbol to validate
            
        Returns:
            tuple: (is_valid, company_name, error_message)
        """
        if not symbol:
            return False, None, "Empty symbol"
        
        symbol = symbol.upper().strip()
        
        # Check format first
        if not self.is_valid_format(symbol):
            return False, None, f"Invalid symbol format: '{symbol}'. Use 1-5 uppercase letters."
        
        # Check cache first
        if symbol in self._cache:
            cached_result = self._cache[symbol]
            return cached_result['valid'], cached_result['company'], cached_result.get('error')
        
        try:
            # Test if symbol exists by fetching its page
            url = f"{YAHOO_FINANCE_BASE_URL}{symbol}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                # Check if it's a valid stock page (not 404 or redirect to search)
                if 'Quote Lookup' in response.text or 'Symbol Lookup' in response.text:
                    error_msg = f"Symbol '{symbol}' not found on Yahoo Finance"
                    self._cache[symbol] = {'valid': False, 'company': None, 'error': error_msg}
                    return False, None, error_msg
                
                # Try to extract company name from the page
                company_name = self._extract_company_name(response.text, symbol)
                
                self._cache[symbol] = {'valid': True, 'company': company_name, 'error': None}
                return True, company_name, None
            else:
                error_msg = f"Symbol '{symbol}' not found (HTTP {response.status_code})"
                self._cache[symbol] = {'valid': False, 'company': None, 'error': error_msg}
                return False, None, error_msg
                
        except requests.RequestException as e:
            error_msg = f"Network error validating '{symbol}': {str(e)}"
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Error validating '{symbol}': {str(e)}"
            return False, None, error_msg
    
    def _extract_company_name(self, html_content: str, symbol: str) -> str:
        """
        Extract company name from Yahoo Finance HTML
        
        Args:
            html_content: HTML content from Yahoo Finance
            symbol: Stock symbol
            
        Returns:
            str: Company name or symbol if extraction fails
        """
        try:
            # Try to find company name in common HTML patterns
            import re
            
            # Pattern 1: Look for title tag
            title_match = re.search(r'<title[^>]*>([^<]*)</title>', html_content, re.IGNORECASE)
            if title_match:
                title = title_match.group(1)
                # Extract company name from title like "Apple Inc. (AAPL) Stock Price..."
                if '(' in title and symbol in title:
                    company_name = title.split('(')[0].strip()
                    if company_name and company_name != symbol:
                        return company_name
            
            # Pattern 2: Look for h1 tags
            h1_matches = re.findall(r'<h1[^>]*>([^<]*)</h1>', html_content, re.IGNORECASE)
            for h1_text in h1_matches:
                if symbol in h1_text and '(' in h1_text:
                    company_name = h1_text.split('(')[0].strip()
                    if company_name and company_name != symbol:
                        return company_name
            
            # If extraction fails, return symbol
            return f"{symbol} Inc."
            
        except Exception:
            return f"{symbol} Inc."
    
    def get_suggestions(self, partial_symbol: str, limit: int = 5) -> list:
        """
        Get symbol suggestions based on partial input
        This is a simple implementation - could be enhanced with a real API
        
        Args:
            partial_symbol: Partial symbol input
            limit: Maximum number of suggestions
            
        Returns:
            list: List of suggested symbols
        """
        if not partial_symbol:
            return []
        
        partial = partial_symbol.upper()
        suggestions = []
        
        # Get suggestions from our predefined categories
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
    
    def clear_cache(self):
        """Clear the validation cache"""
        self._cache.clear()