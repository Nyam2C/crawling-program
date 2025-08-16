#!/usr/bin/env python3
"""
Action Manager - Handles undo/redo functionality for user actions
"""

try:
    from typing import List, Optional, Any, Dict, Callable
except ImportError:
    # Fallback for very old Python versions
    List = list
    Optional = lambda x: x
    Any = object
    Dict = dict
    Callable = object
from datetime import datetime
import copy

class Action:
    """User action data class"""
    def __init__(self, action_type: str, description: str, timestamp: datetime, 
                 undo_data: Dict[str, Any], redo_data: Dict[str, Any],
                 undo_callback: Optional[Callable] = None, redo_callback: Optional[Callable] = None):
        self.action_type = action_type
        self.description = description
        self.timestamp = timestamp
        self.undo_data = undo_data
        self.redo_data = redo_data
        self.undo_callback = undo_callback
        self.redo_callback = redo_callback

class ActionManager:
    """Undo/redo action management class"""
    
    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self.action_history: List[Action] = []
        self.current_position = -1
        self.main_app = None
        
    def set_main_app(self, main_app):
        """메인 앱 참조 설정"""
        self.main_app = main_app
    
    def record_action(self, action_type: str, description: str, 
                     undo_data: Dict[str, Any], redo_data: Dict[str, Any],
                     undo_callback: Optional[Callable] = None, 
                     redo_callback: Optional[Callable] = None):
        """새로운 액션 기록"""
        
        # 현재 위치 이후의 히스토리 제거 (새로운 액션으로 분기)
        if self.current_position < len(self.action_history) - 1:
            self.action_history = self.action_history[:self.current_position + 1]
        
        # 새 액션 생성
        action = Action(
            action_type=action_type,
            description=description,
            timestamp=datetime.now(),
            undo_data=copy.deepcopy(undo_data),
            redo_data=copy.deepcopy(redo_data),
            undo_callback=undo_callback,
            redo_callback=redo_callback
        )
        
        # 히스토리에 추가
        self.action_history.append(action)
        self.current_position = len(self.action_history) - 1
        
        # 최대 히스토리 크기 유지
        if len(self.action_history) > self.max_history:
            self.action_history.pop(0)
            self.current_position -= 1
        
        self._update_ui_state()
    
    def undo(self) -> bool:
        """마지막 액션 실행취소"""
        if not self.can_undo():
            if self.main_app:
                self.main_app.update_status("실행취소할 작업이 없습니다")
            return False
        
        action = self.action_history[self.current_position]
        
        try:
            # 커스텀 실행취소 콜백이 있는 경우
            if action.undo_callback:
                action.undo_callback(action.undo_data)
            else:
                # 기본 실행취소 로직
                self._execute_default_undo(action)
            
            self.current_position -= 1
            self._update_ui_state()
            
            if self.main_app:
                self.main_app.update_status(f"실행취소: {action.description}")
            
            return True
            
        except Exception as e:
            if self.main_app:
                self.main_app.show_error(f"실행취소 실패: {e}")
            return False
    
    def redo(self) -> bool:
        """마지막 실행취소 다시실행"""
        if not self.can_redo():
            if self.main_app:
                self.main_app.update_status("다시실행할 작업이 없습니다")
            return False
        
        self.current_position += 1
        action = self.action_history[self.current_position]
        
        try:
            # 커스텀 다시실행 콜백이 있는 경우
            if action.redo_callback:
                action.redo_callback(action.redo_data)
            else:
                # 기본 다시실행 로직
                self._execute_default_redo(action)
            
            self._update_ui_state()
            
            if self.main_app:
                self.main_app.update_status(f"다시실행: {action.description}")
            
            return True
            
        except Exception as e:
            self.current_position -= 1  # 실패 시 위치 복원
            if self.main_app:
                self.main_app.show_error(f"다시실행 실패: {e}")
            return False
    
    def can_undo(self) -> bool:
        """실행취소 가능 여부"""
        return self.current_position >= 0
    
    def can_redo(self) -> bool:
        """다시실행 가능 여부"""
        return self.current_position < len(self.action_history) - 1
    
    def get_undo_description(self) -> Optional[str]:
        """현재 실행취소할 작업 설명"""
        if self.can_undo():
            return self.action_history[self.current_position].description
        return None
    
    def get_redo_description(self) -> Optional[str]:
        """현재 다시실행할 작업 설명"""
        if self.can_redo():
            return self.action_history[self.current_position + 1].description
        return None
    
    def clear_history(self):
        """히스토리 초기화"""
        self.action_history.clear()
        self.current_position = -1
        self._update_ui_state()
    
    def get_history_summary(self) -> List[str]:
        """히스토리 요약 정보"""
        summary = []
        for i, action in enumerate(self.action_history):
            status = "●" if i == self.current_position else "○"
            timestamp = action.timestamp.strftime("%H:%M:%S")
            summary.append(f"{status} [{timestamp}] {action.description}")
        return summary
    
    def _execute_default_undo(self, action: Action):
        """기본 실행취소 로직"""
        action_type = action.action_type
        undo_data = action.undo_data
        
        if action_type == "add_stock":
            self._undo_add_stock(undo_data)
        elif action_type == "remove_stock":
            self._undo_remove_stock(undo_data)
        elif action_type == "trade_execution":
            self._undo_trade_execution(undo_data)
        elif action_type == "portfolio_change":
            self._undo_portfolio_change(undo_data)
        elif action_type == "settings_change":
            self._undo_settings_change(undo_data)
        else:
            raise NotImplementedError(f"Unknown action type: {action_type}")
    
    def _execute_default_redo(self, action: Action):
        """기본 다시실행 로직"""
        action_type = action.action_type
        redo_data = action.redo_data
        
        if action_type == "add_stock":
            self._redo_add_stock(redo_data)
        elif action_type == "remove_stock":
            self._redo_remove_stock(redo_data)
        elif action_type == "trade_execution":
            self._redo_trade_execution(redo_data)
        elif action_type == "portfolio_change":
            self._redo_portfolio_change(redo_data)
        elif action_type == "settings_change":
            self._redo_settings_change(redo_data)
        else:
            raise NotImplementedError(f"Unknown action type: {action_type}")
    
    # === 주식 관련 실행취소/다시실행 ===
    
    def _undo_add_stock(self, undo_data: Dict[str, Any]):
        """주식 추가 실행취소"""
        symbol = undo_data.get('symbol')
        if symbol and self.main_app and hasattr(self.main_app, 'stock_data_tab'):
            self.main_app.stock_data_tab.remove_stock_silent(symbol)
    
    def _redo_add_stock(self, redo_data: Dict[str, Any]):
        """주식 추가 다시실행"""
        symbol = redo_data.get('symbol')
        if symbol and self.main_app and hasattr(self.main_app, 'stock_data_tab'):
            self.main_app.stock_data_tab.add_stock_silent(symbol)
    
    def _undo_remove_stock(self, undo_data: Dict[str, Any]):
        """주식 제거 실행취소"""
        symbol = undo_data.get('symbol')
        stock_data = undo_data.get('stock_data')
        if symbol and stock_data and self.main_app and hasattr(self.main_app, 'stock_data_tab'):
            self.main_app.stock_data_tab.restore_stock_silent(symbol, stock_data)
    
    def _redo_remove_stock(self, redo_data: Dict[str, Any]):
        """주식 제거 다시실행"""
        symbol = redo_data.get('symbol')
        if symbol and self.main_app and hasattr(self.main_app, 'stock_data_tab'):
            self.main_app.stock_data_tab.remove_stock_silent(symbol)
    
    # === 거래 관련 실행취소/다시실행 ===
    
    def _undo_trade_execution(self, undo_data: Dict[str, Any]):
        """거래 실행 실행취소"""
        trade_id = undo_data.get('trade_id')
        portfolio_state = undo_data.get('portfolio_state')
        
        if self.main_app and hasattr(self.main_app, 'mock_trading_tab'):
            trading_tab = self.main_app.mock_trading_tab
            if hasattr(trading_tab, 'data_manager'):
                # 포트폴리오 상태 복원
                trading_tab.data_manager.restore_portfolio_state(portfolio_state)
                trading_tab.refresh_displays()
    
    def _redo_trade_execution(self, redo_data: Dict[str, Any]):
        """거래 실행 다시실행"""
        trade_data = redo_data.get('trade_data')
        
        if trade_data and self.main_app and hasattr(self.main_app, 'mock_trading_tab'):
            trading_tab = self.main_app.mock_trading_tab
            symbol = trade_data.get('symbol')
            quantity = trade_data.get('quantity')
            order_type = trade_data.get('order_type')
            
            if symbol and quantity and order_type:
                trading_tab.execute_trade_silent(symbol, quantity, order_type)
    
    # === 포트폴리오 관련 실행취소/다시실행 ===
    
    def _undo_portfolio_change(self, undo_data: Dict[str, Any]):
        """포트폴리오 변경 실행취소"""
        previous_state = undo_data.get('previous_state')
        
        if previous_state and self.main_app and hasattr(self.main_app, 'mock_trading_tab'):
            trading_tab = self.main_app.mock_trading_tab
            if hasattr(trading_tab, 'data_manager'):
                trading_tab.data_manager.restore_portfolio_state(previous_state)
                trading_tab.refresh_displays()
    
    def _redo_portfolio_change(self, redo_data: Dict[str, Any]):
        """포트폴리오 변경 다시실행"""
        new_state = redo_data.get('new_state')
        
        if new_state and self.main_app and hasattr(self.main_app, 'mock_trading_tab'):
            trading_tab = self.main_app.mock_trading_tab
            if hasattr(trading_tab, 'data_manager'):
                trading_tab.data_manager.restore_portfolio_state(new_state)
                trading_tab.refresh_displays()
    
    # === 설정 관련 실행취소/다시실행 ===
    
    def _undo_settings_change(self, undo_data: Dict[str, Any]):
        """설정 변경 실행취소"""
        previous_settings = undo_data.get('previous_settings')
        
        if previous_settings and self.main_app and hasattr(self.main_app, 'settings_tab'):
            settings_tab = self.main_app.settings_tab
            for key, value in previous_settings.items():
                setattr(settings_tab, key, value)
            settings_tab.update_ui_from_settings()
    
    def _redo_settings_change(self, redo_data: Dict[str, Any]):
        """설정 변경 다시실행"""
        new_settings = redo_data.get('new_settings')
        
        if new_settings and self.main_app and hasattr(self.main_app, 'settings_tab'):
            settings_tab = self.main_app.settings_tab
            for key, value in new_settings.items():
                setattr(settings_tab, key, value)
            settings_tab.update_ui_from_settings()
    
    def _update_ui_state(self):
        """UI 상태 업데이트"""
        if self.main_app:
            # 메뉴 또는 버튼 상태 업데이트
            # (실제 UI가 있다면 여기서 활성화/비활성화)
            pass
    
    # === 편의 메서드들 ===
    
    def record_stock_addition(self, symbol: str, stock_data: Dict[str, Any]):
        """주식 추가 액션 기록"""
        self.record_action(
            action_type="add_stock",
            description=f"주식 추가: {symbol}",
            undo_data={"symbol": symbol},
            redo_data={"symbol": symbol, "stock_data": stock_data}
        )
    
    def record_stock_removal(self, symbol: str, stock_data: Dict[str, Any]):
        """주식 제거 액션 기록"""
        self.record_action(
            action_type="remove_stock",
            description=f"주식 제거: {symbol}",
            undo_data={"symbol": symbol, "stock_data": stock_data},
            redo_data={"symbol": symbol}
        )
    
    def record_trade_execution(self, trade_data: Dict[str, Any], portfolio_before: Dict[str, Any], portfolio_after: Dict[str, Any]):
        """거래 실행 액션 기록"""
        symbol = trade_data.get('symbol', 'Unknown')
        quantity = trade_data.get('quantity', 0)
        order_type = trade_data.get('order_type', 'Unknown')
        
        self.record_action(
            action_type="trade_execution",
            description=f"{order_type} {abs(quantity)}주 {symbol}",
            undo_data={"portfolio_state": portfolio_before, "trade_id": trade_data.get('id')},
            redo_data={"trade_data": trade_data, "portfolio_state": portfolio_after}
        )
    
    def record_settings_change(self, setting_name: str, old_value: Any, new_value: Any):
        """설정 변경 액션 기록"""
        self.record_action(
            action_type="settings_change",
            description=f"설정 변경: {setting_name}",
            undo_data={"previous_settings": {setting_name: old_value}},
            redo_data={"new_settings": {setting_name: new_value}}
        )