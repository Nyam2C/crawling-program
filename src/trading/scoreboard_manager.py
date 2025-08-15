#!/usr/bin/env python3
"""
Scoreboard Manager for Mock Trading - Handles score persistence and management
모의 투자 스코어보드 매니저 - 점수 데이터 관리 및 저장
"""

import json
import os
from datetime import datetime
from typing import Optional, List, Dict
from .scoreboard_models import Scoreboard, ScoreRecord, ScoreboardResult
from .models import Portfolio


class ScoreboardManager:
    """스코어보드 데이터 관리자"""
    
    def __init__(self, data_file: str = "scoreboard_data.json"):
        self.data_file = data_file
        self.scoreboard = Scoreboard(records=[])
        self.load_data()
        self.session_start_time = datetime.now()  # 세션 시작 시간
    
    def create_record_from_portfolio(self, 
                                   nickname: str, 
                                   portfolio: Portfolio,
                                   result_type: ScoreboardResult,
                                   stock_prices: Dict[str, float],
                                   session_start_time: Optional[datetime] = None) -> ScoreRecord:
        """포트폴리오에서 스코어 기록 생성"""
        
        # 세션 시작 시간 계산
        if session_start_time:
            start_time = session_start_time
        else:
            start_time = self.session_start_time
        
        # 보유 기간 계산 (일 단위)
        holding_period = (datetime.now() - start_time).days
        if holding_period < 1:
            holding_period = 1  # 최소 1일
        
        # 최고 수익 종목 찾기
        best_stock = "None"
        best_stock_return = 0.0
        
        if portfolio.positions:
            best_position = None
            best_return = float('-inf')
            
            for symbol, position in portfolio.positions.items():
                # 현재 가격 정보가 필요하지만 여기서는 평균 가격 기준으로 계산
                current_value = position.quantity * position.average_price
                invested_value = position.total_invested
                
                if invested_value > 0:
                    position_return = ((current_value - invested_value) / invested_value) * 100
                    if position_return > best_return:
                        best_return = position_return
                        best_position = position
            
            if best_position:
                best_stock = best_position.symbol
                best_stock_return = best_return
        
        # 총 거래 횟수
        total_trades = len(portfolio.transactions)
        
        # 스코어 기록 생성
        record = ScoreRecord(
            nickname=nickname,
            date=datetime.now(),
            initial_balance=portfolio.initial_balance,
            final_balance=portfolio.get_total_value(stock_prices),
            return_rate=0.0,  # __post_init__에서 계산됨
            holding_period_days=holding_period,
            best_stock=best_stock,
            best_stock_return=best_stock_return,
            total_trades=total_trades,
            result_type=result_type
        )
        
        return record
    
    def add_score_record(self, record: ScoreRecord):
        """스코어 기록 추가"""
        self.scoreboard.add_record(record)
        self.save_data()
    
    def register_portfolio_score(self, 
                                nickname: str,
                                portfolio: Portfolio,
                                result_type: ScoreboardResult,
                                stock_prices: Dict[str, float],
                                session_start_time: Optional[datetime] = None):
        """포트폴리오 점수 등록"""
        record = self.create_record_from_portfolio(
            nickname, portfolio, result_type, stock_prices, session_start_time
        )
        self.add_score_record(record)
        return record
    
    def get_leaderboard(self, limit: int = 10) -> List[ScoreRecord]:
        """리더보드 조회"""
        return self.scoreboard.get_top_records(limit)
    
    def get_player_records(self, nickname: str) -> List[ScoreRecord]:
        """플레이어별 기록 조회"""
        return self.scoreboard.get_records_by_nickname(nickname)
    
    def get_player_best_score(self, nickname: str) -> Optional[ScoreRecord]:
        """플레이어 최고 기록"""
        player_records = self.get_player_records(nickname)
        if not player_records:
            return None
        return max(player_records, key=lambda x: x.rank_score)
    
    def get_current_rank(self, score: float) -> int:
        """현재 점수의 순위"""
        return self.scoreboard.get_rank_by_score(score)
    
    def get_statistics(self) -> dict:
        """스코어보드 통계"""
        stats = self.scoreboard.get_stats()
        
        # 추가 통계 계산
        if self.scoreboard.records:
            # 등급별 분포
            grade_distribution = {}
            for record in self.scoreboard.records:
                grade = record.grade
                grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
            
            # 결과 유형별 분포
            result_type_distribution = {}
            for record in self.scoreboard.records:
                result_type = record.result_type.value
                result_type_distribution[result_type] = result_type_distribution.get(result_type, 0) + 1
            
            stats['grade_distribution'] = grade_distribution
            stats['result_type_distribution'] = result_type_distribution
        
        return stats
    
    def save_data(self):
        """데이터 파일에 저장"""
        try:
            data = {
                'records': [
                    {
                        'nickname': record.nickname,
                        'date': record.date.isoformat(),
                        'initial_balance': record.initial_balance,
                        'final_balance': record.final_balance,
                        'return_rate': record.return_rate,
                        'holding_period_days': record.holding_period_days,
                        'best_stock': record.best_stock,
                        'best_stock_return': record.best_stock_return,
                        'total_trades': record.total_trades,
                        'result_type': record.result_type.value
                    }
                    for record in self.scoreboard.records
                ],
                'last_saved': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving scoreboard data: {e}")
    
    def load_data(self):
        """파일에서 데이터 로드"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            records = []
            for record_data in data.get('records', []):
                try:
                    record = ScoreRecord(
                        nickname=record_data['nickname'],
                        date=datetime.fromisoformat(record_data['date']),
                        initial_balance=record_data['initial_balance'],
                        final_balance=record_data['final_balance'],
                        return_rate=record_data['return_rate'],
                        holding_period_days=record_data['holding_period_days'],
                        best_stock=record_data['best_stock'],
                        best_stock_return=record_data['best_stock_return'],
                        total_trades=record_data['total_trades'],
                        result_type=ScoreboardResult(record_data['result_type'])
                    )
                    records.append(record)
                except Exception as e:
                    print(f"Error loading record: {e}")
                    continue
            
            self.scoreboard.records = records
            # 점수순으로 다시 정렬
            self.scoreboard.records.sort(key=lambda x: x.rank_score, reverse=True)
                
        except Exception as e:
            print(f"Error loading scoreboard data: {e}")
    
    def reset_session_timer(self):
        """세션 타이머 리셋 (새로운 모의투자 시작)"""
        self.session_start_time = datetime.now()
    
    def clear_all_records(self):
        """모든 기록 삭제 (개발/테스트용)"""
        self.scoreboard.records = []
        self.save_data()
    
    def export_to_csv(self, filename: str = None) -> str:
        """CSV 파일로 내보내기"""
        if not filename:
            filename = f"scoreboard_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Rank', 'Nickname', 'Date', 'Initial Balance', 'Final Balance',
                    'Return Rate (%)', 'Profit/Loss', 'Holding Period (Days)', 
                    'Best Stock', 'Best Stock Return (%)', 'Total Trades',
                    'Grade', 'Result Type', 'Rank Score'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for rank, record in enumerate(self.scoreboard.records, 1):
                    writer.writerow({
                        'Rank': rank,
                        'Nickname': record.nickname,
                        'Date': record.date.strftime('%Y-%m-%d %H:%M'),
                        'Initial Balance': f"${record.initial_balance:,.2f}",
                        'Final Balance': f"${record.final_balance:,.2f}",
                        'Return Rate (%)': f"{record.return_rate:.2f}%",
                        'Profit/Loss': f"${record.profit_loss:,.2f}",
                        'Holding Period (Days)': record.holding_period_days,
                        'Best Stock': record.best_stock,
                        'Best Stock Return (%)': f"{record.best_stock_return:.2f}%",
                        'Total Trades': record.total_trades,
                        'Grade': record.grade,
                        'Result Type': record.result_type.value,
                        'Rank Score': f"{record.rank_score:.2f}"
                    })
            
            return filename
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return None