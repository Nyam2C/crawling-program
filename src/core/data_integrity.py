#!/usr/bin/env python3
"""
Data Integrity Manager - JSON 파일 백업, 복구 및 무결성 검증
"""

import json
import os
import shutil
import gzip
import hashlib
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging


class DataIntegrityManager:
    """데이터 무결성 관리자 - 백업, 복구, 검증"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.backup_dir = self.base_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # 로깅 설정
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.FileHandler(self.base_dir / "data_integrity.log")
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        # 백업 스레드 관리
        self.backup_thread = None
        self.stop_backup = threading.Event()
        self.backup_interval = 300  # 5분마다 백업
        
        # 모니터링할 파일들 (절대 경로로 설정)
        self.monitored_files = [
            self.base_dir / "mock_trading_data.json",
            self.base_dir / "scoreboard_data.json", 
            self.base_dir / "stock_data.json",
            self.base_dir / "settings.json"
        ]
        
        # 파일 체크섬 캐시
        self.file_checksums = {}
        
    def start_auto_backup(self):
        """자동 백업 시작"""
        if self.backup_thread and self.backup_thread.is_alive():
            return
            
        self.stop_backup.clear()
        self.backup_thread = threading.Thread(target=self._backup_worker, daemon=True)
        self.backup_thread.start()
        self.logger.info("Auto backup started")
        
    def stop_auto_backup(self):
        """자동 백업 중지"""
        if self.backup_thread and self.backup_thread.is_alive():
            self.stop_backup.set()
            self.backup_thread.join(timeout=5)
            self.logger.info("Auto backup stopped")
    
    def _backup_worker(self):
        """백업 워커 스레드"""
        while not self.stop_backup.wait(self.backup_interval):
            try:
                self.create_incremental_backup()
            except Exception as e:
                self.logger.error(f"Auto backup failed: {e}")
    
    def calculate_file_checksum(self, file_path: Path) -> str:
        """파일 체크섬 계산"""
        if not file_path.exists():
            return ""
            
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"Checksum calculation failed for {file_path}: {e}")
            return ""
    
    def verify_json_integrity(self, file_path: Path) -> tuple[bool, str]:
        """JSON 파일 무결성 검증"""
        try:
            if not file_path.exists():
                return False, "File does not exist"
                
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
                
            return True, "File is valid"
            
        except json.JSONDecodeError as e:
            return False, f"JSON decode error: {e}"
        except Exception as e:
            return False, f"File access error: {e}"
    
    def create_backup(self, file_path: Path, backup_type: str = "manual") -> bool:
        """개별 파일 백업 생성"""
        try:
            if not file_path.exists():
                self.logger.warning(f"File not found for backup: {file_path}")
                return False
            
            # 무결성 검증
            is_valid, message = self.verify_json_integrity(file_path)
            if not is_valid:
                self.logger.error(f"File integrity check failed: {file_path} - {message}")
                return False
            
            # 백업 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{file_path.stem}_{timestamp}_{backup_type}.json.gz"
            backup_path = self.backup_dir / backup_filename
            
            # 압축 백업 생성
            with open(file_path, 'rb') as f_in:
                with gzip.open(backup_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # 메타데이터 저장
            metadata = {
                "original_file": str(file_path),
                "backup_time": datetime.now().isoformat(),
                "backup_type": backup_type,
                "checksum": self.calculate_file_checksum(file_path),
                "file_size": file_path.stat().st_size
            }
            
            metadata_path = backup_path.with_suffix('.json.gz.meta')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Backup created: {backup_filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Backup creation failed: {e}")
            return False
    
    def create_incremental_backup(self) -> bool:
        """변경된 파일만 증분 백업"""
        backup_count = 0
        
        for file_path in self.monitored_files:
            if not file_path.exists():
                continue
                
            # 체크섬 비교로 변경 여부 확인
            current_checksum = self.calculate_file_checksum(file_path)
            last_checksum = self.file_checksums.get(str(file_path))
            
            if current_checksum != last_checksum:
                if self.create_backup(file_path, "incremental"):
                    self.file_checksums[str(file_path)] = current_checksum
                    backup_count += 1
        
        if backup_count > 0:
            self.logger.info(f"Incremental backup completed: {backup_count} files")
            
        return backup_count > 0
    
    def list_backups(self, file_pattern: Optional[str] = None) -> List[Dict[str, Any]]:
        """백업 파일 목록 조회"""
        backups = []
        
        for backup_file in self.backup_dir.glob("*.json.gz"):
            if file_pattern and file_pattern not in backup_file.name:
                continue
                
            metadata_file = backup_file.with_suffix('.json.gz.meta')
            metadata = {}
            
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                except Exception:
                    pass
            
            backup_info = {
                "filename": backup_file.name,
                "path": backup_file,
                "size": backup_file.stat().st_size,
                "created": datetime.fromtimestamp(backup_file.stat().st_ctime),
                "metadata": metadata
            }
            backups.append(backup_info)
        
        # 생성 시간순 정렬 (최신순)
        backups.sort(key=lambda x: x["created"], reverse=True)
        return backups
    
    def restore_backup(self, backup_path: Path, target_path: Optional[Path] = None) -> bool:
        """백업에서 파일 복원"""
        try:
            if not backup_path.exists():
                self.logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # 메타데이터 로드
            metadata_path = backup_path.with_suffix('.json.gz.meta')
            original_path = None
            
            if metadata_path.exists():
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        original_path = Path(metadata.get("original_file", ""))
                except Exception:
                    pass
            
            # 복원 대상 경로 결정
            if target_path:
                restore_path = target_path
            elif original_path:
                restore_path = original_path
            else:
                # 백업 파일명에서 원본 파일명 추정
                name_parts = backup_path.stem.split('_')
                if len(name_parts) >= 3:
                    original_name = '_'.join(name_parts[:-2]) + '.json'
                    restore_path = self.base_dir / original_name
                else:
                    self.logger.error(f"Cannot determine restore path for {backup_path}")
                    return False
            
            # 기존 파일 백업 (복원 전)
            if restore_path.exists():
                backup_name = f"{restore_path.stem}_pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_copy = restore_path.parent / backup_name
                shutil.copy2(restore_path, backup_copy)
                self.logger.info(f"Pre-restore backup created: {backup_name}")
            
            # 압축 해제 및 복원
            with gzip.open(backup_path, 'rb') as f_in:
                with open(restore_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # 복원된 파일 검증
            is_valid, message = self.verify_json_integrity(restore_path)
            if not is_valid:
                self.logger.error(f"Restored file integrity check failed: {message}")
                return False
            
            self.logger.info(f"File restored successfully: {restore_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Restore failed: {e}")
            return False
    
    def cleanup_old_backups(self, days_to_keep: int = 30):
        """오래된 백업 파일 정리"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted_count = 0
        
        for backup_file in self.backup_dir.glob("*.json.gz"):
            file_date = datetime.fromtimestamp(backup_file.stat().st_ctime)
            if file_date < cutoff_date:
                try:
                    backup_file.unlink()
                    # 메타데이터 파일도 삭제
                    metadata_file = backup_file.with_suffix('.json.gz.meta')
                    if metadata_file.exists():
                        metadata_file.unlink()
                    deleted_count += 1
                except Exception as e:
                    self.logger.error(f"Failed to delete old backup {backup_file}: {e}")
        
        if deleted_count > 0:
            self.logger.info(f"Cleaned up {deleted_count} old backup files")
    
    def get_backup_summary(self) -> Dict[str, Any]:
        """백업 현황 요약"""
        backups = self.list_backups()
        
        if not backups:
            return {
                "total_backups": 0,
                "total_size": 0,
                "latest_backup": None,
                "backup_files": {}
            }
        
        # 파일별 백업 현황
        backup_files = {}
        total_size = 0
        
        for backup in backups:
            total_size += backup["size"]
            
            # 원본 파일명 추출
            name_parts = backup["filename"].split('_')
            if len(name_parts) >= 3:
                original_name = '_'.join(name_parts[:-2])
                if original_name not in backup_files:
                    backup_files[original_name] = []
                backup_files[original_name].append(backup)
        
        return {
            "total_backups": len(backups),
            "total_size": total_size,
            "latest_backup": backups[0]["created"] if backups else None,
            "backup_files": backup_files
        }
    
    def emergency_recovery(self) -> bool:
        """긴급 복구 - 모든 파일의 최신 백업으로 복원"""
        recovery_count = 0
        
        for file_path in self.monitored_files:
            # 현재 파일이 손상되었는지 확인
            if file_path.exists():
                is_valid, _ = self.verify_json_integrity(file_path)
                if is_valid:
                    continue  # 정상 파일은 건드리지 않음
            
            # 최신 백업 찾기
            filename_pattern = file_path.stem  # .json 확장자 제거
            backups = self.list_backups(filename_pattern)
            if not backups:
                self.logger.warning(f"No backup found for {file_path.name}")
                continue
            
            latest_backup = backups[0]
            if self.restore_backup(latest_backup["path"], file_path):
                recovery_count += 1
                self.logger.info(f"Emergency recovery completed for {file_path.name}")
        
        return recovery_count > 0
    
    def __enter__(self):
        """Context manager 진입"""
        self.start_auto_backup()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager 종료"""
        self.stop_auto_backup()