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
    
    def __init__(self, parent_notebook, icon_manager, theme_manager, main_app=None):
        self.parent_notebook = parent_notebook
        self.icon_manager = icon_manager
        self.theme_manager = theme_manager
        self.main_app = main_app
        
        # 현재 분석 중인 심볼
        self.current_symbol = None
        self.current_articles = []
        self.current_sentiment = None
        
        self.setup_tab()
        
    def setup_tab(self):
        """탭 UI 설정"""
        # 메인 프레임 생성 - Individual Analysis 탭과 동일한 패딩
        self.tab_frame = ttk.Frame(self.parent_notebook, padding="15")
        
        # 아이콘 설정 - 다른 탭과 동일한 방식
        tab_icon = self.icon_manager.get_icon("add_4")  # 뉴스용 아이콘 (mail 대신)
        if tab_icon:
            self.parent_notebook.add(self.tab_frame, text="News & Sentiment", image=tab_icon, compound="left")
        else:
            self.parent_notebook.add(self.tab_frame, text="News & Sentiment")
        
        # 상단 컨트롤 패널
        self.setup_control_panel()
        
        # 좌측: 뉴스 리스트
        self.setup_news_list_panel()
        
        # 우측: 감정 분석 결과
        self.setup_sentiment_panel()
        
        # 하단: 트렌딩 토픽
        self.setup_trending_panel()
    
    def setup_control_panel(self):
        """상단 컨트롤 패널 설정 - Analysis 탭과 완전히 동일한 스타일 적용"""
        control_frame = ttk.LabelFrame(self.tab_frame, text="News Analysis Control", padding="15")
        control_frame.pack(fill="x", pady=(0, 15))
        
        # Analysis 탭과 동일한 grid 레이아웃 설정
        ttk.Label(control_frame, text="Stock Symbol:", 
                 font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=(0, 10))
        
        self.symbol_var = tk.StringVar(value="AAPL")
        
        # 컴보박스 - Analysis 탭과 동일한 크기와 스타일
        self.symbol_combo = ttk.Combobox(control_frame, textvariable=self.symbol_var,
                                       values=self._get_current_stock_symbols(),
                                       width=15, font=("Segoe UI", 10), 
                                       style='Pastel.TCombobox', state='readonly')
        self.symbol_combo.grid(row=0, column=1, padx=(0, 15))
        
        # 버튼들을 Analysis 탭과 완전히 동일한 방식으로 배치
        if self.main_app:
            # 새로고침 버튼 - Analysis 탭의 'Refresh List'와 동일
            self.main_app.icon_button(control_frame, 'refresh', 'Refresh List',
                                      self._refresh_stock_list,
                                      style='Pastel.Ghost.TButton').grid(row=0, column=2, padx=(0, 10))
            
            # 분석 버튼 - Analysis 탭의 'Deep Analysis'와 동일
            self.main_app.icon_button(control_frame, 'analyze_advanced', 'Analyze News',
                                      self.analyze_news_async,
                                      style='Pastel.Primary.TButton').grid(row=0, column=3, padx=(0, 10))
            
            # 트렌딩 토픽 버튼 - Analysis 탭의 'Quick Analysis'와 동일
            self.main_app.icon_button(control_frame, 'rainbow', 'Trending Topics',
                                      self.show_trending_topics,
                                      style='Pastel.Secondary.TButton').grid(row=0, column=4, padx=(0, 10))
        
        # 상태 라벨 - 오른쪽 끝에 배치
        self.status_var = tk.StringVar(value="Ready to analyze stock news")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, 
                               font=("Segoe UI", 9, "italic"))
        status_label.grid(row=0, column=5, padx=(15, 0), sticky="e")
        
        # 키워드 초기화
        self.current_keywords = []
    
    def setup_news_list_panel(self):
        """뉴스 리스트 패널 설정"""
        # 메인 컨테이너
        main_container = ttk.Frame(self.tab_frame)
        main_container.pack(fill="both", expand=True, pady=(0, 15))
        
        # 좌측 뉴스 리스트
        news_frame = ttk.LabelFrame(main_container, text="Latest News", padding="10")
        news_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # 뉴스 트리뷰 - 통일된 스타일
        columns = ("Date", "Title", "Source", "Sentiment")
        self.news_tree = ttk.Treeview(news_frame, columns=columns, show="headings", height=16)
        
        # 컬럼 설정 - 다른 탭과 일치하는 폰트
        self.news_tree.heading("Date", text="Date")
        self.news_tree.heading("Title", text="Title")
        self.news_tree.heading("Source", text="Source")
        self.news_tree.heading("Sentiment", text="Sentiment")
        
        self.news_tree.column("Date", width=100, anchor="center")
        self.news_tree.column("Title", width=450)
        self.news_tree.column("Source", width=130, anchor="center")
        self.news_tree.column("Sentiment", width=100, anchor="center")
        
        # 트리뷰 스타일링 - 검정색 텍스트 적용
        self.news_tree.tag_configure('positive', background='#E8F5E8', foreground='black')
        self.news_tree.tag_configure('negative', background='#FFE8E8', foreground='black')
        self.news_tree.tag_configure('neutral', background='#F5F5F5', foreground='black')
        
        # 스크롤바
        news_scrollbar = ttk.Scrollbar(news_frame, orient="vertical", command=self.news_tree.yview)
        self.news_tree.configure(yscrollcommand=news_scrollbar.set)
        
        self.news_tree.pack(side="left", fill="both", expand=True)
        news_scrollbar.pack(side="right", fill="y")
        
        # 뉴스 더블클릭 이벤트로 상세 정보 표시
        self.news_tree.bind("<Double-1>", self.on_news_select)
    
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
            sentiment_frame = ttk.LabelFrame(main_container, text="Sentiment Analysis", padding="10")
            sentiment_frame.pack(side="right", fill="both", expand=False, padx=(10, 0))
            sentiment_frame.configure(width=320)
        else:
            # 메인 컨테이너를 찾을 수 없으면 새로 생성
            sentiment_frame = ttk.LabelFrame(self.tab_frame, text="Sentiment Analysis", padding="10")
            sentiment_frame.pack(side="right", fill="y", padx=(10, 15), pady=(0, 15))
        
        # 전체 감정 점수 - 통일된 폰트
        self.overall_sentiment_var = tk.StringVar(value="No Analysis Yet")
        overall_label = ttk.Label(
            sentiment_frame, 
            textvariable=self.overall_sentiment_var,
            font=("Segoe UI", 12, "bold")
        )
        overall_label.pack(pady=(0, 15))
        
        # 신뢰도 - 통일된 폰트
        self.confidence_var = tk.StringVar(value="Confidence: --")
        confidence_label = ttk.Label(sentiment_frame, textvariable=self.confidence_var,
                                   font=("Segoe UI", 9))
        confidence_label.pack(pady=2)
        
        # 구분선
        separator = ttk.Separator(sentiment_frame, orient='horizontal')
        separator.pack(fill='x', pady=(15, 10))
        
        # 감정 분포 - 통일된 폰트
        ttk.Label(sentiment_frame, text="Sentiment Distribution:", 
                 font=("Segoe UI", 10, "bold")).pack(pady=(0, 8))
        
        self.positive_var = tk.StringVar(value="Positive: --%")
        self.negative_var = tk.StringVar(value="Negative: --%")
        self.neutral_var = tk.StringVar(value="Neutral: --%")
        
        ttk.Label(sentiment_frame, textvariable=self.positive_var, 
                 foreground="white", font=("Segoe UI", 9)).pack(pady=1)
        ttk.Label(sentiment_frame, textvariable=self.negative_var, 
                 foreground="white", font=("Segoe UI", 9)).pack(pady=1)
        ttk.Label(sentiment_frame, textvariable=self.neutral_var, 
                 foreground="white", font=("Segoe UI", 9)).pack(pady=1)
        
        # 키워드 표시 섹션 (Article Details 자리에 배치)
        ttk.Label(sentiment_frame, text="Analysis Keywords:", 
                 font=("Segoe UI", 10, "bold")).pack(pady=(20, 8))
        
        # 키워드 표시 영역 (sentiment score 제거로 공간 확장)
        self.keywords_text = scrolledtext.ScrolledText(
            sentiment_frame, 
            height=11, 
            width=42, 
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg=self.theme_manager.colors['panel_light'] if hasattr(self.theme_manager, 'colors') else '#F8F8FF',
            fg=self.theme_manager.colors['text'] if hasattr(self.theme_manager, 'colors') else '#1B1350',
            insertbackground=self.theme_manager.colors['hotpink'] if hasattr(self.theme_manager, 'colors') else '#FF69B4',
            selectbackground=self.theme_manager.colors['magenta'] if hasattr(self.theme_manager, 'colors') else '#DDA0DD',
            state='disabled'
        )
        self.keywords_text.pack(fill="both", expand=True)
        
        # 초기 메시지
        self.update_keywords_display("Analyze a stock to see keywords used for news search...")
    
    def setup_trending_panel(self):
        """트렌딩 토픽 패널 설정"""
        trending_frame = ttk.LabelFrame(self.tab_frame, text="Trending Topics", padding="10")
        trending_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # 트렌딩 토픽을 스크롤 가능한 텍스트 영역으로 변경
        self.trending_text = scrolledtext.ScrolledText(
            trending_frame,
            height=6,
            wrap=tk.WORD,
            font=("Segoe UI", 9),
            bg=self.theme_manager.colors['panel_light'] if hasattr(self.theme_manager, 'colors') else '#F8F8FF',
            fg=self.theme_manager.colors['text'] if hasattr(self.theme_manager, 'colors') else '#1B1350',
            insertbackground=self.theme_manager.colors['hotpink'] if hasattr(self.theme_manager, 'colors') else '#FF69B4',
            selectbackground=self.theme_manager.colors['magenta'] if hasattr(self.theme_manager, 'colors') else '#DDA0DD',
            state='disabled'  # 읽기 전용
        )
        self.trending_text.pack(fill="both", expand=True, pady=5)
        
        # 초기 메시지 설정
        self.update_trending_display("Click 'Trending Topics' button to load trending market topics...")
    
    def update_keywords_display(self, text):
        """키워드 디스플레이 업데이트"""
        if hasattr(self, 'keywords_text') and self.keywords_text:
            self.keywords_text.config(state='normal')
            self.keywords_text.delete(1.0, tk.END)
            self.keywords_text.insert(1.0, text)
            self.keywords_text.config(state='disabled')
    
    def update_trending_display(self, text):
        """트렌딩 토픽 디스플레이 업데이트"""
        self.trending_text.config(state='normal')
        self.trending_text.delete(1.0, tk.END)
        self.trending_text.insert(1.0, text)
        self.trending_text.config(state='disabled')
    
    def _get_current_stock_symbols(self):
        """Stock Data 탭에서 현재 로드된 주식 심볼 목록 가져오기"""
        if self.main_app and hasattr(self.main_app, 'current_stock_data') and self.main_app.current_stock_data:
            return list(self.main_app.current_stock_data.keys())
        # Fallback: 기본 심볼들
        return ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA"]
    
    def _refresh_stock_list(self):
        """주식 심볼 목록 새로고침"""
        current_symbols = self._get_current_stock_symbols()
        self.symbol_combo['values'] = current_symbols
        
        if current_symbols:
            self.status_var.set(f"Found {len(current_symbols)} stocks for news analysis")
            # 현재 선택된 심볼이 목록에 없으면 첫 번째 심볼로 설정
            if not self.symbol_var.get() or self.symbol_var.get() not in current_symbols:
                self.symbol_var.set(current_symbols[0])
        else:
            self.status_var.set("No stocks found. Add stocks in Stock Data tab first.")
            self.symbol_var.set("AAPL")  # 기본값
    
    def analyze_news_async(self):
        """비동기로 뉴스 분석 실행"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            messagebox.showwarning("Warning", "Please enter a stock symbol")
            return
        
        self.current_symbol = symbol
        self.status_var.set("Analyzing news for " + symbol + "...")
        
        # 백그라운드 스레드에서 분석 실행
        threading.Thread(target=self.analyze_news, daemon=True).start()
    
    def analyze_news(self):
        """뉴스 분석 실행"""
        try:
            # 새로운 3단계 뉴스 분석 알고리즘 적용
            self.status_var.set(f"Step 1/3: Starting analysis for {self.current_symbol}...")
            self.tab_frame.update()
            
            self.status_var.set(f"Step 2/3: Finding relevant keywords for {self.current_symbol}...")
            self.tab_frame.update()
            
            # 키워드 찾기 및 표시
            keywords = news_sentiment_analyzer._get_symbol_keywords(self.current_symbol)
            self.current_keywords = keywords
            
            # 키워드 표시 업데이트 (Company & Business Keywords에만 집중)
            keywords_display = f"Keywords found for {self.current_symbol}:\n\n"
            if keywords:
                # Company & Business Keywords만 필터링
                company_keywords = [kw for kw in keywords 
                                  if kw.upper() not in ['EARNINGS', 'REVENUE', 'PROFIT', 'STOCK', 'SHARES', 'MARKET CAP', 'DIVIDEND']
                                  and kw.upper() != self.current_symbol.upper() 
                                  and kw.lower() != self.current_symbol.lower()]
                
                if company_keywords:
                    keywords_display += f"Company & Business Keywords ({len(company_keywords)}):\n\n"
                    # 키워드를 줄바꿈으로 표시하여 가독성 향상
                    for i, keyword in enumerate(company_keywords[:20], 1):
                        keywords_display += f"{i:2d}. {keyword}\n"
                    
                    if len(company_keywords) > 20:
                        keywords_display += f"\n... and {len(company_keywords) - 20} more keywords\n"
                    
                    keywords_display += f"\nTotal keywords: {len(company_keywords)}\n"
                    keywords_display += f"Search strategy: Company-focused keyword matching"
                else:
                    keywords_display += "No company-specific keywords found.\n"
                    keywords_display += "Using symbol-based search only."
            else:
                keywords_display += "No specific keywords found. Using symbol-based search."
            
            # UI 업데이트
            self.tab_frame.after(0, lambda: self.update_keywords_display(keywords_display))
            
            self.status_var.set(f"Step 3/3: Collecting keyword-based news for {self.current_symbol}...")
            self.tab_frame.update()
            
            articles = news_sentiment_analyzer.get_stock_news(self.current_symbol, limit=50)
            
            if not articles:
                self.status_var.set("No news articles found for " + self.current_symbol)
                messagebox.showinfo("Information", f"No recent news articles found for {self.current_symbol}. Please try a different symbol or check again later.")
                return
            
            # 감정 분석
            self.status_var.set("Performing sentiment analysis...")
            sentiment = news_sentiment_analyzer.analyze_sentiment(articles)
            
            # UI 업데이트
            self.current_articles = articles
            self.current_sentiment = sentiment
            
            # 메인 스레드에서 UI 업데이트
            self.tab_frame.after(0, self.update_news_display)
            self.tab_frame.after(0, self.update_sentiment_display)
            
            self.status_var.set(f"Analysis completed successfully - {len(articles)} articles analyzed")
            
        except Exception as e:
            self.status_var.set("Analysis failed - please try again")
            messagebox.showerror("Analysis Error", f"Failed to analyze news for {self.current_symbol}:\n\n{str(e)}\n\nPlease check your internet connection and try again.")
    
    def update_news_display(self):
        """뉴스 디스플레이 업데이트"""
        # 기존 항목 삭제
        for item in self.news_tree.get_children():
            self.news_tree.delete(item)
        
        # 새 뉴스 추가
        for article in self.current_articles:
            date_str = article.published_date.strftime("%m/%d %H:%M")
            title = article.title[:65] + "..." if len(article.title) > 65 else article.title
            
            # 감정에 따른 영어 텍스트
            sentiment_text = self.get_sentiment_label(article.sentiment_type)
            
            item = self.news_tree.insert("", "end", values=(
                date_str,
                title,
                article.source,
                sentiment_text
            ))
            
            # 감정에 따른 색상 태그 (이모지 제거)
            if article.sentiment_type:
                if article.sentiment_type in [SentimentType.POSITIVE, SentimentType.VERY_POSITIVE]:
                    self.news_tree.item(item, tags=('positive',))
                elif article.sentiment_type in [SentimentType.NEGATIVE, SentimentType.VERY_NEGATIVE]:
                    self.news_tree.item(item, tags=('negative',))
                else:
                    self.news_tree.item(item, tags=('neutral',))
    
    def update_sentiment_display(self):
        """감정 분석 디스플레이 업데이트"""
        if not self.current_sentiment:
            return
        
        sentiment = self.current_sentiment
        
        # 전체 감정 - 영어로 표시
        sentiment_label = self.get_sentiment_label(sentiment.overall_sentiment)
        self.overall_sentiment_var.set(f"Overall Sentiment: {sentiment_label}")
        
        # 신뢰도 - 영어로 표시
        self.confidence_var.set(f"Analysis Confidence: {sentiment.confidence:.1%}")
        
        # 분포 - 영어로 표시
        self.positive_var.set(f"Positive Articles: {sentiment.positive_ratio:.1%}")
        self.negative_var.set(f"Negative Articles: {sentiment.negative_ratio:.1%}")
        self.neutral_var.set(f"Neutral Articles: {sentiment.neutral_ratio:.1%}")
    
    def get_sentiment_label(self, sentiment_type: Optional[SentimentType]) -> str:
        """감정 타입에 따른 영어 라벨 반환"""
        if not sentiment_type:
            return "Unknown"
        
        label_map = {
            SentimentType.VERY_POSITIVE: "Very Positive",
            SentimentType.POSITIVE: "Positive",
            SentimentType.NEUTRAL: "Neutral",
            SentimentType.NEGATIVE: "Negative",
            SentimentType.VERY_NEGATIVE: "Very Negative"
        }
        
        return label_map.get(sentiment_type, "Unknown")
    
    def on_news_select(self, event):
        """뉴스 선택 이벤트 - 알림창으로 상세 정보 표시"""
        selection = self.news_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        index = self.news_tree.index(item)
        
        if index < len(self.current_articles):
            article = self.current_articles[index]
            self.show_article_details_popup(article)
    
    def show_article_details_popup(self, article):
        """기사 상세 정보를 알림창으로 표시"""
        dialog = tk.Toplevel(self.parent_notebook)
        dialog.title(f"Article Details - {article.source}")
        
        # 테마 적용
        if hasattr(self.theme_manager, 'colors'):
            colors = self.theme_manager.colors
        else:
            colors = {
                'panel': '#1F144A',
                'panel_light': '#F8F8FF',
                'text': '#1B1350',
                'periwinkle': '#A78BFA',
                'lavender': '#C4B5FD',
                'hotpink': '#FF69B4',
                'magenta': '#DDA0DD'
            }
        
        dialog.configure(bg=colors['panel'])
        dialog.resizable(True, True)
        
        # 창 크기와 위치 설정
        width, height = 700, 600
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # 창이 완전히 표시된 후 모달 설정
        dialog.update_idletasks()
        dialog.deiconify()  # 창을 확실히 표시
        dialog.lift()       # 창을 맨 앞으로
        dialog.focus_set()  # 포커스 설정
        try:
            dialog.grab_set()  # 모달 창으로 설정
        except tk.TclError:
            # grab_set 실패시 무시하고 계속 진행
            pass
        
        # 메인 프레임
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_label = ttk.Label(main_frame, 
                              text="Article Details",
                              font=('Arial', 14, 'bold'),
                              foreground=colors['periwinkle'])
        title_label.pack(pady=(0, 15))
        
        # 내용을 위한 스크롤 가능한 텍스트 영역
        content_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            height=25,
            width=80,
            font=('Arial', 11),
            bg=colors['panel_light'],
            fg=colors['text'],
            insertbackground=colors['hotpink'],
            selectbackground=colors['magenta'],
            state='normal'
        )
        content_text.pack(fill="both", expand=True, pady=(0, 15))
        
        # 내용 삽입
        detail_text = f"Title: {article.title}\n\n"
        detail_text += f"Source: {article.source}\n"
        detail_text += f"Date: {article.published_date.strftime('%Y-%m-%d %H:%M')}\n"
        
        if article.sentiment_score is not None:
            sentiment_label = self.get_sentiment_label(article.sentiment_type)
            detail_text += f"Sentiment: {article.sentiment_score:.3f} ({sentiment_label})\n"
        
        if hasattr(article, 'keywords') and article.keywords:
            detail_text += f"Keywords: {', '.join(article.keywords)}\n"
        
        # 기사 내용 처리 - 내용이 없거나 매우 짧을 경우 처리
        content = article.content.strip() if article.content else ""
        
        detail_text += f"\nContent:\n{'-'*50}\n"
        
        if content and len(content) > 10:
            detail_text += f"{content}\n\n"
        else:
            detail_text += "Content not available or too short.\n"
            detail_text += "This may be due to RSS feed limitations or content protection.\n\n"
        
        content_text.insert(1.0, detail_text)
        content_text.config(state='disabled')
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 닫기 버튼
        def close_dialog():
            dialog.destroy()
        
        if self.main_app:
            close_btn = self.main_app.icon_button(
                button_frame, 'save', 'Close',
                close_dialog, style='Pastel.Primary.TButton'
            )
        else:
            close_btn = ttk.Button(
                button_frame, text='Close',
                command=close_dialog
            )
        close_btn.pack(side=tk.RIGHT)
        
        # 키보드 바인딩
        dialog.bind('<Escape>', lambda e: close_dialog())
        close_btn.focus_set()
    
    def refresh_news(self):
        """뉴스 새로고침"""
        if self.current_symbol:
            # 캐시 초기화
            news_sentiment_analyzer.clear_cache()
            self.status_var.set("Refreshing news data...")
            self.analyze_news_async()
        else:
            messagebox.showinfo("Information", "Please analyze a stock symbol first before refreshing.")
    
    def show_trending_topics(self):
        """트렌딩 토픽을 GUI 스타일 적용된 팝업 창으로 표시"""
        self.status_var.set("Loading trending market topics...")
        
        def load_trending():
            try:
                topics = news_sentiment_analyzer.get_trending_topics(limit=15)
                
                if topics:
                    # 트렌딩 토픽을 더 읽기 쉽게 포맷팅
                    trending_items = []
                    
                    for topic in topics[:10]:  # 상위 10개 표시
                        sentiment_score = topic['sentiment']
                        mention_count = topic['mention_count']
                        
                        # 감정 표시 (이모티콘 제거)
                        if sentiment_score > 0.1:
                            sentiment_indicator = "Positive"
                        elif sentiment_score < -0.1:
                            sentiment_indicator = "Negative" 
                        else:
                            sentiment_indicator = "Neutral"
                        
                        trending_items.append(f"• {topic['topic'].title()} ({mention_count} mentions) - {sentiment_indicator}")
                    
                    trending_text = f"Top Market Trends Today:\n\n" + "\n".join(trending_items)
                    trending_text += f"\n\nLast updated: {datetime.now().strftime('%H:%M:%S')}"
                    
                    # GUI 스타일 적용된 팝업 창으로 표시
                    self.tab_frame.after(0, lambda: self.show_trending_popup("Trending Market Topics", trending_text))
                    self.tab_frame.after(0, lambda: self.status_var.set(f"Trending topics loaded - {len(topics)} topics found"))
                else:
                    error_text = "No trending topics available at the moment.\n\nThis could be due to:\n• Network connectivity issues\n• RSS feed temporarily unavailable\n• Low news activity\n\nPlease try again in a few minutes."
                    self.tab_frame.after(0, lambda: self.show_trending_popup("Trending Topics - No Data", error_text))
                    self.tab_frame.after(0, lambda: self.status_var.set("No trending topics found"))
                
            except Exception as e:
                error_msg = f"Unable to load trending topics.\n\nError: {str(e)}\n\nPlease check your internet connection and try again."
                self.tab_frame.after(0, lambda: self.show_trending_popup("Trending Topics - Error", error_msg))
                self.tab_frame.after(0, lambda: self.status_var.set("Failed to load trending topics"))
                print(f"Error loading trending topics: {e}")
        
        threading.Thread(target=load_trending, daemon=True).start()
    
    def show_trending_popup(self, title, content):
        """GUI 스타일 적용된 트렌딩 토픽 팝업 창 표시"""
        dialog = tk.Toplevel(self.parent_notebook)
        dialog.title(title)
        
        # 테마 적용
        if hasattr(self.theme_manager, 'colors'):
            colors = self.theme_manager.colors
        else:
            colors = {
                'panel': '#1F144A',
                'panel_light': '#F8F8FF',
                'text': '#1B1350',
                'periwinkle': '#A78BFA',
                'lavender': '#C4B5FD',
                'hotpink': '#FF69B4',
                'magenta': '#DDA0DD'
            }
        
        dialog.configure(bg=colors['panel'])
        dialog.resizable(False, False)
        dialog.grab_set()  # 모달 창으로 설정
        
        # 창 크기와 위치 설정
        width, height = 600, 500
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # 메인 프레임
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_label = ttk.Label(main_frame, 
                              text=title,
                              font=('Arial', 14, 'bold'),
                              foreground=colors['periwinkle'])
        title_label.pack(pady=(0, 15))
        
        # 내용을 위한 스크롤 가능한 텍스트 영역
        content_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            height=18,
            width=70,
            font=('Arial', 11),
            bg=colors['panel_light'],
            fg=colors['text'],
            insertbackground=colors['hotpink'],
            selectbackground=colors['magenta'],
            state='disabled'
        )
        content_text.pack(fill="both", expand=True, pady=(0, 15))
        
        # 내용 삽입
        content_text.config(state='normal')
        content_text.insert(1.0, content)
        content_text.config(state='disabled')
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 닫기 버튼
        def close_dialog():
            dialog.destroy()
        
        if self.main_app:
            close_btn = self.main_app.icon_button(
                button_frame, 'save', 'Close',
                close_dialog, style='Pastel.Primary.TButton'
            )
        else:
            close_btn = ttk.Button(
                button_frame, text='Close',
                command=close_dialog, style='Pastel.Primary.TButton'
            )
        close_btn.pack(side=tk.RIGHT)
        
        # 새로고침 버튼
        if self.main_app:
            refresh_btn = self.main_app.icon_button(
                button_frame, 'refresh', 'Refresh',
                lambda: [dialog.destroy(), self.show_trending_topics()], 
                style='Pastel.Ghost.TButton'
            )
        else:
            refresh_btn = ttk.Button(
                button_frame, text='Refresh',
                command=lambda: [dialog.destroy(), self.show_trending_topics()], 
                style='Pastel.Ghost.TButton'
            )
        refresh_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # 키보드 바인딩
        dialog.bind('<Escape>', lambda e: close_dialog())
        close_btn.focus_set()
    
    def get_tab_frame(self):
        """탭 프레임 반환"""
        return self.tab_frame