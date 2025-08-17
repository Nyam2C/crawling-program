#!/usr/bin/env python3
"""
News & Sentiment Analysis Tab - 뉴스 및 감정 분석 탭
실시간 뉴스 수집 및 감정 분석 결과를 보여주는 GUI 탭
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import webbrowser
from datetime import datetime
from typing import Dict, List, Optional

from src.analysis.news_sentiment_analyzer import (
    news_sentiment_analyzer, SentimentType, NewsArticle, SentimentAnalysis
)

class NewsSentimentTab:
    """뉴스 및 감정 분석 탭"""
    
    def __init__(self, parent_notebook, icon_manager, theme_manager):
        self.parent_notebook = parent_notebook
        self.icon_manager = icon_manager
        self.theme_manager = theme_manager
        
        # 현재 분석 중인 심볼
        self.current_symbol = None
        self.current_articles = []
        self.current_sentiment = None
        
        self.setup_tab()
        
    def setup_tab(self):
        """탭 UI 설정"""
        # 메인 프레임 생성
        self.tab_frame = ttk.Frame(self.parent_notebook)
        self.parent_notebook.add(self.tab_frame, text="📰 News & Sentiment")
        
        # 상단 컨트롤 패널
        self.setup_control_panel()
        
        # 좌측: 뉴스 리스트
        self.setup_news_list_panel()
        
        # 우측: 감정 분석 결과
        self.setup_sentiment_panel()
        
        # 하단: 트렌딩 토픽
        self.setup_trending_panel()
    
    def setup_control_panel(self):
        """상단 컨트롤 패널 설정"""
        control_frame = ttk.LabelFrame(self.tab_frame, text="🎯 Analysis Control", padding=10)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        # 주식 심볼 입력
        ttk.Label(control_frame, text="Stock Symbol:").pack(side="left", padx=(0, 5))
        
        self.symbol_var = tk.StringVar(value="AAPL")
        symbol_entry = ttk.Entry(control_frame, textvariable=self.symbol_var, width=10)
        symbol_entry.pack(side="left", padx=(0, 10))
        
        # 분석 버튼
        analyze_btn = ttk.Button(
            control_frame, 
            text="🔍 Analyze News",
            command=self.analyze_news_async
        )
        analyze_btn.pack(side="left", padx=(0, 10))
        
        # 새로고침 버튼
        refresh_btn = ttk.Button(
            control_frame,
            text="🔄 Refresh",
            command=self.refresh_news
        )
        refresh_btn.pack(side="left", padx=(0, 10))
        
        # 트렌딩 토픽 버튼
        trending_btn = ttk.Button(
            control_frame,
            text="📈 Trending Topics",
            command=self.show_trending_topics
        )
        trending_btn.pack(side="left", padx=(0, 10))
        
        # 상태 라벨
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(control_frame, textvariable=self.status_var)
        status_label.pack(side="right", padx=(10, 0))
    
    def setup_news_list_panel(self):
        """뉴스 리스트 패널 설정"""
        # 메인 컨테이너
        main_container = ttk.Frame(self.tab_frame)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 좌측 뉴스 리스트
        news_frame = ttk.LabelFrame(main_container, text="📰 Latest News", padding=5)
        news_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # 뉴스 트리뷰
        columns = ("Date", "Title", "Source", "Sentiment")
        self.news_tree = ttk.Treeview(news_frame, columns=columns, show="headings", height=15)
        
        # 컬럼 설정
        self.news_tree.heading("Date", text="Date")
        self.news_tree.heading("Title", text="Title")
        self.news_tree.heading("Source", text="Source")
        self.news_tree.heading("Sentiment", text="Sentiment")
        
        self.news_tree.column("Date", width=100, anchor="center")
        self.news_tree.column("Title", width=400)
        self.news_tree.column("Source", width=120, anchor="center")
        self.news_tree.column("Sentiment", width=100, anchor="center")
        
        # 스크롤바
        news_scrollbar = ttk.Scrollbar(news_frame, orient="vertical", command=self.news_tree.yview)
        self.news_tree.configure(yscrollcommand=news_scrollbar.set)
        
        self.news_tree.pack(side="left", fill="both", expand=True)
        news_scrollbar.pack(side="right", fill="y")
        
        # 뉴스 클릭 이벤트
        self.news_tree.bind("<Double-1>", self.on_news_click)
        self.news_tree.bind("<Button-1>", self.on_news_select)
    
    def setup_sentiment_panel(self):
        """감정 분석 패널 설정"""
        # 우측 감정 분석 결과
        sentiment_frame = ttk.LabelFrame(
            self.tab_frame.master.children[list(self.tab_frame.master.children.keys())[-1]].master.children[list(self.tab_frame.master.children[list(self.tab_frame.master.children.keys())[-1]].master.children.keys())[-1]], 
            text="💭 Sentiment Analysis", 
            padding=5
        )
        
        # 다시 올바른 부모 찾기
        main_container = None
        for child in self.tab_frame.winfo_children():
            if isinstance(child, ttk.Frame) and child.winfo_class() == "TFrame":
                main_container = child
                break
        
        if main_container:
            sentiment_frame = ttk.LabelFrame(main_container, text="💭 Sentiment Analysis", padding=5)
            sentiment_frame.pack(side="right", fill="both", expand=False, padx=(5, 0))
            sentiment_frame.configure(width=300)
        else:
            # 메인 컨테이너를 찾을 수 없으면 새로 생성
            sentiment_frame = ttk.LabelFrame(self.tab_frame, text="💭 Sentiment Analysis", padding=5)
            sentiment_frame.pack(side="right", fill="y", padx=(5, 10), pady=5)
        
        # 전체 감정 점수
        self.overall_sentiment_var = tk.StringVar(value="No Analysis")
        overall_label = ttk.Label(
            sentiment_frame, 
            textvariable=self.overall_sentiment_var,
            font=("Arial", 12, "bold")
        )
        overall_label.pack(pady=10)
        
        # 감정 점수
        self.sentiment_score_var = tk.StringVar(value="Score: --")
        score_label = ttk.Label(sentiment_frame, textvariable=self.sentiment_score_var)
        score_label.pack()
        
        # 신뢰도
        self.confidence_var = tk.StringVar(value="Confidence: --")
        confidence_label = ttk.Label(sentiment_frame, textvariable=self.confidence_var)
        confidence_label.pack()
        
        # 감정 분포
        ttk.Label(sentiment_frame, text="Sentiment Distribution:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        
        self.positive_var = tk.StringVar(value="Positive: --%")
        self.negative_var = tk.StringVar(value="Negative: --%")
        self.neutral_var = tk.StringVar(value="Neutral: --%")
        
        ttk.Label(sentiment_frame, textvariable=self.positive_var, foreground="green").pack()
        ttk.Label(sentiment_frame, textvariable=self.negative_var, foreground="red").pack()
        ttk.Label(sentiment_frame, textvariable=self.neutral_var, foreground="gray").pack()
        
        # 기사 상세 정보
        ttk.Label(sentiment_frame, text="Selected Article:", font=("Arial", 10, "bold")).pack(pady=(20, 5))
        
        self.article_detail = scrolledtext.ScrolledText(
            sentiment_frame, 
            height=8, 
            width=40, 
            wrap=tk.WORD,
            font=("Arial", 9)
        )
        self.article_detail.pack(fill="both", expand=True)
    
    def setup_trending_panel(self):
        """트렌딩 토픽 패널 설정"""
        trending_frame = ttk.LabelFrame(self.tab_frame, text="🔥 Trending Topics", padding=5)
        trending_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # 트렌딩 토픽 리스트
        self.trending_var = tk.StringVar(value="Click 'Trending Topics' to load...")
        trending_label = ttk.Label(trending_frame, textvariable=self.trending_var, wraplength=800)
        trending_label.pack(pady=5)
    
    def analyze_news_async(self):
        """비동기로 뉴스 분석 실행"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            messagebox.showwarning("Warning", "Please enter a stock symbol")
            return
        
        self.current_symbol = symbol
        self.status_var.set("Analyzing news...")
        
        # 백그라운드 스레드에서 분석 실행
        threading.Thread(target=self.analyze_news, daemon=True).start()
    
    def analyze_news(self):
        """뉴스 분석 실행"""
        try:
            # 뉴스 수집
            self.status_var.set("Fetching news...")
            articles = news_sentiment_analyzer.get_stock_news(self.current_symbol, limit=30)
            
            if not articles:
                self.status_var.set("No news found")
                messagebox.showinfo("Info", f"No news found for {self.current_symbol}")
                return
            
            # 감정 분석
            self.status_var.set("Analyzing sentiment...")
            sentiment = news_sentiment_analyzer.analyze_sentiment(articles)
            
            # UI 업데이트
            self.current_articles = articles
            self.current_sentiment = sentiment
            
            # 메인 스레드에서 UI 업데이트
            self.tab_frame.after(0, self.update_news_display)
            self.tab_frame.after(0, self.update_sentiment_display)
            
            self.status_var.set(f"Analysis complete - {len(articles)} articles")
            
        except Exception as e:
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", f"Failed to analyze news: {str(e)}")
    
    def update_news_display(self):
        """뉴스 디스플레이 업데이트"""
        # 기존 항목 삭제
        for item in self.news_tree.get_children():
            self.news_tree.delete(item)
        
        # 새 뉴스 추가
        for article in self.current_articles:
            date_str = article.published_date.strftime("%m/%d %H:%M")
            title = article.title[:60] + "..." if len(article.title) > 60 else article.title
            
            # 감정에 따른 색상
            sentiment_text = self.get_sentiment_emoji(article.sentiment_type)
            
            item = self.news_tree.insert("", "end", values=(
                date_str,
                title,
                article.source,
                sentiment_text
            ))
            
            # 감정에 따른 색상 태그
            if article.sentiment_type:
                if article.sentiment_type in [SentimentType.POSITIVE, SentimentType.VERY_POSITIVE]:
                    self.news_tree.set(item, "Sentiment", f"📈 {sentiment_text}")
                elif article.sentiment_type in [SentimentType.NEGATIVE, SentimentType.VERY_NEGATIVE]:
                    self.news_tree.set(item, "Sentiment", f"📉 {sentiment_text}")
                else:
                    self.news_tree.set(item, "Sentiment", f"➖ {sentiment_text}")
    
    def update_sentiment_display(self):
        """감정 분석 디스플레이 업데이트"""
        if not self.current_sentiment:
            return
        
        sentiment = self.current_sentiment
        
        # 전체 감정
        sentiment_emoji = self.get_sentiment_emoji(sentiment.overall_sentiment)
        self.overall_sentiment_var.set(f"{sentiment_emoji} {sentiment.overall_sentiment.value.title()}")
        
        # 점수 및 신뢰도
        self.sentiment_score_var.set(f"Score: {sentiment.sentiment_score:.3f}")
        self.confidence_var.set(f"Confidence: {sentiment.confidence:.1%}")
        
        # 분포
        self.positive_var.set(f"Positive: {sentiment.positive_ratio:.1%}")
        self.negative_var.set(f"Negative: {sentiment.negative_ratio:.1%}")
        self.neutral_var.set(f"Neutral: {sentiment.neutral_ratio:.1%}")
    
    def get_sentiment_emoji(self, sentiment_type: Optional[SentimentType]) -> str:
        """감정 타입에 따른 이모지 반환"""
        if not sentiment_type:
            return "❓"
        
        emoji_map = {
            SentimentType.VERY_POSITIVE: "🟢",
            SentimentType.POSITIVE: "🔵",
            SentimentType.NEUTRAL: "⚪",
            SentimentType.NEGATIVE: "🟠",
            SentimentType.VERY_NEGATIVE: "🔴"
        }
        
        return emoji_map.get(sentiment_type, "❓")
    
    def on_news_click(self, event):
        """뉴스 더블클릭 이벤트"""
        selection = self.news_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        index = self.news_tree.index(item)
        
        if index < len(self.current_articles):
            article = self.current_articles[index]
            if article.url:
                webbrowser.open(article.url)
    
    def on_news_select(self, event):
        """뉴스 선택 이벤트"""
        selection = self.news_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        index = self.news_tree.index(item)
        
        if index < len(self.current_articles):
            article = self.current_articles[index]
            
            # 기사 상세 정보 표시
            self.article_detail.delete(1.0, tk.END)
            
            detail_text = f"Title: {article.title}\n\n"
            detail_text += f"Source: {article.source}\n"
            detail_text += f"Date: {article.published_date.strftime('%Y-%m-%d %H:%M')}\n"
            
            if article.sentiment_score is not None:
                detail_text += f"Sentiment: {article.sentiment_score:.3f}\n"
            
            detail_text += f"\nContent:\n{article.content}\n\n"
            detail_text += f"URL: {article.url}"
            
            self.article_detail.insert(1.0, detail_text)
    
    def refresh_news(self):
        """뉴스 새로고침"""
        if self.current_symbol:
            # 캐시 초기화
            news_sentiment_analyzer.clear_cache()
            self.analyze_news_async()
        else:
            messagebox.showinfo("Info", "Please analyze a symbol first")
    
    def show_trending_topics(self):
        """트렌딩 토픽 표시"""
        self.status_var.set("Loading trending topics...")
        
        def load_trending():
            try:
                topics = news_sentiment_analyzer.get_trending_topics(limit=10)
                
                if topics:
                    trending_text = "🔥 Current trending topics: "
                    trending_items = []
                    
                    for topic in topics[:5]:  # 상위 5개만 표시
                        sentiment_emoji = "📈" if topic['sentiment'] > 0.1 else "📉" if topic['sentiment'] < -0.1 else "➖"
                        trending_items.append(f"{sentiment_emoji} {topic['topic']} ({topic['mention_count']})")
                    
                    trending_text += " | ".join(trending_items)
                else:
                    trending_text = "No trending topics available at the moment"
                
                # UI 업데이트
                self.tab_frame.after(0, lambda: self.trending_var.set(trending_text))
                self.tab_frame.after(0, lambda: self.status_var.set("Trending topics loaded"))
                
            except Exception as e:
                self.tab_frame.after(0, lambda: self.status_var.set("Error loading trending topics"))
                print(f"Error loading trending topics: {e}")
        
        threading.Thread(target=load_trending, daemon=True).start()
    
    def get_tab_frame(self):
        """탭 프레임 반환"""
        return self.tab_frame