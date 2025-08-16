#!/usr/bin/env python3
"""Investment Analysis Tab Component - Kawaii Style Investment Personality Analysis"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, List

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
                               text="🎮 INVESTMENT PERSONALITY ANALYSIS 🎮",
                               font=('Arial', 16, 'bold'),
                               foreground=self.colors['magenta'])
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                  text="Analyze your trading patterns and discover your investor ability stats",
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
        
        # Right panel - Investment Ability Stats
        self.create_ability_stats_panel(main_container)
    
    def create_analysis_panel(self, parent):
        """Create analysis results panel"""
        analysis_frame = ttk.LabelFrame(parent, text="📊 Personality Analysis", padding="10")
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
    
    def create_ability_stats_panel(self, parent):
        """Create investment ability stats panel"""
        stats_frame = ttk.LabelFrame(parent, text="🎯 Investment Ability Stats", padding="10")
        stats_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollable content for ability stats
        canvas = tk.Canvas(stats_frame, bg=self.colors['bg'])
        scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=canvas.yview)
        self.ability_content_frame = ttk.Frame(canvas)
        
        self.ability_content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.ability_content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initial message
        self.show_initial_ability_message()
    
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

🎯 Risk Tolerance (Conservative, Moderate, Aggressive)
📈 Investment Style (Long-term, Short-term, Swing, Day Trading)
⚡ Trading Frequency (Minimal, Moderate, Active, Hyperactive)
📊 Performance Metrics (Patience, Consistency, Profitability, Discipline)

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
    
    def show_initial_ability_message(self):
        """Show initial message when no analysis is loaded"""
        # Clear existing content
        for widget in self.ability_content_frame.winfo_children():
            widget.destroy()
        
        # Welcome message
        welcome_frame = ttk.Frame(self.ability_content_frame)
        welcome_frame.pack(fill=tk.X, pady=20)
        
        welcome_text = """Welcome to Investment Ability Analysis!

Your trading performance will be analyzed across 4 key areas:

🎯 PATIENCE: Long-term holding capability
⚖️ CONSISTENCY: Stable return generation  
💰 PROFITABILITY: Success rate and returns
🎲 DISCIPLINE: Risk management skills

Start an analysis to see your investor ability stats!"""
        
        welcome_label = ttk.Label(welcome_frame, text=welcome_text,
                                 font=('Arial', 11),
                                 foreground=self.colors['text'],
                                 justify=tk.CENTER)
        welcome_label.pack()
    
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
                                        f"No records found for trader '{nickname}'.\\nPlease check the nickname and try again.", 
                                        'skull')
            return
        
        # Perform analysis
        self.current_metrics = self.analyzer.analyze_personality(trader_records)
        self.display_analysis_results(f"Analysis for {nickname}")
        
        # Update footer
        self.last_updated_label.config(text=f"Analyzed: {nickname}")
        self.stats_label.config(text=f"{len(trader_records)} records analyzed")
        
        # Update ability stats
        self.update_ability_stats()
    
    def analyze_all_records(self):
        """Analyze all trading records"""
        all_records = self.scoreboard_manager.get_leaderboard(100)
        
        if not all_records:
            self.kawaii_msg.show_info("No Data", 
                                     "No trading records found in scoreboard.\\nStart trading to generate analysis data!", 
                                     'sparkle')
            return
        
        # Perform analysis on all records
        self.current_metrics = self.analyzer.analyze_personality(all_records)
        self.display_analysis_results("Overall Market Analysis")
        
        # Update footer
        self.last_updated_label.config(text="Analyzed: All traders")
        self.stats_label.config(text=f"{len(all_records)} total records")
        
        # Update ability stats
        self.update_ability_stats()
    
    def clear_analysis(self):
        """Clear current analysis"""
        self.current_metrics = None
        self.nickname_var.set("")
        self.show_initial_message()
        self.show_initial_ability_message()
        
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
        overview_frame = ttk.LabelFrame(self.analysis_content_frame, text="📋 Personality Overview", padding="10")
        overview_frame.pack(fill=tk.X, pady=(0, 10))
        
        overview_text = f"""🎯 Risk Tolerance: {metrics.risk_tolerance.value}
📈 Investment Style: {metrics.investment_style.value}
⚡ Trading Frequency: {metrics.trading_frequency.value}

{metrics.personality_description}"""
        
        overview_label = ttk.Label(overview_frame, text=overview_text,
                                  font=('Arial', 10),
                                  justify=tk.LEFT)
        overview_label.pack(anchor=tk.W)
        
        # Statistics
        stats_frame = ttk.LabelFrame(self.analysis_content_frame, text="📊 Trading Statistics", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        stats_text = f"""📅 Average Holding Period: {metrics.average_holding_period:.1f} days
🎯 Win Rate: {metrics.win_rate:.1f}%
💰 Average Return: {metrics.average_return:.2f}%
📈 Volatility: {metrics.volatility:.2f}%"""
        
        stats_label = ttk.Label(stats_frame, text=stats_text,
                               font=('Arial', 10),
                               justify=tk.LEFT)
        stats_label.pack(anchor=tk.W)
        
        # Strengths
        if metrics.strengths:
            strengths_frame = ttk.LabelFrame(self.analysis_content_frame, text="✅ Strengths", padding="10")
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
            weaknesses_frame = ttk.LabelFrame(self.analysis_content_frame, text="⚠️ Areas for Improvement", padding="10")
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
            recommendations_frame = ttk.LabelFrame(self.analysis_content_frame, text="💡 Recommendations", padding="10")
            recommendations_frame.pack(fill=tk.X, pady=(0, 10))
            
            for recommendation in metrics.recommendations:
                rec_frame = ttk.Frame(recommendations_frame)
                rec_frame.pack(fill=tk.X, pady=1)
                
                ttk.Label(rec_frame, text="• " + recommendation,
                         font=('Arial', 9),
                         foreground=self.colors['text'],
                         wraplength=350).pack(anchor=tk.W)
    
    def update_ability_stats(self):
        """Update ability stats display"""
        if not self.current_metrics:
            self.show_initial_ability_message()
            return
        
        # Clear existing content
        for widget in self.ability_content_frame.winfo_children():
            widget.destroy()
        
        metrics = self.current_metrics
        
        # Title
        title_frame = ttk.Frame(self.ability_content_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="🎮 INVESTOR ABILITY STATS 🎮",
                               font=('Arial', 14, 'bold'),
                               foreground=self.colors['magenta'])
        title_label.pack()
        
        # Create ability stats
        abilities = [
            ("🎯 PATIENCE", metrics.patience_score, "Long-term Investment Capability"),
            ("⚖️ CONSISTENCY", metrics.consistency_score, "Stable Return Generation"),
            ("💰 PROFITABILITY", metrics.profitability_score, "Success Rate & Returns"),
            ("🎲 DISCIPLINE", metrics.discipline_score, "Risk Management Skills")
        ]
        
        for ability_name, score, description in abilities:
            self.create_ability_stat(ability_name, score, description)
        
        # Overall Investment Level
        self.create_overall_level()
        
        # Investment Type Classification
        self.create_investment_type()
    
    def create_ability_stat(self, name: str, score: float, description: str):
        """Create individual ability stat display"""
        stat_frame = ttk.LabelFrame(self.ability_content_frame, text=name, padding="15")
        stat_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Score and level
        score_frame = ttk.Frame(stat_frame)
        score_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Determine level and color
        if score >= 90:
            level = "LEGENDARY"
            level_color = self.colors['magenta']
            stars = "⭐⭐⭐⭐⭐"
        elif score >= 80:
            level = "EXPERT"
            level_color = self.colors['periwinkle']
            stars = "⭐⭐⭐⭐"
        elif score >= 70:
            level = "ADVANCED"
            level_color = self.colors['mint']
            stars = "⭐⭐⭐"
        elif score >= 60:
            level = "INTERMEDIATE"
            level_color = self.colors['lavender']
            stars = "⭐⭐"
        elif score >= 50:
            level = "BEGINNER"
            level_color = self.colors['text']
            stars = "⭐"
        else:
            level = "NOVICE"
            level_color = self.colors['coral']
            stars = "☆"
        
        # Score display
        score_text = f"{score:.1f}/100.0"
        score_label = ttk.Label(score_frame, text=score_text,
                               font=('Arial', 16, 'bold'),
                               foreground=level_color)
        score_label.pack(side=tk.LEFT)
        
        # Level display
        level_label = ttk.Label(score_frame, text=f"  {level} {stars}",
                               font=('Arial', 12, 'bold'),
                               foreground=level_color)
        level_label.pack(side=tk.LEFT)
        
        # Progress bar visualization
        progress_frame = ttk.Frame(stat_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        # ASCII progress bar
        bar_length = 30
        filled_length = int(bar_length * score / 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        progress_label = ttk.Label(progress_frame, text=f"[{bar}]",
                                  font=('Courier', 10),
                                  foreground=level_color)
        progress_label.pack()
        
        # Description
        desc_label = ttk.Label(stat_frame, text=description,
                              font=('Arial', 9),
                              foreground=self.colors['text_muted'])
        desc_label.pack()
    
    def create_overall_level(self):
        """Create overall investment level display"""
        if not self.current_metrics:
            return
        
        metrics = self.current_metrics
        overall_score = (metrics.patience_score + metrics.consistency_score + 
                        metrics.profitability_score + metrics.discipline_score) / 4
        
        level_frame = ttk.LabelFrame(self.ability_content_frame, text="🏆 OVERALL INVESTOR LEVEL", padding="15")
        level_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Determine overall level
        if overall_score >= 85:
            level = "MASTER INVESTOR"
            level_desc = "You demonstrate exceptional investment skills across all areas!"
            level_color = self.colors['magenta']
            badge = "🏆👑"
        elif overall_score >= 75:
            level = "SKILLED INVESTOR"
            level_desc = "You have strong investment capabilities with room for optimization."
            level_color = self.colors['periwinkle']
            badge = "🥇✨"
        elif overall_score >= 65:
            level = "DEVELOPING INVESTOR"
            level_desc = "You're building solid investment fundamentals. Keep practicing!"
            level_color = self.colors['mint']
            badge = "🥈💪"
        elif overall_score >= 50:
            level = "LEARNING INVESTOR"
            level_desc = "You're on the right track. Focus on consistency and patience."
            level_color = self.colors['lavender']
            badge = "🥉📚"
        else:
            level = "BEGINNER INVESTOR"
            level_desc = "Great start! Continue learning and practicing your skills."
            level_color = self.colors['coral']
            badge = "🌱🎯"
        
        # Level display
        level_text = f"{badge} {level}"
        level_label = ttk.Label(level_frame, text=level_text,
                               font=('Arial', 16, 'bold'),
                               foreground=level_color)
        level_label.pack(pady=(0, 10))
        
        # Score display
        score_text = f"Overall Score: {overall_score:.1f}/100.0"
        score_label = ttk.Label(level_frame, text=score_text,
                               font=('Arial', 12),
                               foreground=level_color)
        score_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ttk.Label(level_frame, text=level_desc,
                              font=('Arial', 10),
                              foreground=self.colors['text'],
                              wraplength=400)
        desc_label.pack()
    
    def create_investment_type(self):
        """Create investment type classification"""
        if not self.current_metrics:
            return
        
        metrics = self.current_metrics
        
        type_frame = ttk.LabelFrame(self.ability_content_frame, text="🎭 INVESTOR TYPE PROFILE", padding="15")
        type_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Investment profile based on metrics
        risk_level = metrics.risk_tolerance.value
        style = metrics.investment_style.value
        frequency = metrics.trading_frequency.value
        
        # Create profile text
        profile_text = f"""🎯 Risk Profile: {risk_level} Investor
📈 Trading Style: {style}
⚡ Activity Level: {frequency}

📊 Key Statistics:
• Average Holding Period: {metrics.average_holding_period:.1f} days
• Win Rate: {metrics.win_rate:.1f}%
• Average Return: {metrics.average_return:.2f}%
• Volatility: {metrics.volatility:.2f}%"""
        
        profile_label = ttk.Label(type_frame, text=profile_text,
                                 font=('Arial', 10),
                                 foreground=self.colors['text'],
                                 justify=tk.LEFT)
        profile_label.pack(anchor=tk.W)
    
    def load_analysis(self):
        """Load initial analysis if data is available"""
        # Auto-load analysis for all records if data exists
        try:
            all_records = self.scoreboard_manager.get_leaderboard(10)
            if all_records:
                self.analyze_all_records()
        except Exception:
            pass  # No data available yet