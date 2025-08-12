# 🚀 Magnificent Seven Stock Analysis & Recommendation System

An intelligent Python-based **Windows desktop application** that crawls real-time stock information for the **"Magnificent Seven"** and provides **AI-powered buy recommendations** through a beautiful, user-friendly GUI! 🖥️📈🤖✨

## 🏆 The Magnificent Seven Stocks

This crawler targets the following legendary tech stocks:
- 🍎 **AAPL** - Apple Inc.
- 🖥️ **MSFT** - Microsoft Corporation
- 🔍 **GOOGL** - Alphabet Inc. (Google)
- 📦 **AMZN** - Amazon.com Inc.
- 🎮 **NVDA** - NVIDIA Corporation
- ⚡ **TSLA** - Tesla Inc.
- 👥 **META** - Meta Platforms Inc. (Facebook)

## ✨ Features

### 🌐 Data Collection
- **Real-time stock data extraction** from Yahoo Finance
- **Comprehensive financial metrics**:
  - 💰 Current stock price & changes
  - 📈 Price momentum analysis
  - 🏢 Market capitalization
  - 📊 Trading volume analysis
  - ⏰ Timestamp tracking

### 🤖 AI-Powered Analysis
- **Smart recommendation engine** with weighted scoring
- **Multi-factor analysis**:
  - 📈 Price momentum (25% weight)
  - 📊 Volume trends (15% weight) 
  - 🏢 Market cap stability (20% weight)
  - ⚖️ Volatility assessment (15% weight)
  - 💎 Value proposition (25% weight)
- **Recommendation levels**: Strong Buy 🟢, Buy 🔵, Hold 🟡, Weak Hold 🟠, Avoid 🔴

### 🎯 Operation Modes
- 📊 **Stock Data Collection** (all or individual)
- 💡 **Buy Recommendations** with confidence scoring
- 🔍 **Individual Stock Analysis** with detailed breakdowns
- 📋 **Comprehensive Investment Reports**
- 🌍 **General web crawling** functionality

### 🖥️ GUI Features
- **Modern Windows Desktop Interface** with tabbed navigation
- **Real-time Data Display** in sortable tables
- **Interactive Charts** with matplotlib integration
- **Progress Indicators** and async data loading
- **Export Functionality** for reports and analysis

### 🛡️ Technical Features
- ⚡ **Rate limiting** to respect website resources
- 🛡️ **Error handling** and logging
- 📄 **JSON output** for easy data processing
- 🧪 **Comprehensive test suite**
- 🎨 **Professional GUI** with modern styling

## 🛠️ Installation

1. 📥 **Clone this repository:**
```bash
git clone https://github.com/Nyam2C/crawling-program.git
cd crawling-program
```

2. 📦 **Install required dependencies:**
```bash
pip install -r requirements.txt
```

## 🎮 Usage

### 🖥️ **GUI Application (Recommended)**

Launch the modern desktop interface:
```bash
python run_gui.py
```

**GUI Features:**
- **📊 Stock Data Tab**: View real-time data for all stocks in a sortable table
- **💡 Recommendations Tab**: Generate AI-powered buy/sell recommendations
- **🔍 Individual Analysis Tab**: Deep-dive analysis for specific stocks
- **📈 Charts Tab**: Interactive visualizations and charts
- **⚙️ Settings Tab**: Configure application settings

### 🎪 **Command Line Interface**

For CLI usage (legacy support):
```bash
python main.py
```

**Available Options:**
1. 📊 Get stock data (all Magnificent Seven)
2. 🎯 Get stock data (specific stock)
3. 💡 Get buy recommendations (all stocks)
4. 🔍 Analyze specific stock
5. 🌍 General web crawling

## 🏗️ Project Structure

The crawler is now organized into modular components for better readability and maintainability:

```
📁 project/
├── 🚀 run_gui.py                     # GUI launcher (START HERE!)
├── 🖥️ gui_app.py                     # Main GUI application
├── 📈 gui_charts.py                  # Chart visualizations
├── 🎯 main.py                        # CLI entry point  
├── 💬 cli.py                         # Command line interface
├── 🕷️ stock_crawler.py               # Stock data collection
├── 🤖 recommendation_engine.py       # AI recommendation system
├── 🧮 financial_analyzer.py          # Financial analysis algorithms
├── 🌐 http_client.py                 # HTTP requests and session management
├── 🔍 data_extractors.py             # HTML parsing and data extraction
├── ⚙️ config.py                      # Configuration and constants
├── 🧪 test_crawler.py                # Crawler test suite
├── 🧪 test_recommendation_system.py  # Recommendation system tests
├── 📋 requirements.txt               # Dependencies
└── 📖 README.md                     # Documentation
```

## 🖼️ Screenshots

### 📊 Stock Data View
![Stock Data Tab - Real-time financial data in sortable tables]

### 💡 AI Recommendations  
![Recommendations Tab - Comprehensive investment analysis reports]

### 📈 Interactive Charts
![Charts Tab - Visual analysis with matplotlib integration]

### 🔍 Individual Analysis
![Analysis Tab - Deep-dive stock analysis with scoring breakdown]

### 👨‍💻 Programmatic Usage

#### 📊 Basic Stock Data Collection
```python
from stock_crawler import StockCrawler

# 🚀 Initialize crawler
crawler = StockCrawler(delay=2)

# 📈 Get data for a single stock
stock_data = crawler.get_stock_data('AAPL')
print(stock_data)

# 🎯 Get data for all Magnificent Seven stocks
all_stocks = crawler.get_all_stocks_data()
print(all_stocks)

# 🧹 Clean up resources
crawler.close()
```

#### 🤖 AI-Powered Recommendations
```python
from recommendation_engine import RecommendationEngine

# 🚀 Initialize recommendation engine
engine = RecommendationEngine(delay=2)

# 💡 Get recommendation for a single stock
analysis = engine.analyze_single_stock('AAPL')
print(f"Recommendation: {analysis['recommendation']}")
print(f"Confidence: {analysis['confidence']}")

# 📊 Get comprehensive analysis for all stocks
results = engine.analyze_all_magnificent_seven()
report = engine.generate_investment_report(results)
print(report)

# 🧹 Clean up resources
engine.close()
```

### 🧪 Testing

Run the test suites:
```bash
# Test basic crawler functionality
python test_crawler.py

# Test recommendation system
python test_recommendation_system.py
```

## 📊 Sample Output

### 📈 Stock Data
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

### 🤖 AI Recommendation Analysis
```json
{
  "symbol": "AAPL",
  "company": "Apple Inc.",
  "overall_score": 0.847,
  "recommendation": "🟢 STRONG BUY",
  "confidence": "High",
  "analysis_breakdown": {
    "momentum": {"score": 0.70, "analysis": "📈 Positive momentum (+1.2%)"},
    "volume": {"score": 0.65, "analysis": "📊 Good volume (46M)"},
    "market_cap": {"score": 0.95, "analysis": "🏛️ Mega-cap leader ($2.9T)"},
    "volatility": {"score": 0.75, "analysis": "⚖️ Moderate volatility - balanced risk"},
    "value": {"score": 0.85, "analysis": "💎 Ecosystem dominance & innovation"}
  }
}
```

### 📋 Investment Report Sample
```
📊 MAGNIFICENT SEVEN STOCK ANALYSIS REPORT
================================================================================

🌟 MARKET OVERVIEW
--------------------------------------------------
Market Sentiment: 📈 Bullish
Overall Strength: 72.4%
Description: Good investment climate with selective opportunities
Stocks with Positive Momentum: 5/7

🏆 TOP 3 RECOMMENDATIONS
--------------------------------------------------
1. NVDA - NVIDIA Corporation
   Score: 0.892 | 🟢 STRONG BUY
2. MSFT - Microsoft Corporation  
   Score: 0.856 | 🟢 STRONG BUY
3. AAPL - Apple Inc.
   Score: 0.847 | 🟢 STRONG BUY
```

## 📋 Requirements

- 🐍 **Python 3.6+** (Python 3.8+ recommended)
- 🌐 **requests** - HTTP client library
- 🥄 **beautifulsoup4** - HTML parsing
- 🔍 **lxml** - XML/HTML parser
- 📊 **matplotlib** - Chart visualizations
- 🔢 **numpy** - Numerical computations
- 🖥️ **tkinter** - GUI framework (included with Python)

## ⏱️ Rate Limiting

The crawler includes a 2-second delay between requests by default to be respectful to the target websites. ⏰ You can adjust this in the `StockCrawler` initialization.

## ⚖️ Legal Notice

This tool is for educational and research purposes only. Please:
- 📜 Respect the terms of service of the websites you crawl
- ⏳ Use appropriate delays between requests
- 🤖 Consider the website's robots.txt file
- 📊 Use the data responsibly and in compliance with applicable laws

## 🤝 Contributing

1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. ✨ Make your changes
4. 🧪 Add tests if applicable
5. 🚀 Submit a pull request

## 📄 License

This project is open source. Please use responsibly. 💚

## ⚠️ Disclaimer

Stock prices and financial data are provided for informational purposes only. 📊 This tool does not provide investment advice. Always verify financial information from official sources before making investment decisions. 💼