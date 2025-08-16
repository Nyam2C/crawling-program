#!/usr/bin/env python3
"""Trading Order Panel Component"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from src.trading.models import OrderRequest, TransactionType, OrderType


class TradingOrderPanel:
    """Order placement panel for trading interface"""
    
    def __init__(self, parent, main_app, data_manager, on_order_placed: Optional[Callable] = None):
        self.parent = parent
        self.main_app = main_app
        self.colors = main_app.colors
        self.data_manager = data_manager
        self.on_order_placed = on_order_placed
        
        self.selected_symbol = ""
        self.create_order_panel()
    
    def create_order_panel(self):
        """Create order placement panel"""
        # Order form frame
        order_frame = ttk.LabelFrame(self.parent, text="📋 Place Order", padding="15")
        order_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Stock selection
        self.create_stock_selection(order_frame)
        
        # Order type selection
        self.create_order_type_selection(order_frame)
        
        # Quantity and price inputs
        self.create_quantity_price_inputs(order_frame)
        
        # Order summary and place button
        self.create_order_summary(order_frame)
    
    def create_stock_selection(self, parent):
        """Create stock selection section"""
        stock_frame = ttk.Frame(parent)
        stock_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(stock_frame, text="📊 Stock Symbol:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.symbol_var = tk.StringVar()
        self.symbol_combo = ttk.Combobox(stock_frame, textvariable=self.symbol_var,
                                        width=15, state='readonly',
                                        style='Pastel.TCombobox')
        self.symbol_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        self.symbol_combo.bind('<<ComboboxSelected>>', self.on_symbol_change)
        
        # Current price display
        self.price_display_label = ttk.Label(stock_frame, text="Current Price: N/A",
                                            font=('Arial', 9),
                                            foreground=self.colors['text_muted'])
        self.price_display_label.grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
    
    def create_order_type_selection(self, parent):
        """Create order type selection"""
        type_frame = ttk.Frame(parent)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Transaction type (Buy/Sell)
        ttk.Label(type_frame, text="🔄 Transaction:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.transaction_var = tk.StringVar(value="BUY")
        buy_radio = ttk.Radiobutton(type_frame, text="Buy", variable=self.transaction_var,
                                   value="BUY", style='Pastel.TRadiobutton')
        buy_radio.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        sell_radio = ttk.Radiobutton(type_frame, text="Sell", variable=self.transaction_var,
                                    value="SELL", style='Pastel.TRadiobutton')
        sell_radio.grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        
        # Order type (Market/Limit)
        ttk.Label(type_frame, text="📋 Order Type:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        
        self.order_type_var = tk.StringVar(value="MARKET")
        market_radio = ttk.Radiobutton(type_frame, text="Market", variable=self.order_type_var,
                                      value="MARKET", command=self.on_order_type_change,
                                      style='Pastel.TRadiobutton')
        market_radio.grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        
        limit_radio = ttk.Radiobutton(type_frame, text="Limit", variable=self.order_type_var,
                                     value="LIMIT", command=self.on_order_type_change,
                                     style='Pastel.TRadiobutton')
        limit_radio.grid(row=0, column=5, sticky=tk.W)
    
    def create_quantity_price_inputs(self, parent):
        """Create quantity and price input section"""
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Quantity input
        ttk.Label(input_frame, text="📦 Quantity:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.quantity_var = tk.StringVar()
        self.quantity_var.trace('w', self.validate_quantity_input)
        self.quantity_entry = ttk.Entry(input_frame, textvariable=self.quantity_var,
                                       width=10, style='Pastel.TEntry')
        self.quantity_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Available info
        self.available_label = ttk.Label(input_frame, text="Available: N/A",
                                        font=('Arial', 9),
                                        foreground=self.colors['text_muted'])
        self.available_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        
        # Limit price input (initially disabled)
        ttk.Label(input_frame, text="💰 Limit Price:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        
        self.limit_price_var = tk.StringVar()
        self.limit_price_entry = ttk.Entry(input_frame, textvariable=self.limit_price_var,
                                          width=10, state=tk.DISABLED,
                                          style='Pastel.TEntry')
        self.limit_price_entry.grid(row=0, column=4, sticky=tk.W)
    
    def create_order_summary(self, parent):
        """Create order summary and place button"""
        summary_frame = ttk.Frame(parent)
        summary_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Estimated cost/proceeds
        cost_frame = ttk.Frame(summary_frame)
        cost_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(cost_frame, text="💵 Estimated Cost:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        self.cost_label = ttk.Label(cost_frame, text="$0.00",
                                   font=('Arial', 10),
                                   foreground=self.colors['periwinkle'])
        self.cost_label.pack(side=tk.RIGHT)
        
        # Place order button
        button_container = ttk.Frame(summary_frame)
        button_container.pack(fill=tk.X)
        
        self.place_order_button = self.main_app.icon_button(button_container, 'trade', 'Place Order',
                                                           self.place_order, 'Pastel.Primary.TButton')
        self.place_order_button.pack(side=tk.RIGHT)
        
        # Cancel button
        cancel_btn = ttk.Button(button_container, text="Cancel",
                               command=self.clear_order_form,
                               style='Pastel.Ghost.TButton')
        cancel_btn.pack(side=tk.RIGHT, padx=(0, 10))
    
    def update_symbol_list(self):
        """Update available symbols list"""
        stock_data = self.data_manager.get_stock_prices()
        symbols = list(stock_data.keys())
        self.symbol_combo['values'] = symbols
        
        if symbols and not self.symbol_var.get():
            self.symbol_var.set(symbols[0])
            self.on_symbol_change()
    
    def select_symbol(self, symbol: str):
        """Select a specific symbol"""
        self.symbol_var.set(symbol)
        self.on_symbol_change()
    
    def on_symbol_change(self, event=None):
        """Handle symbol selection change"""
        symbol = self.symbol_var.get()
        if not symbol:
            return
        
        self.selected_symbol = symbol
        
        # Update current price display
        stock_data = self.data_manager.get_stock_prices()
        if symbol in stock_data:
            price = stock_data[symbol].current_price
            self.price_display_label.config(text=f"Current Price: ${price:.2f}")
        
        # Update available quantity for sell orders
        self.update_available_display()
        self.update_cost_estimate()
    
    def on_order_type_change(self):
        """Handle order type change"""
        if self.order_type_var.get() == "LIMIT":
            self.limit_price_entry.config(state=tk.NORMAL)
        else:
            self.limit_price_entry.config(state=tk.DISABLED)
            self.limit_price_var.set("")
        
        self.update_cost_estimate()
    
    def validate_quantity_input(self, *args):
        """Validate quantity input to ensure it doesn't exceed available limits"""
        try:
            quantity = int(self.quantity_var.get()) if self.quantity_var.get() else 0
            symbol = self.symbol_var.get()
            
            if self.transaction_var.get() == "SELL":
                # Check available shares
                portfolio = self.data_manager.get_portfolio()
                available = portfolio.positions.get(symbol, None)
                if available and quantity > available.quantity:
                    self.quantity_var.set(str(available.quantity))
            elif self.transaction_var.get() == "BUY":
                # Check available cash
                stock_data = self.data_manager.get_stock_prices()
                if symbol in stock_data:
                    price = stock_data[symbol].current_price
                    portfolio = self.data_manager.get_portfolio()
                    max_quantity = int(portfolio.cash_balance / price) if price > 0 else 0
                    if quantity > max_quantity:
                        self.quantity_var.set(str(max_quantity))
            
            self.update_cost_estimate()
        except (ValueError, TypeError):
            pass
    
    def update_available_display(self):
        """Update available quantity/cash display"""
        symbol = self.symbol_var.get()
        portfolio = self.data_manager.get_portfolio()
        
        if self.transaction_var.get() == "SELL":
            if symbol in portfolio.positions:
                available = portfolio.positions[symbol].quantity
                self.available_label.config(text=f"Available: {available:,} shares")
            else:
                self.available_label.config(text="Available: 0 shares")
        else:  # BUY
            self.available_label.config(text=f"Available: ${portfolio.cash_balance:,.2f}")
    
    def update_cost_estimate(self):
        """Update estimated cost/proceeds"""
        try:
            symbol = self.symbol_var.get()
            quantity = int(self.quantity_var.get()) if self.quantity_var.get() else 0
            
            if not symbol or quantity <= 0:
                self.cost_label.config(text="$0.00")
                return
            
            stock_data = self.data_manager.get_stock_prices()
            if symbol not in stock_data:
                return
            
            # Determine price
            if self.order_type_var.get() == "LIMIT" and self.limit_price_var.get():
                try:
                    price = float(self.limit_price_var.get())
                except ValueError:
                    price = stock_data[symbol].current_price
            else:
                price = stock_data[symbol].current_price
            
            # Calculate cost/proceeds
            subtotal = quantity * price
            
            if self.transaction_var.get() == "BUY":
                commission = subtotal * 0.00015  # 0.015% commission
                total = subtotal + commission
                self.cost_label.config(text=f"${total:.2f} (includes commission)")
            else:  # SELL
                commission = subtotal * 0.00015
                tax = subtotal * 0.0025  # 0.25% tax
                total = subtotal - commission - tax
                self.cost_label.config(text=f"${total:.2f} (after fees)")
                
        except (ValueError, TypeError):
            self.cost_label.config(text="$0.00")
    
    def place_order(self):
        """Place the order"""
        try:
            # Validate inputs
            symbol = self.symbol_var.get()
            if not symbol:
                raise ValueError("Please select a stock symbol")
            
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Please enter a valid quantity")
            
            # Determine price for limit orders
            price = None
            if self.order_type_var.get() == "LIMIT":
                price = float(self.limit_price_var.get())
                if price <= 0:
                    raise ValueError("Please enter a valid limit price")
            
            # Create order request
            order = OrderRequest(
                symbol=symbol,
                transaction_type=TransactionType(self.transaction_var.get()),
                order_type=OrderType(self.order_type_var.get()),
                quantity=quantity,
                limit_price=price
            )
            
            # Execute order
            success, message = self.data_manager.place_order(order)
            
            if success:
                self.clear_order_form()
                if hasattr(self.main_app, 'show_success'):
                    self.main_app.show_success("Order Placed", message)
                if self.on_order_placed:
                    self.on_order_placed()
            else:
                if hasattr(self.main_app, 'show_error'):
                    self.main_app.show_error("Order Failed", message)
                
        except ValueError as e:
            if hasattr(self.main_app, 'show_error'):
                self.main_app.show_error("Invalid Input", str(e))
        except Exception as e:
            if hasattr(self.main_app, 'show_error'):
                self.main_app.show_error("Error", f"Failed to place order: {str(e)}")
    
    def clear_order_form(self):
        """Clear the order form"""
        self.quantity_var.set("")
        self.limit_price_var.set("")
        self.cost_label.config(text="$0.00")