#!/usr/bin/env python3
"""
Investment Personality Analyzer - Analyzes trading patterns from scoreboard data
투자 성향 분석기 - 스코어보드 데이터로부터 투자 패턴을 분석
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import statistics

from src.trading.scoreboard_models import ScoreRecord


class RiskTolerance(Enum):
    """위험 성향"""
    CONSERVATIVE = "Conservative"  # 보수적
    MODERATE = "Moderate"         # 중간
    AGGRESSIVE = "Aggressive"     # 공격적


class InvestmentStyle(Enum):
    """투자 스타일"""
    LONG_TERM = "Long-term Investor"    # 장기 투자자
    SHORT_TERM = "Short-term Trader"    # 단기 거래자
    SWING_TRADER = "Swing Trader"       # 스윙 트레이더
    DAY_TRADER = "Day Trader"           # 데이 트레이더


class TradingFrequency(Enum):
    """거래 빈도"""
    MINIMAL = "Minimal Trader"      # 최소 거래
    MODERATE = "Moderate Trader"    # 적당한 거래
    ACTIVE = "Active Trader"        # 활발한 거래
    HYPERACTIVE = "Hyperactive"     # 과도한 거래


@dataclass
class PersonalityMetrics:
    """투자 성향 분석 결과"""
    risk_tolerance: RiskTolerance
    investment_style: InvestmentStyle
    trading_frequency: TradingFrequency
    
    # 수치 점수들 (0-100)
    patience_score: float           # 인내심 점수
    consistency_score: float        # 일관성 점수
    profitability_score: float      # 수익성 점수
    discipline_score: float         # 규율성 점수
    
    # 상세 분석
    average_holding_period: float   # 평균 보유 기간
    win_rate: float                # 성공률
    average_return: float          # 평균 수익률
    volatility: float              # 변동성
    
    # 투자 성향 설명
    personality_description: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]


class InvestmentPersonalityAnalyzer:
    """투자 성향 분석기"""
    
    def __init__(self):
        self.analysis_cache = {}
    
    def analyze_personality(self, records: List[ScoreRecord], nickname: str = None) -> PersonalityMetrics:
        """투자 성향 분석 수행"""
        if not records:
            return self._create_default_metrics()
        
        # 특정 닉네임 필터링 (옵션)
        if nickname:
            records = [r for r in records if r.nickname.lower() == nickname.lower()]
            if not records:
                return self._create_default_metrics()
        
        # 각 분석 요소 계산
        risk_tolerance = self._analyze_risk_tolerance(records)
        investment_style = self._analyze_investment_style(records)
        trading_frequency = self._analyze_trading_frequency(records)
        
        # 점수 계산
        patience_score = self._calculate_patience_score(records)
        consistency_score = self._calculate_consistency_score(records)
        profitability_score = self._calculate_profitability_score(records)
        discipline_score = self._calculate_discipline_score(records)
        
        # 통계 계산
        stats = self._calculate_statistics(records)
        
        # 성향 설명 및 조언 생성
        description, strengths, weaknesses, recommendations = self._generate_insights(
            risk_tolerance, investment_style, trading_frequency,
            patience_score, consistency_score, profitability_score, discipline_score
        )
        
        return PersonalityMetrics(
            risk_tolerance=risk_tolerance,
            investment_style=investment_style,
            trading_frequency=trading_frequency,
            patience_score=patience_score,
            consistency_score=consistency_score,
            profitability_score=profitability_score,
            discipline_score=discipline_score,
            average_holding_period=stats['avg_holding_period'],
            win_rate=stats['win_rate'],
            average_return=stats['avg_return'],
            volatility=stats['volatility'],
            personality_description=description,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )
    
    def _analyze_risk_tolerance(self, records: List[ScoreRecord]) -> RiskTolerance:
        """위험 성향 분석"""
        # 수익률 변동성과 손실 허용도를 기반으로 분석
        returns = [r.return_rate for r in records]
        
        if not returns:
            return RiskTolerance.MODERATE
        
        # 변동성 계산
        volatility = statistics.stdev(returns) if len(returns) > 1 else 0
        
        # 손실 기록 비율
        loss_records = [r for r in records if r.return_rate < 0]
        loss_ratio = len(loss_records) / len(records)
        
        # 큰 손실 (-20% 이상) 기록
        big_loss_records = [r for r in records if r.return_rate < -20]
        big_loss_ratio = len(big_loss_records) / len(records)
        
        # 위험 점수 계산 (높을수록 공격적)
        risk_score = 0
        
        # 변동성이 클수록 공격적
        if volatility > 30:
            risk_score += 3
        elif volatility > 15:
            risk_score += 2
        elif volatility > 5:
            risk_score += 1
        
        # 손실을 많이 경험할수록 공격적 (위험 감수)
        if big_loss_ratio > 0.3:
            risk_score += 3
        elif big_loss_ratio > 0.1:
            risk_score += 2
        elif loss_ratio > 0.5:
            risk_score += 1
        
        # 높은 수익률 추구 시 공격적
        max_return = max(returns)
        if max_return > 50:
            risk_score += 2
        elif max_return > 20:
            risk_score += 1
        
        # 분류
        if risk_score >= 5:
            return RiskTolerance.AGGRESSIVE
        elif risk_score >= 2:
            return RiskTolerance.MODERATE
        else:
            return RiskTolerance.CONSERVATIVE
    
    def _analyze_investment_style(self, records: List[ScoreRecord]) -> InvestmentStyle:
        """투자 스타일 분석"""
        if not records:
            return InvestmentStyle.MODERATE
        
        # 평균 보유 기간
        avg_holding = sum(r.holding_period_days for r in records) / len(records)
        
        # 거래 빈도
        avg_trades = sum(r.total_trades for r in records) / len(records)
        
        # 스타일 결정
        if avg_holding >= 90:  # 3개월 이상
            return InvestmentStyle.LONG_TERM
        elif avg_holding >= 7:  # 1주일 이상
            if avg_trades <= 5:
                return InvestmentStyle.SWING_TRADER
            else:
                return InvestmentStyle.SHORT_TERM
        else:  # 1주일 미만
            return InvestmentStyle.DAY_TRADER
    
    def _analyze_trading_frequency(self, records: List[ScoreRecord]) -> TradingFrequency:
        """거래 빈도 분석"""
        if not records:
            return TradingFrequency.MODERATE
        
        avg_trades = sum(r.total_trades for r in records) / len(records)
        
        if avg_trades <= 3:
            return TradingFrequency.MINIMAL
        elif avg_trades <= 10:
            return TradingFrequency.MODERATE
        elif avg_trades <= 25:
            return TradingFrequency.ACTIVE
        else:
            return TradingFrequency.HYPERACTIVE
    
    def _calculate_patience_score(self, records: List[ScoreRecord]) -> float:
        """인내심 점수 계산 (장기 보유 능력)"""
        if not records:
            return 50.0
        
        avg_holding = sum(r.holding_period_days for r in records) / len(records)
        
        # 보유 기간이 길수록 높은 점수
        if avg_holding >= 100:
            return 95.0
        elif avg_holding >= 30:
            return 80.0
        elif avg_holding >= 7:
            return 60.0
        elif avg_holding >= 3:
            return 40.0
        else:
            return 20.0
    
    def _calculate_consistency_score(self, records: List[ScoreRecord]) -> float:
        """일관성 점수 계산 (수익률 안정성)"""
        if len(records) < 2:
            return 50.0
        
        returns = [r.return_rate for r in records]
        volatility = statistics.stdev(returns)
        
        # 변동성이 낮을수록 높은 점수
        if volatility <= 5:
            return 90.0
        elif volatility <= 15:
            return 70.0
        elif volatility <= 30:
            return 50.0
        elif volatility <= 50:
            return 30.0
        else:
            return 10.0
    
    def _calculate_profitability_score(self, records: List[ScoreRecord]) -> float:
        """수익성 점수 계산"""
        if not records:
            return 50.0
        
        profitable_records = [r for r in records if r.return_rate > 0]
        profitability_ratio = len(profitable_records) / len(records)
        avg_return = sum(r.return_rate for r in records) / len(records)
        
        # 수익 비율과 평균 수익률 조합
        ratio_score = profitability_ratio * 50  # 0-50점
        return_score = min(max(avg_return + 10, 0), 50)  # 0-50점
        
        return min(ratio_score + return_score, 100.0)
    
    def _calculate_discipline_score(self, records: List[ScoreRecord]) -> float:
        """규율성 점수 계산 (계획적 투자 여부)"""
        if not records:
            return 50.0
        
        # 거래 빈도의 일관성
        trades = [r.total_trades for r in records]
        if len(trades) > 1:
            trade_consistency = 100 - min(statistics.stdev(trades) * 5, 50)
        else:
            trade_consistency = 50
        
        # 극단적 손실 회피 능력
        extreme_losses = [r for r in records if r.return_rate < -30]
        loss_avoidance = max(100 - len(extreme_losses) * 20, 0)
        
        return (trade_consistency + loss_avoidance) / 2
    
    def _calculate_statistics(self, records: List[ScoreRecord]) -> Dict:
        """통계 계산"""
        if not records:
            return {
                'avg_holding_period': 0,
                'win_rate': 0,
                'avg_return': 0,
                'volatility': 0
            }
        
        returns = [r.return_rate for r in records]
        holding_periods = [r.holding_period_days for r in records]
        
        profitable_records = [r for r in records if r.return_rate > 0]
        win_rate = len(profitable_records) / len(records) * 100
        
        return {
            'avg_holding_period': sum(holding_periods) / len(holding_periods),
            'win_rate': win_rate,
            'avg_return': sum(returns) / len(returns),
            'volatility': statistics.stdev(returns) if len(returns) > 1 else 0
        }
    
    def _generate_insights(self, risk_tolerance: RiskTolerance, investment_style: InvestmentStyle,
                          trading_frequency: TradingFrequency, patience: float, consistency: float,
                          profitability: float, discipline: float) -> Tuple[str, List[str], List[str], List[str]]:
        """성향 설명 및 조언 생성"""
        
        # 기본 성향 설명
        description = f"You are a {risk_tolerance.value.lower()} {investment_style.value.lower()} "
        description += f"with {trading_frequency.value.lower()} characteristics."
        
        strengths = []
        weaknesses = []
        recommendations = []
        
        # 위험 성향별 분석
        if risk_tolerance == RiskTolerance.CONSERVATIVE:
            strengths.append("Risk management - You prioritize capital preservation")
            strengths.append("Stable returns - You achieve consistent performance")
            recommendations.append("Consider gradually increasing position sizes for better returns")
            recommendations.append("Explore moderately risky assets for portfolio growth")
        elif risk_tolerance == RiskTolerance.AGGRESSIVE:
            strengths.append("High return potential - You're not afraid of big opportunities")
            strengths.append("Market volatility tolerance - You can handle market swings")
            weaknesses.append("Higher volatility in returns")
            recommendations.append("Implement stop-loss strategies to limit downside")
            recommendations.append("Consider position sizing to manage overall portfolio risk")
        
        # 점수별 분석
        if patience >= 80:
            strengths.append("Excellent patience - You can hold positions for optimal timing")
        elif patience <= 40:
            weaknesses.append("Impatient trading - May exit positions too early")
            recommendations.append("Practice holding winners longer for better returns")
        
        if consistency >= 80:
            strengths.append("Consistent performance - Your returns are stable and predictable")
        elif consistency <= 40:
            weaknesses.append("Inconsistent results - Performance varies significantly")
            recommendations.append("Focus on developing a systematic trading approach")
        
        if profitability >= 80:
            strengths.append("High profitability - You consistently generate positive returns")
        elif profitability <= 40:
            weaknesses.append("Low win rate - Need to improve trade selection")
            recommendations.append("Study market analysis techniques to improve trade quality")
        
        if discipline >= 80:
            strengths.append("Strong discipline - You stick to your trading plan")
        elif discipline <= 40:
            weaknesses.append("Lack of discipline - Emotional trading decisions")
            recommendations.append("Develop and follow a structured trading plan")
        
        # 기본 조언이 없으면 일반적인 조언 추가
        if not recommendations:
            recommendations.append("Continue your current approach with minor optimizations")
            recommendations.append("Consider diversifying your strategies")
        
        return description, strengths, weaknesses, recommendations
    
    def _create_default_metrics(self) -> PersonalityMetrics:
        """기본 메트릭 생성 (데이터가 없을 때)"""
        return PersonalityMetrics(
            risk_tolerance=RiskTolerance.MODERATE,
            investment_style=InvestmentStyle.SWING_TRADER,
            trading_frequency=TradingFrequency.MODERATE,
            patience_score=50.0,
            consistency_score=50.0,
            profitability_score=50.0,
            discipline_score=50.0,
            average_holding_period=0,
            win_rate=0,
            average_return=0,
            volatility=0,
            personality_description="Insufficient data for analysis",
            strengths=["Ready to start your investment journey"],
            weaknesses=["No trading history available"],
            recommendations=["Start with small positions to build experience", "Focus on learning market fundamentals"]
        )
    
    def compare_personalities(self, records1: List[ScoreRecord], records2: List[ScoreRecord]) -> Dict:
        """두 투자자의 성향 비교"""
        metrics1 = self.analyze_personality(records1)
        metrics2 = self.analyze_personality(records2)
        
        comparison = {
            'investor1': metrics1,
            'investor2': metrics2,
            'differences': {
                'risk_tolerance': f"{metrics1.risk_tolerance.value} vs {metrics2.risk_tolerance.value}",
                'investment_style': f"{metrics1.investment_style.value} vs {metrics2.investment_style.value}",
                'patience_diff': metrics1.patience_score - metrics2.patience_score,
                'consistency_diff': metrics1.consistency_score - metrics2.consistency_score,
                'profitability_diff': metrics1.profitability_score - metrics2.profitability_score,
                'discipline_diff': metrics1.discipline_score - metrics2.discipline_score
            }
        }
        
        return comparison