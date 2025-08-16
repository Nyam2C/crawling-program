#!/usr/bin/env python3
"""Trading Portfolio Panel Component"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from typing import Dict


class TradingPortfolioPanel:
    """Portfolio management panel for trading interface"""
    
    def __init__(self, parent, main_app, data_manager):
        self.parent = parent
        self.main_app = main_app
        self.colors = main_app.colors
        self.data_manager = data_manager
        
        self.create_portfolio_panel()
    
    def create_portfolio_panel(self):
        """Create portfolio display panel"""
        # Portfolio frame
        portfolio_frame = ttk.LabelFrame(self.parent, text="💼 Portfolio Overview", padding="10")
        portfolio_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Portfolio overview
        overview_frame = ttk.Frame(portfolio_frame)
        overview_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Cash balance
        cash_frame = ttk.Frame(overview_frame)
        cash_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(cash_frame, text="💰 Cash Balance:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        self.cash_label = ttk.Label(cash_frame, text="$0.00", 
                                   font=('Arial', 10),
                                   foreground=self.colors['mint'])
        self.cash_label.pack(side=tk.RIGHT)
        
        # Total portfolio value
        value_frame = ttk.Frame(overview_frame)
        value_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(value_frame, text="📊 Total Portfolio Value:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        self.value_label = ttk.Label(value_frame, text="$0.00", 
                                    font=('Arial', 10),
                                    foreground=self.colors['periwinkle'])
        self.value_label.pack(side=tk.RIGHT)
        
        # P&L display
        pnl_frame = ttk.Frame(overview_frame)
        pnl_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(pnl_frame, text="📈 Total P&L:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        self.pnl_label = ttk.Label(pnl_frame, text="$0.00 (0.00%)", 
                                  font=('Arial', 10))
        self.pnl_label.pack(side=tk.RIGHT)
        
        # Positions table
        self.create_positions_table(portfolio_frame)
    
    def create_positions_table(self, parent):
        """Create positions table"""
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Positions table
        columns = ('symbol', 'quantity', 'avg_price', 'current_price', 'market_value', 'pnl', 'pnl_percent')
        
        self.positions_tree = ttk.Treeview(table_frame, columns=columns, 
                                          show='headings', height=8,
                                          style='Pastel.Treeview')
        
        # Column configuration
        column_config = {
            'symbol': ('Symbol', 80),
            'quantity': ('Qty', 60),
            'avg_price': ('Avg Price', 80),
            'current_price': ('Current', 80),
            'market_value': ('Market Value', 100),
            'pnl': ('P&L ($)', 80),
            'pnl_percent': ('P&L (%)', 70)
        }
        
        for col, (heading, width) in column_config.items():
            self.positions_tree.heading(col, text=heading)
            self.positions_tree.column(col, width=width, anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", 
                                   command=self.positions_tree.yview,
                                   style='Pastel.Vertical.TScrollbar')
        self.positions_tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", 
                                   command=self.positions_tree.xview,
                                   style='Pastel.Horizontal.TScrollbar')
        self.positions_tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.positions_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
    
    def update_portfolio_display(self):
        """Update portfolio information display"""
        portfolio = self.data_manager.get_portfolio()
        
        # Update cash balance
        self.cash_label.config(text=f"${portfolio.cash_balance:,.2f}")
        
        # Calculate total portfolio value
        total_value = portfolio.get_total_value(self.data_manager.get_stock_prices())
        self.value_label.config(text=f"${total_value:,.2f}")
        
        # Calculate total P&L
        total_pnl = total_value - portfolio.initial_balance
        pnl_percent = (total_pnl / portfolio.initial_balance) * 100 if portfolio.initial_balance > 0 else 0
        
        pnl_color = self.colors['mint'] if total_pnl >= 0 else self.colors['coral']
        pnl_text = f"${total_pnl:,.2f} ({pnl_percent:+.2f}%)"
        self.pnl_label.config(text=pnl_text, foreground=pnl_color)
        
        # Update positions table
        self.update_positions_table()
    
    def update_positions_table(self):
        """Update positions table"""
        # Clear existing items
        for item in self.positions_tree.get_children():
            self.positions_tree.delete(item)
        
        portfolio = self.data_manager.get_portfolio()
        stock_prices = self.data_manager.get_stock_prices()
        
        # Add positions
        for symbol, position in portfolio.positions.items():
            if symbol in stock_prices:
                current_price = stock_prices[symbol].current_price
                market_value = position.quantity * current_price
                total_cost = position.quantity * position.average_price
                pnl = market_value - total_cost
                pnl_percent = (pnl / total_cost) * 100 if total_cost > 0 else 0
                
                # Color coding based on P&L
                if pnl >= 0:
                    tags = ('profit',)
                else:
                    tags = ('loss',)
                
                self.positions_tree.insert('', 'end', tags=tags, values=(
                    symbol,
                    f"{position.quantity:,}",
                    f"${position.average_price:.2f}",
                    f"${current_price:.2f}",
                    f"${market_value:,.2f}",
                    f"${pnl:,.2f}",
                    f"{pnl_percent:+.2f}%"
                ))
        
        # Configure row colors
        self.positions_tree.tag_configure('profit', background='#E8F5E8', foreground='#2E7D2E')
        self.positions_tree.tag_configure('loss', background='#FEE8E8', foreground='#DC2626')