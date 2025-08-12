# Magnificent Seven Stock Crawler

A Python-based web crawler specifically designed to extract real-time stock information for the "Magnificent Seven" - the top seven U.S. technology stocks.

## The Magnificent Seven Stocks

This crawler targets the following stocks:
- **AAPL** - Apple Inc.
- **MSFT** - Microsoft Corporation
- **GOOGL** - Alphabet Inc. (Google)
- **AMZN** - Amazon.com Inc.
- **NVDA** - NVIDIA Corporation
- **TSLA** - Tesla Inc.
- **META** - Meta Platforms Inc. (Facebook)

## Features

- **Real-time stock data extraction** from Yahoo Finance
- **Multiple operation modes**:
  - Crawl all Magnificent Seven stocks at once
  - Crawl individual stocks
  - General web crawling functionality
- **Comprehensive data extraction**:
  - Current stock price
  - Price change and percentage change
  - Market capitalization
  - Trading volume
  - Company information
  - Timestamp of data retrieval
- **Rate limiting** to respect website resources
- **Error handling** and logging
- **JSON output** for easy data processing

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Nyam2C/crawling-program.git
cd crawling-program
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run the main crawler script:
```bash
python crawler.py
```

Choose from three options:
1. **Crawl all Magnificent Seven stocks** - Gets data for all 7 stocks
2. **Crawl specific stock** - Enter a stock symbol (AAPL, MSFT, etc.)
3. **General web crawling** - Use as a regular web crawler

### Programmatic Usage

```python
from crawler import StockCrawler

# Initialize crawler
crawler = StockCrawler(delay=2)

# Get data for a single stock
stock_data = crawler.extract_stock_data_yahoo('AAPL')
print(stock_data)

# Get data for all Magnificent Seven stocks
all_stocks = crawler.crawl_all_magnificent_seven()
print(all_stocks)
```

### Testing

Run the test script to verify functionality:
```bash
python test_crawler.py
```

## Sample Output

```json
{
  "AAPL": {
    "symbol": "AAPL",
    "company": "Apple Inc.",
    "timestamp": "2024-01-15T10:30:00",
    "source": "Yahoo Finance",
    "url": "https://finance.yahoo.com/quote/AAPL",
    "current_price": "185.64",
    "change": "+2.18",
    "change_percent": "+1.19%",
    "market_cap": "2.89T",
    "volume": "45,678,901"
  }
}
```

## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- lxml

## Rate Limiting

The crawler includes a 2-second delay between requests by default to be respectful to the target websites. You can adjust this in the `StockCrawler` initialization.

## Legal Notice

This tool is for educational and research purposes only. Please:
- Respect the terms of service of the websites you crawl
- Use appropriate delays between requests
- Consider the website's robots.txt file
- Use the data responsibly and in compliance with applicable laws

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please use responsibly.

## Disclaimer

Stock prices and financial data are provided for informational purposes only. This tool does not provide investment advice. Always verify financial information from official sources before making investment decisions.