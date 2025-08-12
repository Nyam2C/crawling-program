"""
Configuration settings for the Magnificent Seven Stock Crawler
"""

MAGNIFICENT_SEVEN = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation', 
    'GOOGL': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.',
    'NVDA': 'NVIDIA Corporation',
    'TSLA': 'Tesla Inc.',
    'META': 'Meta Platforms Inc.'
}

DEFAULT_DELAY = 2

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

YAHOO_FINANCE_BASE_URL = "https://finance.yahoo.com/quote/"