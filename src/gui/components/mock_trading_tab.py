#!/usr/bin/env python3
"""Mock Trading Tab Component - Kawaii Retro Style"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from datetime import datetime
from typing import Optional

from src.trading.data_manager import TradingDataManager
from src.trading.models import OrderRequest, TransactionType, OrderType
from src.gui.components.kawaii_dialogs import KawaiiMessageBox, KawaiiInputDialog, TradingHelpDialog


class MockTradingTab:
    def __init__(self, notebook, main_app):
        self.notebook = notebook
        self.main_app = main_app
        self.colors = main_app.colors
        
        # Initialize kawaii dialogs
        self.kawaii_msg = KawaiiMessageBox(main_app.root, main_app.theme_manager, main_app.icon_manager)
        self.kawaii_input = KawaiiInputDialog(main_app.root, main_app.theme_manager, main_app.icon_manager)
        self.help_dialog = TradingHelpDialog(main_app.root, main_app.theme_manager, main_app.icon_manager)
        
        # Trading data manager
        self.data_manager = TradingDataManager()
        self.data_manager.start_auto_refresh()
        
        self.setup_tab()
        self.refresh_all_data()
        
        # 주기적 데이터 갱신 (UI)
        self.schedule_ui_refresh()
    
    def setup_tab(self):
        """Create the mock trading tab"""
        self.frame = ttk.Frame(self.notebook, padding="15")
        icon = self.main_app.icon_manager.get_icon('tab_trading')
        self.notebook.add(self.frame, text='Mock Trading', image=icon, compound='left')
        
        # Configure grid - only main content now
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Main content area with notebook (Portfolio Summary moved to separate tab)
        self.create_main_content()
    
    
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
        summary_frame = ttk.Frame(self.sub_notebook, padding="20")
        self.sub_notebook.add(summary_frame, text='Summary')
        
        summary_frame.grid_rowconfigure(1, weight=1)
        summary_frame.grid_columnconfigure(0, weight=1)
        
        # Portfolio summary section with more space
        portfolio_frame = ttk.LabelFrame(summary_frame, text="Portfolio Overview", padding="20")
        portfolio_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        portfolio_frame.grid_columnconfigure(1, weight=1)
        
        # Portfolio values in a larger, more readable layout
        values_grid = ttk.Frame(portfolio_frame)
        values_grid.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        values_grid.grid_columnconfigure(1, weight=1)
        
        # Cash Balance
        ttk.Label(values_grid, text="Cash Balance:", font=('Arial', 12, 'bold'),
                 foreground=self.colors['text']).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cash_label = ttk.Label(values_grid, text="$0", font=('Arial', 14),
                                   foreground=self.colors['mint'])
        self.cash_label.grid(row=0, column=1, sticky=tk.W, padx=(20, 0), pady=5)
        
        # Total Value
        ttk.Label(values_grid, text="Total Portfolio Value:", font=('Arial', 12, 'bold'),
                 foreground=self.colors['text']).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.total_value_label = ttk.Label(values_grid, text="$0", font=('Arial', 14),
                                          foreground=self.colors['text'])
        self.total_value_label.grid(row=1, column=1, sticky=tk.W, padx=(20, 0), pady=5)
        
        # P&L
        ttk.Label(values_grid, text="Profit & Loss:", font=('Arial', 12, 'bold'),
                 foreground=self.colors['text']).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.pnl_label = ttk.Label(values_grid, text="$0 (0.00%)", font=('Arial', 14),
                                  foreground=self.colors['text'])
        self.pnl_label.grid(row=2, column=1, sticky=tk.W, padx=(20, 0), pady=5)
        
        # Control buttons in a separate section
        control_frame = ttk.LabelFrame(portfolio_frame, text="Actions", padding="15")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
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
        
        # Quick stats section
        stats_frame = ttk.LabelFrame(summary_frame, text="Quick Statistics", padding="15")
        stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add some quick stats display
        stats_text = tk.Text(stats_frame, height=6, width=60, 
                           bg=self.colors['panel'], fg=self.colors['text'],
                           font=('Arial', 10), wrap=tk.WORD)
        stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Insert some sample content
        stats_content = """Portfolio Performance Summary:

• Trading sessions: View your complete trading history
• Active positions: Check your current stock holdings  
• Real-time updates: Prices refresh automatically every 5 seconds
• Commission rate: 0.015% per transaction (minimum $100)
• Tax rate: 0.25% on sell transactions

Tip: Use the Trading tab to place orders and manage your watchlist!"""
        
        stats_text.insert(tk.END, stats_content)
        stats_text.config(state=tk.DISABLED)
    
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
        
        # Limit price - fixed width container
        ttk.Label(order_frame, text="Limit Price:", foreground=self.colors['text']).grid(row=4, column=0, sticky=tk.W, pady=2)
        price_container = ttk.Frame(order_frame)
        price_container.grid(row=4, column=1, sticky=tk.W, pady=2)
        price_container.grid_columnconfigure(0, minsize=150)  # Wider for better visibility
        
        self.limit_price_var = tk.StringVar()
        self.limit_price_entry = ttk.Entry(price_container, textvariable=self.limit_price_var, width=15, state='disabled')
        self.limit_price_entry.grid(row=0, column=0, sticky=tk.W)
        
        # Estimated cost - compact container
        cost_container = ttk.Frame(order_frame)
        cost_container.grid(row=5, column=0, columnspan=2, pady=(5, 5), sticky=(tk.W, tk.E))
        cost_container.grid_rowconfigure(0, minsize=25)  # Smaller height
        
        self.cost_label = ttk.Label(cost_container, text="Estimated Cost: -", 
                                   foreground=self.colors['text_accent'], font=('Arial', 9))
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
                       foreground=self.colors['text'])
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
            self.kawaii_msg.show_warning("No Symbol Entered", 
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
        
        self.kawaii_msg.show_success("Stock Added Successfully!", 
                                   f"Added {symbol} ({company}) to your watchlist\nCurrent price: ${price:.2f}",
                                   'sparkle')
    
    def on_stock_not_found(self, symbol):
        """Handle stock not found"""
        self.stock_info_label.config(text="Stock not found")
        self.kawaii_msg.show_error("Stock Not Found", 
                                 f"Could not find stock '{symbol}'\nPlease check the symbol and try again",
                                 'skull')
    
    def on_search_error(self, error_msg):
        """Handle search error"""
        self.stock_info_label.config(text="Search failed")
        self.kawaii_msg.show_error("Search Failed", 
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
    
    def place_order(self):
        """Place trading order"""
        if not self.selected_trading_stock:
            self.kawaii_msg.show_warning("No Stock Selected", 
                                       "Please select a stock to trade first!\n\nTip: Double-click a stock from your watchlist",
                                       'bow')
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            self.kawaii_msg.show_error("Invalid Quantity", 
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
                self.kawaii_msg.show_error("Invalid Limit Price", 
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
            
            self.kawaii_msg.show_success("Order Executed!", success_msg, 'heart')
            
            # Clear form
            self.quantity_var.set("")
            self.limit_price_var.set("")
            # Refresh displays
            self.refresh_all_data()
            # Save data
            self.data_manager.save_data()
        else:
            self.kawaii_msg.show_error("Order Failed", message, 'skull')
    
    def remove_watched_stock(self):
        """Remove selected stock from watched list"""
        selection = self.watched_listbox.curselection()
        if not selection:
            self.kawaii_msg.show_warning("No Stock Selected", 
                                       "Please select a stock from the watchlist to remove\n\nTip: Click on a stock first, then click Remove",
                                       'bow')
            return
        
        stock_text = self.watched_listbox.get(selection[0])
        symbol = stock_text.split(' - ')[0]
        
        # Ask for confirmation
        if self.kawaii_msg.show_question("Remove Stock?", 
                                       f"Are you sure you want to remove {symbol} from your watchlist?\n\nYou can always add it back later!",
                                       'glasses'):
            self.data_manager.remove_watched_stock(symbol)
            self.refresh_watched_stocks()
            self.kawaii_msg.show_success("Stock Removed!", 
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
        """Show reset portfolio dialog"""
        if self.kawaii_msg.show_question("Reset Portfolio?", 
                                        "This will delete all trading history and positions, resetting your account.\n\nAre you sure you want to continue?\n\nThis action cannot be undone!",
                                        'bow'):
            # Ask for initial balance
            initial_balance = self.kawaii_input.ask_float(
                "Set Initial Balance",
                "Enter your starting balance (USD):",
                initial_value=100000.0,
                min_value=1000.0,
                max_value=10000000.0,
                icon_key='folder'
            )
            
            if initial_balance:
                self.data_manager.reset_portfolio(initial_balance)
                self.refresh_all_data()
                self.kawaii_msg.show_success("Portfolio Reset!", 
                                           f"Your portfolio has been reset successfully!\nNew starting balance: ${initial_balance:,.2f}\n\nGood luck with your trading!",
                                           'heart')
    
    def show_help(self):
        """Show trading help dialog"""
        self.help_dialog.show_help()
    
    def schedule_ui_refresh(self):
        """Schedule periodic UI refresh"""
        def refresh_ui():
            try:
                self.update_portfolio_summary()
                self.update_watched_stocks_display()
            except Exception as e:
                print(f"UI refresh error: {e}")
            
            # Schedule next refresh
            self.main_app.root.after(10000, refresh_ui)  # Every 10 seconds
        
        # Start the refresh cycle
        self.main_app.root.after(5000, refresh_ui)  # First refresh after 5 seconds
    
    def cleanup(self):
        """Cleanup resources when tab is destroyed"""
        if hasattr(self, 'data_manager'):
            self.data_manager.close()