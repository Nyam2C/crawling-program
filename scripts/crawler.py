import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin, urlparse
import logging
import re
from datetime import datetime

class StockCrawler:
    def __init__(self, delay=1):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        self.magnificent_seven = {
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation', 
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.',
            'NVDA': 'NVIDIA Corporation',
            'TSLA': 'Tesla Inc.',
            'META': 'Meta Platforms Inc.'
        }
        
    def crawl_url(self, url):
        try:
            time.sleep(self.delay)
            response = self.session.get(url)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Error crawling {url}: {e}")
            return None
    
    def extract_text(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(strip=True)
    
    def extract_links(self, html_content, base_url):
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            links.append(full_url)
        return links
    
    def extract_stock_data_yahoo(self, symbol):
        url = f"https://finance.yahoo.com/quote/{symbol}"
        response = self.crawl_url(url)
        if not response:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stock_data = {
            'symbol': symbol,
            'company': self.magnificent_seven.get(symbol, 'Unknown'),
            'timestamp': datetime.now().isoformat(),
            'source': 'Yahoo Finance',
            'url': url
        }
        
        try:
            price_element = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
            if price_element:
                stock_data['current_price'] = price_element.get('value', 'N/A')
            
            change_element = soup.find('fin-streamer', {'data-field': 'regularMarketChange'})
            if change_element:
                stock_data['change'] = change_element.get('value', 'N/A')
                
            change_percent_element = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
            if change_percent_element:
                stock_data['change_percent'] = change_percent_element.get('value', 'N/A')
            
            market_cap_element = soup.find('td', {'data-test': 'MARKET_CAP-value'})
            if market_cap_element:
                stock_data['market_cap'] = market_cap_element.get_text(strip=True)
                
            volume_element = soup.find('fin-streamer', {'data-field': 'regularMarketVolume'})
            if volume_element:
                stock_data['volume'] = volume_element.get('value', 'N/A')
                
        except Exception as e:
            logging.error(f"Error extracting stock data for {symbol}: {e}")
            
        return stock_data
    
    def crawl_all_magnificent_seven(self):
        all_stocks = {}
        for symbol in self.magnificent_seven.keys():
            print(f"Crawling {symbol}...")
            stock_data = self.extract_stock_data_yahoo(symbol)
            if stock_data:
                all_stocks[symbol] = stock_data
            else:
                print(f"Failed to get data for {symbol}")
                
        return all_stocks
    
    def crawl_and_extract(self, url):
        response = self.crawl_url(url)
        if response:
            data = {
                'url': url,
                'status_code': response.status_code,
                'title': '',
                'text': '',
                'links': []
            }
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title_tag = soup.find('title')
            if title_tag:
                data['title'] = title_tag.get_text(strip=True)
            
            data['text'] = self.extract_text(response.text)
            data['links'] = self.extract_links(response.text, url)
            
            return data
        return None

if __name__ == "__main__":
    crawler = StockCrawler(delay=2)
    
    print("Stock Information Crawler for the Magnificent Seven")
    print("=" * 50)
    
    choice = input("Choose option:\n1. Crawl all Magnificent Seven stocks\n2. Crawl specific stock\n3. General web crawling\nEnter choice (1-3): ")
    
    if choice == "1":
        print("\nCrawling all Magnificent Seven stocks...")
        results = crawler.crawl_all_magnificent_seven()
        print(json.dumps(results, indent=2))
        
    elif choice == "2":
        print("\nAvailable stocks:", ", ".join(crawler.magnificent_seven.keys()))
        symbol = input("Enter stock symbol: ").upper()
        if symbol in crawler.magnificent_seven:
            result = crawler.extract_stock_data_yahoo(symbol)
            if result:
                print(json.dumps(result, indent=2))
            else:
                print(f"Failed to get data for {symbol}")
        else:
            print("Invalid symbol. Please choose from the Magnificent Seven.")
            
    elif choice == "3":
        url = input("Enter URL to crawl: ")
        result = crawler.crawl_and_extract(url)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print("Failed to crawl the URL")
    
    else:
        print("Invalid choice.")