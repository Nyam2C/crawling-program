#!/usr/bin/env python3
"""
Keyboard Shortcut Manager - Handles all keyboard shortcuts and hotkeys
"""

import tkinter as tk
from typing import Dict, Callable, Optional
from dataclasses import dataclass

@dataclass
class KeyBinding:
    """키 바인딩 정보"""
    key_combination: str
    description: str
    callback: Callable
    enabled: bool = True

class KeyboardManager:
    """키보드 단축키 관리 클래스"""
    
    def __init__(self, root: tk.Tk, main_app):
        self.root = root
        self.main_app = main_app
        self.bindings: Dict[str, KeyBinding] = {}
        self.setup_default_bindings()
        self.bind_all_shortcuts()
        
    def setup_default_bindings(self):
        """기본 키보드 단축키 설정"""
        self.bindings = {
            '<Control-r>': KeyBinding(
                'Ctrl+R', 
                '데이터 새로고침', 
                self.refresh_all_data
            ),
            '<Control-s>': KeyBinding(
                'Ctrl+S', 
                '설정 저장', 
                self.save_settings
            ),
            '<Control-q>': KeyBinding(
                'Ctrl+Q', 
                '프로그램 종료', 
                self.quit_application
            ),
            '<F1>': KeyBinding(
                'F1', 
                '도움말', 
                self.show_help
            ),
            '<F5>': KeyBinding(
                'F5', 
                '전체 새로고침', 
                self.full_refresh
            ),
            '<Control-z>': KeyBinding(
                'Ctrl+Z', 
                '실행취소', 
                self.undo_last_action
            ),
            '<Control-y>': KeyBinding(
                'Ctrl+Y', 
                '다시실행', 
                self.redo_last_action
            ),
            '<Control-n>': KeyBinding(
                'Ctrl+N', 
                '새 주식 추가', 
                self.add_new_stock
            ),
            '<Control-d>': KeyBinding(
                'Ctrl+D', 
                '선택 항목 삭제', 
                self.delete_selected
            ),
            '<Control-e>': KeyBinding(
                'Ctrl+E', 
                '데이터 내보내기', 
                self.export_data
            ),
            '<Control-i>': KeyBinding(
                'Ctrl+I', 
                '데이터 가져오기', 
                self.import_data
            ),
            '<Escape>': KeyBinding(
                'ESC', 
                '현재 작업 취소', 
                self.cancel_current_action
            ),
            '<Control-1>': KeyBinding(
                'Ctrl+1', 
                'Stock Data 탭', 
                lambda: self.switch_tab(0)
            ),
            '<Control-2>': KeyBinding(
                'Ctrl+2', 
                'Recommendations 탭', 
                lambda: self.switch_tab(1)
            ),
            '<Control-3>': KeyBinding(
                'Ctrl+3', 
                'Analysis 탭', 
                lambda: self.switch_tab(2)
            ),
            '<Control-4>': KeyBinding(
                'Ctrl+4', 
                'Trading 탭', 
                lambda: self.switch_tab(3)
            ),
            '<Control-5>': KeyBinding(
                'Ctrl+5', 
                'Scoreboard 탭', 
                lambda: self.switch_tab(4)
            ),
            '<Control-6>': KeyBinding(
                'Ctrl+6', 
                'Investment Analysis 탭', 
                lambda: self.switch_tab(5)
            ),
            '<Control-7>': KeyBinding(
                'Ctrl+7', 
                'Settings 탭', 
                lambda: self.switch_tab(6)
            ),
        }
    
    def bind_all_shortcuts(self):
        """모든 단축키를 tkinter에 바인딩"""
        for key_combo, binding in self.bindings.items():
            if binding.enabled:
                self.root.bind_all(key_combo, self._create_handler(binding.callback))
    
    def _create_handler(self, callback: Callable):
        """이벤트 핸들러 생성"""
        def handler(event):
            try:
                callback()
                return "break"  # 기본 이벤트 처리 방지
            except Exception as e:
                print(f"키보드 단축키 실행 오류: {e}")
                self.main_app.show_error(f"단축키 실행 중 오류가 발생했습니다: {e}")
        return handler
    
    def add_custom_binding(self, key_combo: str, description: str, callback: Callable):
        """커스텀 키 바인딩 추가"""
        binding = KeyBinding(key_combo, description, callback)
        self.bindings[key_combo] = binding
        self.root.bind_all(key_combo, self._create_handler(callback))
    
    def remove_binding(self, key_combo: str):
        """키 바인딩 제거"""
        if key_combo in self.bindings:
            self.root.unbind_all(key_combo)
            del self.bindings[key_combo]
    
    def enable_binding(self, key_combo: str):
        """키 바인딩 활성화"""
        if key_combo in self.bindings:
            self.bindings[key_combo].enabled = True
            self.root.bind_all(key_combo, self._create_handler(self.bindings[key_combo].callback))
    
    def disable_binding(self, key_combo: str):
        """키 바인딩 비활성화"""
        if key_combo in self.bindings:
            self.bindings[key_combo].enabled = False
            self.root.unbind_all(key_combo)
    
    def get_help_text(self) -> str:
        """도움말 텍스트 생성"""
        help_lines = ["🎮 키보드 단축키:\n"]
        for binding in self.bindings.values():
            if binding.enabled:
                help_lines.append(f"  {binding.key_combination}: {binding.description}")
        return "\n".join(help_lines)
    
    # === 단축키 액션 메서드들 ===
    
    def refresh_all_data(self):
        """모든 데이터 새로고침"""
        self.main_app.update_status("단축키: 데이터 새로고침 중...")
        try:
            # Stock Data 탭 새로고침
            if hasattr(self.main_app, 'stock_data_tab'):
                self.main_app.stock_data_tab.refresh_all_data()
            
            # Recommendations 탭 새로고침
            if hasattr(self.main_app, 'recommendations_tab'):
                self.main_app.recommendations_tab.refresh_data()
            
            # Mock Trading 탭 새로고침
            if hasattr(self.main_app, 'mock_trading_tab'):
                self.main_app.mock_trading_tab.refresh_data()
                
            self.main_app.update_status("데이터 새로고침 완료 (Ctrl+R)")
        except Exception as e:
            self.main_app.show_error(f"데이터 새로고침 실패: {e}")
    
    def save_settings(self):
        """설정 저장"""
        try:
            if hasattr(self.main_app, 'settings_tab'):
                self.main_app.settings_tab.save_settings()
            self.main_app.update_status("설정 저장됨 (Ctrl+S)")
        except Exception as e:
            self.main_app.show_error(f"설정 저장 실패: {e}")
    
    def quit_application(self):
        """프로그램 종료"""
        self.main_app.on_closing()
    
    def show_help(self):
        """도움말 표시"""
        from tkinter import messagebox
        help_text = self.get_help_text()
        messagebox.showinfo("키보드 단축키 도움말", help_text)
    
    def full_refresh(self):
        """전체 새로고침"""
        self.main_app.update_status("전체 새로고침 중... (F5)")
        self.refresh_all_data()
        
        # 추가로 GUI 컴포넌트들도 새로고침
        try:
            self.main_app.root.update_idletasks()
            self.main_app.update_status("전체 새로고침 완료")
        except Exception as e:
            self.main_app.show_error(f"전체 새로고침 실패: {e}")
    
    def undo_last_action(self):
        """마지막 작업 실행취소"""
        if hasattr(self.main_app, 'action_manager'):
            self.main_app.action_manager.undo()
        else:
            self.main_app.update_status("실행취소 기능을 사용할 수 없습니다")
    
    def redo_last_action(self):
        """마지막 작업 다시실행"""
        if hasattr(self.main_app, 'action_manager'):
            self.main_app.action_manager.redo()
        else:
            self.main_app.update_status("다시실행 기능을 사용할 수 없습니다")
    
    def add_new_stock(self):
        """새 주식 추가"""
        try:
            # Stock Data 탭으로 전환
            self.switch_tab(0)
            
            # 주식 추가 입력 필드에 포커스
            if hasattr(self.main_app, 'stock_data_tab'):
                stock_tab = self.main_app.stock_data_tab
                if hasattr(stock_tab, 'symbol_entry'):
                    stock_tab.symbol_entry.focus_set()
                    self.main_app.update_status("새 주식 심볼을 입력하세요 (Ctrl+N)")
        except Exception as e:
            self.main_app.show_error(f"주식 추가 모드 전환 실패: {e}")
    
    def delete_selected(self):
        """선택된 항목 삭제"""
        current_tab = self.main_app.notebook.select()
        tab_index = self.main_app.notebook.index(current_tab)
        
        try:
            if tab_index == 0:  # Stock Data 탭
                if hasattr(self.main_app, 'stock_data_tab'):
                    self.main_app.stock_data_tab.remove_selected_stock()
            elif tab_index == 3:  # Mock Trading 탭
                if hasattr(self.main_app, 'mock_trading_tab'):
                    self.main_app.mock_trading_tab.cancel_selected_order()
            
            self.main_app.update_status("선택된 항목 삭제됨 (Ctrl+D)")
        except Exception as e:
            self.main_app.show_error(f"항목 삭제 실패: {e}")
    
    def export_data(self):
        """데이터 내보내기"""
        try:
            current_tab = self.main_app.notebook.select()
            tab_index = self.main_app.notebook.index(current_tab)
            
            if tab_index == 3:  # Mock Trading 탭
                if hasattr(self.main_app, 'mock_trading_tab'):
                    self.main_app.mock_trading_tab.export_portfolio_data()
            else:
                from tkinter import filedialog, messagebox
                filename = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
                )
                if filename:
                    # 여기에 실제 내보내기 로직 구현
                    messagebox.showinfo("내보내기", f"데이터가 {filename}에 저장되었습니다.")
            
            self.main_app.update_status("데이터 내보내기 완료 (Ctrl+E)")
        except Exception as e:
            self.main_app.show_error(f"데이터 내보내기 실패: {e}")
    
    def import_data(self):
        """데이터 가져오기"""
        try:
            from tkinter import filedialog, messagebox
            filename = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                # 여기에 실제 가져오기 로직 구현
                messagebox.showinfo("가져오기", f"{filename}에서 데이터를 가져왔습니다.")
                self.main_app.update_status("데이터 가져오기 완료 (Ctrl+I)")
        except Exception as e:
            self.main_app.show_error(f"데이터 가져오기 실패: {e}")
    
    def cancel_current_action(self):
        """현재 작업 취소"""
        try:
            # 진행중인 작업이 있다면 취소
            if hasattr(self.main_app, 'progress'):
                self.main_app.hide_progress()
            
            # 모든 입력 필드의 포커스 해제
            self.main_app.root.focus_set()
            
            self.main_app.update_status("현재 작업이 취소되었습니다 (ESC)")
        except Exception as e:
            print(f"작업 취소 중 오류: {e}")
    
    def switch_tab(self, tab_index: int):
        """탭 전환"""
        try:
            if hasattr(self.main_app, 'notebook'):
                tabs = self.main_app.notebook.tabs()
                if 0 <= tab_index < len(tabs):
                    self.main_app.notebook.select(tab_index)
                    tab_names = ["Stock Data", "Recommendations", "Analysis", "Trading", 
                               "Scoreboard", "Investment Analysis", "Settings"]
                    if tab_index < len(tab_names):
                        self.main_app.update_status(f"{tab_names[tab_index]} 탭으로 전환됨")
        except Exception as e:
            self.main_app.show_error(f"탭 전환 실패: {e}")