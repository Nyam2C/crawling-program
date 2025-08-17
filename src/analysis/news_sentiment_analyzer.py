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
        
    def get_stock_news(self, symbol: str, limit: int = 20) -> List[NewsArticle]:
        """
        특정 주식 심볼에 대한 뉴스 수집
        
        Args:
            symbol: 주식 심볼 (예: 'AAPL')
            limit: 최대 뉴스 개수
            
        Returns:
            List[NewsArticle]: 뉴스 기사 리스트
        """
        cache_key = f"{symbol}_{int(time.time() // self.cache_duration)}"
        
        if cache_key in self.article_cache:
            return self.article_cache[cache_key][:limit]
        
        all_articles = []
        
        # RSS 피드에서 뉴스 수집
        for source_name, config in self.news_sources.items():
            try:
                if config['type'] == 'rss':
                    articles = self._fetch_rss_news(source_name, config['url'], symbol)
                    all_articles.extend(articles)
            except Exception as e:
                self.logger.warning(f"Failed to fetch from {source_name}: {e}")
        
        # Yahoo Finance API를 통한 특정 주식 뉴스
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
        
        return unique_articles[:limit]
    
    def _fetch_rss_news(self, source_name: str, rss_url: str, symbol: str) -> List[NewsArticle]:
        """RSS 피드에서 뉴스 수집"""
        articles = []
        
        try:
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries:
                # 제목이나 내용에 심볼이 포함된 경우만 필터링
                title = entry.get('title', '')
                summary = entry.get('summary', entry.get('description', ''))
                
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
            
            for item in news[:10]:  # 최대 10개
                published_date = datetime.fromtimestamp(item.get('providerPublishTime', time.time()))
                
                article = NewsArticle(
                    title=item.get('title', ''),
                    content=item.get('summary', ''),
                    url=item.get('link', ''),
                    source='Yahoo Finance',
                    published_date=published_date,
                    symbol=symbol
                )
                
                articles.append(article)
                
        except Exception as e:
            self.logger.warning(f"Error fetching Yahoo news for {symbol}: {e}")
        
        return articles
    
    def _is_relevant_to_symbol(self, text: str, symbol: str) -> bool:
        """텍스트가 주식 심볼과 관련이 있는지 확인"""
        text_upper = text.upper()
        symbol_upper = symbol.upper()
        
        # 직접적인 심볼 언급
        if symbol_upper in text_upper:
            return True
        
        # 회사명 기반 필터링 (간단한 버전)
        company_names = {
            'AAPL': ['APPLE', 'IPHONE', 'IPAD', 'MAC'],
            'GOOGL': ['GOOGLE', 'ALPHABET', 'ANDROID'],
            'MSFT': ['MICROSOFT', 'WINDOWS', 'OFFICE', 'AZURE'],
            'AMZN': ['AMAZON', 'AWS', 'PRIME'],
            'TSLA': ['TESLA', 'MUSK', 'ELECTRIC'],
            'META': ['META', 'FACEBOOK', 'INSTAGRAM', 'WHATSAPP'],
            'NVDA': ['NVIDIA', 'GPU', 'AI CHIP']
        }
        
        if symbol_upper in company_names:
            for keyword in company_names[symbol_upper]:
                if keyword in text_upper:
                    return True
        
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
                similarity = len(title_words & seen_words) / len(title_words | seen_words)
                if similarity > 0.8:  # 80% 유사도 임계값
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
        
        # 전체 감정 점수
        overall_score = sum(total_scores) / len(total_scores)
        overall_sentiment = self._score_to_sentiment_type(overall_score)
        
        # 신뢰도 계산 (점수의 분산 기반)
        import statistics
        confidence = 1.0 - min(statistics.stdev(total_scores) if len(total_scores) > 1 else 0, 1.0)
        
        # 비율 계산
        total_articles = len(articles)
        positive_ratio = positive_count / total_articles
        negative_ratio = negative_count / total_articles
        neutral_ratio = neutral_count / total_articles
        
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
                    for entry in feed.entries[:20]:  # 각 소스에서 최대 20개
                        article = NewsArticle(
                            title=entry.get('title', ''),
                            content=entry.get('summary', ''),
                            url=entry.get('link', ''),
                            source=source_name,
                            published_date=datetime.now()
                        )
                        all_articles.append(article)
                except Exception as e:
                    self.logger.warning(f"Error fetching trending topics from {source_name}: {e}")
            
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
        # 간단한 키워드 추출 (실제로는 더 정교한 NLP 기법 사용 가능)
        import re
        
        # 불용어 제거
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'shall'}
        
        # 단어 추출 및 정제
        words = re.findall(r'\b[A-Za-z]{3,}\b', text.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # 빈도 기반 필터링
        word_counts = {}
        for word in keywords:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # 최소 2번 이상 언급된 단어만 반환
        return [word for word, count in word_counts.items() if count >= 2]
    
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
        
        return total_score / len(relevant_texts)
    
    def clear_cache(self):
        """캐시 초기화"""
        self.article_cache.clear()

# 전역 인스턴스
news_sentiment_analyzer = NewsSentimentAnalyzer()