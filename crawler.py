import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin, urlparse
import logging

class WebCrawler:
    def __init__(self, delay=1):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
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
    crawler = WebCrawler(delay=1)
    url = input("Enter URL to crawl: ")
    result = crawler.crawl_and_extract(url)
    
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Failed to crawl the URL")