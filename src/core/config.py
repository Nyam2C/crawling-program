"""
Configuration settings for Universal Stock Analysis System
"""

# Legacy support - Magnificent Seven as a preset category
MAGNIFICENT_SEVEN = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation', 
    'GOOGL': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.',
    'NVDA': 'NVIDIA Corporation',
    'TSLA': 'Tesla Inc.',
    'META': 'Meta Platforms Inc.'
}

# Popular stock categories for quick access
STOCK_CATEGORIES = {
    'magnificent_seven': {
        'name': 'Magnificent Seven',
        'stocks': MAGNIFICENT_SEVEN
    },
    'dow_leaders': {
        'name': 'Dow Jones Leaders',
        'stocks': {
            'UNH': 'UnitedHealth Group',
            'GS': 'Goldman Sachs',
            'HD': 'Home Depot',
            'CAT': 'Caterpillar',
            'MCD': 'McDonald\'s',
            'V': 'Visa',
            'BA': 'Boeing',
            'JPM': 'JPMorgan Chase'
        }
    },
    'tech_giants': {
        'name': 'Tech Giants',
        'stocks': {
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation',
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.',
            'META': 'Meta Platforms Inc.',
            'NFLX': 'Netflix Inc.',
            'CRM': 'Salesforce Inc.',
            'ORCL': 'Oracle Corporation'
        }
    },
    'banking': {
        'name': 'Banking Sector',
        'stocks': {
            'JPM': 'JPMorgan Chase',
            'BAC': 'Bank of America',
            'WFC': 'Wells Fargo',
            'GS': 'Goldman Sachs',
            'MS': 'Morgan Stanley',
            'C': 'Citigroup'
        }
    }
}

DEFAULT_DELAY = 2

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

YAHOO_FINANCE_BASE_URL = "https://finance.yahoo.com/quote/"

# Stock symbol validation patterns
VALID_SYMBOL_PATTERN = r'^[A-Z]{1,5}$'