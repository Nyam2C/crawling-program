#!/usr/bin/env python3
"""
Trading Engine - Core trading logic for mock trading system
모의 투자의 핵심 거래 로직
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from .models import (
    Portfolio, Transaction, OrderRequest, Stock,
    TransactionType, OrderType
)


class TradingEngine:
    """모의 투자 거래 엔진"""
    
    # 거래 수수료 및 세금 설정 (한국 주식 기준)
    COMMISSION_RATE = 0.00015  # 0.015% (증권사 수수료)
    MIN_COMMISSION = 100       # 최소 수수료 100원
    TRANSACTION_TAX_RATE = 0.0025  # 0.25% (거래세, 매도시에만)
    
    def __init__(self):
        self.portfolio = Portfolio()
        self.stock_prices: Dict[str, Stock] = {}
    
    def reset_portfolio(self, initial_balance: float = 100000.0):
        """포트폴리오 초기화"""
        self.portfolio.reset(initial_balance)
    
    def update_stock_price(self, symbol: str, price: float, company_name: str = ""):
        """주식 가격 업데이트"""
        if symbol in self.stock_prices:
            self.stock_prices[symbol].update_price(price)
        else:
            self.stock_prices[symbol] = Stock(
                symbol=symbol,
                current_price=price,
                company_name=company_name
            )
    
    def get_stock_price(self, symbol: str) -> Optional[float]:
        """주식 현재가 조회"""
        if symbol in self.stock_prices:
            return self.stock_prices[symbol].current_price
        return None
    
    def calculate_commission(self, amount: float) -> float:
        """수수료 계산"""
        commission = amount * self.COMMISSION_RATE
        return max(commission, self.MIN_COMMISSION)
    
    def calculate_tax(self, amount: float, is_sell: bool = False) -> float:
        """세금 계산 (매도시에만 적용)"""
        if is_sell:
            return amount * self.TRANSACTION_TAX_RATE
        return 0
    
    def calculate_order_cost(self, symbol: str, quantity: int, 
                           order_type: OrderType, 
                           limit_price: Optional[float] = None) -> Tuple[float, float, float, float]:
        """주문 비용 계산
        
        Returns:
            (총 비용, 순 거래금액, 수수료, 세금)
        """
        # 거래 가격 결정
        if order_type == OrderType.MARKET:
            price = self.get_stock_price(symbol)
            if price is None:
                raise ValueError(f"No price information available for {symbol}")
        else:  # LIMIT
            price = limit_price
            if price is None:
                raise ValueError("Price must be specified for limit orders")
        
        # 순 거래금액
        net_amount = quantity * price
        
        # 수수료 계산
        commission = self.calculate_commission(net_amount)
        
        # 세금 계산 (매수시에는 0)
        tax = 0
        
        # 총 비용
        total_cost = net_amount + commission + tax
        
        return total_cost, net_amount, commission, tax
    
    def can_execute_order(self, order: OrderRequest) -> Tuple[bool, str]:
        """주문 실행 가능 여부 확인"""
        if not order.validate():
            return False, "Invalid order information"
        
        # 현재가 확인
        current_price = self.get_stock_price(order.symbol)
        if current_price is None:
            return False, f"No price information available for {order.symbol}"
        
        try:
            if order.transaction_type == TransactionType.BUY:
                return self._can_buy(order)
            else:  # SELL
                return self._can_sell(order)
        except Exception as e:
            return False, str(e)
    
    def _can_buy(self, order: OrderRequest) -> Tuple[bool, str]:
        """매수 가능 여부 확인"""
        total_cost, _, _, _ = self.calculate_order_cost(
            order.symbol, order.quantity, order.order_type, order.price
        )
        
        if self.portfolio.cash_balance < total_cost:
            return False, f"Insufficient balance (Required: ${total_cost:,.2f}, Available: ${self.portfolio.cash_balance:,.2f})"
        
        return True, "Purchase available"
    
    def _can_sell(self, order: OrderRequest) -> Tuple[bool, str]:
        """매도 가능 여부 확인"""
        if order.symbol not in self.portfolio.positions:
            return False, f"You don't own {order.symbol} stock"
        
        position = self.portfolio.positions[order.symbol]
        if position.quantity < order.quantity:
            return False, f"Insufficient shares (Owned: {position.quantity}, Order: {order.quantity})"
        
        return True, "Sale available"
    
    def execute_order(self, order: OrderRequest) -> Tuple[bool, str, Optional[Transaction]]:
        """주문 실행"""
        # 실행 가능 여부 확인
        can_execute, message = self.can_execute_order(order)
        if not can_execute:
            return False, message, None
        
        try:
            if order.transaction_type == TransactionType.BUY:
                return self._execute_buy_order(order)
            else:  # SELL
                return self._execute_sell_order(order)
        except Exception as e:
            return False, f"주문 실행 중 오류: {str(e)}", None
    
    def _execute_buy_order(self, order: OrderRequest) -> Tuple[bool, str, Transaction]:
        """매수 주문 실행"""
        # 거래 가격 결정
        if order.order_type == OrderType.MARKET:
            execution_price = self.get_stock_price(order.symbol)
        else:
            execution_price = order.price
        
        # 비용 계산
        total_cost, net_amount, commission, tax = self.calculate_order_cost(
            order.symbol, order.quantity, order.order_type, order.price
        )
        
        # 거래 실행
        self.portfolio.cash_balance -= total_cost
        self.portfolio.add_position(order.symbol, order.quantity, execution_price)
        
        # 거래 내역 생성
        transaction = Transaction(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            symbol=order.symbol,
            transaction_type=order.transaction_type,
            order_type=order.order_type,
            quantity=order.quantity,
            price=execution_price,
            commission=commission,
            tax=tax,
            total_amount=total_cost
        )
        
        self.portfolio.transactions.append(transaction)
        
        return True, f"{order.symbol} {order.quantity}주 매수 완료", transaction
    
    def _execute_sell_order(self, order: OrderRequest) -> Tuple[bool, str, Transaction]:
        """매도 주문 실행"""
        # 거래 가격 결정
        if order.order_type == OrderType.MARKET:
            execution_price = self.get_stock_price(order.symbol)
        else:
            execution_price = order.price
        
        # 순 거래금액
        net_amount = order.quantity * execution_price
        
        # 수수료 및 세금 계산
        commission = self.calculate_commission(net_amount)
        tax = self.calculate_tax(net_amount, is_sell=True)
        
        # 실제 받을 금액
        proceeds = net_amount - commission - tax
        
        # 거래 실행
        self.portfolio.cash_balance += proceeds
        self.portfolio.remove_position(order.symbol, order.quantity)
        
        # 거래 내역 생성
        transaction = Transaction(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            symbol=order.symbol,
            transaction_type=order.transaction_type,
            order_type=order.order_type,
            quantity=order.quantity,
            price=execution_price,
            commission=commission,
            tax=tax,
            total_amount=proceeds  # 매도시에는 받은 금액
        )
        
        self.portfolio.transactions.append(transaction)
        
        return True, f"{order.symbol} {order.quantity}주 매도 완료", transaction
    
    def get_portfolio_summary(self) -> Dict:
        """포트폴리오 요약 정보"""
        current_prices = {symbol: stock.current_price for symbol, stock in self.stock_prices.items()}
        
        total_value = self.portfolio.get_total_value(current_prices)
        total_pnl = self.portfolio.get_total_pnl(current_prices)
        total_pnl_pct = self.portfolio.get_total_pnl_percentage(current_prices)
        
        return {
            'cash_balance': self.portfolio.cash_balance,
            'total_invested': self.portfolio.get_total_invested(),
            'total_value': total_value,
            'total_pnl': total_pnl,
            'total_pnl_percentage': total_pnl_pct,
            'initial_balance': self.portfolio.initial_balance,
            'positions_count': len(self.portfolio.positions)
        }
    
    def get_positions_summary(self) -> List[Dict]:
        """보유 주식 요약"""
        positions = []
        
        for symbol, position in self.portfolio.positions.items():
            current_price = self.get_stock_price(symbol)
            if current_price is None:
                current_price = position.average_price  # fallback
            
            current_value = position.get_current_value(current_price)
            pnl = position.get_pnl(current_price)
            pnl_pct = position.get_pnl_percentage(current_price)
            
            positions.append({
                'symbol': symbol,
                'quantity': position.quantity,
                'average_price': position.average_price,
                'current_price': current_price,
                'total_invested': position.total_invested,
                'current_value': current_value,
                'pnl': pnl,
                'pnl_percentage': pnl_pct
            })
        
        return positions
    
    def get_recent_transactions(self, limit: int = 10) -> List[Transaction]:
        """최근 거래 내역"""
        return sorted(
            self.portfolio.transactions,
            key=lambda t: t.timestamp,
            reverse=True
        )[:limit]