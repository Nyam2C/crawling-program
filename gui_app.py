#!/usr/bin/env python3
"""
Magnificent Seven Stock Analysis - Windows GUI Application
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
from datetime import datetime
from recommendation_engine import RecommendationEngine
from stock_crawler import StockCrawler
from config import MAGNIFICENT_SEVEN

# Try to import charts module
try:
    from gui_charts import StockChartsFrame
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False
    print("Charts module not available. Install matplotlib for chart functionality.")


class StockAnalysisGUI:
    """Main GUI application for stock analysis and recommendations"""
    
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
        
    def setup_main_window(self):
        """Configure the main window"""
        self.root.title("🚀 Magnificent Seven Stock Analysis & Recommendation System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")  # Add icon file if available
        except:
            pass
            
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_styles(self):
        """Create custom styles for the application"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom colors
        self.colors = {
            'primary': '#2E86AB',      # Blue
            'success': '#A23B72',      # Green
            'warning': '#F18F01',      # Orange  
            'danger': '#C73E1D',       # Red
            'dark': '#2D3748',         # Dark gray
            'light': '#F7FAFC',        # Light gray
            'white': '#FFFFFF'
        }
        
        # Custom button styles
        self.style.configure('Primary.TButton',
                           background=self.colors['primary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none')
        
        self.style.configure('Success.TButton',
                           background=self.colors['success'], 
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none')
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, 
                              text="🚀 Magnificent Seven Stock Analysis System",
                              font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_stock_data_tab()
        self.create_recommendations_tab()
        self.create_individual_analysis_tab()
        
        # Add charts tab if available
        if CHARTS_AVAILABLE:
            self.charts_frame = StockChartsFrame(self.notebook)
        
        self.create_settings_tab()
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_stock_data_tab(self):
        """Create the stock data tab"""
        # Stock Data Frame
        stock_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(stock_frame, text="📊 Stock Data")
        
        # Configure grid
        stock_frame.grid_rowconfigure(1, weight=1)
        stock_frame.grid_columnconfigure(1, weight=1)
        
        # Control panel
        control_frame = ttk.LabelFrame(stock_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="📊 Get All Stock Data", 
                  command=self.get_all_stocks_data,
                  style='Primary.TButton').grid(row=0, column=0, padx=(0, 10))
                  
        ttk.Button(control_frame, text="🔄 Refresh Data",
                  command=self.refresh_stock_data,
                  style='Success.TButton').grid(row=0, column=1, padx=(0, 10))
        
        # Stock selection
        ttk.Label(control_frame, text="Select Stock:").grid(row=0, column=2, padx=(20, 5))
        self.stock_var = tk.StringVar()
        stock_combo = ttk.Combobox(control_frame, textvariable=self.stock_var, 
                                  values=list(MAGNIFICENT_SEVEN.keys()), 
                                  state='readonly', width=10)
        stock_combo.grid(row=0, column=3, padx=(0, 10))
        
        ttk.Button(control_frame, text="🎯 Get Single Stock",
                  command=self.get_single_stock_data).grid(row=0, column=4)
        
        # Stock data display
        data_frame = ttk.LabelFrame(stock_frame, text="Stock Information", padding="10")
        data_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        data_frame.grid_rowconfigure(0, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview for stock data
        columns = ('Symbol', 'Company', 'Price', 'Change', 'Change %', 'Market Cap', 'Volume')
        self.stock_tree = ttk.Treeview(data_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.stock_tree.heading(col, text=col)
            self.stock_tree.column(col, width=120)
        
        # Scrollbars for treeview
        stock_scrollbar_y = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.stock_tree.yview)
        stock_scrollbar_x = ttk.Scrollbar(data_frame, orient=tk.HORIZONTAL, command=self.stock_tree.xview)
        self.stock_tree.configure(yscrollcommand=stock_scrollbar_y.set, xscrollcommand=stock_scrollbar_x.set)
        
        self.stock_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        stock_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        stock_scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def create_recommendations_tab(self):
        """Create the recommendations tab"""
        rec_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(rec_frame, text="💡 Recommendations")
        
        # Configure grid
        rec_frame.grid_rowconfigure(1, weight=1)
        rec_frame.grid_columnconfigure(0, weight=1)
        
        # Control panel
        rec_control_frame = ttk.LabelFrame(rec_frame, text="Generate Recommendations", padding="10")
        rec_control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(rec_control_frame, text="🤖 Generate All Recommendations",
                  command=self.generate_all_recommendations,
                  style='Success.TButton').grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(rec_control_frame, text="📋 Export Report",
                  command=self.export_report).grid(row=0, column=1)
        
        # Recommendations display
        rec_display_frame = ttk.LabelFrame(rec_frame, text="Investment Recommendations", padding="10")
        rec_display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        rec_display_frame.grid_rowconfigure(0, weight=1)
        rec_display_frame.grid_columnconfigure(0, weight=1)
        
        # Text widget for recommendations report
        self.recommendations_text = scrolledtext.ScrolledText(rec_display_frame, 
                                                             wrap=tk.WORD, 
                                                             height=25,
                                                             font=('Consolas', 10))
        self.recommendations_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def create_individual_analysis_tab(self):
        """Create the individual stock analysis tab"""
        analysis_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(analysis_frame, text="🔍 Individual Analysis")
        
        # Configure grid
        analysis_frame.grid_rowconfigure(2, weight=1)
        analysis_frame.grid_columnconfigure(1, weight=1)
        
        # Stock selection
        select_frame = ttk.LabelFrame(analysis_frame, text="Select Stock for Analysis", padding="10")
        select_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(select_frame, text="Stock Symbol:").grid(row=0, column=0, padx=(0, 10))
        self.analysis_stock_var = tk.StringVar()
        analysis_combo = ttk.Combobox(select_frame, textvariable=self.analysis_stock_var,
                                    values=list(MAGNIFICENT_SEVEN.keys()),
                                    state='readonly', width=15)
        analysis_combo.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(select_frame, text="🧮 Analyze Stock",
                  command=self.analyze_individual_stock,
                  style='Primary.TButton').grid(row=0, column=2)
        
        # Analysis results
        results_frame = ttk.LabelFrame(analysis_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Score display
        score_frame = ttk.Frame(results_frame)
        score_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(score_frame, text="Overall Score:").grid(row=0, column=0, padx=(0, 10))
        self.score_label = ttk.Label(score_frame, text="--", font=('Arial', 12, 'bold'))
        self.score_label.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(score_frame, text="Recommendation:").grid(row=0, column=2, padx=(0, 10))
        self.recommendation_label = ttk.Label(score_frame, text="--", font=('Arial', 12, 'bold'))
        self.recommendation_label.grid(row=0, column=3)
        
        # Detailed analysis
        detail_frame = ttk.LabelFrame(analysis_frame, text="Detailed Breakdown", padding="10")
        detail_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        detail_frame.grid_rowconfigure(0, weight=1)
        detail_frame.grid_columnconfigure(0, weight=1)
        
        self.analysis_text = scrolledtext.ScrolledText(detail_frame, wrap=tk.WORD, height=15)
        self.analysis_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # App info
        info_frame = ttk.LabelFrame(settings_frame, text="Application Information", padding="10")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        info_text = """🚀 Magnificent Seven Stock Analysis & Recommendation System
        
Version: 2.0.0
Author: Stock Analysis Team
        
This application provides AI-powered stock analysis and buy recommendations
for the Magnificent Seven technology stocks:
        
🍎 AAPL - Apple Inc.
🖥️ MSFT - Microsoft Corporation  
🔍 GOOGL - Alphabet Inc.
📦 AMZN - Amazon.com Inc.
🎮 NVDA - NVIDIA Corporation
⚡ TSLA - Tesla Inc.
👥 META - Meta Platforms Inc.

⚠️ DISCLAIMER: This tool is for educational purposes only.
Not financial advice. Always do your own research!"""
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.grid(row=0, column=0)
        
        # Settings controls
        controls_frame = ttk.LabelFrame(settings_frame, text="Settings", padding="10")
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(controls_frame, text="Request Delay (seconds):").grid(row=0, column=0, padx=(0, 10))
        self.delay_var = tk.StringVar(value="2")
        delay_spinbox = ttk.Spinbox(controls_frame, from_=1, to=10, textvariable=self.delay_var, width=10)
        delay_spinbox.grid(row=0, column=1)
        
        ttk.Button(controls_frame, text="💾 Save Settings",
                  command=self.save_settings).grid(row=1, column=0, pady=(10, 0))
        
    def create_status_bar(self, parent):
        """Create status bar"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.grid_columnconfigure(0, weight=1)
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=0, column=1, padx=(10, 0))
        
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        self.root.update()
        
    def show_progress(self):
        """Show progress bar"""
        self.progress.start()
        
    def hide_progress(self):
        """Hide progress bar"""
        self.progress.stop()
        
    def get_all_stocks_data(self):
        """Get data for all stocks in a separate thread"""
        def fetch_data():
            try:
                self.update_status("Fetching stock data...")
                self.show_progress()
                
                data = self.stock_crawler.get_all_stocks_data()
                self.current_stock_data = data
                
                # Update UI in main thread
                self.root.after(0, self.update_stock_display, data)
                self.root.after(0, self.update_status, "Stock data loaded successfully")
                self.root.after(0, self.hide_progress)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"Error fetching stock data: {str(e)}")
                self.root.after(0, self.update_status, "Error loading stock data")
                self.root.after(0, self.hide_progress)
        
        threading.Thread(target=fetch_data, daemon=True).start()
        
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
        
    def generate_all_recommendations(self):
        """Generate recommendations for all stocks"""
        def generate():
            try:
                self.update_status("Generating AI recommendations...")
                self.show_progress()
                
                results = self.recommendation_engine.analyze_all_magnificent_seven()
                report = self.recommendation_engine.generate_investment_report(results)
                self.current_recommendations = results
                
                self.root.after(0, self.update_recommendations_display, report)
                
                # Update charts with real data if available
                if CHARTS_AVAILABLE and hasattr(self, 'charts_frame'):
                    self.root.after(0, self.charts_frame.update_with_real_data, results)
                
                self.root.after(0, self.update_status, "Recommendations generated successfully")
                self.root.after(0, self.hide_progress)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"Error generating recommendations: {str(e)}")
                self.root.after(0, self.update_status, "Error generating recommendations")
                self.root.after(0, self.hide_progress)
        
        threading.Thread(target=generate, daemon=True).start()
        
    def update_recommendations_display(self, report):
        """Update the recommendations text display"""
        self.recommendations_text.delete(1.0, tk.END)
        self.recommendations_text.insert(1.0, report)
        
    def analyze_individual_stock(self):
        """Analyze individual stock"""
        symbol = self.analysis_stock_var.get()
        if not symbol:
            messagebox.showwarning("Warning", "Please select a stock symbol")
            return
            
        def analyze():
            try:
                self.update_status(f"Analyzing {symbol}...")
                self.show_progress()
                
                analysis = self.recommendation_engine.analyze_single_stock(symbol)
                
                if 'error' in analysis:
                    self.root.after(0, self.show_error, analysis['error'])
                else:
                    self.root.after(0, self.update_individual_analysis_display, analysis)
                
                self.root.after(0, self.update_status, f"{symbol} analysis completed")
                self.root.after(0, self.hide_progress)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"Error analyzing {symbol}: {str(e)}")
                self.root.after(0, self.hide_progress)
        
        threading.Thread(target=analyze, daemon=True).start()
        
    def update_individual_analysis_display(self, analysis):
        """Update individual analysis display"""
        # Update score and recommendation
        self.score_label.config(text=f"{analysis['overall_score']}")
        self.recommendation_label.config(text=analysis['recommendation'])
        
        # Update detailed analysis
        self.analysis_text.delete(1.0, tk.END)
        
        breakdown = analysis['analysis_breakdown']
        detail_text = f"""Stock Analysis for {analysis['symbol']} - {analysis['company']}
Overall Score: {analysis['overall_score']}
Recommendation: {analysis['recommendation']}
Confidence Level: {analysis['confidence']}

DETAILED BREAKDOWN:
═══════════════════════════════════════════════════════════════

💹 Price Momentum Analysis:
   Score: {breakdown['momentum']['score']}
   {breakdown['momentum']['analysis']}

📊 Volume Analysis:
   Score: {breakdown['volume']['score']}
   {breakdown['volume']['analysis']}

🏢 Market Capitalization:
   Score: {breakdown['market_cap']['score']}
   {breakdown['market_cap']['analysis']}

⚖️ Volatility Assessment:
   Score: {breakdown['volatility']['score']}
   {breakdown['volatility']['analysis']}

💎 Value Proposition:
   Score: {breakdown['value']['score']}
   {breakdown['value']['analysis']}

═══════════════════════════════════════════════════════════════
Analysis Timestamp: {analysis['timestamp']}

⚠️  DISCLAIMER: This analysis is for educational purposes only.
   Not financial advice. Always do your own research!
"""
        
        self.analysis_text.insert(1.0, detail_text)
        
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
        
    def run(self):
        """Run the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    """Main function to run the GUI application"""
    app = StockAnalysisGUI()
    app.run()


if __name__ == "__main__":
    main()