#!/usr/bin/env python3
"""
Scoreboard Models for Mock Trading - Arcade Style Score Records
모의 투자 스코어보드 모델 - 오락실 스타일 점수 기록
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum


class ScoreboardResult(Enum):
    """스코어보드 등록 사유"""
    RESET = "RESET"  # 포트폴리오 리셋
    BANKRUPTCY = "BANKRUPTCY"  # 파산 (자산 < 1000)
    MANUAL_SAVE = "MANUAL_SAVE"  # 수동 저장


@dataclass
class ScoreRecord:
    """개별 스코어 기록"""
    nickname: str  # 닉네임
    date: datetime  # 기록 날짜
    initial_balance: float  # 시작 자본
    final_balance: float  # 최종 자본
    return_rate: float  # 수익률 (%)
    holding_period_days: int  # 보유 기간 (일)
    best_stock: str  # 최고 수익 종목
    best_stock_return: float  # 최고 종목 수익률 (%)
    total_trades: int  # 총 거래 횟수
    result_type: ScoreboardResult  # 기록 사유
    
    def __post_init__(self):
        """계산된 필드 설정"""
        if self.initial_balance > 0:
            self.return_rate = ((self.final_balance - self.initial_balance) / self.initial_balance) * 100
        else:
            self.return_rate = 0.0
    
    @property
    def is_profitable(self) -> bool:
        """수익 여부"""
        return self.return_rate > 0
    
    @property
    def profit_loss(self) -> float:
        """손익 금액"""
        return self.final_balance - self.initial_balance
    
    @property
    def rank_score(self) -> float:
        """랭킹용 점수 계산 (수익률 + 보유기간 보너스)"""
        # 기본 점수는 수익률
        base_score = self.return_rate
        
        # 보유기간에 따른 보너스 (장기투자 우대)
        # 7일 이상: +5%, 30일 이상: +10%, 100일 이상: +20%
        if self.holding_period_days >= 100:
            time_bonus = 20.0
        elif self.holding_period_days >= 30:
            time_bonus = 10.0
        elif self.holding_period_days >= 7:
            time_bonus = 5.0
        else:
            time_bonus = 0.0
        
        # 거래 횟수에 따른 보너스/패널티 (적절한 거래 우대)
        # 5-20회: +2%, 그 외는 패널티 또는 보너스 없음
        if 5 <= self.total_trades <= 20:
            trade_bonus = 2.0
        elif self.total_trades > 50:
            trade_bonus = -5.0  # 과도한 거래 패널티
        else:
            trade_bonus = 0.0
        
        return base_score + time_bonus + trade_bonus
    
    @property
    def grade(self) -> str:
        """성과 등급"""
        if self.return_rate >= 50:
            return "S+"
        elif self.return_rate >= 30:
            return "S"
        elif self.return_rate >= 20:
            return "A+"
        elif self.return_rate >= 10:
            return "A"
        elif self.return_rate >= 5:
            return "B+"
        elif self.return_rate >= 0:
            return "B"
        elif self.return_rate >= -10:
            return "C"
        elif self.return_rate >= -25:
            return "D"
        else:
            return "F"


@dataclass 
class Scoreboard:
    """스코어보드 전체 데이터"""
    records: List[ScoreRecord]
    
    def __post_init__(self):
        if self.records is None:
            self.records = []
    
    def add_record(self, record: ScoreRecord):
        """새로운 기록 추가"""
        self.records.append(record)
        # 점수순으로 정렬 (내림차순)
        self.records.sort(key=lambda x: x.rank_score, reverse=True)
        
        # 상위 100개 기록만 유지
        if len(self.records) > 100:
            self.records = self.records[:100]
    
    def get_top_records(self, limit: int = 10) -> List[ScoreRecord]:
        """상위 기록 조회"""
        return self.records[:limit]
    
    def get_records_by_nickname(self, nickname: str) -> List[ScoreRecord]:
        """특정 닉네임의 기록들"""
        return [r for r in self.records if r.nickname.lower() == nickname.lower()]
    
    def get_rank_by_score(self, score: float) -> int:
        """점수로 순위 계산"""
        higher_scores = [r for r in self.records if r.rank_score > score]
        return len(higher_scores) + 1
    
    @property
    def total_records(self) -> int:
        """총 기록 수"""
        return len(self.records)
    
    @property
    def average_return_rate(self) -> float:
        """평균 수익률"""
        if not self.records:
            return 0.0
        return sum(r.return_rate for r in self.records) / len(self.records)
    
    def get_stats(self) -> dict:
        """스코어보드 통계"""
        if not self.records:
            return {
                'total_records': 0,
                'average_return': 0.0,
                'best_return': 0.0,
                'worst_return': 0.0,
                'profitable_ratio': 0.0
            }
        
        profitable_count = sum(1 for r in self.records if r.is_profitable)
        
        return {
            'total_records': len(self.records),
            'average_return': self.average_return_rate,
            'best_return': max(r.return_rate for r in self.records),
            'worst_return': min(r.return_rate for r in self.records),
            'profitable_ratio': (profitable_count / len(self.records)) * 100
        }