#!/usr/bin/env python3
"""
Data Manager for Mock Trading - Handles persistence and stock data
모의 투자 데이터 관리자 - 데이터 저장 및 주식 정보 관리
"""

from __future__ import annotations
import json
import os
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import asdict

from src.data.yfinance_data_source import YFinanceDataSource
from .models import Portfolio, Transaction, Position, TransactionType, OrderType
from .trading_engine import TradingEngine


class TradingDataManager:
    """모의 투자 데이터 관리자"""
    
    def __init__(self, data_file: str = "mock_trading_data.json"):
        self.data_file = data_file
        self.trading_engine = TradingEngine()
        self.yfinance_source = YFinanceDataSource()
        
        # 자동 갱신을 위한 스레드
        self.auto_refresh_enabled = False
        self.auto_refresh_thread = None
        self.refresh_interval = 20  # 20초
        
        # 추적할 주식 목록
        self.watched_stocks: Set[str] = set()
        
        # 데이터 로드
        self.load_data()
    
    def add_watched_stock(self, symbol: str):
        """감시할 주식 추가"""
        self.watched_stocks.add(symbol.upper())
        self.refresh_stock_price(symbol)
    
    def remove_watched_stock(self, symbol: str):
        """감시 주식 제거"""
        self.watched_stocks.discard(symbol.upper())
    
    def get_portfolio(self) -> Portfolio:
        """현재 포트폴리오 반환"""
        return self.trading_engine.portfolio
    
    def get_trading_engine(self) -> TradingEngine:
        """트레이딩 엔진 반환"""
        return self.trading_engine
    
    def get_watched_stocks(self) -> List[str]:
        """감시 중인 주식 목록"""
        return list(self.watched_stocks)
    
    def refresh_stock_price(self, symbol: str) -> Optional[float]:
        """Refresh stock price for specific symbol"""
        try:
            stock_data = self.yfinance_source.get_stock_data(symbol)
            if stock_data and 'current_price' in stock_data:
                # Handle both string and float formats
                price_str = stock_data['current_price']
                if isinstance(price_str, str):
                    # Remove $ and convert to float
                    price = float(price_str.replace('$', '').replace(',', ''))
                else:
                    price = float(price_str)
                
                company_name = stock_data.get('company', stock_data.get('company_name', symbol))
                
                self.trading_engine.update_stock_price(symbol, price, company_name)
                return price
        except Exception as e:
            print(f"Error refreshing {symbol}: {e}")
        
        return None
    
    def refresh_all_watched_stocks(self):
        """모든 감시 주식의 가격 갱신"""
        for symbol in self.watched_stocks.copy():  # copy to avoid modification during iteration
            self.refresh_stock_price(symbol)
    
    def start_auto_refresh(self):
        """자동 갱신 시작"""
        if self.auto_refresh_enabled:
            return
        
        self.auto_refresh_enabled = True
        self.auto_refresh_thread = threading.Thread(target=self._auto_refresh_loop, daemon=True)
        self.auto_refresh_thread.start()
    
    def stop_auto_refresh(self):
        """자동 갱신 중지"""
        self.auto_refresh_enabled = False
        if self.auto_refresh_thread:
            self.auto_refresh_thread.join(timeout=1)
    
    def _auto_refresh_loop(self):
        """자동 갱신 루프"""
        while self.auto_refresh_enabled:
            try:
                if self.watched_stocks:
                    self.refresh_all_watched_stocks()
                time.sleep(self.refresh_interval)
            except Exception as e:
                print(f"Auto refresh error: {e}")
                time.sleep(self.refresh_interval)
    
    def search_stock(self, symbol: str) -> Optional[Dict]:
        """Search stock and retrieve information"""
        try:
            stock_data = self.yfinance_source.get_stock_data(symbol)
            if stock_data and stock_data.get('valid', False):
                # Handle price format conversion
                price_str = stock_data.get('current_price', '0')
                if isinstance(price_str, str):
                    price = float(price_str.replace('$', '').replace(',', ''))
                else:
                    price = float(price_str)
                
                return {
                    'symbol': symbol.upper(),
                    'company_name': stock_data.get('company', symbol),
                    'current_price': price,
                    'currency': 'USD',
                    'market': 'US'
                }
        except Exception as e:
            print(f"Error searching stock {symbol}: {e}")
        
        return None
    
    def save_data(self):
        """데이터를 파일에 저장"""
        try:
            data = {
                'portfolio': self._portfolio_to_dict(),
                'stock_prices': self._stock_prices_to_dict(),
                'watched_stocks': list(self.watched_stocks),
                'last_saved': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """파일에서 데이터 로드"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 포트폴리오 로드
            if 'portfolio' in data:
                self._load_portfolio_from_dict(data['portfolio'])
            
            # 주식 가격 로드
            if 'stock_prices' in data:
                self._load_stock_prices_from_dict(data['stock_prices'])
            
            # 감시 주식 로드
            if 'watched_stocks' in data:
                self.watched_stocks = set(data['watched_stocks'])
                
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def _portfolio_to_dict(self) -> Dict:
        """포트폴리오를 딕셔너리로 변환"""
        portfolio = self.trading_engine.portfolio
        
        return {
            'cash_balance': portfolio.cash_balance,
            'initial_balance': portfolio.initial_balance,
            'positions': {
                symbol: {
                    'symbol': pos.symbol,
                    'quantity': pos.quantity,
                    'average_price': pos.average_price,
                    'total_invested': pos.total_invested
                }
                for symbol, pos in portfolio.positions.items()
            },
            'transactions': [
                {
                    'id': trans.id,
                    'timestamp': trans.timestamp.isoformat(),
                    'symbol': trans.symbol,
                    'transaction_type': trans.transaction_type.value,
                    'order_type': trans.order_type.value,
                    'quantity': trans.quantity,
                    'price': trans.price,
                    'commission': trans.commission,
                    'tax': trans.tax,
                    'total_amount': trans.total_amount
                }
                for trans in portfolio.transactions
            ]
        }
    
    def _load_portfolio_from_dict(self, data: Dict):
        """딕셔너리에서 포트폴리오 로드"""
        portfolio = self.trading_engine.portfolio
        
        portfolio.cash_balance = data.get('cash_balance', 1000000.0)
        portfolio.initial_balance = data.get('initial_balance', 1000000.0)
        
        # 포지션 로드
        positions_data = data.get('positions', {})
        for symbol, pos_data in positions_data.items():
            position = Position(
                symbol=pos_data['symbol'],
                quantity=pos_data['quantity'],
                average_price=pos_data['average_price'],
                total_invested=pos_data['total_invested']
            )
            portfolio.positions[symbol] = position
        
        # 거래 내역 로드
        transactions_data = data.get('transactions', [])
        for trans_data in transactions_data:
            transaction = Transaction(
                id=trans_data['id'],
                timestamp=datetime.fromisoformat(trans_data['timestamp']),
                symbol=trans_data['symbol'],
                transaction_type=TransactionType(trans_data['transaction_type']),
                order_type=OrderType(trans_data['order_type']),
                quantity=trans_data['quantity'],
                price=trans_data['price'],
                commission=trans_data['commission'],
                tax=trans_data['tax'],
                total_amount=trans_data['total_amount']
            )
            portfolio.transactions.append(transaction)
    
    def _stock_prices_to_dict(self) -> Dict:
        """주식 가격을 딕셔너리로 변환"""
        return {
            symbol: {
                'symbol': stock.symbol,
                'current_price': stock.current_price,
                'last_updated': stock.last_updated.isoformat(),
                'company_name': stock.company_name
            }
            for symbol, stock in self.trading_engine.stock_prices.items()
        }
    
    def _load_stock_prices_from_dict(self, data: Dict):
        """딕셔너리에서 주식 가격 로드"""
        for symbol, stock_data in data.items():
            self.trading_engine.update_stock_price(
                symbol=stock_data['symbol'],
                price=stock_data['current_price'],
                company_name=stock_data.get('company_name', '')
            )
            
            # 마지막 업데이트 시간 설정
            if 'last_updated' in stock_data:
                try:
                    self.trading_engine.stock_prices[symbol].last_updated = \
                        datetime.fromisoformat(stock_data['last_updated'])
                except:
                    pass
    
    def reset_portfolio(self, initial_balance: float = 100000.0):
        """포트폴리오 초기화"""
        self.trading_engine.reset_portfolio(initial_balance)
        self.save_data()
    
    def get_trading_engine(self) -> TradingEngine:
        """거래 엔진 반환"""
        return self.trading_engine
    
    def close(self):
        """리소스 정리"""
        self.stop_auto_refresh()
        self.save_data()
        if hasattr(self.yfinance_source, 'close'):
            self.yfinance_source.close()