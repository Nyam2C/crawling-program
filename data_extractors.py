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
        Extract stock data from Yahoo Finance HTML
        
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
            'url': url
        }
        
        try:
            # Current price
            price_element = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
            if price_element:
                stock_data['current_price'] = price_element.get('value', 'N/A')
            
            # Price change
            change_element = soup.find('fin-streamer', {'data-field': 'regularMarketChange'})
            if change_element:
                stock_data['change'] = change_element.get('value', 'N/A')
                
            # Change percentage
            change_percent_element = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
            if change_percent_element:
                stock_data['change_percent'] = change_percent_element.get('value', 'N/A')
            
            # Market cap
            market_cap_element = soup.find('td', {'data-test': 'MARKET_CAP-value'})
            if market_cap_element:
                stock_data['market_cap'] = market_cap_element.get_text(strip=True)
                
            # Volume
            volume_element = soup.find('fin-streamer', {'data-field': 'regularMarketVolume'})
            if volume_element:
                stock_data['volume'] = volume_element.get('value', 'N/A')
                
        except Exception as e:
            logging.error(f"Error extracting stock data for {symbol}: {e}")
            
        return stock_data