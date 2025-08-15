#!/usr/bin/env python3
"""Investment Analysis Tab Component - Kawaii Style Investment Personality Analysis"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from src.analysis.investment_personality_analyzer import InvestmentPersonalityAnalyzer, PersonalityMetrics
from src.trading.scoreboard_manager import ScoreboardManager
from src.gui.components.dialogs import KawaiiMessageBox


class InvestmentAnalysisTab:
    def __init__(self, notebook, main_app):
        self.notebook = notebook
        self.main_app = main_app
        self.colors = main_app.colors
        
        # Initialize analyzer and scoreboard manager
        self.analyzer = InvestmentPersonalityAnalyzer()
        self.scoreboard_manager = ScoreboardManager()
        self.kawaii_msg = KawaiiMessageBox(self.main_app.root, self.main_app.theme_manager, self.main_app.icon_manager)
        
        # Current analysis data
        self.current_metrics: Optional[PersonalityMetrics] = None
        
        self.setup_tab()
        self.load_analysis()
    
    def setup_tab(self):
        """Create the investment analysis tab"""
        self.frame = ttk.Frame(self.notebook, padding="15")
        icon = self.main_app.icon_manager.get_icon('tab_analysis')
        if icon:
            self.notebook.add(self.frame, text='Investment Analysis', image=icon, compound='left')
        else:
            self.notebook.add(self.frame, text='Investment Analysis')
        
        # Configure grid
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Create header
        self.create_header()
        
        # Create main content
        self.create_main_content()
        
        # Create footer
        self.create_footer()
    
    def create_header(self):
        """Create header section"""
        header_frame = ttk.Frame(self.frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="INVESTMENT PERSONALITY ANALYSIS",
                               font=('Arial', 16, 'bold'),
                               foreground=self.colors['magenta'])
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                  text="Analyze your trading patterns and investment personality",
                                  font=('Arial', 10),
                                  foreground=self.colors['text_muted'])
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 15))
        
        # Controls
        controls_frame = ttk.Frame(header_frame)
        controls_frame.grid(row=2, column=0, columnspan=3, pady=(0, 10))
        
        # Nickname input
        ttk.Label(controls_frame, text="Analyze specific trader:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.nickname_var = tk.StringVar()
        nickname_entry = ttk.Entry(controls_frame, textvariable=self.nickname_var, width=20)
        nickname_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Buttons
        analyze_btn = ttk.Button(controls_frame, text="Analyze Trader",
                               style='Pastel.Primary.TButton',
                               command=self.analyze_specific_trader)
        analyze_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        refresh_btn = ttk.Button(controls_frame, text="Analyze All Records",
                               style='Pastel.Secondary.TButton', 
                               command=self.analyze_all_records)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = ttk.Button(controls_frame, text="Clear",
                             style='Pastel.Ghost.TButton',
                             command=self.clear_analysis)
        clear_btn.pack(side=tk.LEFT)
    
    def create_main_content(self):
        """Create main content area"""
        # Main container
        main_container = ttk.Frame(self.frame)
        main_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # Left panel - Analysis results
        self.create_analysis_panel(main_container)
        
        # Right panel - Visualization
        self.create_visualization_panel(main_container)
    
    def create_analysis_panel(self, parent):
        """Create analysis results panel"""
        analysis_frame = ttk.LabelFrame(parent, text="Personality Analysis", padding="10")
        analysis_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Scrollable content
        canvas = tk.Canvas(analysis_frame, bg=self.colors['bg'])
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=canvas.yview)
        self.analysis_content_frame = ttk.Frame(canvas)
        
        self.analysis_content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.analysis_content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initial message
        self.show_initial_message()
    
    def create_visualization_panel(self, parent):
        """Create visualization panel"""
        viz_frame = ttk.LabelFrame(parent, text="Performance Metrics", padding="10")
        viz_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Matplotlib figure
        self.fig, self.axes = plt.subplots(2, 2, figsize=(8, 6))
        self.fig.patch.set_facecolor(self.colors['bg'])
        
        # Adjust layout
        self.fig.tight_layout(pad=3.0)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initial empty charts
        self.clear_charts()
    
    def create_footer(self):
        """Create footer with additional info"""
        footer_frame = ttk.Frame(self.frame)
        footer_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        
        # Last updated
        self.last_updated_label = ttk.Label(footer_frame, 
                                           text="Ready for analysis",
                                           foreground=self.colors['text_muted'],
                                           font=('Arial', 9))
        self.last_updated_label.pack(side=tk.LEFT)
        
        # Stats
        self.stats_label = ttk.Label(footer_frame,
                                    text="",
                                    foreground=self.colors['text_muted'],
                                    font=('Arial', 9))
        self.stats_label.pack(side=tk.RIGHT)
    
    def show_initial_message(self):
        """Show initial message when no analysis is loaded"""
        # Clear existing content
        for widget in self.analysis_content_frame.winfo_children():
            widget.destroy()
        
        # Welcome message
        welcome_frame = ttk.Frame(self.analysis_content_frame)
        welcome_frame.pack(fill=tk.X, pady=20)
        
        welcome_text = """Welcome to Investment Personality Analysis!

This tool analyzes your trading patterns from scoreboard records to determine:

• Risk Tolerance (Conservative, Moderate, Aggressive)
• Investment Style (Long-term, Short-term, Swing, Day Trading)
• Trading Frequency (Minimal, Moderate, Active, Hyperactive)
• Performance Metrics (Patience, Consistency, Profitability, Discipline)

To get started:
1. Enter a specific trader's nickname and click 'Analyze Trader'
2. Or click 'Analyze All Records' for overall market analysis

Your personality analysis will help you understand your trading behavior and improve your investment strategy!"""
        
        welcome_label = ttk.Label(welcome_frame, text=welcome_text,
                                 font=('Arial', 10),
                                 foreground=self.colors['text'],
                                 justify=tk.LEFT,
                                 wraplength=400)
        welcome_label.pack(anchor=tk.W)
    
    def analyze_specific_trader(self):
        """Analyze specific trader by nickname"""
        nickname = self.nickname_var.get().strip()
        if not nickname:
            self.kawaii_msg.show_warning("No Nickname", 
                                        "Please enter a trader's nickname to analyze.", 
                                        'bow')
            return
        
        # Get records for specific trader
        all_records = self.scoreboard_manager.get_leaderboard(100)  # Get more records
        trader_records = [r for r in all_records if r.nickname.lower() == nickname.lower()]
        
        if not trader_records:
            self.kawaii_msg.show_warning("Trader Not Found", 
                                        f"No records found for trader '{nickname}'.\nPlease check the nickname and try again.", 
                                        'skull')
            return
        
        # Perform analysis
        self.current_metrics = self.analyzer.analyze_personality(trader_records)
        self.display_analysis_results(f"Analysis for {nickname}")
        self.update_visualizations()
        
        # Update footer
        self.last_updated_label.config(text=f"Analyzed: {nickname}")
        self.stats_label.config(text=f"{len(trader_records)} records analyzed")
    
    def analyze_all_records(self):
        """Analyze all trading records"""
        all_records = self.scoreboard_manager.get_leaderboard(100)
        
        if not all_records:
            self.kawaii_msg.show_info("No Data", 
                                     "No trading records found in scoreboard.\nStart trading to generate analysis data!", 
                                     'sparkle')
            return
        
        # Perform analysis on all records
        self.current_metrics = self.analyzer.analyze_personality(all_records)
        self.display_analysis_results("Overall Market Analysis")
        self.update_visualizations()
        
        # Update footer
        self.last_updated_label.config(text="Analyzed: All traders")
        self.stats_label.config(text=f"{len(all_records)} total records")
    
    def clear_analysis(self):
        """Clear current analysis"""
        self.current_metrics = None
        self.nickname_var.set("")
        self.show_initial_message()
        self.clear_charts()
        
        # Update footer
        self.last_updated_label.config(text="Ready for analysis")
        self.stats_label.config(text="")
    
    def display_analysis_results(self, title: str):
        """Display analysis results in the left panel"""
        # Clear existing content
        for widget in self.analysis_content_frame.winfo_children():
            widget.destroy()
        
        if not self.current_metrics:
            self.show_initial_message()
            return
        
        metrics = self.current_metrics
        
        # Title
        title_frame = ttk.Frame(self.analysis_content_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text=title,
                               font=('Arial', 14, 'bold'),
                               foreground=self.colors['magenta'])
        title_label.pack(anchor=tk.W)
        
        # Personality Overview
        overview_frame = ttk.LabelFrame(self.analysis_content_frame, text="Personality Overview", padding="10")
        overview_frame.pack(fill=tk.X, pady=(0, 10))
        
        overview_text = f"""Risk Tolerance: {metrics.risk_tolerance.value}
Investment Style: {metrics.investment_style.value}
Trading Frequency: {metrics.trading_frequency.value}

{metrics.personality_description}"""
        
        overview_label = ttk.Label(overview_frame, text=overview_text,
                                  font=('Arial', 10),
                                  justify=tk.LEFT)
        overview_label.pack(anchor=tk.W)
        
        # Performance Scores
        scores_frame = ttk.LabelFrame(self.analysis_content_frame, text="Performance Scores", padding="10")
        scores_frame.pack(fill=tk.X, pady=(0, 10))
        
        scores_data = [
            ("Patience", metrics.patience_score),
            ("Consistency", metrics.consistency_score),
            ("Profitability", metrics.profitability_score),
            ("Discipline", metrics.discipline_score)
        ]
        
        for i, (label, score) in enumerate(scores_data):
            score_frame = ttk.Frame(scores_frame)
            score_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(score_frame, text=f"{label}:", width=12).pack(side=tk.LEFT)
            
            # Progress bar
            progress = ttk.Progressbar(score_frame, length=150, mode='determinate')
            progress['value'] = score
            progress.pack(side=tk.LEFT, padx=(5, 10))
            
            # Score text
            color = self.colors['mint'] if score >= 70 else self.colors['coral'] if score < 40 else self.colors['text']
            ttk.Label(score_frame, text=f"{score:.1f}%", 
                     foreground=color, font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        # Statistics
        stats_frame = ttk.LabelFrame(self.analysis_content_frame, text="Trading Statistics", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        stats_text = f"""Average Holding Period: {metrics.average_holding_period:.1f} days
Win Rate: {metrics.win_rate:.1f}%
Average Return: {metrics.average_return:.2f}%
Volatility: {metrics.volatility:.2f}%"""
        
        stats_label = ttk.Label(stats_frame, text=stats_text,
                               font=('Arial', 10),
                               justify=tk.LEFT)
        stats_label.pack(anchor=tk.W)
        
        # Strengths
        if metrics.strengths:
            strengths_frame = ttk.LabelFrame(self.analysis_content_frame, text="Strengths", padding="10")
            strengths_frame.pack(fill=tk.X, pady=(0, 10))
            
            for strength in metrics.strengths:
                strength_frame = ttk.Frame(strengths_frame)
                strength_frame.pack(fill=tk.X, pady=1)
                
                ttk.Label(strength_frame, text="• " + strength,
                         font=('Arial', 9),
                         foreground=self.colors['mint'],
                         wraplength=350).pack(anchor=tk.W)
        
        # Weaknesses
        if metrics.weaknesses:
            weaknesses_frame = ttk.LabelFrame(self.analysis_content_frame, text="Areas for Improvement", padding="10")
            weaknesses_frame.pack(fill=tk.X, pady=(0, 10))
            
            for weakness in metrics.weaknesses:
                weakness_frame = ttk.Frame(weaknesses_frame)
                weakness_frame.pack(fill=tk.X, pady=1)
                
                ttk.Label(weakness_frame, text="• " + weakness,
                         font=('Arial', 9),
                         foreground=self.colors['coral'],
                         wraplength=350).pack(anchor=tk.W)
        
        # Recommendations
        if metrics.recommendations:
            recommendations_frame = ttk.LabelFrame(self.analysis_content_frame, text="Recommendations", padding="10")
            recommendations_frame.pack(fill=tk.X, pady=(0, 10))
            
            for recommendation in metrics.recommendations:
                rec_frame = ttk.Frame(recommendations_frame)
                rec_frame.pack(fill=tk.X, pady=1)
                
                ttk.Label(rec_frame, text="• " + recommendation,
                         font=('Arial', 9),
                         foreground=self.colors['text'],
                         wraplength=350).pack(anchor=tk.W)
    
    def update_visualizations(self):
        """Update visualization charts"""
        if not self.current_metrics:
            self.clear_charts()
            return
        
        metrics = self.current_metrics
        
        # Clear all axes
        for ax in self.axes.flat:
            ax.clear()
        
        # Chart 1: Performance Scores Radar
        ax1 = self.axes[0, 0]
        categories = ['Patience', 'Consistency', 'Profitability', 'Discipline']
        values = [metrics.patience_score, metrics.consistency_score, 
                 metrics.profitability_score, metrics.discipline_score]
        
        # Create radar chart
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]  # Close the polygon
        angles += angles[:1]
        
        ax1.plot(angles, values, 'o-', linewidth=2, color=self.colors['magenta'])
        ax1.fill(angles, values, alpha=0.25, color=self.colors['magenta'])
        ax1.set_xticks(angles[:-1])
        ax1.set_xticklabels(categories, fontsize=8)
        ax1.set_ylim(0, 100)
        ax1.set_title('Performance Scores', fontsize=10, fontweight='bold')
        ax1.grid(True)
        
        # Chart 2: Risk vs Return
        ax2 = self.axes[0, 1]
        risk_score = 100 - metrics.consistency_score  # Higher volatility = higher risk
        return_score = metrics.profitability_score
        
        colors_map = {
            'Conservative': self.colors['mint'],
            'Moderate': self.colors['periwinkle'], 
            'Aggressive': self.colors['coral']
        }
        point_color = colors_map.get(metrics.risk_tolerance.value, self.colors['text'])
        
        ax2.scatter([risk_score], [return_score], s=100, c=point_color, alpha=0.7)
        ax2.set_xlabel('Risk Level', fontsize=9)
        ax2.set_ylabel('Return Potential', fontsize=9)
        ax2.set_title('Risk-Return Profile', fontsize=10, fontweight='bold')
        ax2.set_xlim(0, 100)
        ax2.set_ylim(0, 100)
        ax2.grid(True, alpha=0.3)
        
        # Add quadrant labels
        ax2.text(25, 75, 'Low Risk\nHigh Return', ha='center', va='center', fontsize=8, alpha=0.7)
        ax2.text(75, 75, 'High Risk\nHigh Return', ha='center', va='center', fontsize=8, alpha=0.7)
        ax2.text(25, 25, 'Low Risk\nLow Return', ha='center', va='center', fontsize=8, alpha=0.7)
        ax2.text(75, 25, 'High Risk\nLow Return', ha='center', va='center', fontsize=8, alpha=0.7)
        
        # Chart 3: Trading Style Distribution
        ax3 = self.axes[1, 0]
        style_data = {
            'Holding Period': metrics.average_holding_period,
            'Win Rate': metrics.win_rate,
            'Avg Return': max(metrics.average_return + 50, 0)  # Shift to positive
        }
        
        bars = ax3.bar(style_data.keys(), style_data.values(), 
                      color=[self.colors['lavender'], self.colors['mint'], self.colors['coral']])
        ax3.set_title('Trading Characteristics', fontsize=10, fontweight='bold')
        ax3.set_ylabel('Value', fontsize=9)
        
        # Rotate x labels
        plt.setp(ax3.get_xticklabels(), rotation=45, ha='right', fontsize=8)
        
        # Chart 4: Investment Style Breakdown
        ax4 = self.axes[1, 1]
        
        # Create pie chart for personality components
        personality_weights = {
            'Risk Tolerance': (100 - metrics.consistency_score) + 50,  # Risk component
            'Trading Activity': min(metrics.average_holding_period / 10, 50),  # Activity component
            'Performance': (metrics.profitability_score + metrics.discipline_score) / 2  # Performance component
        }
        
        ax4.pie(personality_weights.values(), labels=personality_weights.keys(), 
               autopct='%1.1f%%', startangle=90,
               colors=[self.colors['coral'], self.colors['periwinkle'], self.colors['mint']])
        ax4.set_title('Personality Composition', fontsize=10, fontweight='bold')
        
        # Update canvas
        self.canvas.draw()
    
    def clear_charts(self):
        """Clear all charts"""
        for ax in self.axes.flat:
            ax.clear()
            ax.text(0.5, 0.5, 'No Data\nRun Analysis', 
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=12, alpha=0.5)
            ax.set_xticks([])
            ax.set_yticks([])
        
        self.canvas.draw()
    
    def load_analysis(self):
        """Load initial analysis if data is available"""
        # Auto-load analysis for all records if data exists
        try:
            all_records = self.scoreboard_manager.get_leaderboard(10)
            if all_records:
                self.analyze_all_records()
        except Exception:
            pass  # No data available yet