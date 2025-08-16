#!/usr/bin/env python3
"""Trading Watchlist Panel Component"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Callable


class TradingWatchlistPanel:
    """Watchlist management panel for trading interface"""
    
    def __init__(self, parent, main_app, data_manager, on_stock_select: Callable[[str], None]):
        self.parent = parent
        self.main_app = main_app
        self.colors = main_app.colors
        self.data_manager = data_manager
        self.on_stock_select = on_stock_select
        
        self.create_watchlist_panel()
    
    def create_watchlist_panel(self):
        """Create watchlist display and management panel"""
        # Watchlist frame
        watchlist_frame = ttk.LabelFrame(self.parent, text="👀 Stock Watchlist", padding="10")
        watchlist_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Control buttons
        control_frame = ttk.Frame(watchlist_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.main_app.icon_button(control_frame, 'refresh', 'Refresh All Prices', 
                                  self.refresh_all_prices, 
                                  style='Pastel.Primary.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        self.main_app.icon_button(control_frame, 'remove', 'Remove Selected', 
                                  self.remove_selected_stock,
                                  style='Pastel.Danger.TButton').pack(side=tk.LEFT)
        
        # Watchlist table
        self.create_watchlist_table(watchlist_frame)
        
        # Add stock section
        self.create_add_stock_section(watchlist_frame)
    
    def create_watchlist_table(self, parent):
        """Create watchlist table"""
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Watchlist table
        columns = ('symbol', 'name', 'price', 'change', 'change_percent', 'last_updated')
        
        self.watchlist_tree = ttk.Treeview(table_frame, columns=columns, 
                                          show='headings', height=10,
                                          style='Pastel.Treeview')
        
        # Column configuration
        column_config = {
            'symbol': ('Symbol', 80),
            'name': ('Company', 180),
            'price': ('Price', 80),
            'change': ('Change', 80),
            'change_percent': ('Change %', 80),
            'last_updated': ('Updated', 120)
        }
        
        for col, (heading, width) in column_config.items():
            self.watchlist_tree.heading(col, text=heading)
            self.watchlist_tree.column(col, width=width, anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", 
                                   command=self.watchlist_tree.yview,
                                   style='Pastel.Vertical.TScrollbar')
        self.watchlist_tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", 
                                   command=self.watchlist_tree.xview,
                                   style='Pastel.Horizontal.TScrollbar')
        self.watchlist_tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.watchlist_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Double-click binding
        self.watchlist_tree.bind('<Double-1>', self.on_watchlist_select)
    
    def create_add_stock_section(self, parent):
        """Create add stock section"""
        search_frame = ttk.LabelFrame(parent, text="🔍 Add Stock to Watchlist", padding="5")
        search_frame.pack(fill=tk.X)
        
        input_frame = ttk.Frame(search_frame)
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="Stock Symbol:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.stock_symbol_var = tk.StringVar()
        self.stock_entry = ttk.Entry(input_frame, textvariable=self.stock_symbol_var, 
                                    width=15, style='Pastel.TEntry')
        self.stock_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.stock_entry.bind('<Return>', lambda e: self.add_stock_to_watchlist())
        
        add_btn = self.main_app.icon_button(input_frame, 'search', 'Search&Add', 
                                           self.add_stock_to_watchlist,
                                           style='Pastel.Primary.TButton')
        add_btn.pack(side=tk.LEFT)
    
    def update_watchlist_display(self):
        """Update watchlist display"""
        # Clear existing items
        for item in self.watchlist_tree.get_children():
            self.watchlist_tree.delete(item)
        
        # Get stock data
        stock_data = self.data_manager.get_stock_prices()
        
        # Add stocks to watchlist
        for symbol, stock_info in stock_data.items():
            # Calculate change and change percentage (placeholder logic)
            change = 0.0  # Would need historical data
            change_percent = 0.0
            
            # Color coding based on change
            if change >= 0:
                tags = ('positive',)
            else:
                tags = ('negative',)
            
            # Format last updated time
            last_updated = stock_info.last_updated.strftime('%H:%M:%S') if hasattr(stock_info, 'last_updated') else 'N/A'
            
            self.watchlist_tree.insert('', 'end', tags=tags, values=(
                symbol,
                stock_info.company_name[:25] + '...' if len(stock_info.company_name) > 25 else stock_info.company_name,
                f"${stock_info.current_price:.2f}",
                f"${change:+.2f}",
                f"{change_percent:+.2f}%",
                last_updated
            ))
        
        # Configure row colors
        self.watchlist_tree.tag_configure('positive', background='#E8F5E8', foreground='#2E7D2E')
        self.watchlist_tree.tag_configure('negative', background='#FEE8E8', foreground='#DC2626')
    
    def add_stock_to_watchlist(self):
        """Add stock to watchlist"""
        symbol = self.stock_symbol_var.get().strip().upper()
        if not symbol:
            return
        
        try:
            # Add stock to data manager
            success = self.data_manager.add_stock(symbol)
            if success:
                self.stock_symbol_var.set("")
                self.update_watchlist_display()
                # Show success message
                if hasattr(self.main_app, 'show_success'):
                    self.main_app.show_success("Stock Added", f"Successfully added {symbol} to watchlist!")
            else:
                # Show error message
                if hasattr(self.main_app, 'show_error'):
                    self.main_app.show_error("Error", f"Failed to add {symbol}. Please check the symbol.")
        except Exception as e:
            if hasattr(self.main_app, 'show_error'):
                self.main_app.show_error("Error", f"Error adding stock: {str(e)}")
    
    def remove_selected_stock(self):
        """Remove selected stock from watchlist"""
        selection = self.watchlist_tree.selection()
        if not selection:
            if hasattr(self.main_app, 'show_warning'):
                self.main_app.show_warning("No Selection", "Please select a stock to remove.")
            return
        
        # Get selected stock symbol
        item = self.watchlist_tree.item(selection[0])
        symbol = item['values'][0]
        
        # Confirm removal
        if hasattr(self.main_app, 'show_question'):
            if self.main_app.show_question("Confirm Removal", f"Remove {symbol} from watchlist?"):
                self.data_manager.remove_stock(symbol)
                self.update_watchlist_display()
    
    def refresh_all_prices(self):
        """Refresh all stock prices"""
        try:
            self.data_manager.update_all_stock_prices()
            self.update_watchlist_display()
            if hasattr(self.main_app, 'show_success'):
                self.main_app.show_success("Prices Updated", "All stock prices have been refreshed!")
        except Exception as e:
            if hasattr(self.main_app, 'show_error'):
                self.main_app.show_error("Update Error", f"Error updating prices: {str(e)}")
    
    def on_watchlist_select(self, event):
        """Handle watchlist selection"""
        selection = self.watchlist_tree.selection()
        if selection:
            item = self.watchlist_tree.item(selection[0])
            symbol = item['values'][0]
            if self.on_stock_select:
                self.on_stock_select(symbol)