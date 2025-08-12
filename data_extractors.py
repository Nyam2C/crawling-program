"""
Data extraction utilities for HTML parsing and content extraction
"""

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from datetime import datetime


class HTMLExtractor:
    """General HTML content extraction"""
    
    @staticmethod
    def extract_text(html_content):
        """Extract clean text from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(strip=True)
    
    @staticmethod
    def extract_links(html_content, base_url):
        """Extract all links from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            links.append(full_url)
        return links
    
    @staticmethod
    def extract_title(html_content):
        """Extract page title from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.get_text(strip=True) if title_tag else ''


class YahooFinanceExtractor:
    """Specialized extractor for Yahoo Finance stock data"""
    
    @staticmethod
    def extract_stock_data(html_content, symbol, company_name, url):
        """
        Extract stock data from Yahoo Finance HTML with multiple fallback strategies
        
        Args:
            html_content (str): Raw HTML content
            symbol (str): Stock symbol
            company_name (str): Company name
            url (str): Source URL
            
        Returns:
            dict: Extracted stock data
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        stock_data = {
            'symbol': symbol,
            'company': company_name,
            'timestamp': datetime.now().isoformat(),
            'source': 'Yahoo Finance',
            'url': url,
            'current_price': 'N/A',
            'change': 'N/A',
            'change_percent': 'N/A',
            'market_cap': 'N/A',
            'volume': 'N/A'
        }
        
        try:
            # Strategy 1: fin-streamer elements (current Yahoo Finance)
            price_element = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
            if price_element:
                price_value = price_element.get('value') or price_element.get_text(strip=True)
                if price_value and price_value != 'N/A':
                    stock_data['current_price'] = price_value
            
            change_element = soup.find('fin-streamer', {'data-field': 'regularMarketChange'})
            if change_element:
                change_value = change_element.get('value') or change_element.get_text(strip=True)
                if change_value and change_value != 'N/A':
                    stock_data['change'] = change_value
                    
            change_percent_element = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
            if change_percent_element:
                change_percent_value = change_percent_element.get('value') or change_percent_element.get_text(strip=True)
                if change_percent_value and change_percent_value != 'N/A':
                    stock_data['change_percent'] = change_percent_value
            
            volume_element = soup.find('fin-streamer', {'data-field': 'regularMarketVolume'})
            if volume_element:
                volume_value = volume_element.get('value') or volume_element.get_text(strip=True)
                if volume_value and volume_value != 'N/A':
                    stock_data['volume'] = volume_value
            
            # Strategy 2: Market cap from table
            market_cap_element = soup.find('td', {'data-test': 'MARKET_CAP-value'})
            if market_cap_element:
                market_cap_value = market_cap_element.get_text(strip=True)
                if market_cap_value and market_cap_value not in ['N/A', '--']:
                    stock_data['market_cap'] = market_cap_value
            
            # Strategy 3: Alternative selectors for older Yahoo Finance format
            if stock_data['current_price'] == 'N/A':
                # Try alternative price selectors
                price_selectors = [
                    'span[data-reactid*="50"]',
                    '.Trsdu(0.3s) .Fw(b) .Fz(36px)',
                    '[data-field="regularMarketPrice"]',
                    '.Fw(b).Fz(36px).Mb(-4px).D(ib)'
                ]
                
                for selector in price_selectors:
                    try:
                        element = soup.select_one(selector)
                        if element:
                            price_text = element.get_text(strip=True)
                            if price_text and price_text not in ['N/A', '--', '']:
                                stock_data['current_price'] = price_text
                                break
                    except:
                        continue
            
            # Strategy 4: Regex extraction from script tags as last resort
            if stock_data['current_price'] == 'N/A':
                import re
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.string:
                        # Look for regularMarketPrice in JSON data
                        price_match = re.search(r'"regularMarketPrice"[:\s]*{[^}]*"raw"[:\s]*([0-9.]+)', script.string)
                        if price_match:
                            stock_data['current_price'] = price_match.group(1)
                            break
                        
                        # Look for formatted price
                        price_match = re.search(r'"regularMarketPrice"[:\s]*{[^}]*"fmt"[:\s]*"([^"]+)"', script.string)
                        if price_match:
                            stock_data['current_price'] = price_match.group(1)
                            break
            
            # Generate mock data if no real data found (for demo purposes)
            if all(value == 'N/A' for value in [stock_data['current_price'], stock_data['change'], stock_data['change_percent']]):
                stock_data.update(YahooFinanceExtractor._generate_mock_data(symbol))
                stock_data['source'] = 'Mock Data (Demo)'
                
        except Exception as e:
            logging.error(f"Error extracting stock data for {symbol}: {e}")
            # Generate mock data as fallback
            stock_data.update(YahooFinanceExtractor._generate_mock_data(symbol))
            stock_data['source'] = 'Mock Data (Error Fallback)'
            
        return stock_data
    
    @staticmethod
    def _generate_mock_data(symbol):
        """Generate mock stock data for demo purposes"""
        import random
        
        # Base prices for realistic mock data
        base_prices = {
            'AAPL': 185.0,
            'MSFT': 378.0,
            'GOOGL': 138.0,
            'AMZN': 145.0,
            'NVDA': 485.0,
            'TSLA': 248.0,
            'META': 325.0
        }
        
        base_price = base_prices.get(symbol, 100.0)
        
        # Add some random variation
        current_price = round(base_price * random.uniform(0.95, 1.05), 2)
        change = round(random.uniform(-5.0, 5.0), 2)
        change_percent = round((change / current_price) * 100, 2)
        
        # Market caps (in trillions/billions)
        market_caps = {
            'AAPL': '2.89T',
            'MSFT': '2.78T', 
            'GOOGL': '1.65T',
            'AMZN': '1.48T',
            'NVDA': '1.85T',
            'TSLA': '785B',
            'META': '823B'
        }
        
        volumes = {
            'AAPL': str(random.randint(40000000, 80000000)),
            'MSFT': str(random.randint(25000000, 50000000)),
            'GOOGL': str(random.randint(20000000, 40000000)),
            'AMZN': str(random.randint(30000000, 60000000)),
            'NVDA': str(random.randint(35000000, 70000000)),
            'TSLA': str(random.randint(50000000, 100000000)),
            'META': str(random.randint(25000000, 55000000))
        }
        
        return {
            'current_price': str(current_price),
            'change': f"{'+' if change >= 0 else ''}{change}",
            'change_percent': f"{'+' if change_percent >= 0 else ''}{change_percent:.2f}%",
            'market_cap': market_caps.get(symbol, '500B'),
            'volume': volumes.get(symbol, '45000000')
        }