#!/usr/bin/env python3
"""
UX Enhancement Tests - Tests for keyboard shortcuts and undo/redo functionality
"""

import unittest
import tkinter as tk
from unittest.mock import Mock, patch
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui.components.ui_core.keyboard_manager import KeyboardManager, KeyBinding
from src.gui.components.ui_core.action_manager import ActionManager, Action
from datetime import datetime

class TestKeyboardManager(unittest.TestCase):
    """키보드 매니저 테스트"""
    
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # GUI 숨김
        self.mock_app = Mock()
        self.keyboard_manager = KeyboardManager(self.root, self.mock_app)
    
    def tearDown(self):
        try:
            self.root.destroy()
        except:
            pass
    
    def test_default_bindings_exist(self):
        """기본 키 바인딩이 설정되어 있는지 확인"""
        expected_bindings = [
            '<Control-r>', '<Control-s>', '<Control-q>', 
            '<F1>', '<F5>', '<Control-z>', '<Control-y>'
        ]
        
        for binding in expected_bindings:
            self.assertIn(binding, self.keyboard_manager.bindings)
            self.assertTrue(self.keyboard_manager.bindings[binding].enabled)
    
    def test_custom_binding_addition(self):
        """커스텀 키 바인딩 추가 테스트"""
        def test_callback():
            pass
        
        self.keyboard_manager.add_custom_binding(
            '<Control-t>', 'Test Action', test_callback
        )
        
        self.assertIn('<Control-t>', self.keyboard_manager.bindings)
        self.assertEqual(
            self.keyboard_manager.bindings['<Control-t>'].description, 
            'Test Action'
        )
    
    def test_binding_enable_disable(self):
        """키 바인딩 활성화/비활성화 테스트"""
        # 비활성화
        self.keyboard_manager.disable_binding('<Control-r>')
        self.assertFalse(self.keyboard_manager.bindings['<Control-r>'].enabled)
        
        # 활성화
        self.keyboard_manager.enable_binding('<Control-r>')
        self.assertTrue(self.keyboard_manager.bindings['<Control-r>'].enabled)
    
    def test_help_text_generation(self):
        """도움말 텍스트 생성 테스트"""
        help_text = self.keyboard_manager.get_help_text()
        
        self.assertIn('키보드 단축키', help_text)
        self.assertIn('Ctrl+R', help_text)
        self.assertIn('데이터 새로고침', help_text)
    
    def test_tab_switching(self):
        """탭 전환 기능 테스트"""
        # Mock notebook 설정
        mock_notebook = Mock()
        mock_notebook.tabs.return_value = ['tab1', 'tab2', 'tab3']
        self.mock_app.notebook = mock_notebook
        
        # 탭 전환 실행
        self.keyboard_manager.switch_tab(1)
        
        # notebook.select가 호출되었는지 확인
        mock_notebook.select.assert_called_once_with(1)

class TestActionManager(unittest.TestCase):
    """액션 매니저 테스트"""
    
    def setUp(self):
        self.action_manager = ActionManager(max_history=10)
        self.mock_app = Mock()
        self.action_manager.set_main_app(self.mock_app)
    
    def test_action_recording(self):
        """액션 기록 테스트"""
        undo_data = {"symbol": "AAPL"}
        redo_data = {"symbol": "AAPL", "data": {"price": 150.0}}
        
        self.action_manager.record_action(
            "add_stock", "주식 추가: AAPL", undo_data, redo_data
        )
        
        self.assertEqual(len(self.action_manager.action_history), 1)
        self.assertEqual(self.action_manager.current_position, 0)
        
        action = self.action_manager.action_history[0]
        self.assertEqual(action.action_type, "add_stock")
        self.assertEqual(action.description, "주식 추가: AAPL")
    
    def test_undo_redo_functionality(self):
        """실행취소/다시실행 기능 테스트"""
        # 액션 기록
        self.action_manager.record_action(
            "test_action", "테스트 액션",
            {"test": "undo"}, {"test": "redo"}
        )
        
        # 실행취소 가능 여부 확인
        self.assertTrue(self.action_manager.can_undo())
        self.assertFalse(self.action_manager.can_redo())
        
        # 커스텀 콜백으로 실행취소 테스트
        undo_called = False
        def custom_undo(data):
            nonlocal undo_called
            undo_called = True
            self.assertEqual(data["test"], "undo")
        
        # 커스텀 콜백이 있는 액션 추가
        self.action_manager.record_action(
            "custom_action", "커스텀 액션",
            {"test": "undo"}, {"test": "redo"},
            undo_callback=custom_undo
        )
        
        # 실행취소 실행
        result = self.action_manager.undo()
        self.assertTrue(result)
        self.assertTrue(undo_called)
        
        # 다시실행 가능 여부 확인
        self.assertTrue(self.action_manager.can_redo())
    
    def test_history_limit(self):
        """히스토리 제한 테스트"""
        # 최대 히스토리보다 많은 액션 기록
        for i in range(15):
            self.action_manager.record_action(
                f"action_{i}", f"액션 {i}",
                {"index": i}, {"index": i}
            )
        
        # 히스토리가 제한되었는지 확인
        self.assertEqual(len(self.action_manager.action_history), 10)
        
        # 마지막 액션이 올바른지 확인
        last_action = self.action_manager.action_history[-1]
        self.assertEqual(last_action.action_type, "action_14")
    
    def test_branching_history(self):
        """히스토리 분기 테스트"""
        # 여러 액션 기록
        for i in range(3):
            self.action_manager.record_action(
                f"action_{i}", f"액션 {i}",
                {"index": i}, {"index": i}
            )
        
        # 실행취소
        self.action_manager.undo()
        self.assertEqual(self.action_manager.current_position, 1)
        
        # 새 액션 기록 (분기 생성)
        self.action_manager.record_action(
            "new_action", "새 액션",
            {"new": True}, {"new": True}
        )
        
        # 분기 후 히스토리 길이 확인
        self.assertEqual(len(self.action_manager.action_history), 3)
        self.assertEqual(self.action_manager.current_position, 2)
    
    def test_convenience_methods(self):
        """편의 메서드 테스트"""
        # 주식 추가 기록
        self.action_manager.record_stock_addition("AAPL", {"price": 150.0})
        
        action = self.action_manager.action_history[0]
        self.assertEqual(action.action_type, "add_stock")
        self.assertIn("AAPL", action.description)
        
        # 거래 실행 기록
        trade_data = {
            "symbol": "AAPL",
            "quantity": 10,
            "order_type": "buy",
            "id": "trade_001"
        }
        portfolio_before = {"cash": 10000}
        portfolio_after = {"cash": 8500}
        
        self.action_manager.record_trade_execution(
            trade_data, portfolio_before, portfolio_after
        )
        
        trade_action = self.action_manager.action_history[1]
        self.assertEqual(trade_action.action_type, "trade_execution")
        self.assertIn("buy", trade_action.description)
        self.assertIn("AAPL", trade_action.description)
    
    def test_history_summary(self):
        """히스토리 요약 정보 테스트"""
        # 몇 개의 액션 기록
        self.action_manager.record_action(
            "action1", "첫 번째 액션", {}, {}
        )
        self.action_manager.record_action(
            "action2", "두 번째 액션", {}, {}
        )
        
        # 요약 정보 생성
        summary = self.action_manager.get_history_summary()
        
        self.assertEqual(len(summary), 2)
        self.assertIn("첫 번째 액션", summary[0])
        self.assertIn("두 번째 액션", summary[1])
        
        # 현재 위치 표시 확인
        self.assertIn("○", summary[0])  # 이전 액션
        self.assertIn("●", summary[1])  # 현재 액션

class TestIntegration(unittest.TestCase):
    """통합 테스트"""
    
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Mock main app
        self.mock_app = Mock()
        self.mock_app.root = self.root
        self.mock_app.update_status = Mock()
        self.mock_app.show_error = Mock()
        
        # 매니저들 초기화
        self.action_manager = ActionManager()
        self.action_manager.set_main_app(self.mock_app)
        
        self.keyboard_manager = KeyboardManager(self.root, self.mock_app)
        self.keyboard_manager.main_app.action_manager = self.action_manager
    
    def tearDown(self):
        try:
            self.root.destroy()
        except:
            pass
    
    def test_keyboard_undo_integration(self):
        """키보드 단축키와 실행취소 통합 테스트"""
        # 액션 기록
        self.action_manager.record_action(
            "test", "테스트 액션", {}, {}
        )
        
        # Ctrl+Z 실행취소 테스트
        self.assertTrue(self.action_manager.can_undo())
        
        # 키보드 단축키로 실행취소
        self.keyboard_manager.undo_last_action()
        
        # 상태 변경 확인
        self.assertFalse(self.action_manager.can_undo())
        self.assertTrue(self.action_manager.can_redo())

class TestErrorHandling(unittest.TestCase):
    """에러 처리 테스트"""
    
    def setUp(self):
        self.action_manager = ActionManager()
        self.mock_app = Mock()
        self.action_manager.set_main_app(self.mock_app)
    
    def test_undo_without_history(self):
        """히스토리 없이 실행취소 시도"""
        result = self.action_manager.undo()
        self.assertFalse(result)
    
    def test_redo_without_future(self):
        """다시실행할 액션 없이 다시실행 시도"""
        result = self.action_manager.redo()
        self.assertFalse(result)
    
    def test_invalid_action_type(self):
        """알 수 없는 액션 타입 처리"""
        self.action_manager.record_action(
            "unknown_action", "알 수 없는 액션", {}, {}
        )
        
        # 실행취소 시도 시 NotImplementedError 발생해야 함
        with self.assertRaises(NotImplementedError):
            self.action_manager._execute_default_undo(
                self.action_manager.action_history[0]
            )

def run_ux_tests():
    """UX 개선 기능 테스트 실행"""
    print("🧪 UX Enhancement Tests 실행 중...")
    
    # 테스트 슈트 생성
    test_suite = unittest.TestSuite()
    
    # 테스트 클래스들 추가
    test_classes = [
        TestKeyboardManager,
        TestActionManager,
        TestIntegration,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 결과 요약
    print(f"\n📊 테스트 결과:")
    print(f"   실행된 테스트: {result.testsRun}")
    print(f"   실패: {len(result.failures)}")
    print(f"   에러: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ 실패한 테스트:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n💥 에러가 발생한 테스트:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    if not result.failures and not result.errors:
        print("✅ 모든 테스트가 성공적으로 통과했습니다!")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_ux_tests()
    sys.exit(0 if success else 1)