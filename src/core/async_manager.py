#!/usr/bin/env python3
"""
Async Manager - GUI와 백그라운드 작업을 위한 비동기 관리 시스템
"""

import asyncio
import threading
import queue
import time
import tkinter as tk
from typing import Callable, Any, Optional, Dict, List
from dataclasses import dataclass
from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor, Future
import weakref


class TaskPriority(Enum):
    """작업 우선순위"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class AsyncTask:
    """비동기 작업 정의"""
    task_id: str
    func: Callable
    args: tuple
    kwargs: dict
    priority: TaskPriority
    callback: Optional[Callable] = None
    error_callback: Optional[Callable] = None
    timeout: Optional[float] = None
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


class TaskResult:
    """작업 결과"""
    
    def __init__(self, task_id: str, success: bool, result: Any = None, error: Exception = None):
        self.task_id = task_id
        self.success = success
        self.result = result
        self.error = error
        self.completed_at = time.time()


class BackgroundWorker(threading.Thread):
    """백그라운드 워커 스레드"""
    
    def __init__(self, task_queue: queue.PriorityQueue, result_callback: Callable):
        super().__init__(daemon=True)
        self.task_queue = task_queue
        self.result_callback = result_callback
        self.stop_event = threading.Event()
        self.current_task = None
        
    def run(self):
        """워커 스레드 실행"""
        while not self.stop_event.is_set():
            try:
                # 작업 대기 (타임아웃 있음)
                priority, task = self.task_queue.get(timeout=1.0)
                self.current_task = task
                
                # 작업 실행
                result = self._execute_task(task)
                
                # 결과 콜백
                if self.result_callback:
                    self.result_callback(result)
                
                self.task_queue.task_done()
                self.current_task = None
                
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Background worker error: {e}")
                if self.current_task:
                    error_result = TaskResult(
                        self.current_task.task_id, 
                        False, 
                        error=e
                    )
                    if self.result_callback:
                        self.result_callback(error_result)
    
    def _execute_task(self, task: AsyncTask) -> TaskResult:
        """작업 실행"""
        try:
            start_time = time.time()
            
            # 타임아웃 설정
            if task.timeout:
                # 별도 스레드에서 실행하여 타임아웃 처리
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(task.func, *task.args, **task.kwargs)
                    result = future.result(timeout=task.timeout)
            else:
                result = task.func(*task.args, **task.kwargs)
            
            execution_time = time.time() - start_time
            logging.debug(f"Task {task.task_id} completed in {execution_time:.3f}s")
            
            return TaskResult(task.task_id, True, result)
            
        except Exception as e:
            logging.error(f"Task {task.task_id} failed: {e}")
            return TaskResult(task.task_id, False, error=e)
    
    def stop(self):
        """워커 스레드 중지"""
        self.stop_event.set()


class AsyncDataLoader:
    """비동기 데이터 로더"""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_futures = {}
        self.cache = {}
        self.cache_ttl = 300  # 5분
        
    def load_data_async(self, 
                       data_source: str, 
                       symbols: List[str], 
                       callback: Callable,
                       use_cache: bool = True) -> str:
        """비동기 데이터 로딩"""
        
        task_id = f"data_load_{int(time.time() * 1000)}"
        
        # 캐시 확인
        if use_cache:
            cached_data = {}
            uncached_symbols = []
            
            for symbol in symbols:
                cache_key = f"{data_source}_{symbol}"
                if cache_key in self.cache:
                    cache_entry = self.cache[cache_key]
                    if time.time() - cache_entry["timestamp"] < self.cache_ttl:
                        cached_data[symbol] = cache_entry["data"]
                    else:
                        uncached_symbols.append(symbol)
                        del self.cache[cache_key]
                else:
                    uncached_symbols.append(symbol)
            
            # 캐시된 데이터가 있으면 즉시 콜백 호출
            if cached_data:
                callback(cached_data, from_cache=True)
            
            # 캐시되지 않은 데이터만 로드
            symbols = uncached_symbols
        
        if not symbols:
            return task_id
        
        # 비동기 작업 제출
        future = self.executor.submit(self._fetch_data, data_source, symbols)
        self.active_futures[task_id] = {
            "future": future,
            "callback": callback,
            "symbols": symbols,
            "data_source": data_source,
            "start_time": time.time()
        }
        
        # 완료 콜백 설정
        future.add_done_callback(lambda f: self._handle_completion(task_id, f))
        
        return task_id
    
    def _fetch_data(self, data_source: str, symbols: List[str]) -> Dict[str, Any]:
        """실제 데이터 가져오기"""
        # 여기서 실제 데이터 소스에서 데이터를 가져옴
        # 예시: Yahoo Finance, API 호출 등
        
        # 임시 구현 (실제로는 MultiSourceDataProvider 사용)
        import yfinance as yf
        
        data = {}
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period="1d")
                
                if not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
                    data[symbol] = {
                        "price": current_price,
                        "volume": int(hist['Volume'].iloc[-1]),
                        "market_cap": info.get('marketCap'),
                        "pe_ratio": info.get('trailingPE')
                    }
            except Exception as e:
                logging.error(f"Failed to fetch data for {symbol}: {e}")
                data[symbol] = None
        
        return data
    
    def _handle_completion(self, task_id: str, future: Future):
        """작업 완료 처리"""
        if task_id not in self.active_futures:
            return
        
        task_info = self.active_futures[task_id]
        callback = task_info["callback"]
        symbols = task_info["symbols"]
        data_source = task_info["data_source"]
        
        try:
            result = future.result()
            
            # 캐시에 저장
            for symbol, data in result.items():
                if data is not None:
                    cache_key = f"{data_source}_{symbol}"
                    self.cache[cache_key] = {
                        "data": data,
                        "timestamp": time.time()
                    }
            
            # 콜백 호출
            if callback:
                callback(result, from_cache=False)
                
        except Exception as e:
            logging.error(f"Data loading task {task_id} failed: {e}")
            if callback:
                callback({}, error=str(e))
        
        finally:
            # 완료된 작업 정리
            del self.active_futures[task_id]
    
    def cancel_task(self, task_id: str) -> bool:
        """작업 취소"""
        if task_id in self.active_futures:
            future = self.active_futures[task_id]["future"]
            cancelled = future.cancel()
            if cancelled:
                del self.active_futures[task_id]
            return cancelled
        return False
    
    def get_active_tasks(self) -> List[str]:
        """활성 작업 목록"""
        return list(self.active_futures.keys())
    
    def clear_cache(self):
        """캐시 정리"""
        self.cache.clear()


class TkinterAsyncManager:
    """Tkinter GUI를 위한 비동기 관리자"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.task_queue = queue.PriorityQueue()
        self.result_queue = queue.Queue()
        self.workers = []
        self.task_callbacks = {}  # task_id -> (callback, error_callback)
        self.task_counter = 0
        self.running = False
        
        # 데이터 로더
        self.data_loader = AsyncDataLoader()
        
        # GUI 업데이트 스케줄링
        self._schedule_result_processing()
    
    def start(self, num_workers: int = 2):
        """비동기 매니저 시작"""
        if self.running:
            return
        
        self.running = True
        
        # 워커 스레드 시작
        for i in range(num_workers):
            worker = BackgroundWorker(self.task_queue, self._handle_task_result)
            worker.start()
            self.workers.append(worker)
        
        logging.info(f"Async manager started with {num_workers} workers")
    
    def stop(self):
        """비동기 매니저 중지"""
        if not self.running:
            return
        
        self.running = False
        
        # 워커 스레드 중지
        for worker in self.workers:
            worker.stop()
        
        # 워커 스레드 종료 대기
        for worker in self.workers:
            worker.join(timeout=5.0)
        
        self.workers.clear()
        logging.info("Async manager stopped")
    
    def submit_task(self, 
                   func: Callable, 
                   *args, 
                   priority: TaskPriority = TaskPriority.NORMAL,
                   callback: Optional[Callable] = None,
                   error_callback: Optional[Callable] = None,
                   timeout: Optional[float] = None,
                   **kwargs) -> str:
        """작업 제출"""
        
        task_id = f"task_{self.task_counter}"
        self.task_counter += 1
        
        task = AsyncTask(
            task_id=task_id,
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority,
            timeout=timeout
        )
        
        # 콜백 저장
        if callback or error_callback:
            self.task_callbacks[task_id] = (callback, error_callback)
        
        # 우선순위 큐에 추가 (음수로 하여 높은 우선순위가 먼저 처리되도록)
        self.task_queue.put((-priority.value, task))
        
        return task_id
    
    def _handle_task_result(self, result: TaskResult):
        """작업 결과 처리 (백그라운드 스레드에서 호출)"""
        self.result_queue.put(result)
    
    def _schedule_result_processing(self):
        """결과 처리 스케줄링"""
        self._process_results()
        # 100ms마다 결과 처리
        self.root.after(100, self._schedule_result_processing)
    
    def _process_results(self):
        """결과 처리 (메인 GUI 스레드에서 실행)"""
        while True:
            try:
                result = self.result_queue.get_nowait()
                
                # 콜백 실행
                if result.task_id in self.task_callbacks:
                    callback, error_callback = self.task_callbacks[result.task_id]
                    
                    if result.success and callback:
                        try:
                            callback(result.result)
                        except Exception as e:
                            logging.error(f"Callback error for task {result.task_id}: {e}")
                    elif not result.success and error_callback:
                        try:
                            error_callback(result.error)
                        except Exception as e:
                            logging.error(f"Error callback error for task {result.task_id}: {e}")
                    
                    # 콜백 정리
                    del self.task_callbacks[result.task_id]
                
            except queue.Empty:
                break
    
    def load_stock_data_async(self, 
                             symbols: List[str], 
                             callback: Callable,
                             use_cache: bool = True):
        """주식 데이터 비동기 로딩"""
        return self.data_loader.load_data_async(
            "yahoo_finance", 
            symbols, 
            callback, 
            use_cache
        )
    
    def get_queue_size(self) -> int:
        """대기 중인 작업 수"""
        return self.task_queue.qsize()
    
    def get_active_workers(self) -> int:
        """활성 워커 수"""
        return len([w for w in self.workers if w.is_alive()])


# 전역 비동기 매니저
_global_async_manager = None

def get_async_manager(root: tk.Tk = None) -> Optional[TkinterAsyncManager]:
    """전역 비동기 매니저 조회"""
    global _global_async_manager
    if _global_async_manager is None and root is not None:
        _global_async_manager = TkinterAsyncManager(root)
    return _global_async_manager


def async_task(priority: TaskPriority = TaskPriority.NORMAL, 
               timeout: Optional[float] = None):
    """비동기 작업 데코레이터"""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            manager = get_async_manager()
            if manager:
                return manager.submit_task(
                    func, *args, 
                    priority=priority, 
                    timeout=timeout, 
                    **kwargs
                )
            else:
                # 매니저가 없으면 동기 실행
                return func(*args, **kwargs)
        return wrapper
    return decorator


# 편의 함수들
def run_in_background(func: Callable, 
                     *args, 
                     callback: Optional[Callable] = None,
                     error_callback: Optional[Callable] = None,
                     **kwargs) -> Optional[str]:
    """백그라운드에서 함수 실행"""
    manager = get_async_manager()
    if manager:
        return manager.submit_task(
            func, *args, 
            callback=callback, 
            error_callback=error_callback, 
            **kwargs
        )
    return None


def load_stock_data_background(symbols: List[str], 
                              callback: Callable,
                              use_cache: bool = True) -> Optional[str]:
    """백그라운드에서 주식 데이터 로딩"""
    manager = get_async_manager()
    if manager:
        return manager.load_stock_data_async(symbols, callback, use_cache)
    return None