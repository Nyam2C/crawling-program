#!/usr/bin/env python3
"""
Magnificent Seven Stock Analysis - Cute Kurumi GUI Application
Powered by Kurumi's magical cuteness! 💖✨
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from src.analysis.recommendation_engine import RecommendationEngine
from src.data.stock_crawler import StockCrawler
from src.gui.components.stock_data_tab import StockDataTab
from src.gui.components.recommendations_tab import RecommendationsTab
from src.gui.components.analysis_tab import IndividualAnalysisTab
from src.gui.components.settings_tab import SettingsTab

# Try to import charts module
try:
    from src.gui.gui_charts import StockChartsFrame
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False
    print("Charts module not available. Install matplotlib for chart functionality.")


class StockAnalysisGUI:
    """Main GUI application for stock analysis and recommendations - Cute Kurumi Edition! 💖"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        self.create_styles()
        self.create_widgets()
        
        # Initialize engines
        self.recommendation_engine = RecommendationEngine(delay=1)
        self.stock_crawler = StockCrawler(delay=1)
        
        # Data storage
        self.current_stock_data = {}
        self.current_recommendations = {}
        
        # Animation variables
        self.animation_running = False
        
        # Initialize cute effects
        self.setup_cute_effects()
        
    def setup_main_window(self):
        """Configure the main window with cute Kurumi aesthetics 💖"""
        self.root.title("💖 Kurumi's Magnificent Seven Stock Analysis 💖")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Cute Kurumi dark theme background
        self.root.configure(bg='#0D0B1F')  # Deep dark purple-black
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
            
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_styles(self):
        """Create cute Kurumi-inspired custom styles 🎨"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cute Kurumi color palette 💖
        self.colors = {
            'kurumi_primary': '#8B0000',    # Deep crimson red
            'kurumi_secondary': '#4B0000',  # Darker red  
            'kurumi_accent': '#FF6B6B',     # Soft pink-red
            'kurumi_gold': '#FFD700',       # Elegant gold
            'kurumi_dark': '#0D0B1F',       # Deep dark purple-black
            'kurumi_light': '#1A1A2E',      # Dark blue-purple
            'kurumi_text': '#F8F8FF',       # Ghost white
            'kurumi_shadow': '#2E0016'      # Dark shadow
        }
        
        # Configure cute root theme
        self.style.configure('TFrame', background=self.colors['kurumi_dark'])
        self.style.configure('TLabel', background=self.colors['kurumi_dark'], 
                           foreground=self.colors['kurumi_text'])
        self.style.configure('TLabelFrame', background=self.colors['kurumi_dark'],
                           foreground=self.colors['kurumi_gold'])
        self.style.configure('TLabelFrame.Label', background=self.colors['kurumi_dark'],
                           foreground=self.colors['kurumi_gold'])
        
        # Cute Kurumi button styles 💖
        self.style.configure('Kurumi.Primary.TButton',
                           background=self.colors['kurumi_primary'],
                           foreground=self.colors['kurumi_text'],
                           borderwidth=2,
                           relief='raised',
                           focuscolor=self.colors['kurumi_accent'])
        
        self.style.map('Kurumi.Primary.TButton',
                      background=[('active', self.colors['kurumi_accent']),
                                ('pressed', self.colors['kurumi_secondary'])])
        
        self.style.configure('Kurumi.Gold.TButton',
                           background=self.colors['kurumi_gold'], 
                           foreground=self.colors['kurumi_dark'],
                           borderwidth=2,
                           relief='raised',
                           focuscolor=self.colors['kurumi_accent'])
        
        self.style.map('Kurumi.Gold.TButton',
                      background=[('active', '#FFFF99'),
                                ('pressed', '#B8860B')])
        
        # Cute notebook (tabs) styling
        self.style.configure('TNotebook', background=self.colors['kurumi_dark'],
                           borderwidth=0)
        self.style.configure('TNotebook.Tab', 
                           background=self.colors['kurumi_light'],
                           foreground=self.colors['kurumi_text'],
                           padding=[20, 10],
                           borderwidth=1)
        self.style.map('TNotebook.Tab',
                      background=[('selected', self.colors['kurumi_primary']),
                                ('active', self.colors['kurumi_accent'])])
        
        # Cute treeview styling
        self.style.configure('Kurumi.Treeview',
                           background=self.colors['kurumi_light'],
                           foreground=self.colors['kurumi_text'],
                           fieldbackground=self.colors['kurumi_light'],
                           borderwidth=1,
                           relief='solid')
        self.style.configure('Kurumi.Treeview.Heading',
                           background=self.colors['kurumi_primary'],
                           foreground=self.colors['kurumi_text'],
                           relief='raised',
                           borderwidth=1)
        
        # Cute combobox styling  
        self.style.configure('Kurumi.TCombobox',
                           fieldbackground=self.colors['kurumi_light'],
                           background=self.colors['kurumi_primary'],
                           foreground=self.colors['kurumi_text'])
        
        # Cute progress bar styling
        self.style.configure('Kurumi.Horizontal.TProgressbar',
                           background=self.colors['kurumi_primary'],
                           troughcolor=self.colors['kurumi_light'],
                           borderwidth=1,
                           lightcolor=self.colors['kurumi_accent'],
                           darkcolor=self.colors['kurumi_secondary'])
        
        # Cute scrollbar styling
        self.style.configure('Kurumi.Vertical.TScrollbar',
                           background=self.colors['kurumi_light'],
                           troughcolor=self.colors['kurumi_dark'],
                           borderwidth=1,
                           arrowcolor=self.colors['kurumi_text'])
        self.style.configure('Kurumi.Horizontal.TScrollbar',
                           background=self.colors['kurumi_light'],
                           troughcolor=self.colors['kurumi_dark'],
                           borderwidth=1,
                           arrowcolor=self.colors['kurumi_text'])
        
    def create_widgets(self):
        """Create all GUI widgets with cute styling 💖"""
        # Create main frame with cute Kurumi styling
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Cute Kurumi title with adorable styling
        self.create_title_section(main_frame)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tab components
        self.stock_data_tab = StockDataTab(self.notebook, self)
        self.recommendations_tab = RecommendationsTab(self.notebook, self)
        self.analysis_tab = IndividualAnalysisTab(self.notebook, self)
        
        # Add charts tab if available
        self.charts_frame = None
        if CHARTS_AVAILABLE:
            self.charts_frame = StockChartsFrame(self.notebook)
        
        self.settings_tab = SettingsTab(self.notebook, self)
        
        # Cute status bar
        self.create_status_bar(main_frame)
        
    def create_title_section(self, parent):
        """Create the cute title section"""
        title_frame = ttk.Frame(parent)
        title_frame.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(title_frame, 
                              text="💖 Kurumi's Magnificent Seven Analysis 💖",
                              font=('Arial', 20, 'bold'),
                              foreground=self.colors['kurumi_gold'])
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(title_frame,
                                 text="Time and stocks... both are precious! ✨",
                                 font=('Arial', 12, 'italic'),
                                 foreground=self.colors['kurumi_accent'])
        subtitle_label.grid(row=1, column=0, pady=(5, 0))
        
        
        
        
        
    def create_status_bar(self, parent):
        """Create status bar"""
        self.status_var = tk.StringVar()
        self.status_var.set("準備完了ですわ... くるみの時間操作で素晴らしい投資をお見せいたします ✨🕰️")
        
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.grid_columnconfigure(0, weight=1)
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Kurumi mystical progress indicator
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate',
                                       style='Kurumi.Horizontal.TProgressbar')
        self.progress.grid(row=0, column=1, padx=(10, 0))
        
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        self.root.update()
        
    def show_progress(self):
        """Show progress bar"""
        self.progress.start()
        
    def hide_progress(self):
        """Hide progress bar and stop animations"""
        self.progress.stop()
        self.animation_running = False
        
    def get_all_stocks_data(self):
        """Get data for all stocks in a separate thread"""
        def fetch_data():
            try:
                self.update_status("時の力で株式データを収集中ですわ... さあ、始まりましょう 📊🌙")
                self.show_progress()
                
                data = self.stock_crawler.get_all_stocks_data()
                self.current_stock_data = data
                
                # Update UI in main thread
                self.root.after(0, self.update_stock_display, data)
                self.root.after(0, self.update_status, "株式データ収集完了！ 素晴らしいデータですわね～ ✨📊")
                self.root.after(0, self.hide_progress)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"Error fetching stock data: {str(e)}")
                self.root.after(0, self.update_status, "株式データの読み込みエラー ⚠️")
                self.root.after(0, self.hide_progress)
        
        threading.Thread(target=fetch_data, daemon=True).start()
        self.animate_loading_text("時の魔法でデータ収集中...")
        
    def get_single_stock_data(self):
        """Get data for a single selected stock"""
        symbol = self.stock_var.get()
        if not symbol:
            messagebox.showwarning("Warning", "Please select a stock symbol")
            return
            
        def fetch_data():
            try:
                self.update_status(f"Fetching {symbol} data...")
                self.show_progress()
                
                data = self.stock_crawler.get_stock_data(symbol)
                if data:
                    single_data = {symbol: data}
                    self.current_stock_data.update(single_data)
                    self.root.after(0, self.update_single_stock_display, symbol, data)
                else:
                    self.root.after(0, self.show_error, f"Failed to fetch data for {symbol}")
                
                self.root.after(0, self.update_status, f"{symbol} data loaded")
                self.root.after(0, self.hide_progress)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"Error fetching {symbol} data: {str(e)}")
                self.root.after(0, self.hide_progress)
        
        threading.Thread(target=fetch_data, daemon=True).start()
        
    def refresh_stock_data(self):
        """Refresh current stock data"""
        if self.current_stock_data:
            self.get_all_stocks_data()
        else:
            messagebox.showinfo("Info", "No data to refresh. Please fetch stock data first.")
            
    def update_stock_display(self, data):
        """Update the stock data treeview"""
        # Clear existing data
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
            
        # Add new data
        for symbol, stock_data in data.items():
            if stock_data:  # Check if data is not None
                self.stock_tree.insert('', 'end', values=(
                    stock_data.get('symbol', ''),
                    stock_data.get('company', ''),
                    stock_data.get('current_price', ''),
                    stock_data.get('change', ''),
                    stock_data.get('change_percent', ''),
                    stock_data.get('market_cap', ''),
                    stock_data.get('volume', '')
                ))
                
    def update_single_stock_display(self, symbol, data):
        """Update display with single stock data"""
        # Remove existing entry for this symbol
        for item in self.stock_tree.get_children():
            if self.stock_tree.item(item, 'values')[0] == symbol:
                self.stock_tree.delete(item)
                break
                
        # Add updated data
        self.stock_tree.insert('', 'end', values=(
            data.get('symbol', ''),
            data.get('company', ''),
            data.get('current_price', ''),
            data.get('change', ''),
            data.get('change_percent', ''),
            data.get('market_cap', ''),
            data.get('volume', '')
        ))
        
    def generate_advanced_recommendations(self):
        """Generate advanced multi-criteria recommendations"""
        def generate():
            try:
                self.update_status("Generating Advanced AI Analysis with Multiple Investment Criteria...")
                self.show_progress()
                
                results = self.recommendation_engine.analyze_all_magnificent_seven(use_advanced=True)
                report = self.recommendation_engine.generate_investment_report(results)
                self.current_recommendations = results
                
                self.root.after(0, self.update_recommendations_display, report)
                
                # Update charts with real data if available
                if CHARTS_AVAILABLE and hasattr(self, 'charts_frame'):
                    self.root.after(0, self.charts_frame.update_with_real_data, results)
                
                self.root.after(0, self.update_status, "Advanced analysis completed successfully")
                self.root.after(0, self.hide_progress)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"Error generating advanced recommendations: {str(e)}")
                self.root.after(0, self.update_status, "Error generating advanced analysis")
                self.root.after(0, self.hide_progress)
        
        threading.Thread(target=generate, daemon=True).start()
    
    def generate_basic_recommendations(self):
        """Generate basic recommendations (legacy mode)"""
        def generate():
            try:
                self.update_status("Generating Basic AI Analysis...")
                self.show_progress()
                
                results = self.recommendation_engine.analyze_all_magnificent_seven(use_advanced=False)
                report = self.recommendation_engine.generate_investment_report(results)
                self.current_recommendations = results
                
                self.root.after(0, self.update_recommendations_display, report)
                
                # Update charts with real data if available
                if CHARTS_AVAILABLE and hasattr(self, 'charts_frame'):
                    self.root.after(0, self.charts_frame.update_with_real_data, results)
                
                self.root.after(0, self.update_status, "Basic analysis completed successfully")
                self.root.after(0, self.hide_progress)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"Error generating basic recommendations: {str(e)}")
                self.root.after(0, self.update_status, "Error generating basic analysis")
                self.root.after(0, self.hide_progress)
        
        threading.Thread(target=generate, daemon=True).start()
        
    def generate_all_recommendations(self):
        """Legacy method - redirect to advanced analysis"""
        self.generate_advanced_recommendations()
        
    def update_recommendations_display(self, report):
        """Update the recommendations text display"""
        self.recommendations_text.delete(1.0, tk.END)
        self.recommendations_text.insert(1.0, report)
        
    def analyze_individual_stock_advanced(self):
        """Analyze individual stock with advanced multi-criteria analysis"""
        symbol = self.analysis_stock_var.get()
        if not symbol:
            messagebox.showwarning("ご注意", "分析対象の株式をお選びくださいませ 💎")
            return
            
        def analyze():
            try:
                self.update_status(f"Performing Advanced Analysis on {symbol}...")
                self.show_progress()
                
                analysis = self.recommendation_engine.analyze_single_stock(symbol, use_advanced=True)
                
                if 'error' in analysis:
                    self.root.after(0, self.show_error, analysis['error'])
                else:
                    self.root.after(0, self.update_individual_analysis_display, analysis, True)
                
                self.root.after(0, self.update_status, f"{symbol} advanced analysis completed")
                self.root.after(0, self.hide_progress)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"{symbol} 分析エラー: {str(e)} 💔")
                self.root.after(0, self.hide_progress)
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def analyze_individual_stock_basic(self):
        """Analyze individual stock with basic analysis"""
        symbol = self.analysis_stock_var.get()
        if not symbol:
            messagebox.showwarning("ご注意", "分析対象の株式をお選びくださいませ 💎")
            return
            
        def analyze():
            try:
                self.update_status(f"Performing Basic Analysis on {symbol}...")
                self.show_progress()
                
                analysis = self.recommendation_engine.analyze_single_stock(symbol, use_advanced=False)
                
                if 'error' in analysis:
                    self.root.after(0, self.show_error, analysis['error'])
                else:
                    self.root.after(0, self.update_individual_analysis_display, analysis, False)
                
                self.root.after(0, self.update_status, f"{symbol} basic analysis completed")
                self.root.after(0, self.hide_progress)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"{symbol} 分析エラー: {str(e)} 💔")
                self.root.after(0, self.hide_progress)
        
        threading.Thread(target=analyze, daemon=True).start()
        
    def analyze_individual_stock(self):
        """Legacy method - redirect to advanced analysis"""
        self.analyze_individual_stock_advanced()
        
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
        
        text = f"""ADVANCED STOCK ANALYSIS: {analysis['symbol']} - {analysis['company']}
Analysis Type: Multi-Criteria Investment Analysis
Overall Score: {analysis['overall_score']}
Recommendation: {analysis['recommendation']}
Confidence Level: {analysis['confidence']}

FUNDAMENTAL ANALYSIS:
Financial Health: {detailed['fundamental_analysis']['financial_health']['rating']} (Score: {detailed['fundamental_analysis']['financial_health']['score']:.2f})
Profitability: {detailed['fundamental_analysis']['profitability_metrics']['margin_rating']}
   - {detailed['fundamental_analysis']['profitability_metrics']['analysis']}
Debt Analysis: {detailed['fundamental_analysis']['debt_analysis']['rating']}
   - D/E Ratio: {detailed['fundamental_analysis']['debt_analysis']['debt_to_equity']:.2f}

GROWTH ANALYSIS:
Growth Rating: {detailed['growth_analysis']['rating']}
Historical Growth: {detailed['growth_analysis']['revenue_growth_5y']:.1%} (5-year CAGR)
Industry: {detailed['growth_analysis']['industry']} (Growth Factor: {detailed['growth_analysis']['industry_factor']:.1f}x)

COMPETITIVE POSITION: {detailed['competitive_analysis']['position_strength']}
Key Advantages:"""

        for advantage in detailed['competitive_analysis']['advantages'][:3]:
            text += f"\n   - {advantage}"

        text += f"""

RISK ASSESSMENT: {detailed['risk_assessment']['risk_level']} Risk
Safety Score: {detailed['risk_assessment']['safety_score']:.2f}
Key Risk Factors:"""

        for risk in detailed['risk_assessment']['risk_factors'][:2]:
            text += f"\n   - {risk}"

        if investment_summary:
            text += f"""

INVESTMENT SUMMARY:
Investment Thesis: {investment_summary.get('investment_thesis', 'N/A')}
Price Target: {investment_summary.get('price_target_range', 'N/A')}
Time Horizon: {investment_summary.get('time_horizon', 'N/A')}"""

        text += f"""

Analysis Timestamp: {analysis['timestamp']}

DISCLAIMER: This advanced analysis is for educational 
   and informational purposes only. Not financial advice. Always conduct 
   your own research and consult qualified financial advisors!
"""
        return text
    
    def _format_basic_analysis_display(self, analysis):
        """Format basic analysis for display"""
        breakdown = analysis.get('analysis_breakdown', {})
        
        text = f"""BASIC STOCK ANALYSIS: {analysis['symbol']} - {analysis['company']}
Analysis Type: Basic Technical Analysis
Overall Score: {analysis['overall_score']}
Recommendation: {analysis['recommendation']}
Confidence Level: {analysis['confidence']}

ANALYSIS BREAKDOWN:"""

        if 'momentum' in breakdown:
            text += f"""

Price Momentum:
   Score: {breakdown['momentum']['score']}
   {breakdown['momentum']['analysis']}"""

        if 'volume' in breakdown:
            text += f"""

Volume Analysis:
   Score: {breakdown['volume']['score']}
   {breakdown['volume']['analysis']}"""

        if 'market_cap' in breakdown:
            text += f"""

Market Capitalization:
   Score: {breakdown['market_cap']['score']}
   {breakdown['market_cap']['analysis']}"""

        if 'volatility' in breakdown:
            text += f"""

Volatility Assessment:
   Score: {breakdown['volatility']['score']}
   {breakdown['volatility']['analysis']}"""

        if 'value' in breakdown:
            text += f"""

Value Proposition:
   Score: {breakdown['value']['score']}
   {breakdown['value']['analysis']}"""

        text += f"""

Analysis Timestamp: {analysis['timestamp']}

DISCLAIMER: This basic analysis is for educational purposes only.
   Not financial advice. Always do your own research!
"""
        return text
        
    def export_report(self):
        """Export recommendations report"""
        if not hasattr(self, 'current_recommendations') or not self.current_recommendations:
            messagebox.showwarning("Warning", "No recommendations to export. Generate recommendations first.")
            return
            
        from tkinter.filedialog import asksaveasfilename
        
        filename = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Recommendations Report"
        )
        
        if filename:
            try:
                report = self.recommendation_engine.generate_investment_report(self.current_recommendations)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                messagebox.showinfo("Success", f"Report saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {str(e)}")
                
    def save_settings(self):
        """Save application settings"""
        try:
            delay = int(self.delay_var.get())
            # Update engines with new delay
            self.recommendation_engine.close()
            self.stock_crawler.close()
            
            self.recommendation_engine = RecommendationEngine(delay=delay)
            self.stock_crawler = StockCrawler(delay=delay)
            
            messagebox.showinfo("Success", "Settings saved successfully")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid delay value")
            
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
        
    def on_closing(self):
        """Handle application closing"""
        try:
            self.recommendation_engine.close()
            self.stock_crawler.close()
        except:
            pass
        self.root.destroy()
        
    def setup_kurumi_effects(self):
        """Setup Kurumi-style special effects and animations"""
        # Create floating clock animation variables
        self.clock_angle = 0
        self.loading_dots = 0
        self.mystical_quotes = [
            "時はすべての市場の秘密を明かしますわ... 🕐",
            "影の中にこそ、真の投資機会が隠れているのです 🌙",
            "優雅な投資は忍耐と知恵で花開きますの 🌹",
            "市場の鼓動が時を越えて響きます... 私の魂のように ✨",
            "精霊でさえ良いポートフォリオ助言が必要ですわ ♪",
            "最高の投資助言を差し上げましょう... あら、あら、あら 🌙🖤",
            "時の精霊くるみが、あなたの財産をお守りいたします 🕰️✨",
            "市場のダンスは美しい... でも私のダンスの方がもっと美しいですわ 💃",
            "短期で利益を求めるのは愚かです... 時間こそが真の財宝 ⏳",
            "くふふ... この結果を見て、私の力に驚くでしょう？ 😏🌹"
        ]
        self.current_quote = 0
        
    def animate_loading_text(self, base_text):
        """Animate loading text with Kurumi flair"""
        if self.animation_running:
            return
            
        self.animation_running = True
        
        def animate():
            dots_cycle = ["", "✦", "✦✦", "✦✦✦", "✨"]
            cycle_count = 0
            
            while self.progress['mode'] == 'indeterminate' and cycle_count < 20:
                for dots in dots_cycle:
                    if not self.animation_running:
                        return
                    self.status_var.set(f"▶️ {base_text}{dots}")
                    self.root.update()
                    self.root.after(300)
                cycle_count += 1
                
            self.animation_running = False
            
        threading.Thread(target=animate, daemon=True).start()
        
    def show_mystical_quote(self):
        """Show a rotating mystical quote in status bar"""
        quote = self.mystical_quotes[self.current_quote]
        self.status_var.set(quote)
        self.current_quote = (self.current_quote + 1) % len(self.mystical_quotes)
        # Schedule next quote change
        self.root.after(8000, self.show_mystical_quote)
        
    def add_kurumi_charm(self, widget, hover_color):
        """Add hover effects to widgets"""
        original_bg = widget.cget('background') if hasattr(widget, 'cget') else None
        
        def on_enter(event):
            try:
                widget.config(background=hover_color)
            except:
                pass
                
        def on_leave(event):
            try:
                if original_bg:
                    widget.config(background=original_bg)
            except:
                pass
                
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
        
    def run(self):
        """Run the GUI application with Kurumi magic"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Start the mystical quote rotation
        self.root.after(3000, self.show_mystical_quote)
        self.root.mainloop()


def main():
    """Main function to run the GUI application"""
    app = StockAnalysisGUI()
    app.run()


if __name__ == "__main__":
    main()