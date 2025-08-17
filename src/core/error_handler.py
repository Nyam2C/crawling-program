#!/usr/bin/env python3
"""
Error Handler - 강화된 에러 처리, 로깅, 복구 시스템
"""

import logging
import traceback
import sys
import time
import json
import threading
from typing import Dict, List, Any, Optional, Callable, Type
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum
import tkinter as tk
from tkinter import messagebox
import functools
import inspect


class ErrorSeverity(Enum):
    """에러 심각도"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ErrorCategory(Enum):
    """에러 카테고리"""
    NETWORK = "NETWORK"           # 네트워크 관련
    DATA = "DATA"                 # 데이터 처리 관련
    GUI = "GUI"                   # GUI 관련
    FILE_IO = "FILE_IO"           # 파일 입출력 관련
    API = "API"                   # API 호출 관련
    CALCULATION = "CALCULATION"   # 계산 관련
    VALIDATION = "VALIDATION"     # 데이터 검증 관련
    SYSTEM = "SYSTEM"            # 시스템 관련
    UNKNOWN = "UNKNOWN"          # 분류되지 않은 에러


@dataclass
class ErrorRecord:
    """에러 기록"""
    error_id: str
    timestamp: float
    severity: ErrorSeverity
    category: ErrorCategory
    message: str
    exception_type: str
    traceback_str: str
    function_name: str
    file_name: str
    line_number: int
    context: Dict[str, Any]
    user_action: Optional[str] = None
    resolved: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        data = asdict(self)
        data['severity'] = self.severity.value
        data['category'] = self.category.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ErrorRecord':
        """딕셔너리에서 생성"""
        data['severity'] = ErrorSeverity(data['severity'])
        data['category'] = ErrorCategory(data['category'])
        return cls(**data)


class RecoveryStrategy:
    """복구 전략"""
    
    def __init__(self, name: str, func: Callable, max_attempts: int = 3):
        self.name = name
        self.func = func
        self.max_attempts = max_attempts
        self.attempts = 0
    
    def attempt_recovery(self, error_record: ErrorRecord) -> bool:
        """복구 시도"""
        if self.attempts >= self.max_attempts:
            return False
        
        try:
            self.attempts += 1
            result = self.func(error_record)
            if result:
                self.attempts = 0  # 성공 시 카운터 리셋
            return result
        except Exception as e:
            logging.error(f"Recovery strategy '{self.name}' failed: {e}")
            return False


class ErrorLogger:
    """에러 로깅 시스템"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # 로거 설정
        self.logger = logging.getLogger("StockEdu")
        self.logger.setLevel(logging.DEBUG)
        
        # 파일 핸들러
        log_file = self.log_dir / f"stockedu_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # 포맷터
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 핸들러 추가 (중복 방지)
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        # 에러 기록 저장소
        self.error_records = []
        self.error_file = self.log_dir / "error_records.json"
        self.load_error_records()
        
        # 자동 정리 스케줄링
        self._schedule_cleanup()
    
    def load_error_records(self):
        """에러 기록 로드"""
        if self.error_file.exists():
            try:
                with open(self.error_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.error_records = [ErrorRecord.from_dict(record) for record in data]
            except Exception as e:
                self.logger.error(f"Failed to load error records: {e}")
    
    def save_error_records(self):
        """에러 기록 저장"""
        try:
            with open(self.error_file, 'w', encoding='utf-8') as f:
                data = [record.to_dict() for record in self.error_records]
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save error records: {e}")
    
    def log_error(self, error_record: ErrorRecord):
        """에러 로깅"""
        # 로그 파일에 기록
        self.logger.log(
            getattr(logging, error_record.severity.value),
            f"[{error_record.category.value}] {error_record.message}"
        )
        
        # 에러 기록에 추가
        self.error_records.append(error_record)
        
        # 즉시 저장 (중요한 에러의 경우)
        if error_record.severity in [ErrorSeverity.ERROR, ErrorSeverity.CRITICAL]:
            self.save_error_records()
    
    def get_recent_errors(self, hours: int = 24) -> List[ErrorRecord]:
        """최근 에러 조회"""
        cutoff_time = time.time() - (hours * 3600)
        return [record for record in self.error_records if record.timestamp >= cutoff_time]
    
    def get_errors_by_category(self, category: ErrorCategory) -> List[ErrorRecord]:
        """카테고리별 에러 조회"""
        return [record for record in self.error_records if record.category == category]
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """에러 통계"""
        recent_errors = self.get_recent_errors(24)
        
        severity_counts = {}
        category_counts = {}
        
        for record in recent_errors:
            severity_counts[record.severity.value] = severity_counts.get(record.severity.value, 0) + 1
            category_counts[record.category.value] = category_counts.get(record.category.value, 0) + 1
        
        return {
            "total_errors_24h": len(recent_errors),
            "severity_distribution": severity_counts,
            "category_distribution": category_counts,
            "resolved_count": len([r for r in recent_errors if r.resolved])
        }
    
    def _schedule_cleanup(self):
        """자동 정리 스케줄링"""
        def cleanup():
            # 30일 이상 된 에러 기록 삭제
            cutoff_time = time.time() - (30 * 24 * 3600)
            old_count = len(self.error_records)
            self.error_records = [r for r in self.error_records if r.timestamp >= cutoff_time]
            
            if len(self.error_records) < old_count:
                self.save_error_records()
                self.logger.info(f"Cleaned up {old_count - len(self.error_records)} old error records")
        
        # 매일 자정에 정리
        timer = threading.Timer(24 * 3600, cleanup)
        timer.daemon = True
        timer.start()


class ErrorHandler:
    """통합 에러 처리기"""
    
    def __init__(self, show_gui_errors: bool = True):
        self.logger = ErrorLogger()
        self.recovery_strategies = {}  # category -> List[RecoveryStrategy]
        self.error_callbacks = {}      # category -> List[Callable]
        self.show_gui_errors = show_gui_errors
        self.error_counter = 0
        
        # 기본 복구 전략 등록
        self._register_default_strategies()
    
    def _register_default_strategies(self):
        """기본 복구 전략 등록"""
        # 네트워크 에러 복구
        self.register_recovery_strategy(
            ErrorCategory.NETWORK,
            RecoveryStrategy("retry_connection", self._retry_network_operation, 3)
        )
        
        # 파일 I/O 에러 복구
        self.register_recovery_strategy(
            ErrorCategory.FILE_IO,
            RecoveryStrategy("backup_restore", self._restore_from_backup, 1)
        )
        
        # API 에러 복구
        self.register_recovery_strategy(
            ErrorCategory.API,
            RecoveryStrategy("fallback_data_source", self._try_fallback_api, 2)
        )
    
    def register_recovery_strategy(self, category: ErrorCategory, strategy: RecoveryStrategy):
        """복구 전략 등록"""
        if category not in self.recovery_strategies:
            self.recovery_strategies[category] = []
        self.recovery_strategies[category].append(strategy)
    
    def register_error_callback(self, category: ErrorCategory, callback: Callable):
        """에러 콜백 등록"""
        if category not in self.error_callbacks:
            self.error_callbacks[category] = []
        self.error_callbacks[category].append(callback)
    
    def handle_exception(self, 
                        exception: Exception, 
                        category: ErrorCategory = ErrorCategory.UNKNOWN,
                        context: Optional[Dict[str, Any]] = None,
                        user_action: Optional[str] = None,
                        severity: Optional[ErrorSeverity] = None) -> bool:
        """예외 처리"""
        
        # 에러 기록 생성
        error_record = self._create_error_record(
            exception, category, context, user_action, severity
        )
        
        # 로깅
        self.logger.log_error(error_record)
        
        # 복구 시도
        recovered = self._attempt_recovery(error_record)
        
        if recovered:
            error_record.resolved = True
        
        # 콜백 실행
        self._execute_callbacks(category, error_record)
        
        # GUI 에러 표시
        if not recovered and self.show_gui_errors and error_record.severity in [ErrorSeverity.ERROR, ErrorSeverity.CRITICAL]:
            self._show_gui_error(error_record)
        
        return recovered
    
    def _create_error_record(self, 
                           exception: Exception, 
                           category: ErrorCategory,
                           context: Optional[Dict[str, Any]],
                           user_action: Optional[str],
                           severity: Optional[ErrorSeverity]) -> ErrorRecord:
        """에러 기록 생성"""
        
        self.error_counter += 1
        
        # 스택 추적 정보
        tb = traceback.extract_tb(exception.__traceback__)
        if tb:
            frame = tb[-1]
            function_name = frame.name
            file_name = Path(frame.filename).name
            line_number = frame.lineno
        else:
            function_name = "unknown"
            file_name = "unknown"
            line_number = 0
        
        # 심각도 자동 판정
        if severity is None:
            severity = self._determine_severity(exception, category)
        
        return ErrorRecord(
            error_id=f"ERR_{int(time.time())}_{self.error_counter}",
            timestamp=time.time(),
            severity=severity,
            category=category,
            message=str(exception),
            exception_type=type(exception).__name__,
            traceback_str=traceback.format_exc(),
            function_name=function_name,
            file_name=file_name,
            line_number=line_number,
            context=context or {},
            user_action=user_action
        )
    
    def _determine_severity(self, exception: Exception, category: ErrorCategory) -> ErrorSeverity:
        """심각도 자동 판정"""
        if isinstance(exception, (ConnectionError, TimeoutError)):
            return ErrorSeverity.WARNING
        elif isinstance(exception, (FileNotFoundError, PermissionError)):
            return ErrorSeverity.ERROR
        elif isinstance(exception, (KeyboardInterrupt, SystemExit)):
            return ErrorSeverity.CRITICAL
        elif category == ErrorCategory.GUI:
            return ErrorSeverity.WARNING
        elif category == ErrorCategory.NETWORK:
            return ErrorSeverity.WARNING
        else:
            return ErrorSeverity.ERROR
    
    def _attempt_recovery(self, error_record: ErrorRecord) -> bool:
        """복구 시도"""
        strategies = self.recovery_strategies.get(error_record.category, [])
        
        for strategy in strategies:
            try:
                if strategy.attempt_recovery(error_record):
                    self.logger.logger.info(f"Recovery successful with strategy: {strategy.name}")
                    return True
            except Exception as e:
                self.logger.logger.error(f"Recovery strategy failed: {e}")
        
        return False
    
    def _execute_callbacks(self, category: ErrorCategory, error_record: ErrorRecord):
        """에러 콜백 실행"""
        callbacks = self.error_callbacks.get(category, [])
        
        for callback in callbacks:
            try:
                callback(error_record)
            except Exception as e:
                self.logger.logger.error(f"Error callback failed: {e}")
    
    def _show_gui_error(self, error_record: ErrorRecord):
        """GUI 에러 표시"""
        try:
            title = f"{error_record.severity.value} - {error_record.category.value}"
            message = f"오류가 발생했습니다:\n\n{error_record.message}\n\n"
            
            if error_record.user_action:
                message += f"수행 중이던 작업: {error_record.user_action}\n\n"
            
            message += f"에러 ID: {error_record.error_id}\n"
            message += f"위치: {error_record.file_name}:{error_record.line_number}"
            
            if error_record.severity == ErrorSeverity.CRITICAL:
                messagebox.showerror(title, message)
            elif error_record.severity == ErrorSeverity.ERROR:
                messagebox.showerror(title, message)
            else:
                messagebox.showwarning(title, message)
                
        except Exception as e:
            # GUI 에러 표시 실패 시 로그만 남김
            self.logger.logger.error(f"Failed to show GUI error: {e}")
    
    # 기본 복구 전략들
    def _retry_network_operation(self, error_record: ErrorRecord) -> bool:
        """네트워크 작업 재시도"""
        time.sleep(1)  # 잠시 대기
        # 실제 구현에서는 원래 작업을 재시도
        return False  # 예시로 실패 반환
    
    def _restore_from_backup(self, error_record: ErrorRecord) -> bool:
        """백업에서 복원"""
        # 데이터 무결성 관리자를 사용하여 복원
        try:
            from .data_integrity import DataIntegrityManager
            integrity_manager = DataIntegrityManager()
            return integrity_manager.emergency_recovery()
        except Exception:
            return False
    
    def _try_fallback_api(self, error_record: ErrorRecord) -> bool:
        """대체 API 시도"""
        # 다중 데이터 소스 제공자를 사용하여 대체 소스 시도
        return False  # 예시로 실패 반환


# 전역 에러 핸들러
_global_error_handler = None

def get_error_handler() -> ErrorHandler:
    """전역 에러 핸들러 조회"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler()
    return _global_error_handler


def handle_errors(category: ErrorCategory = ErrorCategory.UNKNOWN, 
                 user_action: Optional[str] = None,
                 severity: Optional[ErrorSeverity] = None,
                 reraise: bool = False):
    """에러 처리 데코레이터"""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler = get_error_handler()
                
                # 컨텍스트 정보 수집
                context = {
                    "function": func.__name__,
                    "args": str(args)[:200],  # 길이 제한
                    "kwargs": str(kwargs)[:200]
                }
                
                # 에러 처리
                recovered = handler.handle_exception(
                    e, category, context, user_action, severity
                )
                
                if not recovered and reraise:
                    raise
                
                return None
        return wrapper
    return decorator


def safe_execute(func: Callable, 
                *args, 
                category: ErrorCategory = ErrorCategory.UNKNOWN,
                default_return: Any = None,
                **kwargs) -> Any:
    """안전한 함수 실행"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        handler = get_error_handler()
        handler.handle_exception(e, category)
        return default_return


# 시스템 전역 예외 처리기
def setup_global_exception_handler():
    """전역 예외 처리기 설정"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        handler = get_error_handler()
        handler.handle_exception(
            exc_value, 
            ErrorCategory.SYSTEM, 
            severity=ErrorSeverity.CRITICAL
        )
    
    sys.excepthook = handle_exception


# GUI 에러 처리 유틸리티
def setup_tkinter_error_handling(root: tk.Tk):
    """Tkinter 에러 처리 설정"""
    def report_callback_exception(exc_type, exc_value, exc_traceback):
        handler = get_error_handler()
        handler.handle_exception(
            exc_value,
            ErrorCategory.GUI,
            context={"widget": "unknown"},
            severity=ErrorSeverity.ERROR
        )
    
    root.report_callback_exception = report_callback_exception