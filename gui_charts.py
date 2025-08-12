"""
Chart visualization components for the GUI application
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from config import MAGNIFICENT_SEVEN


class StockChartsFrame:
    """Chart visualization frame for stock data"""
    
    def __init__(self, parent_notebook):
        self.parent = parent_notebook
        self.create_charts_tab()
        
        # Color scheme
        self.colors = {
            'strong_buy': '#22C55E',    # Green
            'buy': '#3B82F6',          # Blue  
            'hold': '#F59E0B',         # Yellow
            'weak_hold': '#EF4444',    # Orange-Red
            'avoid': '#DC2626'         # Red
        }
        
    def create_charts_tab(self):
        """Create the charts tab"""
        self.charts_frame = ttk.Frame(self.parent, padding="10")
        self.parent.add(self.charts_frame, text="📈 Charts")
        
        # Configure grid
        self.charts_frame.grid_rowconfigure(1, weight=1)
        self.charts_frame.grid_columnconfigure(0, weight=1)
        
        # Control frame
        control_frame = ttk.LabelFrame(self.charts_frame, text="Chart Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="📊 Stock Scores Chart",
                  command=self.create_scores_chart).grid(row=0, column=0, padx=(0, 10))
                  
        ttk.Button(control_frame, text="🥧 Recommendation Pie Chart", 
                  command=self.create_recommendation_pie_chart).grid(row=0, column=1, padx=(0, 10))
                  
        ttk.Button(control_frame, text="📈 Market Cap Comparison",
                  command=self.create_market_cap_chart).grid(row=0, column=2)
        
        # Chart display frame
        self.chart_display_frame = ttk.LabelFrame(self.charts_frame, text="Charts", padding="10")
        self.chart_display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.chart_display_frame.grid_rowconfigure(0, weight=1)
        self.chart_display_frame.grid_columnconfigure(0, weight=1)
        
        # Placeholder for charts
        self.current_canvas = None
        self.create_placeholder_chart()
        
    def create_placeholder_chart(self):
        """Create placeholder chart"""
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.text(0.5, 0.5, '📊 Select a chart type from the controls above\nto visualize stock analysis data', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=14, alpha=0.7)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1) 
        ax.axis('off')
        
        self.display_chart(fig)
        
    def display_chart(self, fig):
        """Display a matplotlib figure in the GUI"""
        if self.current_canvas:
            self.current_canvas.destroy()
            
        self.current_canvas = FigureCanvasTkAgg(fig, self.chart_display_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def create_scores_chart(self):
        """Create bar chart of stock analysis scores"""
        # This would typically use real data from the main app
        # For now, create sample data
        symbols = list(MAGNIFICENT_SEVEN.keys())
        scores = np.random.uniform(0.3, 0.9, len(symbols))  # Sample scores
        
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Create color map based on scores
        colors = []
        for score in scores:
            if score >= 0.8:
                colors.append(self.colors['strong_buy'])
            elif score >= 0.65:
                colors.append(self.colors['buy'])
            elif score >= 0.5:
                colors.append(self.colors['hold'])
            elif score >= 0.35:
                colors.append(self.colors['weak_hold'])
            else:
                colors.append(self.colors['avoid'])
        
        bars = ax.bar(symbols, scores, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
        
        # Customize chart
        ax.set_title('📊 Magnificent Seven - Analysis Scores', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Stock Symbols', fontsize=12, fontweight='bold')
        ax.set_ylabel('Analysis Score', fontsize=12, fontweight='bold')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Add legend
        legend_elements = [
            plt.Rectangle((0,0),1,1, facecolor=self.colors['strong_buy'], label='🟢 Strong Buy (≥0.8)'),
            plt.Rectangle((0,0),1,1, facecolor=self.colors['buy'], label='🔵 Buy (≥0.65)'),
            plt.Rectangle((0,0),1,1, facecolor=self.colors['hold'], label='🟡 Hold (≥0.5)'),
            plt.Rectangle((0,0),1,1, facecolor=self.colors['weak_hold'], label='🟠 Weak Hold (≥0.35)'),
            plt.Rectangle((0,0),1,1, facecolor=self.colors['avoid'], label='🔴 Avoid (<0.35)')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
        
        plt.tight_layout()
        self.display_chart(fig)
        
    def create_recommendation_pie_chart(self):
        """Create pie chart of recommendation distribution"""
        # Sample data - in real app this would come from actual analysis
        recommendations = ['Strong Buy', 'Buy', 'Hold', 'Weak Hold', 'Avoid']
        counts = [3, 2, 1, 1, 0]  # Sample distribution
        colors = [self.colors['strong_buy'], self.colors['buy'], self.colors['hold'], 
                 self.colors['weak_hold'], self.colors['avoid']]
        
        # Filter out zero values
        filtered_data = [(rec, count, color) for rec, count, color in zip(recommendations, counts, colors) if count > 0]
        recommendations, counts, colors = zip(*filtered_data) if filtered_data else ([], [], [])
        
        if not counts:
            # Show empty state
            fig = Figure(figsize=(12, 6), dpi=100)
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, '🥧 No recommendation data available\nGenerate recommendations first', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=14, alpha=0.7)
            ax.axis('off')
            self.display_chart(fig)
            return
        
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(counts, labels=recommendations, colors=colors, 
                                         autopct='%1.1f%%', startangle=90,
                                         explode=[0.05] * len(counts))
        
        # Enhance text
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        ax.set_title('🥧 Recommendation Distribution - Magnificent Seven', 
                    fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        self.display_chart(fig)
        
    def create_market_cap_chart(self):
        """Create market cap comparison chart"""
        # Sample market cap data (in trillions)
        symbols = list(MAGNIFICENT_SEVEN.keys())
        market_caps = [2.9, 2.8, 1.6, 1.4, 1.8, 0.8, 0.7]  # Sample data in trillions
        
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Create horizontal bar chart
        bars = ax.barh(symbols, market_caps, color='skyblue', alpha=0.8, edgecolor='navy')
        
        ax.set_title('📈 Market Capitalization Comparison', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Market Cap (Trillions USD)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Stock Symbols', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for bar, cap in zip(bars, market_caps):
            width = bar.get_width()
            ax.text(width + 0.05, bar.get_y() + bar.get_height()/2,
                   f'${cap:.1f}T', ha='left', va='center', fontweight='bold')
        
        # Set x-axis limit
        ax.set_xlim(0, max(market_caps) * 1.2)
        
        plt.tight_layout()
        self.display_chart(fig)
        
    def update_with_real_data(self, analysis_data):
        """Update charts with real analysis data"""
        # This method would be called by the main app to update charts with real data
        if not analysis_data or 'ranked_recommendations' not in analysis_data:
            return
            
        # Extract data for charts
        stocks = analysis_data['ranked_recommendations']
        symbols = [stock['symbol'] for stock in stocks]
        scores = [stock['overall_score'] for stock in stocks]
        
        # Update scores chart with real data
        self.create_real_scores_chart(symbols, scores)
        
    def create_real_scores_chart(self, symbols, scores):
        """Create scores chart with real data"""
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Create color map based on scores
        colors = []
        for score in scores:
            if score >= 0.8:
                colors.append(self.colors['strong_buy'])
            elif score >= 0.65:
                colors.append(self.colors['buy'])
            elif score >= 0.5:
                colors.append(self.colors['hold'])
            elif score >= 0.35:
                colors.append(self.colors['weak_hold'])
            else:
                colors.append(self.colors['avoid'])
        
        bars = ax.bar(symbols, scores, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
        
        # Customize chart
        ax.set_title('📊 Magnificent Seven - Real-Time Analysis Scores', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Stock Symbols', fontsize=12, fontweight='bold')
        ax.set_ylabel('Analysis Score', fontsize=12, fontweight='bold')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Add legend
        legend_elements = [
            plt.Rectangle((0,0),1,1, facecolor=self.colors['strong_buy'], label='🟢 Strong Buy (≥0.8)'),
            plt.Rectangle((0,0),1,1, facecolor=self.colors['buy'], label='🔵 Buy (≥0.65)'),
            plt.Rectangle((0,0),1,1, facecolor=self.colors['hold'], label='🟡 Hold (≥0.5)'),
            plt.Rectangle((0,0),1,1, facecolor=self.colors['weak_hold'], label='🟠 Weak Hold (≥0.35)'),
            plt.Rectangle((0,0),1,1, facecolor=self.colors['avoid'], label='🔴 Avoid (<0.35)')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
        
        plt.tight_layout()
        self.display_chart(fig)