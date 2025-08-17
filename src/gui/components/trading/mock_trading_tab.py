#!/usr/bin/env python3
"""Mock Trading Tab Component - Kawaii Retro Style"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from datetime import datetime
from typing import Optional, Dict

from src.trading.data_manager import TradingDataManager
from src.trading.models import OrderRequest, TransactionType, OrderType
from src.trading.scoreboard_manager import ScoreboardManager
from src.trading.scoreboard_models import ScoreboardResult
from src.gui.components.dialogs import KawaiiMessageBox, KawaiiInputDialog, TradingHelpDialog


class MockTradingTab:
    def __init__(self, notebook, main_app):
        self.notebook = notebook
        self.main_app = main_app
        self.colors = main_app.colors
        
        # Initialize kawaii dialogs (lazy initialization)
        self.kawaii_msg = None
        self.kawaii_input = None
        self.help_dialog = None
        
        # Trading data manager
        self.data_manager = TradingDataManager()
        self.data_manager.start_auto_refresh()
        
        # Scoreboard manager for high score tracking
        self.scoreboard_manager = ScoreboardManager()
        self.session_start_time = datetime.now()  # Track session start time
        
        self.setup_tab()
        self.refresh_all_data()
        
        # 주기적 데이터 갱신 (UI)
        self.schedule_ui_refresh()
    
    def setup_tab(self):
        """Create the mock trading tab"""
        self.frame = ttk.Frame(self.notebook, padding="15")
        icon = self.main_app.icon_manager.get_icon('tab_trading')
        if icon:
            self.notebook.add(self.frame, text='Mock Trading', image=icon, compound='left')
        else:
            self.notebook.add(self.frame, text='Mock Trading')
        
        # Configure grid - only main content now
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Main content area with notebook (Portfolio Summary moved to separate tab)
        self.create_main_content()
    
    def _get_kawaii_msg(self):
        """Lazy initialization of kawaii message dialog"""
        if self.kawaii_msg is None:
            self.kawaii_msg = KawaiiMessageBox(self.main_app.root, self.main_app.theme_manager, self.main_app.icon_manager)
        return self.kawaii_msg
    
    def _get_kawaii_input(self):
        """Lazy initialization of kawaii input dialog"""
        if self.kawaii_input is None:
            self.kawaii_input = KawaiiInputDialog(self.main_app.root, self.main_app.theme_manager, self.main_app.icon_manager)
        return self.kawaii_input
    
    def _get_help_dialog(self):
        """Lazy initialization of help dialog"""
        if self.help_dialog is None:
            self.help_dialog = TradingHelpDialog(self.main_app.root, self.main_app.theme_manager, self.main_app.icon_manager)
        return self.help_dialog
    
    def create_main_content(self):
        """Create main content with tabbed interface"""
        content_frame = ttk.Frame(self.frame)
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Sub-notebook for trading sections
        self.sub_notebook = ttk.Notebook(content_frame)
        self.sub_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Summary tab (moved from top)
        self.create_summary_tab()
        
        # Trading tab
        self.create_trading_tab()
        
        # Portfolio tab
        self.create_portfolio_tab()
        
        # History tab
        self.create_history_tab()
    
    def create_summary_tab(self):
        """Create portfolio summary tab"""
        summary_frame = ttk.Frame(self.sub_notebook, padding="15")
        self.sub_notebook.add(summary_frame, text='Summary')
        
        # Configure grid layout for three sections
        summary_frame.grid_rowconfigure(0, weight=0, minsize=120)  # Portfolio Overview - compact
        summary_frame.grid_rowconfigure(1, weight=0, minsize=100)  # Update Timer - medium
        summary_frame.grid_rowconfigure(2, weight=1)              # Trading Reference - expandable
        summary_frame.grid_columnconfigure(0, weight=1)
        
        # Portfolio summary section - more compact
        portfolio_frame = ttk.LabelFrame(summary_frame, text="Portfolio Overview", padding="10")
        portfolio_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        portfolio_frame.grid_columnconfigure(1, weight=1)
        
        # Portfolio values in a compact horizontal layout
        values_grid = ttk.Frame(portfolio_frame)
        values_grid.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        values_grid.grid_columnconfigure((1, 3, 5), weight=1)
        
        # Cash Balance
        ttk.Label(values_grid, text="Cash:", font=('Arial', 10, 'bold'),
                 foreground=self.colors['text']).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.cash_label = ttk.Label(values_grid, text="$0", font=('Arial', 11),
                                   foreground=self.colors['mint'])
        self.cash_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 15))
        
        # Total Value
        ttk.Label(values_grid, text="Total:", font=('Arial', 10, 'bold'),
                 foreground=self.colors['text']).grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.total_value_label = ttk.Label(values_grid, text="$0", font=('Arial', 11),
                                          foreground=self.colors['text'])
        self.total_value_label.grid(row=0, column=3, sticky=tk.W, padx=(0, 15))
        
        # P&L
        ttk.Label(values_grid, text="P&L:", font=('Arial', 10, 'bold'),
                 foreground=self.colors['text']).grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.pnl_label = ttk.Label(values_grid, text="$0 (0.00%)", font=('Arial', 11),
                                  foreground=self.colors['text'])
        self.pnl_label.grid(row=0, column=5, sticky=tk.W)
        
        # Control buttons in a separate section
        control_frame = ttk.LabelFrame(portfolio_frame, text="Actions", padding="10")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        button_row = ttk.Frame(control_frame)
        button_row.pack(fill=tk.X)
        
        self.main_app.icon_button(button_row, 'help', 'Help Guide', 
                                 self.show_help,
                                 style='Pastel.Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        self.main_app.icon_button(button_row, 'refresh', 'Refresh All Data', 
                                 self.refresh_all_data, 
                                 style='Pastel.Ghost.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        self.main_app.icon_button(button_row, 'reset', 'Reset Portfolio', 
                                 self.reset_portfolio_dialog,
                                 style='Pastel.Danger.TButton').pack(side=tk.LEFT)
        
        # Update Timer Section
        self.create_update_timer_section(summary_frame)
        
        # Trading Reference Section  
        self.create_trading_reference_section(summary_frame)
    
    def update_stats_content(self, show_update_warning=False):
        """Update stats content with optional update warning"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        base_content = """Portfolio Performance Summary:

• Trading sessions: View your complete trading history
• Active positions: Check your current stock holdings  
• Real-time updates: Prices refresh automatically every 20 seconds
• Commission rate: 0.015% per transaction (minimum $100)
• Tax rate: 0.25% on sell transactions

Tip: Use the Trading tab to place orders and manage your watchlist!"""
        
        if show_update_warning:
            warning_content = "\n\n✿ Price update in 5 seconds..."
            self.stats_text.insert(tk.END, base_content + warning_content)
            # Make warning text stand out
            self.stats_text.tag_add("warning", "end-2l", "end")
            self.stats_text.tag_config("warning", foreground=self.colors['coral'], font=('Arial', 10, 'bold'))
        else:
            self.stats_text.insert(tk.END, base_content)
        
        self.stats_text.config(state=tk.DISABLED)
    
    def create_update_timer_section(self, parent):
        """Create update countdown timer section"""
        timer_frame = ttk.LabelFrame(parent, text="Price Update Timer", padding="15")
        timer_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        timer_frame.grid_columnconfigure(0, weight=1)
        
        # Timer display
        timer_container = ttk.Frame(timer_frame)
        timer_container.pack(expand=True)
        
        self.timer_label = ttk.Label(timer_container, 
                                    text="Next update in: 20s",
                                    font=('Arial', 14, 'bold'),
                                    foreground=self.colors['text'])
        self.timer_label.pack()
        
        # Progress info
        self.timer_info_label = ttk.Label(timer_container,
                                         text="Automatic price refresh every 20 seconds",
                                         font=('Arial', 9),
                                         foreground=self.colors['text_muted'])
        self.timer_info_label.pack(pady=(5, 0))
        
        # Initialize countdown
        self.remaining_seconds = 20
        self.start_countdown()
    
    def create_trading_reference_section(self, parent):
        """Create trading reference information section"""
        reference_frame = ttk.LabelFrame(parent, text="Trading Reference", padding="15")
        reference_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        reference_frame.grid_columnconfigure(0, weight=1)
        reference_frame.grid_rowconfigure(0, weight=1)
        
        # Reference content
        reference_text = tk.Text(reference_frame, height=8, width=60,
                               bg=self.colors['panel'], fg=self.colors['text'],
                               font=('Arial', 10), wrap=tk.WORD)
        reference_text.pack(fill=tk.BOTH, expand=True)
        
        reference_content = """Mock Trading Reference Guide:

• Commission Rate: 0.015% per transaction (minimum $100)
• Tax Rate: 0.25% on sell transactions only
• Starting Balance: $100,000 virtual cash
• Order Types: Market (instant) & Limit (set price)
• Transaction Types: Buy (purchase) & Sell (liquidate)
• Real-time Data: Live market prices with 20-second updates
• Portfolio Tracking: Automatic P&L calculation
• Risk-free Environment: Practice trading without real money

Tip: Start with small positions to learn market behavior!"""
        
        reference_text.insert(tk.END, reference_content)
        reference_text.config(state=tk.DISABLED)
    
    def start_countdown(self):
        """Start countdown timer for next update"""
        def update_timer():
            if hasattr(self, 'timer_label'):
                self.timer_label.config(text=f"Next update in: {self.remaining_seconds}s")
                
                if self.remaining_seconds == 5:
                    # Change color when 5 seconds remaining
                    self.timer_label.config(foreground=self.colors['coral'])
                    self.timer_info_label.config(text="❀ Price update coming soon...")
                elif self.remaining_seconds == 0:
                    # Reset timer
                    self.remaining_seconds = 20
                    self.timer_label.config(foreground=self.colors['text'])
                    self.timer_info_label.config(text="Automatic price refresh every 20 seconds")
                else:
                    self.timer_label.config(foreground=self.colors['text'])
                    self.timer_info_label.config(text="Automatic price refresh every 20 seconds")
                
                self.remaining_seconds -= 1
                if self.remaining_seconds < 0:
                    self.remaining_seconds = 19
                
                # Schedule next update
                self.main_app.root.after(1000, update_timer)
        
        update_timer()
    
    def create_trading_tab(self):
        """Create trading interface tab with more vertical space"""
        trading_frame = ttk.Frame(self.sub_notebook, padding="10")
        self.sub_notebook.add(trading_frame, text='Trading')
        
        # Better grid configuration - Stock Search matches Place Order width
        trading_frame.grid_rowconfigure(1, weight=1)
        trading_frame.grid_columnconfigure(0, weight=1)  # Left side (Search + Order)
        trading_frame.grid_columnconfigure(1, weight=2)  # Right side (Watchlist) gets more space
        
        # Left side: Stock search and Order form
        self.create_stock_search_section(trading_frame)
        self.create_order_form(trading_frame)
        
        # Right side: Complete Watchlist section with all elements
        self.create_complete_watchlist_section(trading_frame)
    
    def create_complete_watchlist_section(self, parent):
        """Create complete watchlist section with all elements"""
        # Main watchlist frame that spans both rows
        watchlist_frame = ttk.LabelFrame(parent, text="Stock Watchlist", padding="15")
        watchlist_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        watchlist_frame.grid_rowconfigure(2, weight=1)  # Stock list gets most space
        watchlist_frame.grid_columnconfigure(0, weight=1)
        
        # Header info
        header_label = ttk.Label(watchlist_frame, 
                                text="Manage your watchlist and select stocks for trading",
                                foreground=self.colors['text_muted'], font=('Arial', 9))
        header_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Control buttons row
        control_frame = ttk.Frame(watchlist_frame)
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.main_app.icon_button(control_frame, 'refresh', 'Refresh All Prices', 
                                 self.refresh_watched_stocks,
                                 style='Pastel.Ghost.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        self.main_app.icon_button(control_frame, 'remove', 'Remove Selected', 
                                 self.remove_watched_stock,
                                 style='Pastel.Danger.TButton').pack(side=tk.LEFT)
        
        # Stock list section
        list_frame = ttk.LabelFrame(watchlist_frame, text="Your Stocks", padding="10")
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        self.watched_listbox = tk.Listbox(list_frame, 
                                         bg=self.colors['panel'], 
                                         fg=self.colors['text'],
                                         font=('Arial', 12),  # Larger font for better readability
                                         activestyle='dotbox')
        self.watched_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.watched_listbox.bind('<Double-Button-1>', self.select_stock_for_trading)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.watched_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.watched_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Instructions at bottom
        tip_frame = ttk.Frame(watchlist_frame)
        tip_frame.grid(row=3, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
        
        tip_label = ttk.Label(tip_frame, 
                             text="Double-click any stock to select for trading",
                             foreground=self.colors['magenta'], font=('Arial', 9, 'italic'))
        tip_label.pack()
    
    def create_stock_search_section(self, parent):
        """Create compact stock search section - reverted to previous design, width matches Place Order"""
        search_frame = ttk.LabelFrame(parent, text="Stock Search", padding="15")  # Match Place Order padding
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 8), padx=(0, 10))  # Match Place Order padx
        
        # Set the search frame to have consistent internal layout
        search_frame.grid_columnconfigure(3, weight=1)  # Info label column expands
        
        # Search input - single row layout, more compact
        ttk.Label(search_frame, text="Symbol:", foreground=self.colors['text']).grid(row=0, column=0, padx=(0, 5))
        
        self.symbol_var = tk.StringVar()
        self.symbol_entry = ttk.Entry(search_frame, textvariable=self.symbol_var, width=10)  # Smaller width
        self.symbol_entry.grid(row=0, column=1, padx=(0, 10))  # Increased spacing to button
        self.symbol_entry.bind('<Return>', lambda e: self.search_and_add_stock())
        
        # Search&Add button with improved spacing
        add_btn = self.main_app.icon_button(search_frame, 'search', 'Search&Add', 
                                           self.search_and_add_stock, spacing=True)
        add_btn.grid(row=0, column=2, padx=(0, 6), ipadx=5)  # Increased internal padding
        add_btn.configure(width=10)  # Increased width for better appearance
        
        # Current stock info - minimal height, moved to same row
        self.stock_info_label = ttk.Label(search_frame, text="", 
                                         foreground=self.colors['text_muted'], font=('Arial', 8))
        self.stock_info_label.grid(row=0, column=3, sticky=tk.W, padx=(8, 0))
    
    def create_order_form(self, parent):
        """Create expanded order form with more vertical space"""
        order_frame = ttk.LabelFrame(parent, text="Place Order", padding="15")
        order_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Configure order frame with compact spacing and center alignment - matches Stock Search
        order_frame.grid_columnconfigure(0, weight=1)  # Label column
        order_frame.grid_columnconfigure(1, weight=1)  # Input column
        for i in range(8):  # Smaller row heights to save space
            order_frame.grid_rowconfigure(i, minsize=30)
        
        # Selected stock
        ttk.Label(order_frame, text="Stock:", foreground=self.colors['text']).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.selected_stock_label = ttk.Label(order_frame, text="Double-click from watchlist", 
                                             foreground=self.colors['text_muted'])
        self.selected_stock_label.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Order type with styled toggle buttons
        ttk.Label(order_frame, text="Order Type:", foreground=self.colors['text']).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.order_type_var = tk.StringVar(value="market")
        order_type_frame = ttk.Frame(order_frame)
        order_type_frame.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        self.market_btn = ttk.Radiobutton(order_type_frame, text="Market", 
                                         variable=self.order_type_var, value="market",
                                         command=self.on_order_type_change,
                                         style='Pastel.Primary.TRadiobutton')
        self.market_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.limit_btn = ttk.Radiobutton(order_type_frame, text="Limit", 
                                        variable=self.order_type_var, value="limit",
                                        command=self.on_order_type_change,
                                        style='Pastel.Secondary.TRadiobutton')
        self.limit_btn.pack(side=tk.LEFT)
        
        # Transaction type with styled toggle buttons - fixed width container
        ttk.Label(order_frame, text="Action:", foreground=self.colors['text']).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.transaction_type_var = tk.StringVar(value="buy")
        trans_type_frame = ttk.Frame(order_frame)
        trans_type_frame.grid(row=2, column=1, sticky=tk.W, pady=2)
        trans_type_frame.grid_columnconfigure(0, minsize=150)  # Fixed width to prevent layout shifting
        
        # Container for buttons to maintain fixed width
        button_container = ttk.Frame(trans_type_frame)
        button_container.grid(row=0, column=0, sticky=tk.W)
        
        self.buy_btn = ttk.Radiobutton(button_container, text="Buy", 
                                      variable=self.transaction_type_var, value="buy",
                                      command=self.on_transaction_type_change,
                                      style='Pastel.Success.TRadiobutton')
        self.buy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.sell_btn = ttk.Radiobutton(button_container, text="Sell", 
                                       variable=self.transaction_type_var, value="sell",
                                       command=self.on_transaction_type_change,
                                       style='Pastel.Danger.TRadiobutton')
        self.sell_btn.pack(side=tk.LEFT)
        
        # Quantity - fixed width container
        ttk.Label(order_frame, text="Quantity:", foreground=self.colors['text']).grid(row=3, column=0, sticky=tk.W, pady=2)
        qty_container = ttk.Frame(order_frame)
        qty_container.grid(row=3, column=1, sticky=tk.W, pady=2)
        qty_container.grid_columnconfigure(0, minsize=150)  # Wider for better visibility
        
        self.quantity_var = tk.StringVar()
        self.quantity_entry = ttk.Entry(qty_container, textvariable=self.quantity_var, width=15)
        self.quantity_entry.grid(row=0, column=0, sticky=tk.W)
        
        # Add validation for quantity input
        self.quantity_entry.bind('<KeyRelease>', self.validate_quantity_input)
        self.quantity_entry.bind('<FocusOut>', self.validate_quantity_input)
        
        # Limit price - fixed width container
        ttk.Label(order_frame, text="Limit Price:", foreground=self.colors['text']).grid(row=4, column=0, sticky=tk.W, pady=2)
        price_container = ttk.Frame(order_frame)
        price_container.grid(row=4, column=1, sticky=tk.W, pady=2)
        price_container.grid_columnconfigure(0, minsize=150)  # Wider for better visibility
        
        self.limit_price_var = tk.StringVar()
        self.limit_price_entry = ttk.Entry(price_container, textvariable=self.limit_price_var, width=15, state='disabled')
        self.limit_price_entry.grid(row=0, column=0, sticky=tk.W)
        
        # Estimated cost - fixed width container
        cost_container = ttk.Frame(order_frame)
        cost_container.grid(row=5, column=0, columnspan=2, pady=(5, 5), sticky=(tk.W, tk.E))
        cost_container.grid_rowconfigure(0, minsize=25)  # Smaller height
        cost_container.grid_columnconfigure(0, minsize=400, weight=1)  # Fixed minimum width
        
        self.cost_label = ttk.Label(cost_container, text="Estimated Cost: -", 
                                   foreground=self.colors['text_accent'], font=('Arial', 9),
                                   width=50)  # Fixed character width
        self.cost_label.grid(row=0, column=0, sticky=tk.W)
        
        # Place order button - compact but visible
        button_container = ttk.Frame(order_frame)
        button_container.grid(row=6, column=0, columnspan=2, pady=(5, 0), sticky=(tk.W, tk.E))
        button_container.grid_rowconfigure(0, minsize=35)  # Reasonable button height
        
        self.place_order_button = self.main_app.icon_button(button_container, 'trade', 'Place Order', 
                                                          self.place_order,
                                                          style='Pastel.Success.TButton')
        self.place_order_button.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Bind events for cost calculation
        self.quantity_var.trace('w', self.update_estimated_cost)
        self.limit_price_var.trace('w', self.update_estimated_cost)
        
        # Selected stock for trading
        self.selected_trading_stock = None
    
    
    def create_portfolio_tab(self):
        """Create portfolio holdings tab with kawaii styling"""
        portfolio_frame = ttk.Frame(self.sub_notebook, padding="20")
        self.sub_notebook.add(portfolio_frame, text='Portfolio')
        
        portfolio_frame.grid_rowconfigure(1, weight=1)
        portfolio_frame.grid_columnconfigure(0, weight=1)
        
        # Header section
        header_frame = ttk.LabelFrame(portfolio_frame, text="Your Stock Holdings", padding="10")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        info_label = ttk.Label(header_frame, 
                              text="Track your portfolio performance and current positions",
                              foreground=self.colors['text_muted'], font=('Arial', 9))
        info_label.pack()
        
        # Table container with styling
        table_frame = ttk.LabelFrame(portfolio_frame, text="Portfolio Details", padding="10")
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Portfolio table with kawaii styling
        columns = ('Symbol', 'Quantity', 'Avg Price', 'Current Price', 'Market Value', 'P&L', 'P&L %')
        
        # Create style for the treeview
        self.portfolio_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Configure treeview colors to match kawaii theme
        style = ttk.Style()
        style.configure("Treeview", 
                       background=self.colors['panel'],
                       foreground=self.colors['text'],
                       fieldbackground=self.colors['panel'])
        style.configure("Treeview.Heading",
                       background=self.colors['lavender'],
                       foreground='#1B1350')  # Dark purple/black for better visibility
        style.map("Treeview.Heading",
                 background=[('active', self.colors['mint'])])
        style.map("Treeview",
                 background=[('selected', self.colors['lavender'])],
                 foreground=[('selected', self.colors['bg'])])
        
        # Configure columns with kawaii styling
        for col in columns:
            self.portfolio_tree.heading(col, text=col, anchor='center')
            if col in ['Quantity']:
                self.portfolio_tree.column(col, width=90, anchor='e')
            elif col in ['Avg Price', 'Current Price', 'Market Value', 'P&L']:
                self.portfolio_tree.column(col, width=130, anchor='e')
            elif col == 'P&L %':
                self.portfolio_tree.column(col, width=110, anchor='e')
            else:
                self.portfolio_tree.column(col, width=110, anchor='center')
        
        # Apply kawaii colors and styling
        self.portfolio_tree.tag_configure('profit', foreground=self.colors['mint'], font=('Arial', 10, 'bold'))
        self.portfolio_tree.tag_configure('loss', foreground=self.colors['coral'], font=('Arial', 10, 'bold'))
        self.portfolio_tree.tag_configure('normal', foreground=self.colors['text'], font=('Arial', 10))
        
        self.portfolio_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Portfolio scrollbar
        port_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.portfolio_tree.yview)
        port_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.portfolio_tree.configure(yscrollcommand=port_scrollbar.set)
    
    def create_history_tab(self):
        """Create transaction history tab with kawaii styling"""
        history_frame = ttk.Frame(self.sub_notebook, padding="20")
        self.sub_notebook.add(history_frame, text='History')
        
        history_frame.grid_rowconfigure(1, weight=1)
        history_frame.grid_columnconfigure(0, weight=1)
        
        # Header section
        header_frame = ttk.LabelFrame(history_frame, text="Transaction History", padding="10")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        info_label = ttk.Label(header_frame, 
                              text="Complete record of all your buy and sell transactions",
                              foreground=self.colors['text_muted'], font=('Arial', 9))
        info_label.pack()
        
        # Table container with styling
        table_frame = ttk.LabelFrame(history_frame, text="Transaction Details", padding="10")
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # History table with kawaii styling
        hist_columns = ('Date', 'Symbol', 'Type', 'Order', 'Quantity', 'Price', 'Commission', 'Tax', 'Total')
        self.history_tree = ttk.Treeview(table_frame, columns=hist_columns, show='headings', height=12)
        
        # Apply same kawaii styling to history tree (style already configured above)
        
        # Configure columns with kawaii styling
        for col in hist_columns:
            self.history_tree.heading(col, text=col, anchor='center')
            if col == 'Date':
                self.history_tree.column(col, width=160, anchor='center')
            elif col in ['Symbol', 'Type', 'Order']:
                self.history_tree.column(col, width=90, anchor='center')
            elif col == 'Quantity':
                self.history_tree.column(col, width=90, anchor='e')
            else:
                self.history_tree.column(col, width=130, anchor='e')
        
        # Apply kawaii colors and styling
        self.history_tree.tag_configure('buy', foreground=self.colors['mint'], font=('Arial', 10, 'bold'))
        self.history_tree.tag_configure('sell', foreground=self.colors['coral'], font=('Arial', 10, 'bold'))
        self.history_tree.tag_configure('normal', foreground=self.colors['text'], font=('Arial', 10))
        
        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # History scrollbar
        hist_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        hist_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_tree.configure(yscrollcommand=hist_scrollbar.set)
    
    def search_and_add_stock(self):
        """Search for stock and add to watched list"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            self._get_kawaii_msg().show_warning("No Symbol Entered", 
                                        "Please enter a stock symbol first!\n\nExample: AAPL, GOOGL, TSLA, MSFT",
                                        'bow')
            return
        
        # Show loading
        self.stock_info_label.config(text="Searching...")
        self.main_app.root.update()
        
        def search_thread():
            try:
                stock_info = self.data_manager.search_stock(symbol)
                if stock_info:
                    # Add to watched stocks
                    self.data_manager.add_watched_stock(symbol)
                    
                    # Update UI in main thread
                    self.main_app.root.after(0, lambda: self.on_stock_found(stock_info))
                else:
                    self.main_app.root.after(0, lambda: self.on_stock_not_found(symbol))
            except Exception as e:
                self.main_app.root.after(0, lambda: self.on_search_error(str(e)))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def on_stock_found(self, stock_info):
        """Handle successful stock search"""
        symbol = stock_info['symbol']
        price = stock_info['current_price']
        company = stock_info.get('company_name', symbol)
        
        # Ensure price is a number for formatting
        if isinstance(price, str):
            try:
                price = float(price.replace('$', '').replace(',', ''))
            except:
                price = 0.0
        
        self.stock_info_label.config(text=f"{symbol} - {company}: ${price:.2f}")
        self.symbol_var.set("")
        self.refresh_watched_stocks()
        
        self._get_kawaii_msg().show_success("Stock Added Successfully!", 
                                   f"Added {symbol} ({company}) to your watchlist\nCurrent price: ${price:.2f}",
                                   'sparkle')
    
    def on_stock_not_found(self, symbol):
        """Handle stock not found"""
        self.stock_info_label.config(text="Stock not found")
        self._get_kawaii_msg().show_error("Stock Not Found", 
                                 f"Could not find stock '{symbol}'\nPlease check the symbol and try again",
                                 'skull')
    
    def on_search_error(self, error_msg):
        """Handle search error"""
        self.stock_info_label.config(text="Search failed")
        self._get_kawaii_msg().show_error("Search Failed", 
                                 f"Search failed: {error_msg}\nPlease try again later",
                                 'skull')
    
    def select_stock_for_trading(self, event=None):
        """Select stock for trading from watched list"""
        selection = self.watched_listbox.curselection()
        if not selection:
            return
        
        stock_text = self.watched_listbox.get(selection[0])
        # Extract symbol from the display text (format: "SYMBOL - $price")
        symbol = stock_text.split(' - ')[0]
        
        self.selected_trading_stock = symbol
        
        # Update display based on current transaction type (buy/sell)
        self.update_stock_selection_display()
        self.update_estimated_cost()
    
    def on_transaction_type_change(self):
        """Handle transaction type change (Buy/Sell)"""
        if self.selected_trading_stock:
            self.update_stock_selection_display()
        self.update_estimated_cost()
    
    def update_stock_selection_display(self):
        """Update stock selection display based on transaction type"""
        if not self.selected_trading_stock:
            return
        
        symbol = self.selected_trading_stock
        trading_engine = self.data_manager.get_trading_engine()
        
        if self.transaction_type_var.get() == "buy":
            # Show max buyable shares
            current_price = trading_engine.get_stock_price(symbol)
            cash_balance = trading_engine.portfolio.cash_balance
            
            if current_price and current_price > 0:
                commission_rate = 0.00015
                min_commission = 100
                max_shares = 0
                
                for shares in range(1, int(cash_balance / current_price) + 100):
                    net_amount = shares * current_price
                    commission = max(net_amount * commission_rate, min_commission)
                    total_cost = net_amount + commission
                    
                    if total_cost <= cash_balance:
                        max_shares = shares
                    else:
                        break
                
                self.selected_stock_label.config(text=f"{symbol} (Max: {max_shares:,} shares)", 
                                                foreground=self.colors['mint'])
            else:
                self.selected_stock_label.config(text=f"{symbol}", 
                                                foreground=self.colors['mint'])
        else:  # sell
            # Show max sellable shares
            if symbol in trading_engine.portfolio.positions:
                available_shares = trading_engine.portfolio.positions[symbol].quantity
                self.selected_stock_label.config(text=f"{symbol} (Available: {available_shares:,} shares)", 
                                                foreground=self.colors['coral'])
            else:
                self.selected_stock_label.config(text=f"{symbol} (No shares owned)", 
                                                foreground=self.colors['coral'])
    
    def on_order_type_change(self):
        """Handle order type change"""
        if self.order_type_var.get() == "limit":
            self.limit_price_entry.config(state='normal')
        else:
            self.limit_price_entry.config(state='disabled')
            self.limit_price_var.set("")
        self.update_estimated_cost()
    
    def update_estimated_cost(self, *args):
        """Update estimated cost display"""
        if not self.selected_trading_stock:
            self.cost_label.config(text="Estimated Cost: - (Select a stock)")
            return
        
        try:
            quantity = int(self.quantity_var.get() or 0)
            if quantity <= 0:
                self.cost_label.config(text="Estimated Cost: - (Enter quantity)")
                return
        except ValueError:
            self.cost_label.config(text="Estimated Cost: - (Invalid quantity)")
            return
        
        try:
            order_type = OrderType.MARKET if self.order_type_var.get() == "market" else OrderType.LIMIT
            limit_price = None
            
            if order_type == OrderType.LIMIT:
                try:
                    limit_price = float(self.limit_price_var.get() or 0)
                    if limit_price <= 0:
                        self.cost_label.config(text="Estimated Cost: - (Enter limit price)")
                        return
                except ValueError:
                    self.cost_label.config(text="Estimated Cost: - (Invalid limit price)")
                    return
            
            # Calculate cost
            trading_engine = self.data_manager.get_trading_engine()
            total_cost, net_amount, commission, tax = trading_engine.calculate_order_cost(
                self.selected_trading_stock, quantity, order_type, limit_price
            )
            
            if self.transaction_type_var.get() == "buy":
                self.cost_label.config(text=f"Estimated Cost: ${total_cost:,.2f} (Inc. ${commission:,.2f} commission)")
            else:  # sell
                proceeds = net_amount - commission - tax
                self.cost_label.config(text=f"Estimated Proceeds: ${proceeds:,.2f} (After fees)")
                
        except Exception as e:
            self.cost_label.config(text=f"Estimated Cost: Error - {str(e)}")
    
    def validate_quantity_input(self, event=None):
        """Validate quantity input to ensure it doesn't exceed available limits"""
        if not self.selected_trading_stock:
            return
        
        try:
            current_value = self.quantity_var.get()
            if not current_value.isdigit():
                return  # Allow empty or non-numeric input for user typing
            
            quantity = int(current_value)
            if quantity <= 0:
                return
            
            trading_engine = self.data_manager.get_trading_engine()
            
            if self.transaction_type_var.get() == "buy":
                # Calculate max buyable shares
                current_price = trading_engine.get_stock_price(self.selected_trading_stock)
                cash_balance = trading_engine.portfolio.cash_balance
                
                if current_price and current_price > 0:
                    commission_rate = 0.00015
                    min_commission = 100
                    max_shares = 0
                    
                    for shares in range(1, int(cash_balance / current_price) + 100):
                        net_amount = shares * current_price
                        commission = max(net_amount * commission_rate, min_commission)
                        total_cost = net_amount + commission
                        
                        if total_cost <= cash_balance:
                            max_shares = shares
                        else:
                            break
                    
                    # Limit quantity to max buyable shares
                    if quantity > max_shares:
                        self.quantity_var.set(str(max_shares))
                        self.update_estimated_cost()
            else:  # sell
                # Limit to available shares
                if self.selected_trading_stock in trading_engine.portfolio.positions:
                    available_shares = trading_engine.portfolio.positions[self.selected_trading_stock].quantity
                    if quantity > available_shares:
                        self.quantity_var.set(str(available_shares))
                        self.update_estimated_cost()
                else:
                    # No shares to sell
                    self.quantity_var.set("0")
                    self.update_estimated_cost()
                    
        except Exception as e:
            print(f"Quantity validation error: {e}")
    
    def place_order(self):
        """Place trading order"""
        if not self.selected_trading_stock:
            self._get_kawaii_msg().show_warning("No Stock Selected", 
                                       "Please select a stock to trade first!\n\nTip: Double-click a stock from your watchlist",
                                       'bow')
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            self._get_kawaii_msg().show_error("Invalid Quantity", 
                                     "Please enter a valid quantity (positive number)\nExample: 10, 5, 100",
                                     'skull')
            return
        
        order_type = OrderType.MARKET if self.order_type_var.get() == "market" else OrderType.LIMIT
        transaction_type = TransactionType.BUY if self.transaction_type_var.get() == "buy" else TransactionType.SELL
        
        limit_price = None
        if order_type == OrderType.LIMIT:
            try:
                limit_price = float(self.limit_price_var.get())
                if limit_price <= 0:
                    raise ValueError("Limit price must be positive")
            except ValueError:
                self._get_kawaii_msg().show_error("Invalid Limit Price", 
                                         "Please enter a valid limit price (positive number)\nExample: 150.50, 25.00",
                                         'skull')
                return
        
        # Create order request
        order_request = OrderRequest(
            symbol=self.selected_trading_stock,
            transaction_type=transaction_type,
            order_type=order_type,
            quantity=quantity,
            price=limit_price
        )
        
        # Execute order
        trading_engine = self.data_manager.get_trading_engine()
        success, message, transaction = trading_engine.execute_order(order_request)
        
        if success:
            # Create success message with transaction details
            action = "Bought" if transaction_type == TransactionType.BUY else "Sold"
            order_desc = "Market" if order_type == OrderType.MARKET else f"Limit at ${limit_price:.2f}"
            
            success_msg = (f"{action} {quantity} shares of {self.selected_trading_stock}\n"
                          f"Order type: {order_desc}\n"
                          f"Price: ${transaction.price:.2f} per share\n"
                          f"Total: ${transaction.total_amount:.2f}")
            
            self._get_kawaii_msg().show_success("Order Executed!", success_msg, 'heart')
            
            # Clear form
            self.quantity_var.set("")
            self.limit_price_var.set("")
            # Refresh displays
            self.refresh_all_data()
            # Save data
            self.data_manager.save_data()
            
            # Notify Investment Analysis tab to refresh
            self._notify_investment_analysis_update()
            
            # Check for bankruptcy after each trade
            self._check_for_bankruptcy()
        else:
            self._get_kawaii_msg().show_error("Order Failed", message, 'skull')
    
    def remove_watched_stock(self):
        """Remove selected stock from watched list"""
        selection = self.watched_listbox.curselection()
        if not selection:
            self._get_kawaii_msg().show_warning("No Stock Selected", 
                                       "Please select a stock from the watchlist to remove\n\nTip: Click on a stock first, then click Remove",
                                       'bow')
            return
        
        stock_text = self.watched_listbox.get(selection[0])
        symbol = stock_text.split(' - ')[0]
        
        # Ask for confirmation
        if self._get_kawaii_msg().show_question("Remove Stock?", 
                                       f"Are you sure you want to remove {symbol} from your watchlist?\n\nYou can always add it back later!",
                                       'glasses'):
            self.data_manager.remove_watched_stock(symbol)
            self.refresh_watched_stocks()
            self._get_kawaii_msg().show_success("Stock Removed!", 
                                       f"Removed {symbol} from your watchlist",
                                       'sparkle')
    
    def refresh_watched_stocks(self):
        """Refresh watched stocks display"""
        def refresh_thread():
            self.data_manager.refresh_all_watched_stocks()
            self.main_app.root.after(0, self.update_watched_stocks_display)
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def update_watched_stocks_display(self):
        """Update watched stocks listbox"""
        self.watched_listbox.delete(0, tk.END)
        
        watched_stocks = self.data_manager.get_watched_stocks()
        trading_engine = self.data_manager.get_trading_engine()
        
        for symbol in watched_stocks:
            price = trading_engine.get_stock_price(symbol)
            if price is not None:
                self.watched_listbox.insert(tk.END, f"{symbol} - ${price:.2f}")
            else:
                self.watched_listbox.insert(tk.END, f"{symbol} - Loading...")
    
    def refresh_all_data(self):
        """Refresh all trading data"""
        self.update_portfolio_summary()
        self.update_portfolio_display()
        self.update_history_display()
        self.update_watched_stocks_display()
    
    def update_portfolio_summary(self):
        """Update portfolio summary labels in Summary tab"""
        trading_engine = self.data_manager.get_trading_engine()
        summary = trading_engine.get_portfolio_summary()
        
        # Update the labels in the Summary tab (new format without prefixes)
        self.cash_label.config(text=f"${summary['cash_balance']:,.2f}")
        self.total_value_label.config(text=f"${summary['total_value']:,.2f}")
        
        pnl = summary['total_pnl']
        pnl_pct = summary['total_pnl_percentage']
        pnl_color = self.colors['mint'] if pnl >= 0 else self.colors['coral']
        pnl_sign = "+" if pnl >= 0 else ""
        
        self.pnl_label.config(
            text=f"{pnl_sign}${pnl:,.2f} ({pnl_sign}{pnl_pct:.2f}%)",
            foreground=pnl_color
        )
    
    def update_portfolio_display(self):
        """Update portfolio holdings table"""
        # Clear existing items
        for item in self.portfolio_tree.get_children():
            self.portfolio_tree.delete(item)
        
        trading_engine = self.data_manager.get_trading_engine()
        positions = trading_engine.get_positions_summary()
        
        for pos in positions:
            pnl_sign = "+" if pos['pnl'] >= 0 else ""
            
            values = (
                pos['symbol'],
                f"{pos['quantity']:,}",
                f"${pos['average_price']:.2f}",
                f"${pos['current_price']:.2f}",
                f"${pos['current_value']:,.2f}",
                f"{pnl_sign}${pos['pnl']:,.2f}",
                f"{pnl_sign}{pos['pnl_percentage']:.2f}%"
            )
            
            # Use tag for color styling
            tag = 'profit' if pos['pnl'] >= 0 else 'loss'
            item = self.portfolio_tree.insert('', tk.END, values=values, tags=(tag,))
    
    def update_history_display(self):
        """Update transaction history table"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        trading_engine = self.data_manager.get_trading_engine()
        transactions = trading_engine.get_recent_transactions(50)  # Show last 50 transactions
        
        for trans in transactions:
            values = (
                trans.timestamp.strftime("%Y-%m-%d %H:%M"),
                trans.symbol,
                trans.transaction_type.value.title(),
                trans.order_type.value.title(),
                f"{trans.quantity:,}",
                f"${trans.price:.2f}",
                f"${trans.commission:.2f}",
                f"${trans.tax:.2f}",
                f"${trans.total_amount:.2f}"
            )
            
            # Use tag for color styling based on transaction type
            tag = 'buy' if trans.transaction_type.value == 'buy' else 'sell'
            self.history_tree.insert('', tk.END, values=values, tags=(tag,))
    
    def reset_portfolio_dialog(self):
        """Show reset portfolio dialog with scoreboard registration"""
        if self._get_kawaii_msg().show_question("Reset Portfolio?", 
                                        "This will delete all trading history and positions, resetting your account.\n\nAre you sure you want to continue?\n\nThis action cannot be undone!",
                                        'bow'):
            # Get current portfolio for scoreboard
            current_portfolio = self.data_manager.get_trading_engine().portfolio
            
            # Register current session in scoreboard if it has significant activity
            stock_prices = self._get_current_stock_prices()
            if len(current_portfolio.transactions) > 0 or current_portfolio.get_total_value(stock_prices) != current_portfolio.initial_balance:
                self._register_scoreboard_entry(current_portfolio, ScoreboardResult.RESET)
            
            # Ask for initial balance
            initial_balance = self._get_kawaii_input().ask_float(
                "Set Initial Balance",
                "Enter your starting balance (USD):",
                initial_value=100000.0,
                min_value=1000.0,
                max_value=10000000.0,
                icon_key='folder'
            )
            
            if initial_balance:
                self.data_manager.reset_portfolio(initial_balance)
                self.session_start_time = datetime.now()  # Reset session timer
                self.refresh_all_data()
                self._get_kawaii_msg().show_success("Portfolio Reset!", 
                                           f"Your portfolio has been reset successfully!\nNew starting balance: ${initial_balance:,.2f}\n\nGood luck with your trading!",
                                           'heart')
    
    def _register_scoreboard_entry(self, portfolio, result_type: ScoreboardResult):
        """Register current portfolio performance in scoreboard"""
        try:
            # Get current stock prices for portfolio value calculation
            stock_prices = self._get_current_stock_prices()
            current_value = portfolio.get_total_value(stock_prices)
            return_rate = ((current_value - portfolio.initial_balance) / portfolio.initial_balance * 100) if portfolio.initial_balance > 0 else 0
            
            # Ask for nickname
            nickname = self._get_kawaii_input().ask_string(
                "Enter Your Nickname",
                f"Enter your nickname for the scoreboard:\n\nYour Performance:\n"
                f"• Starting Balance: ${portfolio.initial_balance:,.2f}\n"
                f"• Current Balance: ${current_value:,.2f}\n"
                f"• Return: {return_rate:.2f}%\n"
                f"• Total Trades: {len(portfolio.transactions)}",
                initial_value="Player",
                icon_key='bow'
            )
            
            # Convert to string in case it returns a float
            if nickname is not None:
                nickname = str(nickname)
            
            if nickname and nickname.strip():
                # Register score
                record = self.scoreboard_manager.register_portfolio_score(
                    nickname.strip()[:20],  # Limit nickname length
                    portfolio,
                    result_type,
                    stock_prices,
                    self.session_start_time
                )
                
                # Show registration success
                self._get_kawaii_msg().show_success(
                    "Score Registered!",
                    f"Your score has been registered in the Hall of Fame!\n\n"
                    f"Nickname: {record.nickname}\n"
                    f"Return Rate: {record.return_rate:.2f}%\n"
                    f"Grade: {record.grade}\n"
                    f"Rank Score: {record.rank_score:.1f}\n\n"
                    f"Check the Scoreboard tab to see your ranking!",
                    'heart'
                )
            
        except Exception as e:
            print(f"Error registering scoreboard entry: {e}")
    
    def _get_current_stock_prices(self) -> Dict[str, float]:
        """Get current stock prices from trading engine"""
        trading_engine = self.data_manager.get_trading_engine()
        stock_prices = {}
        for symbol, stock in trading_engine.stock_prices.items():
            stock_prices[symbol] = stock.current_price
        return stock_prices
    
    def _check_for_bankruptcy(self):
        """Check if portfolio has gone bankrupt (< $1000)"""
        portfolio = self.data_manager.get_trading_engine().portfolio
        stock_prices = self._get_current_stock_prices()
        total_value = portfolio.get_total_value(stock_prices)
        
        if total_value < 1000.0 and len(portfolio.transactions) > 0:
            # Show bankruptcy message
            self._get_kawaii_msg().show_warning(
                "💸 Bankruptcy Alert!",
                f"Your portfolio value has fallen below $1,000!\n\n"
                f"Current Value: ${total_value:.2f}\n"
                f"Total Loss: ${portfolio.initial_balance - total_value:.2f}\n\n"
                f"Don't give up! This is a great learning experience.\n"
                f"Your score will be registered and you can try again!",
                'skull'
            )
            
            # Register bankruptcy score
            self._register_scoreboard_entry(portfolio, ScoreboardResult.BANKRUPTCY)
            
            # Auto reset with confirmation
            if self._get_kawaii_msg().show_question(
                "Auto Reset Portfolio?",
                "Would you like to reset your portfolio and start over?\n\n"
                "This will give you a fresh start with a new balance.",
                'bow'
            ):
                # Ask for new balance
                new_balance = self._get_kawaii_input().ask_float(
                    "New Starting Balance",
                    "Enter your new starting balance:",
                    initial_value=100000.0,
                    min_value=1000.0,
                    max_value=10000000.0,
                    icon_key='folder'
                )
                
                if new_balance:
                    self.data_manager.reset_portfolio(new_balance)
                    self.session_start_time = datetime.now()
                    self.refresh_all_data()
                    
                    self._get_kawaii_msg().show_success(
                        "Fresh Start!",
                        f"Welcome back! Your portfolio has been reset.\n"
                        f"New starting balance: ${new_balance:,.2f}\n\n"
                        f"Use your previous experience to do even better!",
                        'heart'
                    )

    def show_help(self):
        """Show trading help dialog"""
        self._get_help_dialog().show_help()
    
    def schedule_ui_refresh(self):
        """Schedule periodic UI refresh every 20 seconds with 5-second warning"""
        def show_warning():
            """Show 5-second warning before update"""
            try:
                current_tab = self.notebook.tab(self.notebook.select(), "text")
                if "Mock Trading" in current_tab and hasattr(self, 'timer_info_label'):
                    self.timer_info_label.config(text="❀ Price update in 5 seconds...")
            except Exception as e:
                print(f"Warning display error: {e}")
        
        def refresh_ui():
            try:
                # Mock Trading 탭이 활성 상태일 때만 업데이트 수행
                current_tab = self.notebook.tab(self.notebook.select(), "text")
                if "Mock Trading" in current_tab:
                    # 백그라운드에서 주가 데이터 새로고침
                    self.data_manager.refresh_all_watched_stocks()
                    
                    # UI 업데이트
                    self.update_portfolio_summary()
                    self.update_watched_stocks_display()
                    self.update_portfolio_display()  # Portfolio 탭도 업데이트
                    
                    # 데이터 저장
                    self.data_manager.save_data()
                    
                    # 타이머 리셋
                    if hasattr(self, 'remaining_seconds'):
                        self.remaining_seconds = 20
                    
                    current_time = datetime.now().strftime('%H:%M:%S')
                    print(f"[{current_time}] Mock Trading - Price update completed")
            except Exception as e:
                print(f"UI refresh error: {e}")
            
            # 15초 후에 경고 메시지 표시 (20-5=15)
            self.main_app.root.after(15000, show_warning)
            # 20초 후에 다음 업데이트
            self.main_app.root.after(20000, refresh_ui)
        
        # 첫 번째 새로고침 시작 (20초 후)
        self.main_app.root.after(20000, refresh_ui)
        # 첫 번째 경고 메시지 (15초 후)
        self.main_app.root.after(15000, show_warning)
    
    def _notify_investment_analysis_update(self):
        """Notify Investment Analysis tab that new trading data is available"""
        try:
            # Check if Investment Analysis tab exists and refresh it
            if hasattr(self.main_app, 'investment_analysis_tab'):
                self.main_app.investment_analysis_tab.refresh_trader_list()
        except Exception as e:
            print(f"Failed to notify Investment Analysis tab: {e}")
    
    def cleanup(self):
        """Cleanup resources when tab is destroyed"""
        if hasattr(self, 'data_manager'):
            self.data_manager.close()