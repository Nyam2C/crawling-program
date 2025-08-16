#!/usr/bin/env python3
"""
Trading Models - Data classes for mock trading system
모의 투자를 위한 데이터 모델들
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Literal
from enum import Enum


class OrderType(Enum):
    """주문 유형"""
    MARKET = "market"  # 시장가
    LIMIT = "limit"    # 지정가


class TransactionType(Enum):
    """거래 유형"""
    BUY = "buy"     # 매수
    SELL = "sell"   # 매도


@dataclass
class Stock:
    """주식 정보"""
    symbol: str
    current_price: float
    last_updated: datetime = field(default_factory=datetime.now)
    company_name: str = ""
    
    def update_price(self, new_price: float):
        """주식 가격 업데이트"""
        self.current_price = new_price
        self.last_updated = datetime.now()


@dataclass
class Position:
    """포지션 (보유 주식)"""
    symbol: str
    quantity: int
    average_price: float  # 평균 매입가
    total_invested: float  # 총 투자금액
    
    def add_shares(self, quantity: int, price: float):
        """주식 추가 (매수)"""
        new_total_invested = self.total_invested + (quantity * price)
        new_quantity = self.quantity + quantity
        self.average_price = new_total_invested / new_quantity
        self.quantity = new_quantity
        self.total_invested = new_total_invested
    
    def remove_shares(self, quantity: int) -> bool:
        """주식 제거 (매도)"""
        if quantity > self.quantity:
            return False
        
        self.quantity -= quantity
        if self.quantity == 0:
            self.total_invested = 0
            self.average_price = 0
        else:
            self.total_invested = self.quantity * self.average_price
        
        return True
    
    def get_current_value(self, current_price: float) -> float:
        """현재 평가 금액"""
        return self.quantity * current_price
    
    def get_pnl(self, current_price: float) -> float:
        """손익 계산"""
        return self.get_current_value(current_price) - self.total_invested
    
    def get_pnl_percentage(self, current_price: float) -> float:
        """손익률 계산"""
        if self.total_invested == 0:
            return 0
        return (self.get_pnl(current_price) / self.total_invested) * 100


@dataclass
class Transaction:
    """거래 내역"""
    id: str
    timestamp: datetime
    symbol: str
    transaction_type: TransactionType
    order_type: OrderType
    quantity: int
    price: float
    commission: float  # 수수료
    tax: float        # 세금
    total_amount: float  # 총 거래 금액 (수수료, 세금 포함)
    
    def get_net_amount(self) -> float:
        """순 거래 금액 (수수료, 세금 제외)"""
        return self.quantity * self.price


@dataclass
class Portfolio:
    """포트폴리오 (전체 계좌 정보)"""
    cash_balance: float = 100000.0  # 현금 잔고 (기본 $100,000)
    positions: Dict[str, Position] = field(default_factory=dict)  # 보유 주식들
    transactions: List[Transaction] = field(default_factory=list)  # 거래 내역
    initial_balance: float = 100000.0  # 초기 자금 (기본 $100,000)
    
    def get_total_invested(self) -> float:
        """총 투자 금액"""
        return sum(pos.total_invested for pos in self.positions.values())
    
    def get_total_value(self, stock_prices: Dict[str, float]) -> float:
        """총 평가 금액"""
        total = self.cash_balance
        for symbol, position in self.positions.items():
            if symbol in stock_prices:
                total += position.get_current_value(stock_prices[symbol])
        return total
    
    def get_total_pnl(self, stock_prices: Dict[str, float]) -> float:
        """총 손익"""
        return self.get_total_value(stock_prices) - self.initial_balance
    
    def get_total_pnl_percentage(self, stock_prices: Dict[str, float]) -> float:
        """총 손익률"""
        if self.initial_balance == 0:
            return 0
        return (self.get_total_pnl(stock_prices) / self.initial_balance) * 100
    
    def can_buy(self, quantity: int, price: float, commission: float, tax: float) -> bool:
        """매수 가능 여부 확인"""
        total_cost = (quantity * price) + commission + tax
        return self.cash_balance >= total_cost
    
    def add_position(self, symbol: str, quantity: int, price: float):
        """포지션 추가 또는 업데이트"""
        if symbol in self.positions:
            self.positions[symbol].add_shares(quantity, price)
        else:
            self.positions[symbol] = Position(
                symbol=symbol,
                quantity=quantity,
                average_price=price,
                total_invested=quantity * price
            )
    
    def remove_position(self, symbol: str, quantity: int) -> bool:
        """포지션 제거 또는 감소"""
        if symbol not in self.positions:
            return False
        
        position = self.positions[symbol]
        success = position.remove_shares(quantity)
        
        # 모든 주식을 매도한 경우 포지션 삭제
        if success and position.quantity == 0:
            del self.positions[symbol]
        
        return success
    
    def reset(self, initial_balance: float = 100000.0):
        """계좌 초기화"""
        self.cash_balance = initial_balance
        self.initial_balance = initial_balance
        self.positions.clear()
        self.transactions.clear()


@dataclass
class OrderRequest:
    """주문 요청"""
    symbol: str
    transaction_type: TransactionType
    order_type: OrderType
    quantity: int
    price: Optional[float] = None  # 지정가 주문시 사용
    
    def validate(self) -> bool:
        """주문 요청 유효성 검사"""
        if self.quantity <= 0:
            return False
        if self.order_type == OrderType.LIMIT and (self.price is None or self.price <= 0):
            return False
        return True