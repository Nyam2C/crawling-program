#!/usr/bin/env python3
"""
Multi Data Source Manager - 다중 데이터 소스 통합 관리
야후 파이낸스, Alpha Vantage, Polygon 등 여러 데이터 소스를 통합 관리
"""

import asyncio
import aiohttp
import yfinance as yf
import time
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import json
import concurrent.futures

class DataSourceType(Enum):
    """데이터 소스 타입"""
    YAHOO_FINANCE = "yahoo_finance"
    ALPHA_VANTAGE = "alpha_vantage"
    POLYGON = "polygon"
    FINNHUB = "finnhub"
    TWELVE_DATA = "twelve_data"

@dataclass
class DataSourceConfig:
    """데이터 소스 설정"""
    source_type: DataSourceType
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    rate_limit: float = 1.0  # requests per second
    priority: int = 1  # 1=highest, 5=lowest
    enabled: bool = True

@dataclass
class StockDataResult:
    """주식 데이터 결과"""
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    data_source: str = ""
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class MultiDataSourceManager:
    """다중 데이터 소스 매니저"""
    
    def __init__(self):
        self.data_sources = self._initialize_data_sources()
        self.cache = {}
        self.cache_ttl = 300  # 5분 캐시
        self.logger = logging.getLogger(__name__)
        
        # 비동기 세션
        self.session = None
        
    def _initialize_data_sources(self) -> Dict[DataSourceType, DataSourceConfig]:
        """데이터 소스 초기화"""
        return {
            DataSourceType.YAHOO_FINANCE: DataSourceConfig(
                DataSourceType.YAHOO_FINANCE,
                priority=1,
                rate_limit=2.0
            ),
            DataSourceType.ALPHA_VANTAGE: DataSourceConfig(
                DataSourceType.ALPHA_VANTAGE,
                api_key=None,  # 사용자가 설정
                base_url="https://www.alphavantage.co/query",
                priority=2,
                rate_limit=0.2,  # 5 requests per minute for free tier
                enabled=False
            ),
            DataSourceType.FINNHUB: DataSourceConfig(
                DataSourceType.FINNHUB,
                api_key=None,
                base_url="https://finnhub.io/api/v1",
                priority=3,
                rate_limit=1.0,
                enabled=False
            ),
            DataSourceType.TWELVE_DATA: DataSourceConfig(
                DataSourceType.TWELVE_DATA,
                api_key=None,
                base_url="https://api.twelvedata.com",
                priority=4,
                rate_limit=0.125,  # 8 requests per minute for free tier
                enabled=False
            )
        }
    
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self.session:
            await self.session.close()
    
    def configure_data_source(self, source_type: DataSourceType, api_key: str = None, enabled: bool = True):
        """데이터 소스 설정"""
        if source_type in self.data_sources:
            self.data_sources[source_type].api_key = api_key
            self.data_sources[source_type].enabled = enabled
            self.logger.info(f"Configured {source_type.value} - Enabled: {enabled}")
    
    def get_stock_data_sync(self, symbol: str) -> Optional[StockDataResult]:
        """동기식 주식 데이터 조회 (기존 호환성)"""
        try:
            # 캐시 확인
            cache_key = f"{symbol}_{int(time.time() // self.cache_ttl)}"
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # 우선순위 순으로 데이터 소스 시도
            enabled_sources = [
                (source, config) for source, config in self.data_sources.items()
                if config.enabled
            ]
            enabled_sources.sort(key=lambda x: x[1].priority)
            
            for source_type, config in enabled_sources:
                try:
                    if source_type == DataSourceType.YAHOO_FINANCE:
                        result = self._get_yahoo_finance_data(symbol)
                    elif source_type == DataSourceType.ALPHA_VANTAGE and config.api_key:
                        result = self._get_alpha_vantage_data(symbol, config.api_key)
                    elif source_type == DataSourceType.FINNHUB and config.api_key:
                        result = self._get_finnhub_data(symbol, config.api_key)
                    else:
                        continue
                    
                    if result:
                        self.cache[cache_key] = result
                        return result
                        
                    # Rate limiting
                    time.sleep(1.0 / config.rate_limit)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to get data from {source_type.value}: {e}")
                    continue
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting stock data for {symbol}: {e}")
            return None
    
    def _get_yahoo_finance_data(self, symbol: str) -> Optional[StockDataResult]:
        """Yahoo Finance 데이터 조회"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if hist.empty or len(hist) < 1:
                return None
            
            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - prev_price
            change_percent = (change / prev_price) * 100 if prev_price != 0 else 0
            
            return StockDataResult(
                symbol=symbol,
                price=float(current_price),
                change=float(change),
                change_percent=float(change_percent),
                volume=int(hist['Volume'].iloc[-1]) if 'Volume' in hist else 0,
                market_cap=info.get('marketCap'),
                pe_ratio=info.get('trailingPE'),
                dividend_yield=info.get('dividendYield'),
                fifty_two_week_high=info.get('fiftyTwoWeekHigh'),
                fifty_two_week_low=info.get('fiftyTwoWeekLow'),
                data_source="Yahoo Finance"
            )
            
        except Exception as e:
            self.logger.error(f"Yahoo Finance error for {symbol}: {e}")
            return None
    
    def _get_alpha_vantage_data(self, symbol: str, api_key: str) -> Optional[StockDataResult]:
        """Alpha Vantage 데이터 조회"""
        try:
            import requests
            
            # 실시간 데이터
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'Global Quote' not in data:
                return None
            
            quote = data['Global Quote']
            
            return StockDataResult(
                symbol=symbol,
                price=float(quote['05. price']),
                change=float(quote['09. change']),
                change_percent=float(quote['10. change percent'].rstrip('%')),
                volume=int(quote['06. volume']),
                data_source="Alpha Vantage"
            )
            
        except Exception as e:
            self.logger.error(f"Alpha Vantage error for {symbol}: {e}")
            return None
    
    def _get_finnhub_data(self, symbol: str, api_key: str) -> Optional[StockDataResult]:
        """Finnhub 데이터 조회"""
        try:
            import requests
            
            # 실시간 가격
            url = f"https://finnhub.io/api/v1/quote"
            params = {
                'symbol': symbol,
                'token': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'c' not in data:  # current price
                return None
            
            current_price = data['c']
            prev_close = data['pc']
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100 if prev_close != 0 else 0
            
            return StockDataResult(
                symbol=symbol,
                price=float(current_price),
                change=float(change),
                change_percent=float(change_percent),
                volume=0,  # Finnhub quote doesn't include volume
                fifty_two_week_high=data.get('h'),
                fifty_two_week_low=data.get('l'),
                data_source="Finnhub"
            )
            
        except Exception as e:
            self.logger.error(f"Finnhub error for {symbol}: {e}")
            return None
    
    async def get_multiple_stocks_async(self, symbols: List[str]) -> Dict[str, StockDataResult]:
        """비동기 다중 주식 데이터 조회"""
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")
        
        tasks = []
        for symbol in symbols:
            task = self._get_stock_data_async(symbol)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        stock_data = {}
        for symbol, result in zip(symbols, results):
            if not isinstance(result, Exception) and result:
                stock_data[symbol] = result
        
        return stock_data
    
    async def _get_stock_data_async(self, symbol: str) -> Optional[StockDataResult]:
        """비동기 주식 데이터 조회"""
        # 현재는 동기 함수를 executor로 실행
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor, self.get_stock_data_sync, symbol
            )
        return result
    
    def get_data_source_status(self) -> Dict[str, Dict[str, Any]]:
        """데이터 소스 상태 확인"""
        status = {}
        for source_type, config in self.data_sources.items():
            status[source_type.value] = {
                'enabled': config.enabled,
                'priority': config.priority,
                'rate_limit': config.rate_limit,
                'has_api_key': config.api_key is not None,
                'last_success': None  # TODO: 구현
            }
        return status
    
    def test_data_sources(self, test_symbol: str = "AAPL") -> Dict[str, bool]:
        """데이터 소스 테스트"""
        results = {}
        
        for source_type, config in self.data_sources.items():
            if not config.enabled:
                results[source_type.value] = False
                continue
            
            try:
                if source_type == DataSourceType.YAHOO_FINANCE:
                    result = self._get_yahoo_finance_data(test_symbol)
                elif source_type == DataSourceType.ALPHA_VANTAGE and config.api_key:
                    result = self._get_alpha_vantage_data(test_symbol, config.api_key)
                elif source_type == DataSourceType.FINNHUB and config.api_key:
                    result = self._get_finnhub_data(test_symbol, config.api_key)
                else:
                    results[source_type.value] = False
                    continue
                
                results[source_type.value] = result is not None
                
            except Exception as e:
                self.logger.error(f"Test failed for {source_type.value}: {e}")
                results[source_type.value] = False
        
        return results

# 전역 인스턴스
multi_data_manager = MultiDataSourceManager()