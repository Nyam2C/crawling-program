# 📊 StockEdu - Stock Analysis & Trading Simulation Platform

**A comprehensive stock analysis and virtual trading platform for educational purposes**

> *"Practical stock market tools designed for educational use and risk-free learning"*

## 🎯 Platform Overview

StockEdu is a stock analysis and virtual trading platform designed for educational purposes. It provides real-time stock data analysis, AI-powered recommendations, and risk-free trading simulation to help users understand stock market mechanics without financial risk.

### 🌟 Core Philosophy
- **📚 Educational Focus**: All features designed for learning, not real trading
- **🛡️ Risk-Free Environment**: Virtual trading with no real money involved
- **📊 Real Data**: Actual market data for realistic learning experience
- **🤖 AI Insights**: Intelligent analysis to understand market patterns

## ✨ Key Features

### 📈 Stock Analysis Tools
- **Real-time Stock Data**: Live stock prices via Yahoo Finance API
- **AI-Powered Analysis**: Comprehensive stock analysis reports
- **Individual Stock Analysis**: Deep-dive analysis of specific stocks
- **Market Recommendations**: AI-based buy/sell recommendations
- **Advanced Technical Analysis**: Multi-criteria evaluation with 20+ indicators
- **Quick Analysis**: Basic technical evaluation for rapid insights

### 📰 News & Sentiment Analysis
- **Multi-Source News Feed**: Aggregated news from various financial sources
- **3-Step Analysis Algorithm**: Symbol → Keywords → News discovery
- **Sentiment Analysis**: AI-powered sentiment scoring using VADER and TextBlob
- **Keyword Extraction**: Company-specific keyword identification
- **Trending Topics**: GUI-styled trending topics display
- **Article Details**: Full article content with double-click activation

### 🎮 Virtual Trading System
- **Mock Portfolio**: Start with $100,000 virtual cash
- **Real-time Trading**: Buy and sell stocks with live market prices
- **Portfolio Tracking**: Monitor positions, P&L, and performance
- **Transaction History**: Complete record of all virtual trades
- **Realistic Fees**: Simulated commission (0.015%) and tax (0.25%)
- **Order Management**: Market and limit orders with validation

### 🧠 Investment Analysis
- **Personality Analysis**: AI-based investment style assessment
- **Performance Evaluation**: 5-tier skill rating system (NOVICE to EXPERT)
- **Risk Profiling**: Personal risk tolerance evaluation
- **Investment Metrics**: Comprehensive performance analytics
- **Individual Status Updates**: Real-time analysis results integration

### 📊 Market Data & Tools
- **Universal Symbol Support**: Not limited to Magnificent 7 stocks
- **Dynamic Symbol Loading**: Pull from Stock Data tab's symbol list
- **Watchlist Management**: Track multiple stocks of interest
- **Scoreboard System**: Performance rankings and achievements
- **Data Export**: Save analysis reports and trading history
- **Auto-refresh**: Real-time price updates every 20 seconds
- **Keyboard Shortcuts**: Full keyboard navigation support (Ctrl+1-8)

## 🚀 Getting Started

### 📋 System Requirements
- **Python 3.8+** (Python 3.9+ recommended)
- **Operating System**: Windows, macOS, Linux
- **Memory**: Minimum 4GB RAM
- **Storage**: 1GB+ free space

### ⚙️ Installation

1. **Clone Repository**
```bash
git clone https://github.com/Nyam2C/crawling-program.git
cd crawling-program
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Install GUI Library**

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**CentOS/Fedora:**
```bash
sudo dnf install python3-tkinter
```

**Windows/macOS:** Included with Python installation

### 🎮 Running the Platform

**Launch GUI Application:**
```bash
python main.py
```

## 🖥️ Platform Interface

### 📱 Main Tabs Overview

1. **📊 Stock Data**: Manage and add stocks for analysis
2. **🤖 AI Recommendations**: Get intelligent investment suggestions
3. **🔍 Individual Analysis**: Detailed analysis of specific stocks
4. **💰 Mock Trading**: Virtual trading simulation
5. **🏆 Scoreboard**: Performance rankings and achievements
6. **📈 Investment Analysis**: Personal investment style assessment
7. **⚙️ Settings**: Platform configuration and preferences
8. **📰 News & Sentiment**: News analysis with sentiment scoring

### 💼 How to Use

**Getting Started:**
1. Launch the application with `python main.py`
2. Add stocks of interest in the **Stock Data** tab
3. Explore AI recommendations for market insights
4. Practice trading in the **Mock Trading** tab with virtual money
5. Analyze your investment style in the **Investment Analysis** tab

**Virtual Trading:**
- Start with $100,000 virtual cash
- Buy and sell stocks using real market prices
- Track your portfolio performance over time
- Learn from trading decisions without financial risk

**Analysis Features:**
- Get comprehensive stock analysis reports
- Understand your investment personality and risk tolerance
- Track performance with detailed metrics and rankings

**News & Sentiment Analysis:**
- Browse news articles with sentiment scoring
- View trending topics in a styled popup window
- Use keyword-based news discovery algorithm
- Double-click articles for detailed content view

### ⌨️ Keyboard Shortcuts
- **Ctrl+1**: Stock Data Tab
- **Ctrl+2**: Recommendations Tab  
- **Ctrl+3**: Analysis Tab
- **Ctrl+4**: Trading Tab
- **Ctrl+5**: Scoreboard Tab
- **Ctrl+6**: Investment Analysis Tab
- **Ctrl+7**: Settings Tab
- **Ctrl+8**: News & Sentiment Tab
- **Ctrl+R**: Refresh Data
- **Ctrl+S**: Save Settings
- **F1**: Help Dialog
- **ESC**: Cancel Current Action

## 🛠️ Technical Architecture

### 🔧 Core Technologies
- **Python 3.8+**: Core application logic
- **tkinter**: Cross-platform GUI framework
- **yfinance**: Real-time stock data integration
- **Pillow**: Image processing and icon management
- **feedparser**: RSS news feed processing
- **TextBlob & VADER**: Sentiment analysis engines
- **requests & beautifulsoup4**: Web scraping and data extraction

### 📁 Project Structure
```
📂 stockedu/
├── 🚀 main.py                    # Main application entry point
├── 📋 requirements.txt           # Python dependencies
├── 🛠️ scripts/                  # Launch scripts
├── 🧬 src/                       # Source code
│   ├── 📚 education/             # Educational modules
│   ├── 🤖 analysis/              # AI analysis engines
│   ├── 💾 data/                  # Data collection and processing
│   ├── 🖥️ gui/                   # User interface components
│   ├── 📈 trading/               # Virtual trading system
│   └── ⚙️ core/                  # Core utilities
├── 🎨 assets/                    # UI assets and icons
└── 📚 docs/                      # Documentation
```

## 🏅 Performance Evaluation

### 📈 5-Tier Rating System
- **🥇 EXPERT (80-100 points)**: Master-level performance
- **🥈 ADVANCED (70-79 points)**: Skilled investor profile
- **🥉 INTERMEDIATE (60-69 points)**: Developing investor
- **📚 BEGINNER (50-59 points)**: Learning phase
- **🔰 NOVICE (0-49 points)**: Starting level

### 📊 Evaluation Metrics
- **PATIENCE**: Long-term investment capability
- **CONSISTENCY**: Stable return generation
- **PROFITABILITY**: Success rate and returns
- **DISCIPLINE**: Risk management skills

## 🛡️ Educational Purpose & Disclaimers

### ⚠️ Important Notice
- This platform is designed for **educational purposes only**
- All trading is virtual with **no real money involved**
- **Not intended for actual investment advice**
- Users should **consult qualified financial advisors** for real investments
- **Past performance does not guarantee future results**

### 🔒 Data & Privacy
- Personal data stored locally only
- No real financial information collected
- All transactions are virtual simulations
- Real market data used for educational realism

## 🧪 Testing & Validation

**Run Application:**
```bash
python main.py
```

**Check Dependencies:**
```bash
python -c "import tkinter, yfinance, PIL; print('All dependencies installed successfully')"
```

## 📄 License

This project is open source and available for educational use.

## ⚠️ Disclaimer

**This platform is for educational purposes only.** It provides virtual trading simulation and analysis tools to help users understand stock market mechanics. Always:
- Verify information from official financial sources
- Consult qualified financial advisors for investment decisions
- Understand that virtual performance may not reflect real trading results
- Use this platform as a learning tool, not for actual investment guidance

---

*Educational stock analysis and trading simulation platform*