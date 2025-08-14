#!/usr/bin/env python3
"""Individual Analysis Tab Component - Cute Kuromi Style"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from src.core.config import MAGNIFICENT_SEVEN


class IndividualAnalysisTab:
    def __init__(self, notebook, main_app):
        self.notebook = notebook
        self.main_app = main_app
        self.colors = main_app.colors
        self.setup_tab()
        
    def setup_tab(self):
        """Create the individual stock analysis tab"""
        self.frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.frame, text="(@_@) Individual Analysis")
        
        # Configure grid
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        # Stock selection
        self.create_stock_selection()
        
        # Analysis results summary
        self.create_results_summary()
        
        # Detailed analysis
        self.create_detailed_analysis()
        
    def create_stock_selection(self):
        """Create stock selection panel"""
        select_frame = ttk.LabelFrame(self.frame, text="˚‧꒰ა 𓂋 ໒꒱ ‧˚ Choose Stock to Analyze", padding="15")
        select_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(select_frame, text="Stock Symbol:").grid(row=0, column=0, padx=(0, 10))
        
        self.analysis_stock_var = tk.StringVar()
        analysis_combo = ttk.Combobox(select_frame, textvariable=self.analysis_stock_var,
                                    values=list(MAGNIFICENT_SEVEN.keys()),
                                    state='readonly', width=15,
                                    style='Pastel.TCombobox')
        analysis_combo.grid(row=0, column=1, padx=(0, 15))
        
        ttk.Button(select_frame, text="(*o*) Deep Analysis",
                  command=self.analyze_individual_stock_advanced,
                  style='Pastel.Primary.TButton').grid(row=0, column=2, padx=(0, 10))
                  
        ttk.Button(select_frame, text="˚‧꒰ა 𓂋 ໒꒱ ‧˚ Quick Analysis",
                  command=self.analyze_individual_stock_basic,
                  style='Pastel.Primary.TButton').grid(row=0, column=3)
        
    def create_results_summary(self):
        """Create analysis results summary"""
        results_frame = ttk.LabelFrame(self.frame, text="(@_@) Analysis Summary", padding="15")
        results_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Score display
        score_frame = ttk.Frame(results_frame)
        score_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(score_frame, text="Overall Score:").grid(row=0, column=0, padx=(0, 10))
        self.score_label = ttk.Label(score_frame, text="--", font=('Arial', 14, 'bold'),
                                   foreground=self.colors['periwinkle'])
        self.score_label.grid(row=0, column=1, padx=(0, 30))
        
        ttk.Label(score_frame, text="Recommendation:").grid(row=0, column=2, padx=(0, 10))
        self.recommendation_label = ttk.Label(score_frame, text="--", font=('Arial', 14, 'bold'),
                                            foreground=self.colors['pink'])
        self.recommendation_label.grid(row=0, column=3)
        
    def create_detailed_analysis(self):
        """Create detailed analysis display"""
        detail_frame = ttk.LabelFrame(self.frame, text="(@_@) Detailed Analysis", padding="15")
        detail_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        detail_frame.grid_rowconfigure(0, weight=1)
        detail_frame.grid_columnconfigure(0, weight=1)
        
        self.analysis_text = scrolledtext.ScrolledText(
            detail_frame, 
            wrap=tk.WORD, 
            height=15,
            font=('Consolas', 11),
            bg=self.colors['panel_alt'],
            fg=self.colors['text'],
            insertbackground=self.colors['pink'],
            selectbackground=self.colors['periwinkle']
        )
        self.analysis_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add cute initial message
        initial_message = """(>.<) Individual Stock Analysis (>.<)

˚‧꒰ა 𓂋 ໒꒱ ‧˚ Select a stock symbol from the dropdown above
(*o*) Click "Deep Analysis" for comprehensive multi-criteria analysis
˚‧꒰ა 𓂋 ໒꒱ ‧˚ Click "Quick Analysis" for basic technical analysis

Ready to dive deep into your favorite stock? 
Choose a symbol and analysis type to get started! ⸜(｡˃ ᵕ ˂ )⸝♡

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        self.analysis_text.insert(1.0, initial_message)
        
    def analyze_individual_stock_advanced(self):
        """Analyze individual stock with advanced multi-criteria analysis"""
        symbol = self.analysis_stock_var.get()
        if not symbol:
            messagebox.showwarning("Notice", "Please select a stock symbol to analyze! (>.<)")
            return
            
        def analyze():
            try:
                self.main_app.update_status(f"(*o*) Performing advanced analysis on {symbol}...")
                self.main_app.show_progress()
                
                analysis = self.main_app.recommendation_engine.analyze_single_stock(symbol, use_advanced=True)
                
                if 'error' in analysis:
                    self.main_app.root.after(0, self.main_app.show_error, analysis['error'])
                else:
                    self.main_app.root.after(0, self.update_individual_analysis_display, analysis, True)
                
                self.main_app.root.after(0, self.main_app.update_status, f"₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ {symbol} advanced analysis completed!")
                self.main_app.root.after(0, self.main_app.hide_progress)
                
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"˚‧꒰ა 𓂋 ໒꒱ ‧˚ {symbol} analysis error: {str(e)}")
                self.main_app.root.after(0, self.main_app.hide_progress)
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def analyze_individual_stock_basic(self):
        """Analyze individual stock with basic analysis"""
        symbol = self.analysis_stock_var.get()
        if not symbol:
            messagebox.showwarning("Notice", "Please select a stock symbol to analyze! (>.<)")
            return
            
        def analyze():
            try:
                self.main_app.update_status(f"˚‧꒰ა 𓂋 ໒꒱ ‧˚ Performing basic analysis on {symbol}...")
                self.main_app.show_progress()
                
                analysis = self.main_app.recommendation_engine.analyze_single_stock(symbol, use_advanced=False)
                
                if 'error' in analysis:
                    self.main_app.root.after(0, self.main_app.show_error, analysis['error'])
                else:
                    self.main_app.root.after(0, self.update_individual_analysis_display, analysis, False)
                
                self.main_app.root.after(0, self.main_app.update_status, f"₍₍⚞(˶˃ ꒳ ˂˶)⚟⁾⁾ {symbol} basic analysis completed!")
                self.main_app.root.after(0, self.main_app.hide_progress)
                
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"˚‧꒰ა 𓂋 ໒꒱ ‧˚ {symbol} analysis error: {str(e)}")
                self.main_app.root.after(0, self.main_app.hide_progress)
        
        threading.Thread(target=analyze, daemon=True).start()
        
    def update_individual_analysis_display(self, analysis, is_advanced=True):
        """Update individual analysis display"""
        # Update score and recommendation
        self.score_label.config(text=f"{analysis['overall_score']}")
        self.recommendation_label.config(text=analysis['recommendation'])
        
        # Update detailed analysis
        self.analysis_text.delete(1.0, tk.END)
        
        if is_advanced and 'detailed_analysis' in analysis:
            detail_text = self._format_advanced_analysis_display(analysis)
        else:
            detail_text = self._format_basic_analysis_display(analysis)
        
        self.analysis_text.insert(1.0, detail_text)
        
    def _format_advanced_analysis_display(self, analysis):
        """Format advanced analysis for display"""
        detailed = analysis['detailed_analysis']
        investment_summary = analysis.get('investment_summary', {})
        
        text = f"""✨ KUROMI'S ADVANCED STOCK ANALYSIS ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(@_@) Stock: {analysis['symbol']} - {analysis['company']}
📈 Analysis Type: Multi-Criteria Investment Analysis
(*o*) Overall Score: {analysis['overall_score']}
🎯 Recommendation: {analysis['recommendation']}
🔒 Confidence Level: {analysis['confidence']}

💰 FUNDAMENTAL ANALYSIS:
Financial Health: {detailed['fundamental_analysis']['financial_health']['rating']} (Score: {detailed['fundamental_analysis']['financial_health']['score']:.2f})
Profitability: {detailed['fundamental_analysis']['profitability_metrics']['margin_rating']}
   └─ {detailed['fundamental_analysis']['profitability_metrics']['analysis']}
Debt Analysis: {detailed['fundamental_analysis']['debt_analysis']['rating']}
   └─ D/E Ratio: {detailed['fundamental_analysis']['debt_analysis']['debt_to_equity']:.2f}

📈 GROWTH ANALYSIS:
Growth Rating: {detailed['growth_analysis']['rating']}
Historical Growth: {detailed['growth_analysis']['revenue_growth_5y']:.1%} (5-year CAGR)
Industry: {detailed['growth_analysis']['industry']} (Growth Factor: {detailed['growth_analysis']['industry_factor']:.1f}x)

🏆 COMPETITIVE POSITION: {detailed['competitive_analysis']['position_strength']}
Key Advantages:"""

        for advantage in detailed['competitive_analysis']['advantages'][:3]:
            text += f"\n   💎 {advantage}"

        text += f"""

⚠️ RISK ASSESSMENT: {detailed['risk_assessment']['risk_level']} Risk
🛡️ Safety Score: {detailed['risk_assessment']['safety_score']:.2f}
Key Risk Factors:"""

        for risk in detailed['risk_assessment']['risk_factors'][:2]:
            text += f"\n   ⚡ {risk}"

        if investment_summary:
            text += f"""

💝 INVESTMENT SUMMARY:
Investment Thesis: {investment_summary.get('investment_thesis', 'N/A')}
Price Target: {investment_summary.get('price_target_range', 'N/A')}
Time Horizon: {investment_summary.get('time_horizon', 'N/A')}"""

        text += f"""

⏰ Analysis Timestamp: {analysis['timestamp']}

🌸 DISCLAIMER: This advanced analysis is for educational 
   and informational purposes only. Not financial advice! 
   Always do your own research! 💖
"""
        return text
    
    def _format_basic_analysis_display(self, analysis):
        """Format basic analysis for display"""
        breakdown = analysis.get('analysis_breakdown', {})
        
        text = f"""⚡ KUROMI'S QUICK STOCK ANALYSIS ⚡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(@_@) Stock: {analysis['symbol']} - {analysis['company']}
📈 Analysis Type: Basic Technical Analysis
(*o*) Overall Score: {analysis['overall_score']}
🎯 Recommendation: {analysis['recommendation']}
🔒 Confidence Level: {analysis['confidence']}

📊 ANALYSIS BREAKDOWN:"""

        if 'momentum' in breakdown:
            text += f"""

📈 Price Momentum:
   Score: {breakdown['momentum']['score']}
   {breakdown['momentum']['analysis']}"""

        if 'volume' in breakdown:
            text += f"""

📊 Volume Analysis:
   Score: {breakdown['volume']['score']}
   {breakdown['volume']['analysis']}"""

        if 'market_cap' in breakdown:
            text += f"""

🏢 Market Capitalization:
   Score: {breakdown['market_cap']['score']}
   {breakdown['market_cap']['analysis']}"""

        if 'volatility' in breakdown:
            text += f"""

⚖️ Volatility Assessment:
   Score: {breakdown['volatility']['score']}
   {breakdown['volatility']['analysis']}"""

        if 'value' in breakdown:
            text += f"""

💎 Value Proposition:
   Score: {breakdown['value']['score']}
   {breakdown['value']['analysis']}"""

        text += f"""

⏰ Analysis Timestamp: {analysis['timestamp']}

🌸 DISCLAIMER: This basic analysis is for educational purposes only.
   Not financial advice! Always do your own research! 💖
"""
        return text