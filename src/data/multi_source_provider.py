#!/usr/bin/env python3
"""
Multi-Source Data Provider - 다중 데이터 소스 지원 및 폴백 시스템
"""

import asyncio
import aiohttp
import yfinance as yf
import json
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
import pickle
import hashlib


class DataSource(Enum):
    """데이터 소스 타입"""
    YAHOO_FINANCE = "yahoo_finance"
    ALPHA_VANTAGE = "alpha_vantage"
    POLYGON = "polygon"
    CACHE = "cache"


@dataclass
class StockData:
    """주식 데이터 표준 포맷"""
    symbol: str
    current_price: float
    change: float
    change_percent: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    high_52w: Optional[float] = None
    low_52w: Optional[float] = None
    timestamp: float = None
    source: DataSource = DataSource.CACHE
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class DataSourceConfig:
    """데이터 소스 설정"""
    
    def __init__(self):
        self.sources = {
            DataSource.YAHOO_FINANCE: {
                "enabled": True,
                "priority": 1,
                "rate_limit": 2000,  # 시간당 요청 제한
                "timeout": 10,
                "retry_count": 3
            },
            DataSource.ALPHA_VANTAGE: {
                "enabled": False,  # API 키 필요
                "priority": 2,
                "rate_limit": 500,
                "timeout": 15,
                "retry_count": 2,
                "api_key": None
            },
            DataSource.POLYGON: {
                "enabled": False,  # API 키 필요
                "priority": 3,
                "rate_limit": 1000,
                "timeout": 12,
                "retry_count": 2,
                "api_key": None
            }
        }
        
        # 설정 파일에서 로드
        self.load_config()
    
    def load_config(self):
        """설정 파일에서 데이터 소스 설정 로드"""
        config_file = Path("data_source_config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    for source_name, settings in config.items():
                        if hasattr(DataSource, source_name.upper()):
                            source = DataSource(source_name.lower())
                            if source in self.sources:
                                self.sources[source].update(settings)
            except Exception as e:
                logging.warning(f"Failed to load data source config: {e}")
    
    def save_config(self):
        """현재 설정을 파일로 저장"""
        config_file = Path("data_source_config.json")
        try:
            config = {}
            for source, settings in self.sources.items():
                config[source.value] = settings
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save data source config: {e}")


class DataCache:
    """데이터 캐싱 시스템"""
    
    def __init__(self, cache_dir: str = "cache", cache_ttl: int = 60):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_ttl = cache_ttl  # 캐시 유효 시간 (초)
        self.memory_cache = {}  # 메모리 캐시
        
    def _get_cache_key(self, symbol: str, data_type: str = "quote") -> str:
        """캐시 키 생성"""
        return hashlib.md5(f"{symbol}_{data_type}".encode()).hexdigest()
    
    def get_cache_file(self, cache_key: str) -> Path:
        """캐시 파일 경로"""
        return self.cache_dir / f"{cache_key}.pkl"
    
    def set_cache(self, symbol: str, data: StockData, data_type: str = "quote"):
        """캐시에 데이터 저장"""
        cache_key = self._get_cache_key(symbol, data_type)
        
        # 메모리 캐시
        self.memory_cache[cache_key] = {
            "data": data,
            "timestamp": time.time()
        }
        
        # 파일 캐시
        try:
            cache_file = self.get_cache_file(cache_key)
            with open(cache_file, 'wb') as f:
                pickle.dump({
                    "data": data,
                    "timestamp": time.time()
                }, f)
        except Exception as e:
            logging.error(f"Failed to save cache for {symbol}: {e}")
    
    def get_cache(self, symbol: str, data_type: str = "quote") -> Optional[StockData]:
        """캐시에서 데이터 조회"""
        cache_key = self._get_cache_key(symbol, data_type)
        current_time = time.time()
        
        # 메모리 캐시 먼저 확인
        if cache_key in self.memory_cache:
            cache_entry = self.memory_cache[cache_key]
            if current_time - cache_entry["timestamp"] < self.cache_ttl:
                cache_entry["data"].source = DataSource.CACHE
                return cache_entry["data"]
            else:
                del self.memory_cache[cache_key]
        
        # 파일 캐시 확인
        try:
            cache_file = self.get_cache_file(cache_key)
            if cache_file.exists():
                with open(cache_file, 'rb') as f:
                    cache_entry = pickle.load(f)
                    if current_time - cache_entry["timestamp"] < self.cache_ttl:
                        cache_entry["data"].source = DataSource.CACHE
                        return cache_entry["data"]
                    else:
                        cache_file.unlink()  # 만료된 캐시 삭제
        except Exception as e:
            logging.error(f"Failed to load cache for {symbol}: {e}")
        
        return None
    
    def clear_expired_cache(self):
        """만료된 캐시 정리"""
        current_time = time.time()
        
        # 메모리 캐시 정리
        expired_keys = []
        for key, entry in self.memory_cache.items():
            if current_time - entry["timestamp"] >= self.cache_ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.memory_cache[key]
        
        # 파일 캐시 정리
        for cache_file in self.cache_dir.glob("*.pkl"):
            try:
                if cache_file.stat().st_mtime < current_time - self.cache_ttl:
                    cache_file.unlink()
            except Exception:
                pass


class RateLimiter:
    """API 요청 제한 관리"""
    
    def __init__(self):
        self.request_history = {}  # source -> list of timestamps
    
    async def wait_if_needed(self, source: DataSource, rate_limit: int):
        """필요 시 대기"""
        if source not in self.request_history:
            self.request_history[source] = []
        
        current_time = time.time()
        history = self.request_history[source]
        
        # 1시간 이전 기록 제거
        history[:] = [t for t in history if current_time - t < 3600]
        
        # 제한 확인
        if len(history) >= rate_limit:
            # 가장 오래된 요청 이후 1시간 대기
            wait_time = 3600 - (current_time - history[0])
            if wait_time > 0:
                logging.warning(f"Rate limit reached for {source.value}, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
                history.clear()
        
        # 현재 요청 기록
        history.append(current_time)


class MultiSourceDataProvider:
    """다중 소스 데이터 제공자"""
    
    def __init__(self):
        self.config = DataSourceConfig()
        self.cache = DataCache()
        self.rate_limiter = RateLimiter()
        self.logger = logging.getLogger(__name__)
        
        # 세션 관리
        self.session = None
        
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self.session:
            await self.session.close()
    
    async def get_stock_data(self, symbol: str, use_cache: bool = True) -> Optional[StockData]:
        """주식 데이터 조회 (폴백 지원)"""
        # 캐시에서 먼저 확인
        if use_cache:
            cached_data = self.cache.get_cache(symbol)
            if cached_data:
                return cached_data
        
        # 활성화된 소스들을 우선순위순으로 정렬
        enabled_sources = [
            (source, config) for source, config in self.config.sources.items()
            if config.get("enabled", False)
        ]
        enabled_sources.sort(key=lambda x: x[1].get("priority", 999))
        
        # 각 소스에서 시도
        for source, source_config in enabled_sources:
            try:
                data = await self._fetch_from_source(symbol, source, source_config)
                if data:
                    # 캐시에 저장
                    self.cache.set_cache(symbol, data)
                    return data
            except Exception as e:
                self.logger.warning(f"Failed to fetch {symbol} from {source.value}: {e}")
                continue
        
        # 모든 소스 실패 시 오래된 캐시라도 반환
        cached_data = self.cache.get_cache(symbol)
        if cached_data:
            self.logger.info(f"Using stale cache for {symbol}")
            return cached_data
        
        self.logger.error(f"Failed to fetch data for {symbol} from all sources")
        return None
    
    async def _fetch_from_source(self, symbol: str, source: DataSource, config: Dict) -> Optional[StockData]:
        """특정 소스에서 데이터 조회"""
        # 요청 제한 확인
        await self.rate_limiter.wait_if_needed(source, config.get("rate_limit", 1000))
        
        if source == DataSource.YAHOO_FINANCE:
            return await self._fetch_yahoo_finance(symbol, config)
        elif source == DataSource.ALPHA_VANTAGE:
            return await self._fetch_alpha_vantage(symbol, config)
        elif source == DataSource.POLYGON:
            return await self._fetch_polygon(symbol, config)
        else:
            return None
    
    async def _fetch_yahoo_finance(self, symbol: str, config: Dict) -> Optional[StockData]:
        """Yahoo Finance에서 데이터 조회"""
        try:
            # yfinance는 동기 라이브러리이므로 executor에서 실행
            loop = asyncio.get_event_loop()
            ticker = await loop.run_in_executor(None, yf.Ticker, symbol)
            info = await loop.run_in_executor(None, lambda: ticker.info)
            hist = await loop.run_in_executor(None, lambda: ticker.history(period="2d"))
            
            if hist.empty or len(hist) == 0:
                return None
            
            current_price = float(hist['Close'].iloc[-1])
            
            # 전일 대비 변화 계산
            if len(hist) > 1:
                prev_price = float(hist['Close'].iloc[-2])
                change = current_price - prev_price
                change_percent = (change / prev_price) * 100
            else:
                change = 0.0
                change_percent = 0.0
            
            return StockData(
                symbol=symbol,
                current_price=current_price,
                change=change,
                change_percent=change_percent,
                volume=int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
                market_cap=info.get('marketCap'),
                pe_ratio=info.get('trailingPE'),
                dividend_yield=info.get('dividendYield'),
                high_52w=info.get('fiftyTwoWeekHigh'),
                low_52w=info.get('fiftyTwoWeekLow'),
                source=DataSource.YAHOO_FINANCE
            )
            
        except Exception as e:
            self.logger.error(f"Yahoo Finance error for {symbol}: {e}")
            return None
    
    async def _fetch_alpha_vantage(self, symbol: str, config: Dict) -> Optional[StockData]:
        """Alpha Vantage에서 데이터 조회"""
        api_key = config.get("api_key")
        if not api_key:
            return None
        
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": api_key
            }
            
            async with self.session.get(url, params=params, timeout=config.get("timeout", 10)) as response:
                if response.status != 200:
                    return None
                
                data = await response.json()
                quote = data.get("Global Quote", {})
                
                if not quote:
                    return None
                
                return StockData(
                    symbol=symbol,
                    current_price=float(quote.get("05. price", 0)),
                    change=float(quote.get("09. change", 0)),
                    change_percent=float(quote.get("10. change percent", "0%").replace("%", "")),
                    volume=int(quote.get("06. volume", 0)),
                    high_52w=float(quote.get("03. high", 0)),
                    low_52w=float(quote.get("04. low", 0)),
                    source=DataSource.ALPHA_VANTAGE
                )
                
        except Exception as e:
            self.logger.error(f"Alpha Vantage error for {symbol}: {e}")
            return None
    
    async def _fetch_polygon(self, symbol: str, config: Dict) -> Optional[StockData]:
        """Polygon.io에서 데이터 조회"""
        api_key = config.get("api_key")
        if not api_key:
            return None
        
        try:
            # 현재 가격 조회
            url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev"
            params = {"apikey": api_key}
            
            async with self.session.get(url, params=params, timeout=config.get("timeout", 10)) as response:
                if response.status != 200:
                    return None
                
                data = await response.json()
                results = data.get("results", [])
                
                if not results:
                    return None
                
                result = results[0]
                current_price = float(result.get("c", 0))  # close price
                open_price = float(result.get("o", 0))     # open price
                
                change = current_price - open_price
                change_percent = (change / open_price) * 100 if open_price > 0 else 0
                
                return StockData(
                    symbol=symbol,
                    current_price=current_price,
                    change=change,
                    change_percent=change_percent,
                    volume=int(result.get("v", 0)),
                    high_52w=float(result.get("h", 0)),
                    low_52w=float(result.get("l", 0)),
                    source=DataSource.POLYGON
                )
                
        except Exception as e:
            self.logger.error(f"Polygon error for {symbol}: {e}")
            return None
    
    async def get_multiple_stocks(self, symbols: List[str], use_cache: bool = True) -> Dict[str, Optional[StockData]]:
        """여러 주식 데이터 동시 조회"""
        tasks = [self.get_stock_data(symbol, use_cache) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        stock_data = {}
        for symbol, result in zip(symbols, results):
            if isinstance(result, Exception):
                self.logger.error(f"Error fetching {symbol}: {result}")
                stock_data[symbol] = None
            else:
                stock_data[symbol] = result
        
        return stock_data
    
    def get_source_status(self) -> Dict[str, Dict[str, Any]]:
        """데이터 소스 상태 확인"""
        status = {}
        
        for source, config in self.config.sources.items():
            request_count = len(self.rate_limiter.request_history.get(source, []))
            
            status[source.value] = {
                "enabled": config.get("enabled", False),
                "priority": config.get("priority", 999),
                "rate_limit": config.get("rate_limit", 0),
                "recent_requests": request_count,
                "has_api_key": bool(config.get("api_key"))
            }
        
        return status
    
    def update_source_config(self, source: DataSource, **kwargs):
        """데이터 소스 설정 업데이트"""
        if source in self.config.sources:
            self.config.sources[source].update(kwargs)
            self.config.save_config()
    
    def clear_cache(self):
        """캐시 완전 삭제"""
        self.cache.memory_cache.clear()
        for cache_file in self.cache.cache_dir.glob("*.pkl"):
            try:
                cache_file.unlink()
            except Exception:
                pass


# 편의 함수들
async def get_stock_quote(symbol: str, use_cache: bool = True) -> Optional[StockData]:
    """단일 주식 시세 조회"""
    async with MultiSourceDataProvider() as provider:
        return await provider.get_stock_data(symbol, use_cache)


async def get_multiple_quotes(symbols: List[str], use_cache: bool = True) -> Dict[str, Optional[StockData]]:
    """여러 주식 시세 동시 조회"""
    async with MultiSourceDataProvider() as provider:
        return await provider.get_multiple_stocks(symbols, use_cache)