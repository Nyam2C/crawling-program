#!/usr/bin/env python3
"""
News Sentiment Analyzer - 뉴스 감정 분석기
주식 관련 뉴스를 수집하고 감정을 분석하여 투자 인사이트 제공
"""

import asyncio
import aiohttp
import feedparser
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
import re
import time

# Sentiment analysis libraries
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentType(Enum):
    """감정 타입"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"

@dataclass
class NewsArticle:
    """뉴스 기사 데이터 클래스"""
    title: str
    content: str
    url: str
    source: str
    published_date: datetime
    symbol: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_type: Optional[SentimentType] = None
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []

@dataclass
class SentimentAnalysis:
    """감정 분석 결과"""
    overall_sentiment: SentimentType
    sentiment_score: float  # -1 to 1
    confidence: float  # 0 to 1
    positive_ratio: float
    negative_ratio: float
    neutral_ratio: float
    article_count: int
    analysis_date: datetime

class NewsSentimentAnalyzer:
    """뉴스 감정 분석기"""
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.logger = logging.getLogger(__name__)
        
        # News sources configuration
        self.news_sources = {
            'yahoo_finance_rss': {
                'url': 'https://feeds.finance.yahoo.com/rss/2.0/headline',
                'type': 'rss'
            },
            'marketwatch_rss': {
                'url': 'http://feeds.marketwatch.com/marketwatch/marketpulse/',
                'type': 'rss'
            },
            'reuters_business': {
                'url': 'http://feeds.reuters.com/reuters/businessNews',
                'type': 'rss'
            },
            'cnbc_rss': {
                'url': 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114',
                'type': 'rss'
            }
        }
        
        # Cache for articles
        self.article_cache = {}
        self.cache_duration = 3600  # 1 hour
        
    def get_stock_news(self, symbol: str, limit: int = 50) -> List[NewsArticle]:
        """
        새로운 3단계 뉴스 분석 알고리즘
        1단계: 심볼 분석 시작
        2단계: 해당 심볼과 관련된 주요 키워드 탐색
        3단계: 해당 키워드와 관련된 뉴스 탐색
        
        Args:
            symbol: 주식 심볼 (예: 'AAPL')
            limit: 최대 뉴스 개수
            
        Returns:
            List[NewsArticle]: 뉴스 기사 리스트
        """
        cache_key = f"{symbol}_{int(time.time() // self.cache_duration)}"
        
        if cache_key in self.article_cache:
            return self.article_cache[cache_key][:limit]
        
        # 1단계: 심볼 분석 시작
        self.logger.info(f"Starting 3-step news analysis for {symbol}")
        
        # 2단계: 해당 심볼과 관련된 주요 키워드 탐색
        relevant_keywords = self._get_symbol_keywords(symbol)
        self.logger.info(f"Found {len(relevant_keywords)} relevant keywords for {symbol}: {relevant_keywords}")
        
        # 3단계: 해당 키워드와 관련된 뉴스 탐색
        all_articles = []
        
        # 키워드 기반 뉴스 수집
        for keyword in relevant_keywords:
            # RSS 피드에서 키워드 기반 뉴스 수집
            for source_name, config in self.news_sources.items():
                try:
                    if config['type'] == 'rss':
                        articles = self._fetch_keyword_based_news(source_name, config['url'], symbol, keyword)
                        all_articles.extend(articles)
                except Exception as e:
                    self.logger.warning(f"Failed to fetch from {source_name} for keyword {keyword}: {e}")
        
        # Yahoo Finance API를 통한 특정 주식 뉴스 (기존 방식 유지)
        try:
            yahoo_articles = self._fetch_yahoo_stock_news(symbol)
            all_articles.extend(yahoo_articles)
        except Exception as e:
            self.logger.warning(f"Failed to fetch Yahoo news for {symbol}: {e}")
        
        # 날짜순 정렬 및 중복 제거
        unique_articles = self._deduplicate_articles(all_articles)
        unique_articles.sort(key=lambda x: x.published_date, reverse=True)
        
        # 캐시 저장
        self.article_cache[cache_key] = unique_articles
        
        self.logger.info(f"Completed 3-step analysis: collected {len(unique_articles)} unique articles for {symbol}")
        return unique_articles[:limit]
    
    def _get_symbol_keywords(self, symbol: str) -> List[str]:
        """2단계: 심볼과 관련된 주요 키워드 탐색 (외부 소스 활용)"""
        symbol_upper = symbol.upper()
        
        # 기본 키워드 (회사 심볼과 일반적인 주식 관련 용어)
        base_keywords = [symbol_upper, symbol.lower()]
        
        # 일반적인 주식 관련 키워드
        stock_keywords = ['earnings', 'revenue', 'profit', 'stock', 'shares', 'market cap', 'dividend']
        base_keywords.extend(stock_keywords)
        
        # 외부 소스에서 키워드 찾기
        external_keywords = self._fetch_external_keywords(symbol_upper)
        if external_keywords:
            base_keywords.extend(external_keywords)
            self.logger.info(f"Found {len(external_keywords)} external keywords for {symbol}: {external_keywords[:5]}...")
        
        return base_keywords
    
    def _fetch_external_keywords(self, symbol: str) -> List[str]:
        """외부 소스에서 키워드 찾기"""
        keywords = []
        
        try:
            # 방법1: Yahoo Finance 주식 정보에서 키워드 추출
            yahoo_keywords = self._get_yahoo_finance_keywords(symbol)
            keywords.extend(yahoo_keywords)
            
            # 방법2: 주식 관련 뉴스 제목에서 키워드 추출  
            news_keywords = self._extract_keywords_from_recent_news(symbol)
            keywords.extend(news_keywords)
            
            # 방법3: 기본 회사 정보 매핑 (fallback)
            fallback_keywords = self._get_fallback_keywords(symbol)
            keywords.extend(fallback_keywords)
            
        except Exception as e:
            self.logger.warning(f"Error fetching external keywords for {symbol}: {e}")
            # 오류 시 fallback 키워드만 사용
            keywords = self._get_fallback_keywords(symbol)
        
        # 중복 제거 및 강화된 필터링
        unique_keywords = list(set(keywords))
        
        # 강화된 키워드 필터링
        filtered_keywords = []
        for kw in unique_keywords:
            if self._is_relevant_keyword(kw, symbol):
                filtered_keywords.append(kw)
        
        return filtered_keywords[:15]  # 최대 15개로 제한
    
    def _is_relevant_keyword(self, keyword: str, symbol: str) -> bool:
        """키워드가 해당 주식과 관련성이 있는지 강화된 검사"""
        keyword_lower = keyword.lower().strip()
        symbol_lower = symbol.lower()
        
        # 기본 필터링: 길이, 문자 타입 검사
        if len(keyword_lower) < 3 or len(keyword_lower) > 25:
            return False
        
        if not keyword.replace(' ', '').replace('-', '').isalnum():
            return False
        
        # 너무 일반적인 단어들 제외 (대폭 강화된 불용어 리스트)
        common_words = {
            'company', 'companies', 'corporation', 'corp', 'inc', 'ltd', 'llc',
            'business', 'industry', 'market', 'markets', 'financial', 'finance',
            'stock', 'stocks', 'share', 'shares', 'investment', 'invest', 'investor',
            'trading', 'trade', 'trader', 'money', 'cash', 'profit', 'revenue',
            'sales', 'growth', 'development', 'service', 'services', 'product',
            'products', 'technology', 'tech', 'digital', 'online', 'internet',
            'global', 'international', 'national', 'american', 'united', 'states',
            'world', 'worldwide', 'network', 'system', 'systems', 'solutions',
            'software', 'hardware', 'platform', 'platforms', 'data', 'information',
            'management', 'operations', 'operational', 'strategic', 'strategy',
            'million', 'billion', 'dollar', 'dollars', 'percent', 'percentage',
            'quarter', 'quarterly', 'annual', 'yearly', 'report', 'reports',
            'news', 'media', 'communication', 'communications', 'group', 'holdings',
            # 추가 일반적인 단어들
            'company\'s', 'business\'s', 'people', 'person', 'human', 'customer',
            'customers', 'client', 'clients', 'team', 'teams', 'leader', 'leaders',
            'employee', 'employees', 'worker', 'workers', 'staff', 'user', 'users',
            'time', 'times', 'year', 'years', 'day', 'days', 'week', 'weeks',
            'month', 'months', 'today', 'tomorrow', 'yesterday', 'future', 'past',
            'first', 'second', 'third', 'last', 'next', 'previous', 'current',
            'new', 'old', 'good', 'bad', 'best', 'better', 'great', 'excellent',
            'high', 'low', 'big', 'small', 'large', 'huge', 'tiny', 'major', 'minor',
            'more', 'most', 'less', 'least', 'many', 'much', 'few', 'little',
            'market', 'markets', 'economy', 'economic', 'economics', 'analyst',
            'analysts', 'expert', 'experts', 'research', 'researcher', 'study',
            'studies', 'survey', 'surveys', 'analysis', 'analytics'
        }
        
        if keyword_lower in common_words:
            return False
        
        # 심볼과 동일한 경우 제외
        if keyword_lower == symbol_lower:
            return False
        
        # 숫자만 있는 키워드 제외
        if keyword.isdigit():
            return False
        
        # 특정 회사별 엄격한 필터링
        if symbol_lower == 'nke':  # Nike 특별 필터링
            nike_irrelevant = {
                'brand', 'brands', 'fashion', 'style', 'design', 'designer',
                'retail', 'retailer', 'store', 'stores', 'shop', 'shopping',
                'consumer', 'consumers', 'lifestyle', 'culture', 'trend', 'trends',
                'marketing', 'advertisement', 'campaign', 'promotion', 'celebrity',
                'endorsement', 'partnership', 'collaboration', 'athlete', 'athletes',
                'sport', 'sports', 'fitness', 'training', 'performance', 'competition'
            }
            if keyword_lower in nike_irrelevant:
                return False
        
        # 너무 짧은 약어 제외 (단, 잘 알려진 브랜드명은 허용)
        known_brands = {'nike', 'apple', 'google', 'meta', 'tesla', 'amazon', 'microsoft', 'aws', 'ios'}
        if len(keyword_lower) <= 3 and keyword_lower not in known_brands:
            return False
        
        # 특정 패턴 제외
        if any(pattern in keyword_lower for pattern in ['www.', 'http', '.com', '.org', '.net', 'email', 'phone']):
            return False
        
        # 관사, 전치사, 접속사 등 제외
        function_words = {'the', 'and', 'for', 'with', 'but', 'not', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 'will', 'would', 'could', 'should'}
        if keyword_lower in function_words:
            return False
        
        return True
    
    def _get_yahoo_finance_keywords(self, symbol: str) -> List[str]:
        """야후 파이낸스에서 키워드 추출"""
        keywords = []
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # 회사 이름 및 비즈니스 설명에서 키워드 추출
            company_name = info.get('longName', '')
            business_summary = info.get('longBusinessSummary', '')
            industry = info.get('industry', '')
            sector = info.get('sector', '')
            
            # 회사 이름에서 키워드 추출
            if company_name:
                # 회사 이름을 단어별로 분리
                name_words = company_name.replace(',', '').replace('.', '').split()
                keywords.extend([word for word in name_words if len(word) > 2])
            
            # 산업 및 섹터 정보
            if industry:
                keywords.extend(industry.split())
            if sector:
                keywords.extend(sector.split())
            
            # 비즈니스 설명에서 주요 키워드 추출
            if business_summary and len(business_summary) > 50:
                # 비즈니스 설명에서 주요 단어 추출
                summary_keywords = self._extract_business_keywords(business_summary)
                keywords.extend(summary_keywords)
                
        except ImportError:
            self.logger.warning(f"yfinance not available for keyword extraction")
        except Exception as e:
            self.logger.warning(f"Error extracting Yahoo Finance keywords for {symbol}: {e}")
        
        return keywords
    
    def _extract_business_keywords(self, business_summary: str) -> List[str]:
        """비즈니스 설명에서 키워드 추출"""
        import re
        
        # 매우 구체적인 제품/브랜드명 패턴만 (일반적인 단어 완전 제외)
        business_patterns = [
            r'\b(jordan|swoosh|dunk|blazer|react|airmax|cortez)\b',  # Nike 전용 제품
            r'\b(iphone|ipad|macbook|airpods|imac|appletv)\b',  # Apple 제품
            r'\b(android|pixel|chrome|youtube|gmail|nest)\b',  # Google 제품
            r'\b(windows|office|azure|xbox|teams|surface)\b',  # Microsoft 제품
            r'\b(prime|alexa|kindle|aws|echo|firestick)\b',  # Amazon 제품
            r'\b(cybertruck|gigafactory|supercharger|autopilot|roadster)\b',  # Tesla 제품
            r'\b(instagram|whatsapp|metaverse|oculus|quest)\b',  # Meta 제품
            r'\b(geforce|rtx|cuda|omniverse|shield)\b',  # NVIDIA 제품
            r'\b(photoshop|creative|acrobat|illustrator|premiere)\b',  # Adobe 제품
            r'\b(salesforce|trailhead|einstein|mulesoft|slack)\b',  # CRM 제품
            r'\b(netflix|streaming|originals|stranger|bridgerton)\b',  # Netflix 제품
            r'\b(disney|marvel|pixar|espn|hulu)\b',  # Disney 제품
            r'\b(paypal|venmo|braintree|xoom|hyperwallet)\b'  # PayPal 제품
        ]
        
        keywords = []
        text_lower = business_summary.lower()
        
        for pattern in business_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if isinstance(matches[0] if matches else None, tuple):
                keywords.extend([match[0] for match in matches if match[0]])
            else:
                keywords.extend(matches)
        
        # 길이 제한 및 정리
        filtered_keywords = [kw.strip() for kw in keywords if 3 <= len(kw.strip()) <= 25]
        return list(set(filtered_keywords))[:10]  # 상위 10개
    
    def _extract_keywords_from_recent_news(self, symbol: str) -> List[str]:
        """최근 뉴스 제목에서 키워드 추출"""
        keywords = []
        try:
            # 간단한 뉴스 검색으로 최근 뉴스 제목 수집
            for source_name, config in list(self.news_sources.items())[:2]:  # 상위 2개 소스만 사용
                try:
                    feed = feedparser.parse(config['url'])
                    for entry in feed.entries[:5]:  # 각 소스에서 5개만
                        title = entry.get('title', '').strip()
                        if symbol.upper() in title.upper() and len(title) > 10:
                            # 제목에서 주요 단어 추출
                            title_keywords = self._extract_title_keywords(title, symbol)
                            keywords.extend(title_keywords)
                except Exception as e:
                    continue
        except Exception as e:
            self.logger.warning(f"Error extracting news keywords for {symbol}: {e}")
        
        return keywords
    
    def _extract_title_keywords(self, title: str, symbol: str) -> List[str]:
        """뉴스 제목에서 키워드 추출"""
        import re
        
        # 제목에서 주요 비즈니스 용어 추출
        business_words = re.findall(r'\b[A-Z][a-z]{3,}\b', title)
        
        # 너무 일반적인 단어 제외
        common_words = {'Stock', 'News', 'Report', 'Update', 'Price', 'Market', 'Today', 'This', 'That', 'With', 'From'}
        filtered_words = [word for word in business_words if word not in common_words and word.upper() != symbol.upper()]
        
        return filtered_words[:3]  # 상위 3개
    
    def _get_fallback_keywords(self, symbol: str) -> List[str]:
        """외부 소스 실패 시 사용할 기본 키워드 매핑 (핵심 비즈니스 키워드만)"""
        # 주요 주식들에 대한 핵심 비즈니스 키워드 (일반적인 용어 제외)
        basic_mapping = {
            'AAPL': ['iPhone', 'iPad', 'MacBook', 'AirPods', 'iOS'],
            'GOOGL': ['Alphabet', 'Android', 'YouTube', 'Chrome', 'Pixel'],
            'MSFT': ['Windows', 'Office', 'Azure', 'Xbox', 'Teams'],
            'AMZN': ['AWS', 'Prime', 'Alexa', 'Kindle', 'Echo'],
            'TSLA': ['Cybertruck', 'Gigafactory', 'Supercharger', 'Autopilot', 'FSD'],
            'META': ['Instagram', 'WhatsApp', 'Metaverse', 'Oculus', 'Reality'],
            'NVDA': ['GeForce', 'RTX', 'GPU', 'CUDA', 'Omniverse'],
            'NKE': ['Jordan', 'swoosh', 'Dunk', 'Blazer', 'React'],  # Nike 전용 제품명
            'ADBE': ['Photoshop', 'Creative', 'Acrobat', 'Illustrator', 'Premiere'],
            'CRM': ['Salesforce', 'Trailhead', 'Einstein', 'MuleSoft', 'Slack'],
            'NFLX': ['Netflix', 'streaming', 'originals', 'subscribers', 'Stranger'],
            'DIS': ['Disney', 'Marvel', 'Pixar', 'Star Wars', 'ESPN'],
            'PYPL': ['PayPal', 'Venmo', 'Braintree', 'checkout', 'wallet'],
            'INTC': ['Intel', 'processor', 'semiconductor', 'Xeon', 'Core'],
            'AMD': ['Ryzen', 'Radeon', 'EPYC', 'Threadripper', 'GPU']
        }
        
        return basic_mapping.get(symbol.upper(), [])
    
    def _fetch_keyword_based_news(self, source_name: str, rss_url: str, symbol: str, keyword: str) -> List[NewsArticle]:
        """3단계: 키워드 기반 뉴스 탐색"""
        articles = []
        
        try:
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:30]:  # 각 키워드당 최대 30개 처리
                title = entry.get('title', '').strip()
                summary = entry.get('summary', entry.get('description', '')).strip()
                
                # 빈 제목 필터링
                if not title or len(title) < 5:
                    continue
                
                # 키워드 관련성 확인 (더 유연한 매칭)
                if self._is_keyword_relevant(title + ' ' + summary, keyword):
                    # 날짜 파싱
                    published_date = datetime.now()
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        published_date = datetime(*entry.updated_parsed[:6])
                    
                    article = NewsArticle(
                        title=title,
                        content=summary,
                        url=entry.get('link', ''),
                        source=source_name,
                        published_date=published_date,
                        symbol=symbol,
                        keywords=[keyword]  # 관련 키워드 저장
                    )
                    
                    articles.append(article)
                    
        except Exception as e:
            self.logger.error(f"Error fetching keyword-based news from {source_name} for keyword {keyword}: {e}")
        
        return articles
    
    def _is_keyword_relevant(self, text: str, keyword: str) -> bool:
        """키워드 관련성 확인 (유연한 매칭)"""
        text_upper = text.upper()
        keyword_upper = keyword.upper()
        
        # 정확한 매칭
        if keyword_upper in text_upper:
            return True
        
        # 부분 매칭 (3글자 이상인 키워드)
        if len(keyword_upper) >= 3:
            # 단어 경계를 고려한 매칭
            import re
            pattern = r'\b' + re.escape(keyword_upper) + r'\b'
            if re.search(pattern, text_upper):
                return True
            
            # 부분 문자열 매칭 (더 유연함)
            if keyword_upper in text_upper.replace(' ', '').replace('-', ''):
                return True
        
        return False
    
    def _fetch_rss_news(self, source_name: str, rss_url: str, symbol: str) -> List[NewsArticle]:
        """RSS 피드에서 뉴스 수집"""
        articles = []
        
        try:
            feed = feedparser.parse(rss_url)
            
            # 각 RSS 소스에서 더 많은 entries 처리 (기본적으로 모든 entries 처리)
            for entry in feed.entries[:50]:  # 최대 50개까지 처리
                # 제목이나 내용에 심볼이 포함된 경우만 필터링
                title = entry.get('title', '').strip()
                summary = entry.get('summary', entry.get('description', '')).strip()
                
                # 빈 제목이나 너무 짧은 제목 필터링 (완화)
                if not title or len(title) < 5:  # 10에서 5로 완화
                    continue
                
                # 심볼 관련성 확인
                if not self._is_relevant_to_symbol(title + ' ' + summary, symbol):
                    continue
                
                # 날짜 파싱
                published_date = datetime.now()
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published_date = datetime(*entry.updated_parsed[:6])
                
                article = NewsArticle(
                    title=title,
                    content=summary,
                    url=entry.get('link', ''),
                    source=source_name,
                    published_date=published_date,
                    symbol=symbol
                )
                
                articles.append(article)
                
        except Exception as e:
            self.logger.error(f"Error fetching RSS from {source_name}: {e}")
        
        return articles
    
    def _fetch_yahoo_stock_news(self, symbol: str) -> List[NewsArticle]:
        """Yahoo Finance에서 특정 주식 뉴스 수집"""
        articles = []
        
        try:
            import yfinance as yf
            
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            for item in news[:20]:  # 최대 20개로 증가
                title = item.get('title', '').strip()
                summary = item.get('summary', '').strip()
                
                # 빈 제목 필터링
                if not title or len(title) < 5:
                    continue
                    
                # 내용이 없으면 제목을 내용으로 사용
                if not summary:
                    summary = title
                
                published_date = datetime.fromtimestamp(item.get('providerPublishTime', time.time()))
                
                article = NewsArticle(
                    title=title,
                    content=summary,
                    url=item.get('link', ''),
                    source='Yahoo Finance',
                    published_date=published_date,
                    symbol=symbol
                )
                
                # 기사 품질 체크 - 제목과 내용이 모두 있는지 확인
                if title and (summary or len(title) > 20):
                    articles.append(article)
                
        except ImportError:
            self.logger.warning(f"yfinance not installed, skipping Yahoo Finance news for {symbol}")
        except Exception as e:
            self.logger.warning(f"Error fetching Yahoo news for {symbol}: {e}")
        
        return articles
    
    def _is_relevant_to_symbol(self, text: str, symbol: str) -> bool:
        """텍스트가 주식 심볼과 관련이 있는지 확인 (완화된 필터링)"""
        text_upper = text.upper()
        symbol_upper = symbol.upper()
        
        # 직접적인 심볼 언급
        if symbol_upper in text_upper:
            return True
        
        # 확장된 회사명 및 관련 키워드 매핑
        company_names = {
            'AAPL': ['APPLE', 'IPHONE', 'IPAD', 'MAC', 'MACBOOK', 'IOS', 'ITUNES', 'APP STORE', 'TIM COOK', 'CUPERTINO'],
            'GOOGL': ['GOOGLE', 'ALPHABET', 'ANDROID', 'YOUTUBE', 'GMAIL', 'CHROME', 'SEARCH', 'PIXEL', 'SUNDAR PICHAI'],
            'MSFT': ['MICROSOFT', 'WINDOWS', 'OFFICE', 'AZURE', 'XBOX', 'TEAMS', 'OUTLOOK', 'SATYA NADELLA'],
            'AMZN': ['AMAZON', 'AWS', 'PRIME', 'ALEXA', 'KINDLE', 'BEZOS', 'CLOUD', 'E-COMMERCE'],
            'TSLA': ['TESLA', 'MUSK', 'ELECTRIC', 'EV', 'AUTOPILOT', 'GIGAFACTORY', 'MODEL', 'SPACEX'],
            'META': ['META', 'FACEBOOK', 'INSTAGRAM', 'WHATSAPP', 'ZUCKERBERG', 'METAVERSE', 'VR'],
            'NVDA': ['NVIDIA', 'GPU', 'AI CHIP', 'GRAPHICS', 'GAMING', 'CUDA', 'TENSOR']
        }
        
        if symbol_upper in company_names:
            for keyword in company_names[symbol_upper]:
                if keyword in text_upper:
                    return True
        
        # 더 유연한 검색 - 부분 매칭도 허용
        if len(symbol_upper) >= 3:
            # 3글자 이상인 심볼의 경우 부분 매칭도 허용
            if symbol_upper in text_upper.replace(' ', ''):
                return True
        
        # 일반적인 기술/금융 뉴스도 포함 (너무 제한적이지 않도록)
        general_keywords = ['STOCK', 'MARKET', 'TRADING', 'INVESTMENT', 'TECHNOLOGY', 'EARNINGS', 'REVENUE']
        if any(keyword in text_upper for keyword in general_keywords):
            # 일반 키워드가 포함된 경우, 심볼이 언급되지 않아도 50% 확률로 포함
            import random
            return random.random() > 0.5
        
        return False
    
    def _deduplicate_articles(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        """중복 기사 제거"""
        seen_urls = set()
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            # URL 기반 중복 확인
            if article.url and article.url in seen_urls:
                continue
            
            # 제목 기반 중복 확인 (유사도 체크)
            title_words = set(article.title.lower().split())
            is_duplicate = False
            
            for seen_title in seen_titles:
                seen_words = set(seen_title.lower().split())
                union_words = title_words | seen_words
                if len(union_words) > 0:  # division by zero 방지
                    similarity = len(title_words & seen_words) / len(union_words)
                    if similarity > 0.9:  # 90% 유사도 임계값 (80%에서 90%로 완화)
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                unique_articles.append(article)
                seen_urls.add(article.url)
                seen_titles.add(article.title)
        
        return unique_articles
    
    def analyze_sentiment(self, articles: List[NewsArticle]) -> SentimentAnalysis:
        """
        뉴스 기사들의 감정 분석
        
        Args:
            articles: 분석할 뉴스 기사 리스트
            
        Returns:
            SentimentAnalysis: 감정 분석 결과
        """
        if not articles:
            return SentimentAnalysis(
                overall_sentiment=SentimentType.NEUTRAL,
                sentiment_score=0.0,
                confidence=0.0,
                positive_ratio=0.0,
                negative_ratio=0.0,
                neutral_ratio=1.0,
                article_count=0,
                analysis_date=datetime.now()
            )
        
        total_scores = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for article in articles:
            # TextBlob과 VADER를 모두 사용하여 감정 분석
            textblob_score = self._analyze_with_textblob(article.title + ' ' + article.content)
            vader_score = self._analyze_with_vader(article.title + ' ' + article.content)
            
            # 두 점수의 평균
            combined_score = (textblob_score + vader_score) / 2
            total_scores.append(combined_score)
            
            # 기사별 감정 저장
            article.sentiment_score = combined_score
            article.sentiment_type = self._score_to_sentiment_type(combined_score)
            
            # 카운트
            if combined_score > 0.1:
                positive_count += 1
            elif combined_score < -0.1:
                negative_count += 1
            else:
                neutral_count += 1
        
        # 전체 감정 점수 - division by zero 방지
        if len(total_scores) > 0:
            overall_score = sum(total_scores) / len(total_scores)
        else:
            overall_score = 0.0
        overall_sentiment = self._score_to_sentiment_type(overall_score)
        
        # 신뢰도 계산 (점수의 분산 기반)
        import statistics
        confidence = 1.0 - min(statistics.stdev(total_scores) if len(total_scores) > 1 else 0, 1.0)
        
        # 비율 계산 - division by zero 방지
        total_articles = len(articles)
        if total_articles > 0:
            positive_ratio = positive_count / total_articles
            negative_ratio = negative_count / total_articles
            neutral_ratio = neutral_count / total_articles
        else:
            positive_ratio = negative_ratio = neutral_ratio = 0.0
        
        return SentimentAnalysis(
            overall_sentiment=overall_sentiment,
            sentiment_score=overall_score,
            confidence=confidence,
            positive_ratio=positive_ratio,
            negative_ratio=negative_ratio,
            neutral_ratio=neutral_ratio,
            article_count=total_articles,
            analysis_date=datetime.now()
        )
    
    def _analyze_with_textblob(self, text: str) -> float:
        """TextBlob을 사용한 감정 분석"""
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity  # -1 to 1
        except Exception:
            return 0.0
    
    def _analyze_with_vader(self, text: str) -> float:
        """VADER를 사용한 감정 분석"""
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            return scores['compound']  # -1 to 1
        except Exception:
            return 0.0
    
    def _score_to_sentiment_type(self, score: float) -> SentimentType:
        """감정 점수를 감정 타입으로 변환"""
        if score >= 0.5:
            return SentimentType.VERY_POSITIVE
        elif score >= 0.1:
            return SentimentType.POSITIVE
        elif score <= -0.5:
            return SentimentType.VERY_NEGATIVE
        elif score <= -0.1:
            return SentimentType.NEGATIVE
        else:
            return SentimentType.NEUTRAL
    
    def get_market_sentiment_overview(self, symbols: List[str]) -> Dict[str, SentimentAnalysis]:
        """
        여러 주식의 시장 감정 개요
        
        Args:
            symbols: 분석할 주식 심볼 리스트
            
        Returns:
            Dict[str, SentimentAnalysis]: 심볼별 감정 분석 결과
        """
        results = {}
        
        for symbol in symbols:
            try:
                articles = self.get_stock_news(symbol, limit=10)
                sentiment = self.analyze_sentiment(articles)
                results[symbol] = sentiment
            except Exception as e:
                self.logger.error(f"Error analyzing sentiment for {symbol}: {e}")
                results[symbol] = SentimentAnalysis(
                    overall_sentiment=SentimentType.NEUTRAL,
                    sentiment_score=0.0,
                    confidence=0.0,
                    positive_ratio=0.0,
                    negative_ratio=0.0,
                    neutral_ratio=1.0,
                    article_count=0,
                    analysis_date=datetime.now()
                )
        
        return results
    
    def get_trending_topics(self, limit: int = 10) -> List[Dict]:
        """
        트렌딩 토픽 추출
        
        Args:
            limit: 반환할 토픽 수
            
        Returns:
            List[Dict]: 트렌딩 토픽 리스트
        """
        try:
            # 일반 시장 뉴스 수집
            all_articles = []
            
            for source_name, config in self.news_sources.items():
                try:
                    feed = feedparser.parse(config['url'])
                    for entry in feed.entries[:30]:  # 각 소스에서 최대 30개로 증가
                        title = entry.get('title', '').strip()
                        summary = entry.get('summary', entry.get('description', '')).strip()
                        
                        # 빈 제목 필터링 (완화)
                        if not title or len(title) < 5:  # 10에서 5로 완화
                            continue
                        
                        # 날짜 파싱
                        published_date = datetime.now()
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            published_date = datetime(*entry.published_parsed[:6])
                        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                            published_date = datetime(*entry.updated_parsed[:6])
                        
                        article = NewsArticle(
                            title=title,
                            content=summary,
                            url=entry.get('link', ''),
                            source=source_name,
                            published_date=published_date
                        )
                        all_articles.append(article)
                except Exception as e:
                    self.logger.warning(f"Error fetching trending topics from {source_name}: {e}")
                    continue
            
            # 키워드 추출 및 빈도 계산
            keyword_counts = {}
            for article in all_articles:
                keywords = self._extract_keywords(article.title + ' ' + article.content)
                for keyword in keywords:
                    keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
            
            # 상위 키워드들을 토픽으로 변환
            trending_topics = []
            sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
            
            for keyword, count in sorted_keywords[:limit]:
                trending_topics.append({
                    'topic': keyword,
                    'mention_count': count,
                    'sentiment': self._get_keyword_sentiment(keyword, all_articles)
                })
            
            return trending_topics
            
        except Exception as e:
            self.logger.error(f"Error getting trending topics: {e}")
            return []
    
    def _extract_keywords(self, text: str) -> List[str]:
        """텍스트에서 키워드 추출"""
        import re
        
        # 확장된 불용어 제거
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 
            'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'shall',
            'this', 'that', 'these', 'those', 'up', 'down', 'out', 'off', 'over', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
            'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'll', 'just',
            'says', 'said', 'get', 'go', 'know', 'take', 'see', 'come', 'think', 'look', 'want',
            'give', 'use', 'find', 'tell', 'ask', 'work', 'seem', 'feel', 'try', 'leave', 'call'
        }
        
        # 금융 관련 주요 키워드들
        financial_keywords = {
            'stock', 'stocks', 'market', 'markets', 'trading', 'price', 'prices', 'shares', 'share',
            'earnings', 'revenue', 'profit', 'loss', 'growth', 'decline', 'investors', 'investment',
            'company', 'companies', 'business', 'financial', 'economy', 'economic', 'billion',
            'million', 'quarter', 'quarterly', 'annual', 'sales', 'acquisition', 'merger', 'deal',
            'ceo', 'technology', 'tech', 'energy', 'healthcare', 'bank', 'banks', 'federal',
            'dollar', 'dollars', 'percent', 'inflation', 'interest', 'rates', 'crypto', 'bitcoin'
        }
        
        # 단어 추출 및 정제
        words = re.findall(r'\b[A-Za-z]{4,}\b', text.lower())
        keywords = []
        
        for word in words:
            if word not in stop_words and len(word) >= 4:
                # 금융 관련 키워드는 우선적으로 선택
                if word in financial_keywords:
                    keywords.append(word)
                # 대문자로 시작하는 단어들 (회사명, 브랜드명 등)
                elif word.istitle() and len(word) >= 3:
                    keywords.append(word.lower())
                # 일반 키워드
                elif len(word) >= 5:
                    keywords.append(word)
        
        # 중복 제거 및 반환
        return list(set(keywords))
    
    def _get_keyword_sentiment(self, keyword: str, articles: List[NewsArticle]) -> float:
        """특정 키워드의 감정 점수 계산"""
        relevant_texts = []
        
        for article in articles:
            full_text = article.title + ' ' + article.content
            if keyword.lower() in full_text.lower():
                relevant_texts.append(full_text)
        
        if not relevant_texts:
            return 0.0
        
        total_score = 0.0
        for text in relevant_texts:
            textblob_score = self._analyze_with_textblob(text)
            vader_score = self._analyze_with_vader(text)
            total_score += (textblob_score + vader_score) / 2
        
        return total_score / len(relevant_texts) if len(relevant_texts) > 0 else 0.0
    
    def clear_cache(self):
        """캐시 초기화"""
        self.article_cache.clear()

# 전역 인스턴스
news_sentiment_analyzer = NewsSentimentAnalyzer()