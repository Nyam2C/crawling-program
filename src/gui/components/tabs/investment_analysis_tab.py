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
        self.refresh_trader_list()
        self.load_analysis()
    
    def setup_tab(self):
        """Create the investment analysis tab"""
        self.frame = ttk.Frame(self.notebook, padding="15")
        # Start with default level_3 icon, will be updated based on analysis
        icon = self.main_app.icon_manager.get_icon('level_3')
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
        
        # Create comprehensive analysis status
        self.create_comprehensive_status()
        
        # Create footer
        self.create_footer()
    
    def create_header(self):
        """Create header section"""
        header_frame = ttk.Frame(self.frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Controls only - removed title and subtitle to save space
        controls_frame = ttk.Frame(header_frame)
        controls_frame.grid(row=0, column=0, columnspan=3, pady=(0, 5))
        
        # Trader selection dropdown
        ttk.Label(controls_frame, text="Select trader:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.nickname_var = tk.StringVar()
        self.trader_combo = ttk.Combobox(controls_frame, textvariable=self.nickname_var, 
                                        width=20, state='readonly', style='Pastel.TCombobox')
        self.trader_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh traders button
        refresh_traders_btn = self.main_app.icon_button(controls_frame, 'glasses', 'Refresh', 
                                                       self.refresh_trader_list, 'Pastel.Ghost.TButton')
        refresh_traders_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Buttons with different icons
        analyze_btn = self.main_app.icon_button(controls_frame, 'heart', 'Analyze Trader',
                                               self.analyze_specific_trader, 'Pastel.Primary.TButton')
        analyze_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        refresh_btn = self.main_app.icon_button(controls_frame, 'sparkle', 'Analyze All Records',
                                               self.analyze_all_records, 'Pastel.Secondary.TButton')
        refresh_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = self.main_app.icon_button(controls_frame, 'skull', 'Clear',
                                             self.clear_analysis, 'Pastel.Ghost.TButton')
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
        analysis_frame = ttk.LabelFrame(parent, text="Personality Analysis", padding="10")
        analysis_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        analysis_frame.grid_rowconfigure(0, weight=1)
        analysis_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollable content with reduced height to fit comprehensive status
        canvas = tk.Canvas(analysis_frame, bg=self.colors['panel_light'], height=320)
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=canvas.yview)
        self.analysis_content_frame = ttk.Frame(canvas)
        
        self.analysis_content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.analysis_content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Initial message
        self.show_initial_message()
    
    def create_ability_stats_panel(self, parent):
        """Create investment ability stats panel"""
        stats_frame = ttk.LabelFrame(parent, text="Investment Ability Stats", padding="10")
        stats_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        stats_frame.grid_rowconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollable content for ability stats with reduced height to fit comprehensive status
        canvas = tk.Canvas(stats_frame, bg=self.colors['panel_light'], height=320)
        scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=canvas.yview)
        self.ability_content_frame = ttk.Frame(canvas)
        
        self.ability_content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.ability_content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Initial message
        self.show_initial_ability_message()
    
    def create_comprehensive_status(self):
        """Create comprehensive analysis status section"""
        status_frame = ttk.LabelFrame(self.frame, text="Comprehensive Analysis Status", padding="8")
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(8, 0))
        status_frame.grid_columnconfigure(0, weight=1)
        status_frame.grid_columnconfigure(1, weight=1)
        
        # Individual Analysis Status
        individual_frame = ttk.Frame(status_frame)
        individual_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Label(individual_frame, text="Individual Analysis:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        self.individual_icon_label = ttk.Label(individual_frame)
        self.individual_icon_label.pack(side=tk.LEFT, padx=(5, 5))
        
        self.individual_status_label = ttk.Label(individual_frame, text="Ready", 
                                               foreground=self.colors['text'])
        self.individual_status_label.pack(side=tk.LEFT)
        
        # Investment Analysis Status  
        investment_frame = ttk.Frame(status_frame)
        investment_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(investment_frame, text="Investment Analysis:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        self.investment_icon_label = ttk.Label(investment_frame)
        self.investment_icon_label.pack(side=tk.LEFT, padx=(5, 5))
        
        self.investment_status_label = ttk.Label(investment_frame, text="Ready", 
                                               foreground=self.colors['text'])
        self.investment_status_label.pack(side=tk.LEFT)
        
        # Initialize with default icons
        self.update_individual_status("Ready", "level_3")
        self.update_investment_status("Ready", "level_3")
    
    def update_individual_status(self, status_text, icon_key):
        """Update individual analysis status"""
        icon = self.main_app.icon_manager.get_icon(icon_key)
        if icon:
            self.individual_icon_label.config(image=icon)
        self.individual_status_label.config(text=status_text)
        
    def update_investment_status(self, status_text, icon_key):
        """Update investment analysis status"""
        icon = self.main_app.icon_manager.get_icon(icon_key)
        if icon:
            self.investment_icon_label.config(image=icon)
        self.investment_status_label.config(text=status_text)
    
    def create_footer(self):
        """Create footer with additional info"""
        footer_frame = ttk.Frame(self.frame)
        footer_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
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
                                 justify=tk.CENTER,
                                 wraplength=400,
                                 background=self.colors['panel_light'])
        welcome_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
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

• PATIENCE: Long-term holding capability
• CONSISTENCY: Stable return generation  
• PROFITABILITY: Success rate and returns
• DISCIPLINE: Risk management skills

Start an analysis to see your investor ability stats!"""
        
        welcome_label = ttk.Label(welcome_frame, text=welcome_text,
                                 font=('Arial', 11),
                                 foreground=self.colors['text'],
                                 justify=tk.CENTER,
                                 background=self.colors['panel_light'])
        welcome_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
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
        
        # Update tab icon based on overall score
        self.update_tab_icon()
        
        # Update main app evaluation area
        self.update_main_evaluation_area()
    
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
        
        # Update tab icon based on overall score
        self.update_tab_icon()
        
        # Update main app evaluation area
        self.update_main_evaluation_area()
    
    def clear_analysis(self):
        """Clear current analysis"""
        self.current_metrics = None
        self.nickname_var.set("")
        self.show_initial_message()
        self.show_initial_ability_message()
        
        # Reset tab icon to default
        icon = self.main_app.icon_manager.get_icon('level_3')
        if icon:
            for i in range(self.notebook.index("end")):
                if self.notebook.tab(i, "text") == "Investment Analysis":
                    self.notebook.tab(i, image=icon)
                    break
        
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
        
        title_label = ttk.Label(title_frame, text="INVESTOR ABILITY STATS",
                               font=('Arial', 14, 'bold'),
                               foreground=self.colors['magenta'])
        title_label.pack()
        
        # Create ability stats
        abilities = [
            ("PATIENCE", metrics.patience_score, "Long-term Investment Capability"),
            ("CONSISTENCY", metrics.consistency_score, "Stable Return Generation"),
            ("PROFITABILITY", metrics.profitability_score, "Success Rate & Returns"),
            ("DISCIPLINE", metrics.discipline_score, "Risk Management Skills")
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
        
        # Determine level, color, and icon
        if score >= 80:
            level = "EXPERT"
            level_color = self.colors['magenta']
            icon_key = "level_5"
        elif score >= 70:
            level = "ADVANCED"
            level_color = self.colors['periwinkle']
            icon_key = "level_4"
        elif score >= 60:
            level = "INTERMEDIATE"
            level_color = self.colors['mint']
            icon_key = "level_3"
        elif score >= 50:
            level = "BEGINNER"
            level_color = self.colors['lavender']
            icon_key = "level_2"
        else:
            level = "NOVICE"
            level_color = self.colors['coral']
            icon_key = "level_1"
        
        # Score display
        score_text = f"{score:.1f}/100.0"
        score_label = ttk.Label(score_frame, text=score_text,
                               font=('Arial', 16, 'bold'),
                               foreground=level_color)
        score_label.pack(side=tk.LEFT)
        
        # Level display with icon
        level_frame = ttk.Frame(score_frame)
        level_frame.pack(side=tk.LEFT, padx=(10, 0))
        
        # Level icon
        level_icon = self.main_app.icon_manager.get_icon(icon_key)
        if level_icon:
            icon_label = ttk.Label(level_frame, image=level_icon)
            icon_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Level text
        level_label = ttk.Label(level_frame, text=level,
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
        
        level_frame = ttk.LabelFrame(self.ability_content_frame, text="OVERALL INVESTOR LEVEL", padding="15")
        level_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Determine overall level
        if overall_score >= 80:
            level = "MASTER INVESTOR"
            level_desc = "You demonstrate exceptional investment skills across all areas!"
            level_color = self.colors['magenta']
            icon_key = "level_5"
        elif overall_score >= 70:
            level = "SKILLED INVESTOR"
            level_desc = "You have strong investment capabilities with room for optimization."
            level_color = self.colors['periwinkle']
            icon_key = "level_4"
        elif overall_score >= 60:
            level = "DEVELOPING INVESTOR"
            level_desc = "You're building solid investment fundamentals. Keep practicing!"
            level_color = self.colors['mint']
            icon_key = "level_3"
        elif overall_score >= 50:
            level = "LEARNING INVESTOR"
            level_desc = "You're on the right track. Focus on consistency and patience."
            level_color = self.colors['lavender']
            icon_key = "level_2"
        else:
            level = "BEGINNER INVESTOR"
            level_desc = "Great start! Continue learning and practicing your skills."
            level_color = self.colors['coral']
            icon_key = "level_1"
        
        # Level display with icon
        level_display_frame = ttk.Frame(level_frame)
        level_display_frame.pack(pady=(0, 10))
        
        # Level icon
        level_icon = self.main_app.icon_manager.get_icon(icon_key)
        if level_icon:
            icon_label = ttk.Label(level_display_frame, image=level_icon)
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Level text
        level_label = ttk.Label(level_display_frame, text=level,
                               font=('Arial', 16, 'bold'),
                               foreground=level_color)
        level_label.pack(side=tk.LEFT)
        
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
        
        type_frame = ttk.LabelFrame(self.ability_content_frame, text="INVESTOR TYPE PROFILE", padding="15")
        type_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Investment profile based on metrics
        risk_level = metrics.risk_tolerance.value
        style = metrics.investment_style.value
        frequency = metrics.trading_frequency.value
        
        # Create profile text
        profile_text = f"""Risk Profile: {risk_level} Investor
Trading Style: {style}
Activity Level: {frequency}

Key Statistics:
• Average Holding Period: {metrics.average_holding_period:.1f} days
• Win Rate: {metrics.win_rate:.1f}%
• Average Return: {metrics.average_return:.2f}%
• Volatility: {metrics.volatility:.2f}%"""
        
        profile_label = ttk.Label(type_frame, text=profile_text,
                                 font=('Arial', 10),
                                 foreground=self.colors['text'],
                                 justify=tk.LEFT)
        profile_label.pack(anchor=tk.W)
    
    def update_tab_icon(self):
        """Update tab icon and title based on overall score"""
        if not self.current_metrics:
            return
        
        metrics = self.current_metrics
        overall_score = (metrics.patience_score + metrics.consistency_score + 
                        metrics.profitability_score + metrics.discipline_score) / 4
        
        # Determine icon and level name based on overall score (5 levels)
        if overall_score >= 80:
            icon_key = "level_5"
            level_name = "EXPERT"
        elif overall_score >= 70:
            icon_key = "level_4"
            level_name = "ADVANCED"
        elif overall_score >= 60:
            icon_key = "level_3"
            level_name = "INTERMEDIATE"
        elif overall_score >= 50:
            icon_key = "level_2"
            level_name = "BEGINNER"
        else:
            icon_key = "level_1"
            level_name = "NOVICE"
        
        # Title removed to save space - no update needed
        
        # Get the icon
        icon = self.main_app.icon_manager.get_icon(icon_key)
        if icon:
            # Find the tab index and update its icon
            for i in range(self.notebook.index("end")):
                if self.notebook.tab(i, "text") == "Investment Analysis":
                    self.notebook.tab(i, image=icon)
                    break
    
    def update_main_evaluation_area(self):
        """Update the main app's evaluation area with investment analysis status"""
        if not self.current_metrics:
            return
        
        metrics = self.current_metrics
        overall_score = (metrics.patience_score + metrics.consistency_score + 
                        metrics.profitability_score + metrics.discipline_score) / 4
        
        # Determine level and status text
        if overall_score >= 80:
            level_icon = "level_5"
            status_text = "EXPERT - Master Investor"
        elif overall_score >= 70:
            level_icon = "level_4"
            status_text = "ADVANCED - Skilled Investor"
        elif overall_score >= 60:
            level_icon = "level_3"
            status_text = "INTERMEDIATE - Developing Investor"
        elif overall_score >= 50:
            level_icon = "level_2"
            status_text = "BEGINNER - Learning Investor"
        else:
            level_icon = "level_1"
            status_text = "NOVICE - Beginner Investor"
        
        # Update investment status in comprehensive status area
        self.update_investment_status(status_text, level_icon)
    
    def refresh_trader_list(self):
        """Refresh the trader dropdown list"""
        try:
            # Get all records and extract unique nicknames
            all_records = self.scoreboard_manager.get_leaderboard(1000)  # Get many records
            nicknames = list(set(record.nickname for record in all_records))
            nicknames.sort()  # Sort alphabetically
            
            # Update combobox values
            self.trader_combo['values'] = nicknames
            
            # Clear current selection if the selected trader is no longer in the list
            current_selection = self.nickname_var.get()
            if current_selection and current_selection not in nicknames:
                self.nickname_var.set("")
                
        except Exception as e:
            print(f"Error refreshing trader list: {e}")
            self.trader_combo['values'] = []
    
    def load_analysis(self):
        """Load initial analysis if data is available"""
        # Auto-load analysis for all records if data exists
        try:
            all_records = self.scoreboard_manager.get_leaderboard(10)
            if all_records:
                self.analyze_all_records()
        except Exception:
            pass  # No data available yet