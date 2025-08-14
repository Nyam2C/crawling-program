# Magnificent Seven Stock Analysis & Recommendation System - Retro Pastel Edition

Advanced stock analysis application with retro 90s Windows aesthetics and pastel purple/pink color scheme.

## The Magnificent Seven Stocks

This application analyzes the following technology stocks:
- **AAPL** - Apple Inc.
- **MSFT** - Microsoft Corporation
- **GOOGL** - Alphabet Inc. (Google)
- **AMZN** - Amazon.com Inc.
- **NVDA** - NVIDIA Corporation
- **TSLA** - Tesla Inc.
- **META** - Meta Platforms Inc. (Facebook)

## Features

### Data Collection
- **Real-time stock data extraction** from Yahoo Finance
- **Comprehensive financial metrics**:
  - Current stock price & changes
  - Price momentum analysis
  - Market capitalization
  - Trading volume analysis
  - Timestamp tracking

### AI-Powered Analysis
- **Smart recommendation engine** with weighted scoring
- **Multi-factor analysis**:
  - Price momentum (25% weight)
  - Volume trends (15% weight) 
  - Market cap stability (20% weight)
  - Volatility assessment (15% weight)
  - Value proposition (25% weight)
- **Recommendation levels**: Strong Buy, Buy, Hold, Weak Hold, Avoid

### Operation Modes
- **Stock Data Collection** (all or individual)
- **Buy Recommendations** with confidence scoring
- **Individual Stock Analysis** with detailed breakdowns
- **Comprehensive Investment Reports**
- **General web crawling** functionality

### GUI Features - Retro Pastel Edition
- **Retro Windows 95/98 Interface** with pastel purple/pink theme
- **Pixel-perfect icons** with 24x24px retro-style graphics
- **Component-Based Architecture** - Clean, modular code structure
- **Real-time Data Display** in sortable tables with retro styling
- **Interactive Charts** with matplotlib integration and pastel colors
- **Progress Indicators** with retro window styling
- **Export Functionality** for reports and analysis

#### Retro Pastel Design Features:
- **Color Palette**: Deep navy purple (#1F144A) background with lavender (#C4B5FD) and soft pink (#FBCFE8) accents
- **Retro Buttons**: Ridge-style borders with 3D effects reminiscent of Windows 95
- **Pixel Icons**: 24x24px icons with nearest-neighbor scaling for authentic pixel art feel
- **Clean Typography**: Simple, readable fonts without decorative elements
- **Professional Layout**: Tab-based interface with consistent spacing and alignment

### Technical Features
- **Rate limiting** to respect website resources
- **Error handling** and logging
- **JSON output** for easy data processing
- **Comprehensive test suite**
- **Professional GUI** with retro styling

## Installation

1. **Clone this repository:**
```bash
git clone https://github.com/your-username/claude.git
cd claude
```

2. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install tkinter (for GUI):**

tkinter is required for the GUI version. It's usually included with Python, but if you get a "No module named 'tkinter'" error:

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Linux (CentOS/Fedora):**
```bash
sudo dnf install python3-tkinter
```

**Windows/macOS:** tkinter should be included with Python.

See [INSTALL_TKINTER.md](INSTALL_TKINTER.md) for detailed installation instructions.

## Usage

### GUI Application (Recommended)

Launch the retro pastel interface:
```bash
python main.py
# OR
python scripts/run_gui.py
```

**GUI Features (Retro Pastel Edition):**
- **Stock Data Tab**: View real-time data with retro styling
- **Recommendations Tab**: Generate AI-powered recommendations with clean presentation
- **Individual Analysis Tab**: Deep-dive analysis with professional layout
- **Charts Tab**: Interactive visualizations with pastel color scheme
- **Settings Tab**: Configure application with retro interface

### Retro Pastel Experience Highlights:
- **Clean Interface**: Professional layout without decorative elements
- **Consistent Styling**: All components follow the same retro Windows aesthetic
- **Readable Typography**: Clear, professional fonts throughout
- **Pastel Color Scheme**: Soothing purple and pink tones with dark backgrounds
- **Component Architecture**: Clean, modular design with separate tab components

### Command Line Interface

For CLI usage (legacy support):
```bash
python scripts/cli.py
```

**Available Options:**
1. Get stock data (all Magnificent Seven)
2. Get stock data (specific stock)
3. Get buy recommendations (all stocks)
4. Analyze specific stock
5. General web crawling

## Project Structure

The project is organized into a clean, modular structure for better maintainability and scalability:

```
project/
├── main.py                        # Main entry point
├── requirements.txt               # Dependencies
├── README.md                     # Documentation
├── scripts/                      # Entry point scripts
│   ├── run_gui.py                # GUI launcher
│   ├── cli.py                    # Command line interface
│   ├── main.py                   # Legacy CLI entry point
│   └── verify_modules.py         # Dependency checker
├── src/                          # Source code
│   ├── analysis/                 # Financial analysis engines
│   │   ├── recommendation_engine.py    # AI recommendation system
│   │   ├── financial_analyzer.py       # Basic financial analysis
│   │   └── advanced_financial_analyzer.py # Advanced analysis
│   ├── data/                     # Data collection & processing
│   │   ├── stock_crawler.py     # Stock data collection
│   │   └── data_extractors.py    # HTML parsing and data extraction
│   ├── gui/                      # User interface components
│   │   ├── gui_app.py            # Main GUI application
│   │   ├── gui_charts.py         # Chart visualizations
│   │   └── components/           # Modular GUI components
│   │       ├── stock_data_tab.py     # Stock data display tab
│   │       ├── recommendations_tab.py # AI recommendations tab
│   │       ├── analysis_tab.py       # Individual stock analysis tab
│   │       └── settings_tab.py        # Application settings tab
│   └── core/                     # Core utilities
│       ├── http_client.py        # HTTP requests and session management
│       └── config.py             # Configuration and constants
├── assets/                       # Application assets
│   └── pixel_icons/             # 24x24px retro-style icons
└── tests/                        # Test suite
    ├── test_crawler.py           # Crawler functionality tests
    ├── test_recommendation_system.py # Recommendation system tests
    ├── test_fixes.py             # Bug fix verification tests
    └── test_tkinter.py           # GUI dependency tests
```

## Programmatic Usage

### Basic Stock Data Collection
```python
from src.data.stock_crawler import StockCrawler

# Initialize crawler
crawler = StockCrawler(delay=2)

# Get data for a single stock
stock_data = crawler.get_stock_data('AAPL')
print(stock_data)

# Get data for all Magnificent Seven stocks
all_stocks = crawler.get_all_stocks_data()
print(all_stocks)

# Clean up resources
crawler.close()
```

### AI-Powered Recommendations
```python
from src.analysis.recommendation_engine import RecommendationEngine

# Initialize recommendation engine
engine = RecommendationEngine(delay=2)

# Get recommendation for a single stock
analysis = engine.analyze_single_stock('AAPL')
print(f"Recommendation: {analysis['recommendation']}")
print(f"Confidence: {analysis['confidence']}")

# Get comprehensive analysis for all stocks
results = engine.analyze_all_magnificent_seven()
report = engine.generate_investment_report(results)
print(report)

# Clean up resources
engine.close()
```

### Testing

Run the test suites:
```bash
# Test basic crawler functionality
python tests/test_crawler.py

# Test recommendation system
python tests/test_recommendation_system.py

# Test bug fixes
python tests/test_fixes.py
```

## Sample Output

### Stock Data
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

### AI Recommendation Analysis
```json
{
  "symbol": "AAPL",
  "company": "Apple Inc.",
  "overall_score": 0.847,
  "recommendation": "STRONG BUY",
  "confidence": "High",
  "analysis_breakdown": {
    "momentum": {"score": 0.70, "analysis": "Positive momentum (+1.2%)"},
    "volume": {"score": 0.65, "analysis": "Good volume (46M)"},
    "market_cap": {"score": 0.95, "analysis": "Mega-cap leader ($2.9T)"},
    "volatility": {"score": 0.75, "analysis": "Moderate volatility - balanced risk"},
    "value": {"score": 0.85, "analysis": "Ecosystem dominance & innovation"}
  }
}
```

### Investment Report Sample
```
MAGNIFICENT SEVEN STOCK ANALYSIS REPORT
================================================================================

MARKET OVERVIEW
--------------------------------------------------
Market Sentiment: Bullish
Overall Strength: 72.4%
Description: Good investment climate with selective opportunities
Stocks with Positive Momentum: 5/7

TOP 3 RECOMMENDATIONS
--------------------------------------------------
1. NVDA - NVIDIA Corporation
   Score: 0.892 | STRONG BUY
2. MSFT - Microsoft Corporation  
   Score: 0.856 | STRONG BUY
3. AAPL - Apple Inc.
   Score: 0.847 | STRONG BUY
```

## Requirements

- **Python 3.6+** (Python 3.8+ recommended)
- **requests** - HTTP client library
- **beautifulsoup4** - HTML parsing
- **lxml** - XML/HTML parser
- **matplotlib** - Chart visualizations
- **numpy** - Numerical computations
- **tkinter** - GUI framework (included with Python)
- **Pillow** - Image processing for icons

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
3. Make your changes (maintain retro theme consistency!)
4. Add tests if applicable
5. Submit a pull request

### Retro Pastel Theme Guidelines:
- Maintain professional and clean design
- Use pastel purple/pink color scheme
- Follow retro Windows 95/98 styling patterns
- Keep interface elements simple and readable
- Use pixel-perfect 24x24px icons
- Follow modular component architecture

## License

This project is open source. Please use responsibly.

## Disclaimer

Stock prices and financial data are provided for informational purposes only. This tool does not provide investment advice. Always verify financial information from official sources before making investment decisions.