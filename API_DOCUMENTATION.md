# Kawaii StockEdu Platform - API Documentation

## 📋 개요
이 문서는 Kawaii StockEdu Platform의 내부 API와 확장 개발을 위한 가이드를 제공합니다.

## 🏗️ 아키텍처 개요

```
┌─────────────────────────────────────────────────────────┐
│                    GUI Layer                           │ 
│  gui_app.py, tabs/, panels/, widgets/                 │
├─────────────────────────────────────────────────────────┤
│                 Business Logic                         │
│  analysis/, trading/, education/                       │  
├─────────────────────────────────────────────────────────┤
│                  Data Layer                            │
│  data/, core/                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 핵심 모듈 API

### 1. Trading Engine API (`src/trading/`)

#### TradingEngine Class
```python
class TradingEngine:
    """모의 거래 엔진 - 모든 거래 로직을 담당"""
    
    def __init__(self, data_manager: DataManager)
    def execute_market_order(self, symbol: str, quantity: int, order_type: str) -> OrderResult
    def execute_limit_order(self, symbol: str, quantity: int, price: float, order_type: str) -> OrderResult
    def cancel_order(self, order_id: str) -> bool
    def get_portfolio_summary(self) -> PortfolioSummary
```

**Parameters:**
- `symbol` (str): 주식 심볼 (예: "AAPL")
- `quantity` (int): 거래 수량 (양수: 매수, 음수: 매도)
- `order_type` (str): "buy" 또는 "sell"
- `price` (float): 지정가 (limit order에서만 사용)

**Returns:**
- `OrderResult`: 거래 결과 객체
- `PortfolioSummary`: 포트폴리오 요약 정보

**Example:**
```python
from src.trading.trading_engine import TradingEngine
from src.trading.data_manager import DataManager

# 초기화
data_manager = DataManager()
engine = TradingEngine(data_manager)

# 시장가 매수 주문
result = engine.execute_market_order("AAPL", 10, "buy")
if result.success:
    print(f"주문 성공: {result.order_id}")
else:
    print(f"주문 실패: {result.error_message}")
```

#### Portfolio Model
```python
class Portfolio:
    """포트폴리오 데이터 모델"""
    
    @property
    def cash_balance(self) -> float
    @property  
    def positions(self) -> Dict[str, Position]
    @property
    def total_value(self) -> float
    
    def add_position(self, symbol: str, quantity: int, price: float)
    def remove_position(self, symbol: str, quantity: int) -> bool
    def get_position(self, symbol: str) -> Optional[Position]
```

#### Position Model
```python
class Position:
    """개별 주식 포지션"""
    
    symbol: str
    quantity: int
    average_price: float
    current_price: float
    
    @property
    def market_value(self) -> float
    @property
    def unrealized_pnl(self) -> float
    @property
    def unrealized_pnl_percent(self) -> float
```

### 2. Data Management API (`src/data/`)

#### StockCrawler Class
```python
class StockCrawler:
    """주식 데이터 수집 엔진"""
    
    def __init__(self, delay: int = 2)
    def get_stock_data(self, symbol: str) -> Optional[StockData]
    def get_multiple_stocks(self, symbols: List[str]) -> Dict[str, StockData]
    def is_valid_symbol(self, symbol: str) -> bool
```

**StockData Model:**
```python
class StockData:
    symbol: str
    current_price: float
    change_percent: float
    volume: int
    market_cap: Optional[float]
    pe_ratio: Optional[float]
    dividend_yield: Optional[float]
    last_updated: datetime
```

**Example:**
```python
from src.data.stock_crawler import StockCrawler

crawler = StockCrawler(delay=1)
data = crawler.get_stock_data("AAPL")

if data:
    print(f"현재가: ${data.current_price}")
    print(f"변동률: {data.change_percent}%")
```

#### YFinanceDataSource Class
```python
class YFinanceDataSource:
    """YFinance API 연동 클래스"""
    
    def fetch_real_time_data(self, symbol: str) -> Dict
    def fetch_historical_data(self, symbol: str, period: str) -> pd.DataFrame
    def validate_symbol(self, symbol: str) -> bool
```

### 3. Analysis Engine API (`src/analysis/`)

#### RecommendationEngine Class
```python
class RecommendationEngine:
    """AI 추천 엔진"""
    
    def __init__(self, delay: int = 2)
    def analyze_stock(self, symbol: str) -> RecommendationResult
    def analyze_portfolio(self, portfolio: Portfolio) -> PortfolioAnalysis
    def get_market_recommendations(self, symbols: List[str]) -> List[RecommendationResult]
```

**RecommendationResult Model:**
```python
class RecommendationResult:
    symbol: str
    recommendation: str  # "BUY", "SELL", "HOLD"
    confidence_score: float  # 1.0 - 10.0
    reasoning: List[str]
    target_price: Optional[float]
    risk_level: int  # 1-5
    investment_style: str  # "Conservative", "Moderate", "Aggressive"
```

**Example:**
```python
from src.analysis.recommendation_engine import RecommendationEngine

engine = RecommendationEngine()
result = engine.analyze_stock("AAPL")

print(f"추천: {result.recommendation}")
print(f"신뢰도: {result.confidence_score}/10")
print(f"이유: {', '.join(result.reasoning)}")
```

#### InvestmentPersonalityAnalyzer Class
```python
class InvestmentPersonalityAnalyzer:
    """투자 성향 분석 엔진"""
    
    def analyze_trading_history(self, transactions: List[Transaction]) -> PersonalityMetrics
    def calculate_risk_tolerance(self, transactions: List[Transaction]) -> RiskProfile
    def determine_investment_style(self, transactions: List[Transaction]) -> InvestmentStyle
```

**PersonalityMetrics Model:**
```python
class PersonalityMetrics:
    patience_score: int  # 0-100
    consistency_score: int  # 0-100  
    profitability_score: int  # 0-100
    discipline_score: int  # 0-100
    overall_level: str  # "NOVICE" to "LEGENDARY"
    risk_tolerance: str  # "Conservative", "Moderate", "Aggressive"
    investment_style: str  # "Long-term", "Swing", "Day Trading"
```

### 4. GUI Components API (`src/gui/`)

#### Base Tab Class
```python
class BaseTab:
    """모든 탭의 기본 클래스"""
    
    def __init__(self, notebook: ttk.Notebook, main_app: StockAnalysisGUI)
    def setup_tab(self) -> None
    def refresh_data(self) -> None
    def on_data_update(self, data: Any) -> None
```

#### Custom Widget Creation
```python
# 커스텀 버튼 생성
button = main_app.icon_button(
    parent=frame,
    key='buy',  # 아이콘 키
    text='Buy Stock',
    command=self.buy_stock,
    style='Pastel.Primary.TButton'
)

# 커스텀 패널 생성  
panel = TradingPanel(parent_frame, main_app, data_manager)
```

---

## 🔧 확장 개발 가이드

### 새로운 탭 추가하기

1. **탭 클래스 생성**
```python
# src/gui/components/tabs/my_custom_tab.py
from .base_tab import BaseTab

class MyCustomTab(BaseTab):
    def setup_tab(self):
        self.frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.frame, text="My Tab")
        
        # 커스텀 UI 구성
        self.create_widgets()
    
    def create_widgets(self):
        # 위젯 생성 로직
        pass
```

2. **메인 앱에 등록**
```python
# src/gui/gui_app.py
from src.gui.components.tabs.my_custom_tab import MyCustomTab

def create_widgets(self):
    # 기존 탭들...
    self.my_custom_tab = MyCustomTab(self.notebook, self)
```

### 새로운 분석 엔진 추가하기

1. **분석 엔진 클래스 생성**
```python
# src/analysis/my_analyzer.py
class MyAnalyzer:
    def __init__(self, config: dict = None):
        self.config = config or {}
    
    def analyze(self, data: StockData) -> AnalysisResult:
        # 분석 로직 구현
        return AnalysisResult(
            score=score,
            recommendation=recommendation,
            details=details
        )
```

2. **기존 시스템에 통합**
```python
# src/analysis/recommendation_engine.py
from .my_analyzer import MyAnalyzer

class RecommendationEngine:
    def __init__(self):
        self.analyzers = [
            FinancialAnalyzer(),
            MyAnalyzer(),  # 새 분석기 추가
        ]
```

### 새로운 데이터 소스 추가하기

1. **데이터 소스 인터페이스 구현**
```python
# src/data/my_data_source.py
from .base_data_source import BaseDataSource

class MyDataSource(BaseDataSource):
    def fetch_data(self, symbol: str) -> StockData:
        # 데이터 수집 로직
        pass
    
    def validate_symbol(self, symbol: str) -> bool:
        # 심볼 검증 로직
        pass
```

2. **데이터 매니저에 등록**
```python
# src/trading/data_manager.py
def __init__(self):
    self.data_sources = [
        YFinanceDataSource(),
        MyDataSource(),  # 새 데이터 소스 추가
    ]
```

---

## 🎨 테마 및 스타일링 API

### ThemeManager Class
```python
class ThemeManager:
    """테마 관리 클래스"""
    
    @property
    def colors(self) -> Dict[str, str]:
        return {
            'background': '#1F144A',
            'panel': '#2B1E6B', 
            'lavender': '#C4B5FD',
            'periwinkle': '#A78BFA',
            'pink': '#FBCFE8',
            'text': '#F8F8FF'
        }
    
    def apply_styles(self) -> None
    def create_custom_style(self, name: str, config: dict) -> None
```

### IconManager Class  
```python
class IconManager:
    """아이콘 관리 클래스"""
    
    def load_icons(self) -> None
    def get_icon(self, key: str) -> Optional[PhotoImage]
    def has_icon(self, key: str) -> bool
    def add_custom_icon(self, key: str, path: str) -> bool
```

**사용 가능한 아이콘 키:**
- `'add'`, `'buy'`, `'sell'`, `'refresh'`, `'save'`
- `'settings'`, `'help'`, `'export'`, `'import'`
- `'level_1'` ~ `'level_5'`, `'heart'`, `'star'`

---

## 📊 이벤트 시스템

### Event Types
```python
class EventType:
    DATA_UPDATED = "data_updated"
    TRADE_EXECUTED = "trade_executed"  
    PORTFOLIO_CHANGED = "portfolio_changed"
    ANALYSIS_COMPLETED = "analysis_completed"
```

### Event Subscription
```python
# 이벤트 구독
def on_trade_executed(self, event_data):
    print(f"거래 실행됨: {event_data['symbol']}")

main_app.subscribe(EventType.TRADE_EXECUTED, on_trade_executed)

# 이벤트 발생
main_app.emit(EventType.TRADE_EXECUTED, {
    'symbol': 'AAPL',
    'quantity': 10,
    'price': 150.0
})
```

---

## 🧪 테스트 API

### 단위 테스트 예제
```python
import unittest
from src.trading.trading_engine import TradingEngine

class TestTradingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = TradingEngine()
    
    def test_buy_order(self):
        result = self.engine.execute_market_order("AAPL", 10, "buy")
        self.assertTrue(result.success)
        self.assertIsNotNone(result.order_id)
    
    def test_insufficient_funds(self):
        result = self.engine.execute_market_order("AAPL", 1000000, "buy")
        self.assertFalse(result.success)
        self.assertIn("insufficient", result.error_message.lower())
```

### 통합 테스트
```python
from tests.test_base import BaseIntegrationTest

class TestFullWorkflow(BaseIntegrationTest):
    def test_complete_trading_workflow(self):
        # 데이터 수집
        data = self.crawler.get_stock_data("AAPL")
        self.assertIsNotNone(data)
        
        # 분석 실행
        recommendation = self.analyzer.analyze_stock("AAPL")
        self.assertIn(recommendation.recommendation, ["BUY", "SELL", "HOLD"])
        
        # 거래 실행
        if recommendation.recommendation == "BUY":
            result = self.engine.execute_market_order("AAPL", 10, "buy")
            self.assertTrue(result.success)
```

---

## 🔐 보안 고려사항

### 입력 검증
```python
def validate_stock_symbol(symbol: str) -> bool:
    """주식 심볼 검증"""
    if not symbol or len(symbol) > 10:
        return False
    return symbol.isalpha() and symbol.isupper()

def validate_quantity(quantity: int) -> bool:
    """거래 수량 검증"""
    return 1 <= quantity <= 10000

def validate_price(price: float) -> bool:
    """가격 검증"""
    return 0.01 <= price <= 100000.0
```

### 에러 처리
```python
try:
    result = trading_engine.execute_order(symbol, quantity)
except InsufficientFundsError as e:
    logger.warning(f"자금 부족: {e}")
    return {"error": "insufficient_funds"}
except InvalidSymbolError as e:
    logger.error(f"잘못된 심볼: {e}")
    return {"error": "invalid_symbol"}
except Exception as e:
    logger.error(f"예상치 못한 오류: {e}")
    return {"error": "unexpected_error"}
```

---

## 📈 성능 최적화

### 데이터 캐싱
```python
from functools import lru_cache
from datetime import datetime, timedelta

class DataCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self.cache = {}
    
    @lru_cache(maxsize=128)
    def get_cached_data(self, symbol: str) -> Optional[StockData]:
        if symbol in self.cache:
            data, timestamp = self.cache[symbol]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                return data
        return None
```

### 비동기 처리
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncDataManager:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def fetch_multiple_stocks(self, symbols: List[str]) -> Dict[str, StockData]:
        loop = asyncio.get_event_loop()
        tasks = []
        
        for symbol in symbols:
            task = loop.run_in_executor(
                self.executor, 
                self.crawler.get_stock_data, 
                symbol
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return dict(zip(symbols, results))
```

---

## 📞 기술 지원

### 디버깅 도구
```python
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stockedu.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 개발자 모드
```python
# config.py에서 개발자 모드 활성화
DEBUG_MODE = True

if DEBUG_MODE:
    # 상세한 로깅
    logging.getLogger().setLevel(logging.DEBUG)
    
    # 추가 디버그 정보 표시
    print(f"API 호출 횟수: {api_call_count}")
    print(f"메모리 사용량: {memory_usage}MB")
```

이제 문서화가 완료되었습니다. 다음 단계로 UX 개선 작업을 진행하겠습니다!