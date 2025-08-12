"""
HTTP client for web requests with rate limiting and error handling
"""

import requests
import time
import logging
from .config import USER_AGENT


class HTTPClient:
    def __init__(self, delay=2):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT
        })
        
    def get(self, url):
        """
        Make a GET request with rate limiting and error handling
        
        Args:
            url (str): URL to request
            
        Returns:
            requests.Response or None: Response object or None if error
        """
        try:
            time.sleep(self.delay)
            response = self.session.get(url)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Error requesting {url}: {e}")
            return None
            
    def close(self):
        """Close the session"""
        self.session.close()