#!/usr/bin/env python3
"""Stock Fundamentals Education Module"""

from typing import Dict, List, Any


class StockFundamentalsEducator:
    """Educational component for stock market fundamentals"""
    
    def __init__(self):
        self.lessons = {
            'basic_concepts': {
                'title': '주식 기초 개념',
                'content': self._get_basic_concepts_lesson(),
                'difficulty': 'beginner'
            },
            'financial_statements': {
                'title': '재무제표 읽기',
                'content': self._get_financial_statements_lesson(),
                'difficulty': 'intermediate'
            },
            'valuation_metrics': {
                'title': '주식 가치평가 지표',
                'content': self._get_valuation_metrics_lesson(),
                'difficulty': 'intermediate'
            },
            'market_analysis': {
                'title': '시장 분석 방법론',
                'content': self._get_market_analysis_lesson(),
                'difficulty': 'advanced'
            }
        }
    
    def get_lesson(self, lesson_id: str) -> Dict[str, Any]:
        """Get specific lesson content"""
        return self.lessons.get(lesson_id, {})
    
    def get_all_lessons(self) -> Dict[str, Dict[str, Any]]:
        """Get all available lessons"""
        return self.lessons
    
    def get_lessons_by_difficulty(self, difficulty: str) -> Dict[str, Dict[str, Any]]:
        """Get lessons filtered by difficulty level"""
        return {
            lesson_id: lesson for lesson_id, lesson in self.lessons.items()
            if lesson['difficulty'] == difficulty
        }
    
    def _get_basic_concepts_lesson(self) -> List[Dict[str, str]]:
        """Basic stock market concepts lesson"""
        return [
            {
                'section': '주식이란?',
                'content': '''
주식(Stock)은 회사의 소유권을 나타내는 증권입니다.

🏢 **회사 소유권**: 주식을 보유하면 해당 회사의 일부를 소유하게 됩니다
📊 **수익 참여**: 회사의 성장과 수익에 따라 주식 가치가 변동됩니다  
🗳️ **의결권**: 주주총회에서 회사 경영에 대한 의결권을 행사할 수 있습니다
💰 **배당금**: 회사가 수익을 배당할 때 지분에 따라 배당금을 받을 수 있습니다
                '''
            },
            {
                'section': '주식 거래 기초',
                'content': '''
주식 거래의 기본 원리를 이해해봅시다.

📈 **매수(Buy)**: 주식을 구매하는 것
📉 **매도(Sell)**: 보유한 주식을 판매하는 것
💹 **호가**: 매수/매도 희망 가격
⏰ **시장가 주문**: 현재 시장가로 즉시 거래
🎯 **지정가 주문**: 원하는 가격에서 거래 대기
                '''
            },
            {
                'section': '주식 시장 참가자',
                'content': '''
주식 시장에는 다양한 참가자들이 있습니다.

👤 **개인투자자**: 일반 개인들의 투자
🏛️ **기관투자자**: 연기금, 보험회사, 자산운용사 등
🏢 **외국인투자자**: 해외에서 투자하는 기관이나 개인
📊 **시장조성자**: 유동성을 제공하는 전문 거래회사
                '''
            }
        ]
    
    def _get_financial_statements_lesson(self) -> List[Dict[str, str]]:
        """Financial statements education lesson"""
        return [
            {
                'section': '재무제표의 종류',
                'content': '''
기업의 재무 상태를 파악하는 3가지 핵심 재무제표

📋 **재무상태표 (Balance Sheet)**
- 특정 시점의 자산, 부채, 자본 현황
- 회사의 재무 건전성을 파악

💰 **손익계산서 (Income Statement)**  
- 일정 기간의 수익과 비용
- 회사의 수익성을 평가

💸 **현금흐름표 (Cash Flow Statement)**
- 현금의 유입과 유출
- 실제 현금 창출 능력을 확인
                '''
            },
            {
                'section': '핵심 재무 지표',
                'content': '''
투자 결정에 중요한 재무 지표들

📊 **수익성 지표**
- ROE (자기자본이익률): 투자한 자본 대비 수익률
- ROA (총자산이익률): 전체 자산 대비 수익률
- 영업이익률: 매출 대비 영업이익 비율

💪 **안정성 지표**
- 부채비율: 자본 대비 부채 비율
- 유동비율: 단기 부채 상환 능력
- 이자보상배율: 이자 지급 능력

⚡ **성장성 지표**
- 매출 성장률: 매출의 증가 추세
- 순이익 성장률: 순이익의 증가 추세
                '''
            }
        ]
    
    def _get_valuation_metrics_lesson(self) -> List[Dict[str, str]]:
        """Stock valuation metrics lesson"""
        return [
            {
                'section': 'PER (Price to Earnings Ratio)',
                'content': '''
주가수익비율 - 가장 기본적인 밸류에이션 지표

🧮 **계산법**: 주가 ÷ 주당순이익(EPS)
📊 **의미**: 현재 주가가 1년간 벌어들인 순이익의 몇 배인가?

✅ **PER이 낮을 때**: 상대적으로 저평가 가능성
❌ **PER이 높을 때**: 상대적으로 고평가 가능성

⚠️ **주의사항**:
- 업종별로 평균 PER이 다름
- 성장주는 높은 PER도 정당화될 수 있음
- 일시적 손실로 PER이 왜곡될 수 있음
                '''
            },
            {
                'section': 'PBR (Price to Book Ratio)',
                'content': '''
주가순자산비율 - 자산 가치 대비 주가 평가

🧮 **계산법**: 주가 ÷ 주당순자산(BPS)  
📊 **의미**: 회사를 청산할 때 받을 수 있는 가치 대비 주가

✅ **PBR 1 미만**: 순자산보다 주가가 낮음 (저평가 가능성)
❌ **PBR이 높음**: 자산 가치 대비 주가가 높음

🎯 **활용법**:
- 자산집약적 업종(제조업, 건설업)에서 유용
- 성장 가능성보다 안정성 중시 투자에 적합
                '''
            },
            {
                'section': 'PCR, PSR 등 기타 지표',
                'content': '''
다양한 밸류에이션 지표들

💰 **PCR (Price to Cash Flow Ratio)**
- 주가 ÷ 주당현금흐름
- 실제 현금 창출 능력 대비 주가 평가

📈 **PSR (Price to Sales Ratio)**
- 주가 ÷ 주당매출
- 적자 기업이나 초기 성장 기업 평가에 유용

🔄 **EV/EBITDA**  
- 기업가치 ÷ 법인세·이자·감가상각비 차감전 영업이익
- 부채가 많은 기업 비교에 유용
                '''
            }
        ]
    
    def _get_market_analysis_lesson(self) -> List[Dict[str, str]]:
        """Market analysis methodology lesson"""
        return [
            {
                'section': '기본적 분석 (Fundamental Analysis)',
                'content': '''
기업의 내재 가치를 분석하는 방법

🏢 **기업 분석**
- 사업 모델 및 경쟁력 분석
- 재무제표 분석
- 경영진 역량 평가

🌍 **산업 분석**
- 산업의 성장성과 전망
- 경쟁 구조 분석  
- 규제 환경 변화

📊 **거시경제 분석**
- 경제 성장률, 금리, 환율
- 정부 정책 변화
- 글로벌 경제 동향
                '''
            },
            {
                'section': '기술적 분석 (Technical Analysis)',
                'content': '''
차트와 거래량을 통한 주가 분석

📈 **차트 패턴**
- 지지선과 저항선
- 추세선 분석
- 각종 패턴 (헤드앤숄더, 더블탑 등)

📊 **기술적 지표**
- 이동평균선 (MA)
- RSI (상대강도지수)
- MACD (이동평균수렴확산)
- 볼린저 밴드

📦 **거래량 분석**
- 거래량과 주가의 관계
- 거래량 급증의 의미
                '''
            }
        ]