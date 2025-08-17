#!/usr/bin/env python3
"""
Performance Optimizer - 데이터 압축, 메모리 최적화, 성능 향상
"""

import json
import gzip
import pickle
import sqlite3
import threading
import time
import gc
import psutil
import weakref
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import deque, OrderedDict
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio


@dataclass
class PerformanceMetrics:
    """성능 메트릭"""
    memory_usage: float  # MB
    cpu_usage: float     # %
    disk_usage: float    # MB
    response_time: float # ms
    cache_hit_rate: float # %
    timestamp: float


class LRUCache:
    """LRU (Least Recently Used) 캐시"""
    
    def __init__(self, maxsize: int = 1000):
        self.maxsize = maxsize
        self.cache = OrderedDict()
        self.lock = threading.RLock()
    
    def get(self, key: str, default=None):
        """캐시에서 값 조회"""
        with self.lock:
            if key in self.cache:
                # 최근 사용으로 이동
                value = self.cache.pop(key)
                self.cache[key] = value
                return value
            return default
    
    def set(self, key: str, value: Any):
        """캐시에 값 저장"""
        with self.lock:
            if key in self.cache:
                # 기존 항목 업데이트
                self.cache.pop(key)
            elif len(self.cache) >= self.maxsize:
                # 가장 오래된 항목 제거
                self.cache.popitem(last=False)
            
            self.cache[key] = value
    
    def clear(self):
        """캐시 전체 삭제"""
        with self.lock:
            self.cache.clear()
    
    def size(self) -> int:
        """캐시 크기"""
        return len(self.cache)


class CompressedDataManager:
    """압축 데이터 관리자"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.compressed_dir = self.base_dir / "compressed_data"
        self.compressed_dir.mkdir(exist_ok=True)
        
        # SQLite DB for metadata
        self.db_path = self.compressed_dir / "metadata.db"
        self._init_database()
        
    def _init_database(self):
        """메타데이터 데이터베이스 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS compressed_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_path TEXT UNIQUE,
                    compressed_path TEXT,
                    original_size INTEGER,
                    compressed_size INTEGER,
                    compression_ratio REAL,
                    created_at REAL,
                    last_accessed REAL
                )
            """)
            conn.commit()
    
    def compress_json_file(self, file_path: Path) -> bool:
        """JSON 파일 압축"""
        try:
            if not file_path.exists():
                return False
            
            # 원본 크기
            original_size = file_path.stat().st_size
            
            # 압축 파일 경로
            compressed_path = self.compressed_dir / f"{file_path.stem}_compressed.gz"
            
            # 압축 실행
            with open(file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb', compresslevel=9) as f_out:
                    f_out.write(f_in.read())
            
            # 압축 크기
            compressed_size = compressed_path.stat().st_size
            compression_ratio = compressed_size / original_size if original_size > 0 else 1.0
            
            # 메타데이터 저장
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO compressed_files 
                    (original_path, compressed_path, original_size, compressed_size, 
                     compression_ratio, created_at, last_accessed)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(file_path), str(compressed_path), original_size, compressed_size,
                    compression_ratio, time.time(), time.time()
                ))
                conn.commit()
            
            return True
            
        except Exception as e:
            logging.error(f"Compression failed for {file_path}: {e}")
            return False
    
    def decompress_file(self, original_path: Path) -> Optional[Dict]:
        """압축 파일 해제 및 로드"""
        try:
            # 메타데이터 조회
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT compressed_path FROM compressed_files WHERE original_path = ?",
                    (str(original_path),)
                )
                result = cursor.fetchone()
            
            if not result:
                return None
            
            compressed_path = Path(result[0])
            if not compressed_path.exists():
                return None
            
            # 압축 해제 및 JSON 로드
            with gzip.open(compressed_path, 'rb') as f:
                data = json.loads(f.read().decode('utf-8'))
            
            # 액세스 시간 업데이트
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "UPDATE compressed_files SET last_accessed = ? WHERE original_path = ?",
                    (time.time(), str(original_path))
                )
                conn.commit()
            
            return data
            
        except Exception as e:
            logging.error(f"Decompression failed for {original_path}: {e}")
            return None
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """압축 통계"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as file_count,
                    SUM(original_size) as total_original_size,
                    SUM(compressed_size) as total_compressed_size,
                    AVG(compression_ratio) as avg_compression_ratio
                FROM compressed_files
            """)
            result = cursor.fetchone()
        
        if result and result[0] > 0:
            return {
                "file_count": result[0],
                "total_original_size": result[1] or 0,
                "total_compressed_size": result[2] or 0,
                "space_saved": (result[1] or 0) - (result[2] or 0),
                "avg_compression_ratio": result[3] or 1.0
            }
        else:
            return {
                "file_count": 0,
                "total_original_size": 0,
                "total_compressed_size": 0,
                "space_saved": 0,
                "avg_compression_ratio": 1.0
            }


class MemoryManager:
    """메모리 관리자"""
    
    def __init__(self, memory_limit_mb: int = 512):
        self.memory_limit = memory_limit_mb * 1024 * 1024  # bytes
        self.object_registry = weakref.WeakSet()
        self.cleanup_callbacks = []
        
    def register_object(self, obj):
        """메모리 관리 대상 객체 등록"""
        self.object_registry.add(obj)
    
    def add_cleanup_callback(self, callback: Callable):
        """정리 콜백 추가"""
        self.cleanup_callbacks.append(callback)
    
    def get_memory_usage(self) -> float:
        """현재 메모리 사용량 (MB)"""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    
    def check_memory_pressure(self) -> bool:
        """메모리 압박 상황 확인"""
        current_usage = self.get_memory_usage() * 1024 * 1024
        return current_usage > self.memory_limit
    
    def force_garbage_collection(self):
        """강제 가비지 컬렉션"""
        # 정리 콜백 실행
        for callback in self.cleanup_callbacks:
            try:
                callback()
            except Exception as e:
                logging.error(f"Cleanup callback error: {e}")
        
        # 가비지 컬렉션 강제 실행
        collected = gc.collect()
        logging.info(f"Garbage collection completed: {collected} objects collected")
        
        return collected
    
    def optimize_memory(self):
        """메모리 최적화"""
        if self.check_memory_pressure():
            logging.info("Memory pressure detected, starting optimization")
            
            # 가비지 컬렉션
            self.force_garbage_collection()
            
            # 추가 정리 작업
            if hasattr(gc, 'set_threshold'):
                # 가비지 컬렉션 임계값 조정
                gc.set_threshold(700, 10, 10)


class AsyncTaskManager:
    """비동기 작업 관리자"""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_tasks = {}
        self.task_counter = 0
        self.lock = threading.Lock()
    
    def submit_task(self, func: Callable, *args, **kwargs) -> int:
        """비동기 작업 제출"""
        with self.lock:
            task_id = self.task_counter
            self.task_counter += 1
            
            future = self.executor.submit(func, *args, **kwargs)
            self.active_tasks[task_id] = {
                "future": future,
                "start_time": time.time(),
                "function": func.__name__
            }
            
        return task_id
    
    def get_task_status(self, task_id: int) -> Optional[Dict[str, Any]]:
        """작업 상태 조회"""
        with self.lock:
            if task_id not in self.active_tasks:
                return None
            
            task = self.active_tasks[task_id]
            future = task["future"]
            
            status = {
                "task_id": task_id,
                "function": task["function"],
                "start_time": task["start_time"],
                "elapsed_time": time.time() - task["start_time"],
                "done": future.done(),
                "cancelled": future.cancelled()
            }
            
            if future.done():
                try:
                    status["result"] = future.result()
                    status["success"] = True
                except Exception as e:
                    status["error"] = str(e)
                    status["success"] = False
            
            return status
    
    def cancel_task(self, task_id: int) -> bool:
        """작업 취소"""
        with self.lock:
            if task_id not in self.active_tasks:
                return False
            
            future = self.active_tasks[task_id]["future"]
            return future.cancel()
    
    def cleanup_completed_tasks(self):
        """완료된 작업 정리"""
        with self.lock:
            completed_tasks = []
            for task_id, task in self.active_tasks.items():
                if task["future"].done():
                    completed_tasks.append(task_id)
            
            for task_id in completed_tasks:
                del self.active_tasks[task_id]
            
            return len(completed_tasks)
    
    def get_active_task_count(self) -> int:
        """활성 작업 수"""
        return len(self.active_tasks)
    
    def shutdown(self, wait: bool = True):
        """작업 관리자 종료"""
        self.executor.shutdown(wait=wait)


class PerformanceMonitor:
    """성능 모니터"""
    
    def __init__(self, history_size: int = 100):
        self.metrics_history = deque(maxlen=history_size)
        self.monitoring = False
        self.monitor_thread = None
        self.monitor_interval = 5.0  # seconds
        
    def start_monitoring(self):
        """모니터링 시작"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=self.monitor_interval + 1)
    
    def _monitor_loop(self):
        """모니터링 루프"""
        while self.monitoring:
            try:
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)
                time.sleep(self.monitor_interval)
            except Exception as e:
                logging.error(f"Performance monitoring error: {e}")
    
    def _collect_metrics(self) -> PerformanceMetrics:
        """성능 메트릭 수집"""
        process = psutil.Process()
        
        # 메모리 사용량
        memory_info = process.memory_info()
        memory_usage = memory_info.rss / 1024 / 1024  # MB
        
        # CPU 사용률
        cpu_usage = process.cpu_percent()
        
        # 디스크 사용량 (현재 프로세스의 파일 I/O)
        io_counters = process.io_counters() if hasattr(process, 'io_counters') else None
        disk_usage = 0
        if io_counters:
            disk_usage = (io_counters.read_bytes + io_counters.write_bytes) / 1024 / 1024
        
        return PerformanceMetrics(
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            disk_usage=disk_usage,
            response_time=0.0,  # 별도 측정 필요
            cache_hit_rate=0.0,  # 별도 측정 필요
            timestamp=time.time()
        )
    
    def get_current_metrics(self) -> Optional[PerformanceMetrics]:
        """현재 메트릭 조회"""
        if self.metrics_history:
            return self.metrics_history[-1]
        return None
    
    def get_average_metrics(self, minutes: int = 5) -> Optional[PerformanceMetrics]:
        """평균 메트릭 계산"""
        if not self.metrics_history:
            return None
        
        cutoff_time = time.time() - (minutes * 60)
        recent_metrics = [m for m in self.metrics_history if m.timestamp >= cutoff_time]
        
        if not recent_metrics:
            return None
        
        count = len(recent_metrics)
        return PerformanceMetrics(
            memory_usage=sum(m.memory_usage for m in recent_metrics) / count,
            cpu_usage=sum(m.cpu_usage for m in recent_metrics) / count,
            disk_usage=sum(m.disk_usage for m in recent_metrics) / count,
            response_time=sum(m.response_time for m in recent_metrics) / count,
            cache_hit_rate=sum(m.cache_hit_rate for m in recent_metrics) / count,
            timestamp=time.time()
        )


class PerformanceOptimizer:
    """통합 성능 최적화 관리자"""
    
    def __init__(self):
        self.memory_manager = MemoryManager()
        self.task_manager = AsyncTaskManager()
        self.monitor = PerformanceMonitor()
        self.compressed_data = CompressedDataManager()
        self.lru_cache = LRUCache(maxsize=500)
        
        # 정리 콜백 등록
        self.memory_manager.add_cleanup_callback(self.lru_cache.clear)
        self.memory_manager.add_cleanup_callback(self.task_manager.cleanup_completed_tasks)
    
    def start(self):
        """최적화 시스템 시작"""
        self.monitor.start_monitoring()
        logging.info("Performance optimizer started")
    
    def stop(self):
        """최적화 시스템 중지"""
        self.monitor.stop_monitoring()
        self.task_manager.shutdown()
        logging.info("Performance optimizer stopped")
    
    def optimize_if_needed(self):
        """필요 시 최적화 실행"""
        if self.memory_manager.check_memory_pressure():
            self.memory_manager.optimize_memory()
        
        # 완료된 작업 정리
        self.task_manager.cleanup_completed_tasks()
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """최적화 리포트 생성"""
        current_metrics = self.monitor.get_current_metrics()
        avg_metrics = self.monitor.get_average_metrics()
        compression_stats = self.compressed_data.get_compression_stats()
        
        return {
            "current_metrics": asdict(current_metrics) if current_metrics else None,
            "average_metrics": asdict(avg_metrics) if avg_metrics else None,
            "compression_stats": compression_stats,
            "cache_size": self.lru_cache.size(),
            "active_tasks": self.task_manager.get_active_task_count(),
            "memory_limit_mb": self.memory_manager.memory_limit / 1024 / 1024
        }
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


# 전역 최적화 인스턴스
_global_optimizer = None

def get_global_optimizer() -> PerformanceOptimizer:
    """전역 최적화 인스턴스 조회"""
    global _global_optimizer
    if _global_optimizer is None:
        _global_optimizer = PerformanceOptimizer()
    return _global_optimizer


def optimize_data_loading(data_loader_func: Callable) -> Callable:
    """데이터 로딩 함수 최적화 데코레이터"""
    def wrapper(*args, **kwargs):
        # 캐시 키 생성
        cache_key = f"{data_loader_func.__name__}_{hash(str(args) + str(kwargs))}"
        
        # 캐시에서 확인
        optimizer = get_global_optimizer()
        cached_result = optimizer.lru_cache.get(cache_key)
        if cached_result is not None:
            return cached_result
        
        # 비동기 실행
        task_id = optimizer.task_manager.submit_task(data_loader_func, *args, **kwargs)
        
        # 결과 대기 (동기식 인터페이스 유지)
        while True:
            status = optimizer.task_manager.get_task_status(task_id)
            if status and status["done"]:
                if status["success"]:
                    result = status["result"]
                    optimizer.lru_cache.set(cache_key, result)
                    return result
                else:
                    raise Exception(status.get("error", "Task failed"))
            time.sleep(0.1)
    
    return wrapper