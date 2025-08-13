#!/usr/bin/env python3
"""Stock Data Tab Component - Cool Kuromi Style"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from src.core.config import MAGNIFICENT_SEVEN


class StockDataTab:
    def __init__(self, notebook, main_app):
        self.notebook = notebook
        self.main_app = main_app
        self.colors = main_app.colors
        self.setup_tab()
        
    def setup_tab(self):
        """Create the stock data tab"""
        # Stock Data Frame
        self.frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.frame, text="(@_@) Stock Data")
        
        # Configure grid
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        # Control panel
        self.create_control_panel()
        
        # Stock data display
        self.create_data_display()
        
    def create_control_panel(self):
        """Create control panel with cool buttons"""
        control_frame = ttk.LabelFrame(self.frame, text="(>.<) Control Panel", padding="15")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Main action buttons
        ttk.Button(control_frame, text="(*_*) Get All Stocks", 
                  command=self.get_all_stocks_data,
                  style='Kuromi.Primary.TButton').grid(row=0, column=0, padx=(0, 10))
                  
        ttk.Button(control_frame, text="(^_^) Refresh",
                  command=self.refresh_stock_data,
                  style='Kuromi.Black.TButton').grid(row=0, column=1, padx=(0, 10))
        
        # Stock selection
        ttk.Label(control_frame, text="Choose Stock:",
                 foreground=self.colors['kuromi_primary']).grid(row=0, column=2, padx=(20, 5))
        
        self.stock_var = tk.StringVar()
        stock_combo = ttk.Combobox(control_frame, textvariable=self.stock_var, 
                                  values=list(MAGNIFICENT_SEVEN.keys()), 
                                  state='readonly', width=12,
                                  style='Kuromi.TCombobox')
        stock_combo.grid(row=0, column=3, padx=(0, 10))
        
        ttk.Button(control_frame, text="(>_<) Get Single Stock",
                  command=self.get_single_stock_data,
                  style='Kuromi.Primary.TButton').grid(row=0, column=4)
        
    def create_data_display(self):
        """Create data display area"""
        data_frame = ttk.LabelFrame(self.frame, text="(@_@) Stock Information", padding="15")
        data_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        data_frame.grid_rowconfigure(0, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)
        
        # Create treeview for stock data
        columns = ('Symbol', 'Company', 'Price', 'Change', 'Change %', 'Market Cap', 'Volume')
        self.stock_tree = ttk.Treeview(data_frame, columns=columns, show='headings', 
                                     height=15, style='Kuromi.Treeview')
        
        for col in columns:
            self.stock_tree.heading(col, text=col)
            self.stock_tree.column(col, width=120)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, 
                                   command=self.stock_tree.yview,
                                   style='Kuromi.Vertical.TScrollbar')
        scrollbar_x = ttk.Scrollbar(data_frame, orient=tk.HORIZONTAL, 
                                   command=self.stock_tree.xview,
                                   style='Kuromi.Horizontal.TScrollbar')
        self.stock_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.stock_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def get_all_stocks_data(self):
        """Get data for all stocks in a separate thread"""
        def fetch_data():
            try:
                self.main_app.update_status("(*_*) Fetching all stock data with Kuromi's rebel magic...")
                self.main_app.show_progress()
                
                data = self.main_app.stock_crawler.get_all_stocks_data()
                self.main_app.current_stock_data = data
                
                # Update UI in main thread
                self.main_app.root.after(0, self.update_stock_display, data)
                self.main_app.root.after(0, self.main_app.update_status, "(^_^) Stock data collection completed!")
                self.main_app.root.after(0, self.main_app.hide_progress)
                
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"Error fetching stock data: {str(e)}")
                self.main_app.root.after(0, self.main_app.update_status, "(>_<) Error loading stock data")
                self.main_app.root.after(0, self.main_app.hide_progress)
        
        threading.Thread(target=fetch_data, daemon=True).start()
        
    def get_single_stock_data(self):
        """Get data for a single selected stock"""
        symbol = self.stock_var.get()
        if not symbol:
            messagebox.showwarning("Warning", "Please select a stock symbol first! (>.<)")
            return
            
        def fetch_data():
            try:
                self.main_app.update_status(f"(*_*) Fetching {symbol} data...")
                self.main_app.show_progress()
                
                data = self.main_app.stock_crawler.get_stock_data(symbol)
                if data:
                    single_data = {symbol: data}
                    self.main_app.current_stock_data.update(single_data)
                    self.main_app.root.after(0, self.update_single_stock_display, symbol, data)
                else:
                    self.main_app.root.after(0, self.main_app.show_error, f"Failed to fetch data for {symbol}")
                
                self.main_app.root.after(0, self.main_app.update_status, f"(^_^) {symbol} data loaded")
                self.main_app.root.after(0, self.main_app.hide_progress)
                
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"Error fetching {symbol} data: {str(e)}")
                self.main_app.root.after(0, self.main_app.hide_progress)
        
        threading.Thread(target=fetch_data, daemon=True).start()
        
    def refresh_stock_data(self):
        """Refresh current stock data"""
        if self.main_app.current_stock_data:
            self.get_all_stocks_data()
        else:
            messagebox.showinfo("Info", "No data to refresh. Please fetch stock data first! (^_^)")
            
    def update_stock_display(self, data):
        """Update the stock data treeview"""
        # Clear existing data
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
            
        # Add new data
        for symbol, stock_data in data.items():
            if stock_data:
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