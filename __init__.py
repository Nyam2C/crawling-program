"""
Magnificent Seven Stock Crawler

A modular web crawler specifically designed to extract real-time stock information 
for the "Magnificent Seven" - the top seven U.S. technology stocks.
"""

from .stock_crawler import StockCrawler
from .config import MAGNIFICENT_SEVEN

__version__ = "2.0.0"
__all__ = ["StockCrawler", "MAGNIFICENT_SEVEN"]