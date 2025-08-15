#!/usr/bin/env python3
"""Stock Data Tab Component - Retro Pastel Style"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from src.core.config import MAGNIFICENT_SEVEN, STOCK_CATEGORIES


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
        icon = self.main_app.icon_manager.get_icon('tab_data')
        self.notebook.add(self.frame, text='Stock Data', image=icon, compound='left')
        
        # Configure grid
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        # Control panel
        self.create_control_panel()
        
        # Stock data display
        self.create_data_display()
        
    def create_control_panel(self):
        """Create control panel with cool buttons"""
        control_frame = ttk.LabelFrame(self.frame, text="Control Panel", padding="15")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Category buttons with icons (replacing Get All)
        self.main_app.icon_button(control_frame, 'get_all', 'Magnificent 7', 
                                  lambda: self.get_category_data('magnificent_seven')).grid(row=0, column=0, padx=(0, 10))
                  
        self.main_app.icon_button(control_frame, 'refresh', 'Refresh',
                                  self.refresh_stock_data, style='Pastel.Ghost.TButton').grid(row=0, column=1, padx=(0, 10))
        
        # Stock search/input (keeping same visual style)
        ttk.Label(control_frame, text="Enter Symbol:",
                 foreground=self.colors['text']).grid(row=0, column=2, padx=(20, 5))
        
        self.stock_var = tk.StringVar()
        # Changed from readonly Combobox to Entry for typing, but keeping same style
        self.stock_entry = ttk.Entry(control_frame, textvariable=self.stock_var, 
                                    width=12, style='Pastel.TEntry')
        self.stock_entry.grid(row=0, column=3, padx=(0, 10))
        self.stock_entry.insert(0, 'AAPL')  # Default 
        
        # Bind enter key and real-time validation
        self.stock_entry.bind('<KeyRelease>', self.on_symbol_change)
        self.stock_entry.bind('<Return>', lambda e: self.get_single_stock_data())
        
        # Validation label (same styling)
        self.validation_label = ttk.Label(control_frame, text="", 
                                         foreground=self.colors['text_accent'])
        self.validation_label.grid(row=1, column=3, padx=(0, 10))
        
        self.main_app.icon_button(control_frame, 'get_one', 'Get Stock', 
                                  self.get_single_stock_data).grid(row=0, column=4)
        
    def create_data_display(self):
        """Create data display area"""
        data_frame = ttk.LabelFrame(self.frame, text="Stock Information", padding="15")
        data_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        data_frame.grid_rowconfigure(0, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)
        
        # Create treeview for stock data
        columns = ('Symbol', 'Company', 'Price', 'Change', 'Change %', 'Market Cap', 'Volume')
        self.stock_tree = ttk.Treeview(data_frame, columns=columns, show='headings', 
                                     height=15, style='Pastel.Treeview')
        
        for col in columns:
            self.stock_tree.heading(col, text=col)
            self.stock_tree.column(col, width=120)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, 
                                   command=self.stock_tree.yview,
                                   style='Pastel.Vertical.TScrollbar')
        scrollbar_x = ttk.Scrollbar(data_frame, orient=tk.HORIZONTAL, 
                                   command=self.stock_tree.xview,
                                   style='Pastel.Horizontal.TScrollbar')
        self.stock_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.stock_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configure alternating row colors for better readability
        self.stock_tree.tag_configure('oddrow',  background=self.colors['panel_alt'])
        self.stock_tree.tag_configure('evenrow', background=self.colors['panel_light'])
        
        # Add right-click context menu for removing stocks
        self.setup_context_menu()
        
    def on_symbol_change(self, event=None):
        """Handle symbol input changes for real-time validation"""
        symbol = self.stock_var.get().upper().strip()
        
        if not symbol:
            self.validation_label.config(text="", foreground=self.colors['text_accent'])
            return
        
        # Basic format check
        if not symbol.replace('.', '').isalpha() or len(symbol) > 5:
            self.validation_label.config(text="Invalid format", foreground=self.colors['text'])
            return
        
        # Show suggestions for partial symbols
        if len(symbol) >= 1:
            suggestions = self.main_app.stock_crawler.get_stock_suggestions(symbol)
            if suggestions and symbol in suggestions:
                self.validation_label.config(text="Valid", foreground=self.colors['text_accent'])
            elif suggestions:
                self.validation_label.config(text=f"Try: {', '.join(suggestions[:3])}", 
                                           foreground=self.colors['text_accent'])
            else:
                self.validation_label.config(text="Checking...", foreground=self.colors['text'])
    
    def get_category_data(self, category_key):
        """Get data for a stock category"""
        def fetch_data():
            try:
                category_name = STOCK_CATEGORIES[category_key]['name']
                self.main_app.update_status(f"Fetching {category_name} data...")
                self.main_app.show_progress()
                
                data = self.main_app.stock_crawler.get_category_stocks_data(category_key)
                self.main_app.current_stock_data = data
                
                # Update UI in main thread
                self.main_app.root.after(0, self.update_stock_display, data)
                self.main_app.root.after(0, self.main_app.update_status, f"{category_name} data collection completed!")
                self.main_app.root.after(0, self.main_app.hide_progress)
                
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"Error fetching category data: {str(e)}")
                self.main_app.root.after(0, self.main_app.hide_progress)
                self.main_app.root.after(0, self.main_app.update_status, "Ready")
        
        thread = threading.Thread(target=fetch_data)
        thread.daemon = True
        thread.start()
        
    def get_all_stocks_data(self):
        """Legacy method - get Magnificent Seven data"""
        self.get_category_data('magnificent_seven')
        
    def get_single_stock_data(self):
        """Get data for a single entered stock symbol"""
        symbol = self.stock_var.get().upper().strip()
        if not symbol:
            messagebox.showwarning("Warning", "Please enter a stock symbol first!")
            return
            
        def fetch_data():
            try:
                self.main_app.update_status(f"Fetching {symbol} data (,,>﹏<,,)...")
                self.main_app.show_progress()
                
                data = self.main_app.stock_crawler.get_stock_data(symbol)
                
                if data:
                    # Add new stock to existing data instead of replacing
                    if not hasattr(self.main_app, 'current_stock_data') or not self.main_app.current_stock_data:
                        self.main_app.current_stock_data = {}
                    
                    self.main_app.current_stock_data[symbol] = data
                    
                    if 'error' not in data:
                        # Success case - show data even if it's fallback data
                        self.main_app.root.after(0, self.update_single_stock_in_display, symbol, data)
                        
                        if data.get('source') == 'fallback':
                            self.main_app.root.after(0, self.main_app.update_status, f"{symbol} loaded (limited data) (,,>﹏<,,)")
                        else:
                            self.main_app.root.after(0, self.main_app.update_status, f"{symbol} data loaded successfully!")
                        
                        self.main_app.root.after(0, self.main_app.hide_progress)
                    else:
                        # Error case
                        error_msg = data.get('error', f'Unknown error for {symbol}')
                        self.main_app.root.after(0, self.main_app.show_error, f"Invalid Symbol: {error_msg}")
                        self.main_app.root.after(0, self.main_app.hide_progress)
                        self.main_app.root.after(0, self.main_app.update_status, "Ready to analyze (,,>﹏<,,)")
                else:
                    self.main_app.root.after(0, self.main_app.show_error, f"No data received for {symbol}")
                    self.main_app.root.after(0, self.main_app.hide_progress)
                    self.main_app.root.after(0, self.main_app.update_status, "Ready to analyze (,,>﹏<,,)")
                    
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"Error fetching {symbol} data: {str(e)}")
                self.main_app.root.after(0, self.main_app.hide_progress)
                self.main_app.root.after(0, self.main_app.update_status, "Error occurred")
        
        thread = threading.Thread(target=fetch_data)
        thread.daemon = True
        thread.start()
        
    def refresh_stock_data(self):
        """Refresh current stock data - keeps existing stock list"""
        if hasattr(self.main_app, 'current_stock_data') and self.main_app.current_stock_data:
            # Get list of currently loaded symbols
            current_symbols = list(self.main_app.current_stock_data.keys())
            
            if current_symbols:
                # Refresh all currently loaded stocks
                def refresh_data():
                    try:
                        self.main_app.update_status(f"Refreshing {len(current_symbols)} stocks...")
                        self.main_app.show_progress()
                        
                        refreshed_data = {}
                        for symbol in current_symbols:
                            print(f"Refreshing {symbol}...")
                            stock_data = self.main_app.stock_crawler.get_stock_data(symbol)
                            if stock_data:
                                refreshed_data[symbol] = stock_data
                        
                        # Update the main data and UI
                        self.main_app.current_stock_data = refreshed_data
                        
                        # Update UI in main thread
                        self.main_app.root.after(0, self.update_stock_display, refreshed_data)
                        self.main_app.root.after(0, self.main_app.update_status, f"Refreshed {len(refreshed_data)} stocks successfully!")
                        self.main_app.root.after(0, self.main_app.hide_progress)
                        
                    except Exception as e:
                        self.main_app.root.after(0, self.main_app.show_error, f"Error refreshing data: {str(e)}")
                        self.main_app.root.after(0, self.main_app.hide_progress)
                        self.main_app.root.after(0, self.main_app.update_status, "Refresh failed (,,>﹏<,,)")
                
                # Run in separate thread
                import threading
                thread = threading.Thread(target=refresh_data)
                thread.daemon = True
                thread.start()
            else:
                messagebox.showinfo("Info", "No stocks to refresh!")
        else:
            messagebox.showinfo("Info", "No data to refresh. Please fetch stock data first!")
            
    def update_stock_display(self, data):
        """Update the stock data treeview"""
        # Clear existing data
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
            
        # Add new data with alternating row colors
        for i, (symbol, stock_data) in enumerate(data.items()):
            if stock_data:
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.stock_tree.insert('', 'end', values=(
                    stock_data.get('symbol', ''),
                    stock_data.get('company', ''),
                    stock_data.get('current_price', ''),
                    stock_data.get('change', ''),
                    stock_data.get('change_percent', ''),
                    stock_data.get('market_cap', ''),
                    stock_data.get('volume', '')
                ), tags=(tag,))
                
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
    
    def update_single_stock_in_display(self, symbol, data):
        """Add or update single stock in the display"""
        # Remove existing entry for this symbol if it exists
        for item in self.stock_tree.get_children():
            if self.stock_tree.item(item, 'values')[0] == symbol:
                self.stock_tree.delete(item)
                break
        
        # Add new/updated data
        # Determine row color based on current row count
        row_count = len(self.stock_tree.get_children())
        tag = 'evenrow' if row_count % 2 == 0 else 'oddrow'
        
        self.stock_tree.insert('', 'end', values=(
            data.get('symbol', ''),
            data.get('company', ''),
            data.get('current_price', ''),
            data.get('change', ''),
            data.get('change_percent', ''),
            data.get('market_cap', ''),
            data.get('volume', '')
        ), tags=(tag,))
    
    def setup_context_menu(self):
        """Setup right-click context menu for stock list"""
        self.context_menu = tk.Menu(self.main_app.root, tearoff=0,
                                   bg=self.colors['panel_light'], 
                                   fg=self.colors['text'],
                                   activebackground=self.colors['periwinkle'],
                                   activeforeground='#1B1350',
                                   borderwidth=1,
                                   relief='solid')
        
        self.context_menu.add_command(label="Remove Stock", command=self.remove_selected_stock)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Refresh This Stock", command=self.refresh_selected_stock)
        
        # Bind right-click to treeview
        self.stock_tree.bind("<Button-3>", self.show_context_menu)  # Right click
        
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Identify the clicked item
        item = self.stock_tree.identify_row(event.y)
        if item:
            # Select the item
            self.stock_tree.selection_set(item)
            self.stock_tree.focus(item)
            
            # Show context menu
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
    
    def remove_selected_stock(self):
        """Remove selected stock from the list"""
        selected_items = self.stock_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a stock to remove!")
            return
        
        # Get symbol from selected item
        item = selected_items[0]
        values = self.stock_tree.item(item, 'values')
        if values:
            symbol = values[0]  # First column is symbol
            
            # Use custom styled confirmation dialog
            if self._show_styled_confirmation("Confirm Remove", 
                                            f"Remove {symbol} from the list?\n\nThis will not affect other stocks."):
                
                # Remove from UI
                self.stock_tree.delete(item)
                
                # Remove from data
                if hasattr(self.main_app, 'current_stock_data') and self.main_app.current_stock_data:
                    if symbol in self.main_app.current_stock_data:
                        del self.main_app.current_stock_data[symbol]
                
                self.main_app.update_status(f"Removed {symbol} from list")
                
                # Reapply alternating row colors after removal
                self.reapply_row_colors()
    
    def refresh_selected_stock(self):
        """Refresh data for selected stock only"""
        selected_items = self.stock_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a stock to refresh!")
            return
        
        # Get symbol from selected item
        item = selected_items[0]
        values = self.stock_tree.item(item, 'values')
        if values:
            symbol = values[0]  # First column is symbol
            
            def refresh_single():
                try:
                    self.main_app.update_status(f"Refreshing {symbol}...")
                    self.main_app.show_progress()
                    
                    # Get fresh data
                    stock_data = self.main_app.stock_crawler.get_stock_data(symbol)
                    
                    if stock_data:
                        # Update data
                        if not hasattr(self.main_app, 'current_stock_data'):
                            self.main_app.current_stock_data = {}
                        self.main_app.current_stock_data[symbol] = stock_data
                        
                        # Update UI
                        self.main_app.root.after(0, self.update_single_stock_in_display, symbol, stock_data)
                        
                        if stock_data.get('source') == 'fallback':
                            self.main_app.root.after(0, self.main_app.update_status, f"{symbol} refreshed (limited data)")
                        else:
                            self.main_app.root.after(0, self.main_app.update_status, f"{symbol} refreshed successfully!")
                    else:
                        self.main_app.root.after(0, self.main_app.show_error, f"Failed to refresh {symbol}")
                        self.main_app.root.after(0, self.main_app.update_status, "Refresh failed (,,>﹏<,,)")
                    
                    self.main_app.root.after(0, self.main_app.hide_progress)
                    
                except Exception as e:
                    self.main_app.root.after(0, self.main_app.show_error, f"Error refreshing {symbol}: {str(e)}")
                    self.main_app.root.after(0, self.main_app.hide_progress)
                    self.main_app.root.after(0, self.main_app.update_status, "Error occurred")
            
            # Run in separate thread
            import threading
            thread = threading.Thread(target=refresh_single)
            thread.daemon = True
            thread.start()
    
    def reapply_row_colors(self):
        """Reapply alternating row colors after modifications"""
        children = self.stock_tree.get_children()
        for i, child in enumerate(children):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.stock_tree.item(child, tags=(tag,))
    
    def _show_styled_confirmation(self, title, message):
        """Show custom styled confirmation dialog matching the retro pastel theme"""
        # Create custom dialog window
        dialog = tk.Toplevel(self.main_app.root)
        dialog.title(title)
        dialog.configure(bg=self.colors['panel'])
        dialog.resizable(False, False)
        dialog.grab_set()  # Make dialog modal
        
        # Set dialog size and center it
        dialog.geometry("350x180")
        dialog.transient(self.main_app.root)
        
        # Position dialog in center of parent window
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (180 // 2)
        dialog.geometry(f"350x180+{x}+{y}")
        
        # Main frame with padding
        main_frame = ttk.Frame(dialog, padding="20", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message label with retro styling
        message_label = ttk.Label(main_frame, text=message, 
                                foreground=self.colors['text'],
                                background=self.colors['panel'],
                                font=('Arial', 11),
                                justify=tk.CENTER)
        message_label.pack(pady=(10, 20))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # Result variable
        result = tk.BooleanVar()
        
        # Yes button (styled to match theme)
        yes_btn = ttk.Button(button_frame, text="Yes", 
                           style='Pastel.Primary.TButton',
                           command=lambda: [result.set(True), dialog.destroy()])
        yes_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # No button (styled to match theme)
        no_btn = ttk.Button(button_frame, text="No", 
                          style='Pastel.Ghost.TButton',
                          command=lambda: [result.set(False), dialog.destroy()])
        no_btn.pack(side=tk.RIGHT, padx=(5, 5))
        
        # Focus on No button by default (safer choice)
        no_btn.focus_set()
        
        # Bind Enter to Yes and Escape to No
        dialog.bind('<Return>', lambda e: [result.set(True), dialog.destroy()])
        dialog.bind('<Escape>', lambda e: [result.set(False), dialog.destroy()])
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result.get()