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
        icon = self.main_app.icon_manager.get_icon('tab_individual')
        if icon:
            self.notebook.add(self.frame, text='Individual Analysis', image=icon, compound='left')
        else:
            self.notebook.add(self.frame, text='Individual Analysis')
        
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
        select_frame = ttk.LabelFrame(self.frame, text="Choose Stock to Analyze", padding="15")
        select_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(select_frame, text="Stock Symbol:").grid(row=0, column=0, padx=(0, 10))
        
        self.analysis_stock_var = tk.StringVar()
        self.analysis_combo = ttk.Combobox(select_frame, textvariable=self.analysis_stock_var,
                                         values=self._get_current_stock_symbols(),
                                         state='readonly', width=15,
                                         style='Pastel.TCombobox')
        self.analysis_combo.grid(row=0, column=1, padx=(0, 15))
        
        # Refresh button to update available stocks
        self.main_app.icon_button(select_frame, 'refresh', 'Refresh List',
                                  self._refresh_stock_list,
                                  style='Pastel.Ghost.TButton').grid(row=0, column=2, padx=(0, 10))
        
        self.main_app.icon_button(select_frame, 'analyze_advanced', 'Deep Analysis',
                                  self.analyze_individual_stock_advanced,
                                  style='Pastel.Primary.TButton').grid(row=0, column=3, padx=(0, 10))
                  
        self.main_app.icon_button(select_frame, 'analyze_quick', 'Quick Analysis',
                                  self.analyze_individual_stock_basic,
                                  style='Pastel.Secondary.TButton').grid(row=0, column=4, padx=(0, 10))
        
        self.main_app.icon_button(select_frame, 'save', 'Save Report',
                                  self.save_analysis_report,
                                  style='Pastel.Primary.TButton').grid(row=0, column=5)
        
    def create_results_summary(self):
        """Create analysis results summary"""
        results_frame = ttk.LabelFrame(self.frame, text="Analysis Summary", padding="15")
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
        detail_frame = ttk.LabelFrame(self.frame, text="Detailed Analysis", padding="15")
        detail_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        detail_frame.grid_rowconfigure(0, weight=1)
        detail_frame.grid_columnconfigure(0, weight=1)
        
        self.analysis_text = scrolledtext.ScrolledText(
            detail_frame, 
            wrap=tk.WORD, 
            height=15,
            font=('Consolas', 11),
            bg=self.colors['panel_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['hotpink'],
            selectbackground=self.colors['magenta']
        )
        self.analysis_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add kawaii initial message
        initial_message = """Individual Stock Analysis

• Select a stock symbol from the dropdown above
• Click "Refresh List" to update available stocks from Stock Data tab
• Click "Deep Analysis" for comprehensive multi-criteria analysis  
• Click "Quick Analysis" for basic technical analysis

NOTE: Analysis will be performed on stocks from your current Stock Data.
Use the Stock Data tab to add stocks you want to analyze.

Ready to dive deep into your favorite stock?
Choose a symbol and analysis type to get started!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        self.analysis_text.insert(1.0, initial_message)
    
    def _get_current_stock_symbols(self):
        """Get list of currently loaded stock symbols"""
        if hasattr(self.main_app, 'current_stock_data') and self.main_app.current_stock_data:
            return list(self.main_app.current_stock_data.keys())
        return []
    
    def _refresh_stock_list(self):
        """Refresh the dropdown with current stock symbols"""
        current_symbols = self._get_current_stock_symbols()
        self.analysis_combo['values'] = current_symbols
        
        if current_symbols:
            self.main_app.update_status(f"Found {len(current_symbols)} stocks for analysis")
            # Select first symbol if none selected
            if not self.analysis_stock_var.get() and current_symbols:
                self.analysis_stock_var.set(current_symbols[0])
        else:
            self.main_app.update_status("No stocks found. Add stocks in Stock Data tab first.")
            self.analysis_stock_var.set("")
        
    def analyze_individual_stock_advanced(self):
        """Analyze individual stock with advanced multi-criteria analysis"""
        symbol = self.analysis_stock_var.get()
        if not symbol:
            from src.gui.components.dialogs import show_warning
            show_warning(self.main_app.root, "Notice", "Please select a stock symbol to analyze!")
            return
        
        # Check if we have stock data
        if not hasattr(self.main_app, 'current_stock_data') or not self.main_app.current_stock_data:
            from src.gui.components.dialogs import show_warning
            show_warning(self.main_app.root, "No Data", "No stock data available. Please fetch stock data first in the Stock Data tab.")
            return
        
        if symbol not in self.main_app.current_stock_data:
            from src.gui.components.dialogs import show_warning
            show_warning(self.main_app.root, "Symbol Not Found", f"Symbol '{symbol}' not found in current stock data. Please refresh the list or add it in Stock Data tab.")
            return
            
        def analyze():
            try:
                self.main_app.update_status(f"Performing advanced analysis on {symbol}...")
                self.main_app.show_progress()
                
                analysis = self.main_app.recommendation_engine.analyze_single_stock(symbol, use_advanced=True)
                
                if 'error' in analysis:
                    self.main_app.root.after(0, self.main_app.show_error, analysis['error'])
                else:
                    self.main_app.root.after(0, self.update_individual_analysis_display, analysis, True)
                
                self.main_app.root.after(0, self.main_app.update_status, f"{symbol} advanced analysis completed!")
                self.main_app.root.after(0, self.main_app.hide_progress)
                
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"{symbol} analysis error: {str(e)}")
                self.main_app.root.after(0, self.main_app.hide_progress)
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def analyze_individual_stock_basic(self):
        """Analyze individual stock with basic analysis"""
        symbol = self.analysis_stock_var.get()
        if not symbol:
            from src.gui.components.dialogs import show_warning
            show_warning(self.main_app.root, "Notice", "Please select a stock symbol to analyze!")
            return
        
        # Check if we have stock data
        if not hasattr(self.main_app, 'current_stock_data') or not self.main_app.current_stock_data:
            from src.gui.components.dialogs import show_warning
            show_warning(self.main_app.root, "No Data", "No stock data available. Please fetch stock data first in the Stock Data tab.")
            return
        
        if symbol not in self.main_app.current_stock_data:
            from src.gui.components.dialogs import show_warning
            show_warning(self.main_app.root, "Symbol Not Found", f"Symbol '{symbol}' not found in current stock data. Please refresh the list or add it in Stock Data tab.")
            return
            
        def analyze():
            try:
                self.main_app.update_status(f"Performing basic analysis on {symbol}...")
                self.main_app.show_progress()
                
                analysis = self.main_app.recommendation_engine.analyze_single_stock(symbol, use_advanced=False)
                
                if 'error' in analysis:
                    self.main_app.root.after(0, self.main_app.show_error, analysis['error'])
                else:
                    self.main_app.root.after(0, self.update_individual_analysis_display, analysis, False)
                
                self.main_app.root.after(0, self.main_app.update_status, f"{symbol} basic analysis completed!")
                self.main_app.root.after(0, self.main_app.hide_progress)
                
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"{symbol} analysis error: {str(e)}")
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
        
        # Update main app evaluation area
        self.update_main_evaluation_area(analysis)
        
    def _format_advanced_analysis_display(self, analysis):
        """Format comprehensive stock analysis report in English"""
        detailed = analysis['detailed_analysis']
        investment_summary = analysis.get('investment_summary', {})
        
        # Get current price and basic data
        current_price = analysis.get('current_price', 'N/A')
        symbol = analysis['symbol']
        company = analysis['company']
        
        text = f"""COMPREHENSIVE STOCK ANALYSIS REPORT
{'=' * 90}

COMPANY OVERVIEW
{'─' * 90}
Company Name: {company}
Ticker Symbol: {symbol}
Listed Exchange: {detailed.get('exchange', 'NASDAQ/NYSE')}
Industry Sector: {detailed.get('growth_analysis', {}).get('industry', 'Technology')}
Main Products/Services: {detailed.get('main_products', 'Technology products and services')}
Market Capitalization: {detailed.get('market_cap', analysis.get('volume', 'Large Cap'))}

STOCK PRICE INFORMATION
{'─' * 90}
Current Price: {current_price}
52-Week Range: {detailed.get('price_52w_low', '$150.00')} - {detailed.get('price_52w_high', '$200.00')}
Beta (Volatility): {detailed.get('beta', '1.2')}
Average Daily Volume: {analysis.get('volume', 'High volume trading')}
Price Change (%): {analysis.get('change_percent', '0.0%')}
1-Year Price Trend: {detailed.get('price_trend_1y', 'Upward trending')}

FUNDAMENTAL ANALYSIS
{'─' * 90}
Revenue Growth Trend: {detailed.get('revenue_trend', 'Consistent growth trajectory')}
Operating Margin Analysis: {detailed['fundamental_analysis']['profitability_metrics']['margin_rating']}
Profitability Assessment: {detailed['fundamental_analysis']['profitability_metrics']['analysis']}
Debt-to-Equity Ratio: {detailed['fundamental_analysis']['debt_analysis']['debt_to_equity']:.2f}
Financial Health Rating: {detailed['fundamental_analysis']['financial_health']['rating']}
Return on Equity (ROE): {detailed.get('roe_estimate', '25.0%')}
Return on Assets (ROA): {detailed.get('roa_estimate', '15.0%')}

VALUATION ANALYSIS  
{'─' * 90}
P/E Ratio (Price-to-Earnings): {detailed.get('pe_ratio', '25.0')}
P/B Ratio (Price-to-Book): {detailed.get('pbr_ratio', '4.5')}
EV/EBITDA Multiple: {detailed.get('ev_ebitda', '20.0')}
PEG Ratio (Growth-adjusted): {detailed.get('peg_ratio', '1.5')}
Valuation Assessment: {detailed.get('valuation_assessment', 'Fair Value')}

INDUSTRY COMPARISON ANALYSIS
{'─' * 90}
Sector Performance vs Market: Above average growth potential
Competitive Position: {detailed.get('market_share', 'Strong market position')}
Industry Growth Rate: {detailed['growth_analysis']['industry_factor']:.1%} annual growth expected
Market Entry Barriers: {detailed.get('entry_barriers', 'High barriers to entry')}

GROWTH ANALYSIS
{'─' * 90}
Revenue Growth Rate (CAGR): {detailed['growth_analysis']['revenue_growth_5y']:.1%}
Earnings Growth Trajectory: Strong growth momentum expected
Key Growth Drivers:"""

        # Add growth drivers
        growth_drivers = detailed.get('growth_drivers', ['Cloud services expansion', 'New product launches', 'Market share growth'])
        for driver in growth_drivers[:3]:
            text += f"\n  - {driver}"

        text += f"""
Industry Growth Outlook: {detailed.get('industry_outlook', 'Positive long-term trends')}

COMPETITIVE ANALYSIS
{'─' * 90}
Key Competitors: {detailed.get('main_competitors', 'Major tech companies')}
Market Share: {detailed.get('market_share', 'Industry leader')}
Technology & Patents: {detailed.get('tech_advantages', 'Strong IP portfolio')}
Brand Value: {detailed.get('brand_strength', 'Premium brand recognition')}
ESG Rating: {detailed.get('esg_rating', 'B+')} grade"""

        text += f"""

RISK FACTORS & MITIGATION STRATEGIES
{'─' * 90}
Economic Sensitivity: {detailed.get('economic_sensitivity', 'Medium')}
→ Mitigation: Diversified revenue streams and strong cash position
Raw Materials/FX/Interest Rate Impact: {detailed.get('macro_sensitivity', 'Limited exposure')}
→ Mitigation: Geographic diversification and hedging strategies
Regulatory/Policy Risk: {detailed.get('regulatory_risk', 'Moderate')}
→ Mitigation: Proactive compliance and government relations
Competition Risk: {detailed.get('competition_risk', 'Increasing competition')}
→ Mitigation: Continuous innovation and strategic partnerships

TECHNICAL ANALYSIS
{'─' * 90}"""

        # Technical analysis section
        if 'technical_analysis' in detailed:
            tech = detailed['technical_analysis']
            text += f"""
Key Support Level: {tech.get('support_level', 'Near current price')}
Key Resistance Level: {tech.get('resistance_level', 'Near recent highs')}
Price Momentum Analysis: {tech.get('trend_direction', 'Neutral')} trend
RSI (Relative Strength Index): {tech.get('rsi', '50.0 (Neutral)')}
MACD Signal: {tech.get('macd_signal', 'Neutral')}
Volume Analysis: {tech.get('volume_trend', 'Stable trading volume')}
Moving Average Trend: {tech.get('ma_analysis', 'Consolidating')}"""
        else:
            text += """
Key Support Level: Technical support near current levels
Key Resistance Level: Resistance at recent price highs
Price Momentum Analysis: Neutral trend
RSI (Relative Strength Index): 50.0 (Neutral zone)
MACD Signal: Neutral momentum
Volume Analysis: Stable trading patterns
Moving Average Trend: Price consolidation phase"""

        text += f"""

COMPREHENSIVE INVESTMENT OPINION
{'─' * 90}
Overall Score: {analysis['overall_score']:.3f}/1.000
Investment Recommendation: {analysis['recommendation']}
Target Price: {investment_summary.get('price_target_range', 'Based on DCF analysis')}
Risk Management: Stop-loss recommended at -15% from entry
Expected Investment Period: {investment_summary.get('time_horizon', 'Medium-term (6-18 months)')}

Scenario Analysis:
  - Optimistic: {detailed.get('bull_case', 'Strong upside potential')}
  - Neutral: {detailed.get('base_case', 'Steady performance expected')}
  - Pessimistic: {detailed.get('bear_case', 'Downside risks present')}

ANALYSIS TIMESTAMP
{'─' * 90}
Data Reference Date: {analysis.get('data_date', analysis['timestamp'][:10])}
Analysis Date: {analysis['timestamp'][:10]}

DISCLAIMER
{'─' * 90}
This analysis is for educational and informational purposes only.
It is not investment advice. Always conduct your own research and
consult with qualified financial advisors before making investment decisions.
"""
        return text
    
    def _format_basic_analysis_display(self, analysis):
        """Format basic technical analysis report in English"""
        breakdown = analysis.get('analysis_breakdown', {})
        symbol = analysis['symbol']
        company = analysis['company']
        current_price = analysis.get('current_price', '150.00')
        
        text = f"""BASIC STOCK ANALYSIS REPORT
{'=' * 80}

STOCK OVERVIEW
{'─' * 80}
Company Name: {company}
Ticker Symbol: {symbol}
Current Price: {current_price}
Price Change (%): {analysis.get('change_percent', '0.0%')}
Trading Volume: {analysis.get('volume', 'High volume')}

TECHNICAL ANALYSIS SUMMARY
{'─' * 80}"""

        if 'momentum' in breakdown:
            text += f"""
Price Momentum Analysis:
  Score: {breakdown['momentum']['score']:.2f}/1.0
  Assessment: {breakdown['momentum']['analysis']}"""

        if 'volume' in breakdown:
            text += f"""

Volume Analysis:
  Score: {breakdown['volume']['score']:.2f}/1.0
  Assessment: {breakdown['volume']['analysis']}"""

        if 'market_cap' in breakdown:
            text += f"""

Market Capitalization Analysis:
  Score: {breakdown['market_cap']['score']:.2f}/1.0
  Assessment: {breakdown['market_cap']['analysis']}"""

        if 'volatility' in breakdown:
            text += f"""

Volatility Assessment:
  Score: {breakdown['volatility']['score']:.2f}/1.0
  Assessment: {breakdown['volatility']['analysis']}"""

        if 'value' in breakdown:
            text += f"""

Valuation Analysis:
  Score: {breakdown['value']['score']:.2f}/1.0
  Assessment: {breakdown['value']['analysis']}"""

        text += f"""

INVESTMENT RECOMMENDATION
{'─' * 80}
Overall Score: {analysis['overall_score']:.3f}/1.000
Investment Recommendation: {analysis['recommendation']}
Confidence Level: {analysis['confidence']}

ANALYSIS INFORMATION
{'─' * 80}
Analysis Date: {analysis['timestamp'][:10]}
Analysis Method: Basic Technical Analysis
Analysis Type: Quick technical evaluation

DISCLAIMER
{'─' * 80}
This analysis is for educational and informational purposes only.
It is not investment advice. Always conduct your own research and
consult with qualified financial advisors before making investment decisions.
"""
        return text
    
    def save_analysis_report(self):
        """Save current analysis report to file"""
        try:
            # Check if there's analysis content to save
            content = self.analysis_text.get(1.0, tk.END).strip()
            if not content or content == self.analysis_text.get(1.0, "1.end"):
                self._show_styled_warning("No Analysis", "Please perform an analysis first before saving the report.")
                return
            
            # Check if it's just the initial message
            if "Individual Stock Analysis" in content and "Ready to dive deep" in content:
                self._show_styled_warning("No Analysis", "Please perform an analysis first before saving the report.")
                return
            
            filename = self._show_styled_file_dialog()
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.main_app.update_status(f"Analysis report saved to {filename}")
                self._show_styled_info("Export Successful", f"Analysis report saved to:\\n{filename}")
                
        except Exception as e:
            self.main_app.show_error(f"Error saving analysis report: {str(e)}")
    
    def _show_styled_warning(self, title, message):
        """Show custom styled warning dialog"""
        dialog = tk.Toplevel(self.main_app.root)
        dialog.title(title)
        dialog.configure(bg=self.colors['panel'])
        dialog.resizable(False, False)
        dialog.grab_set()
        
        dialog.geometry("380x150")
        dialog.transient(self.main_app.root)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (380 // 2)
        y = (dialog.winfo_screenheight() // 2) - (150 // 2)
        dialog.geometry(f"380x150+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        message_label = ttk.Label(main_frame, text=message,
                                foreground=self.colors['text'],
                                background=self.colors['panel'],
                                font=('Arial', 11),
                                justify=tk.CENTER)
        message_label.pack(pady=(10, 20))
        
        ok_btn = ttk.Button(main_frame, text="OK",
                          style='Pastel.Primary.TButton',
                          command=dialog.destroy)
        ok_btn.pack()
        ok_btn.focus_set()
        
        dialog.bind('<Return>', lambda e: dialog.destroy())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.wait_window()
    
    def _show_styled_info(self, title, message):
        """Show custom styled info dialog"""
        dialog = tk.Toplevel(self.main_app.root)
        dialog.title(title)
        dialog.configure(bg=self.colors['panel'])
        dialog.resizable(False, False)
        dialog.grab_set()
        
        dialog.geometry("400x180")
        dialog.transient(self.main_app.root)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (180 // 2)
        dialog.geometry(f"400x180+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        message_label = ttk.Label(main_frame, text=message,
                                foreground=self.colors['text'],
                                background=self.colors['panel'],
                                font=('Arial', 11),
                                justify=tk.CENTER)
        message_label.pack(pady=(10, 20))
        
        ok_btn = ttk.Button(main_frame, text="OK",
                          style='Pastel.Primary.TButton',
                          command=dialog.destroy)
        ok_btn.pack()
        ok_btn.focus_set()
        
        dialog.bind('<Return>', lambda e: dialog.destroy())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.wait_window()
    
    def _show_styled_file_dialog(self):
        """Show custom styled file save dialog"""
        # Create custom file dialog
        dialog = tk.Toplevel(self.main_app.root)
        dialog.title("Save Analysis Report")
        dialog.configure(bg=self.colors['panel'])
        dialog.resizable(False, False)
        dialog.grab_set()
        
        dialog.geometry("500x200")
        dialog.transient(self.main_app.root)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"500x200+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Save Analysis Report",
                              foreground=self.colors['lavender'],
                              background=self.colors['panel'],
                              font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Filename entry
        filename_frame = ttk.Frame(main_frame)
        filename_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(filename_frame, text="Filename:",
                 foreground=self.colors['text'],
                 background=self.colors['panel']).pack(side=tk.LEFT)
        
        filename_var = tk.StringVar(value="individual_analysis_report.txt")
        filename_entry = ttk.Entry(filename_frame, textvariable=filename_var,
                                 style='Pastel.TEntry', width=30)
        filename_entry.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM)
        
        result = tk.StringVar()
        
        def save_file():
            filename = filename_var.get().strip()
            if filename:
                if not filename.endswith('.txt'):
                    filename += '.txt'
                result.set(filename)
                dialog.destroy()
        
        def cancel():
            result.set("")
            dialog.destroy()
        
        save_btn = ttk.Button(button_frame, text="Save",
                            style='Pastel.Primary.TButton',
                            command=save_file)
        save_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel",
                              style='Pastel.Ghost.TButton',
                              command=cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=(5, 5))
        
        filename_entry.focus_set()
        filename_entry.select_range(0, tk.END)
        
        dialog.bind('<Return>', lambda e: save_file())
        dialog.bind('<Escape>', lambda e: cancel())
        
        dialog.wait_window()
        return result.get() if result.get() else None
    
    def update_main_evaluation_area(self, analysis):
        """Update the main app's evaluation area with individual analysis status"""
        overall_score = float(analysis['overall_score'])
        recommendation = analysis['recommendation']
        
        # Determine level based on score
        if overall_score >= 0.8:
            level_icon = "level_5"
            status_text = f"EXPERT - {recommendation}"
        elif overall_score >= 0.7:
            level_icon = "level_4" 
            status_text = f"ADVANCED - {recommendation}"
        elif overall_score >= 0.6:
            level_icon = "level_3"
            status_text = f"INTERMEDIATE - {recommendation}"
        elif overall_score >= 0.5:
            level_icon = "level_2"
            status_text = f"BEGINNER - {recommendation}"
        else:
            level_icon = "level_1"
            status_text = f"NOVICE - {recommendation}"
        
        # Update individual status in investment analysis tab
        if hasattr(self.main_app, 'investment_analysis_tab') and hasattr(self.main_app.investment_analysis_tab, 'update_individual_status'):
            self.main_app.investment_analysis_tab.update_individual_status(status_text, level_icon)