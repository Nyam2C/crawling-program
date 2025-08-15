#!/usr/bin/env python3
"""
Kawaii-styled custom dialog boxes for the trading interface
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
import random


class KawaiiMessageBox:
    """Custom kawaii-styled message box"""
    
    def __init__(self, parent, theme_manager, icon_manager):
        self.parent = parent
        self.theme = theme_manager
        self.icon_manager = icon_manager
        self.colors = theme_manager.colors
        self.result = None
    
    def show_info(self, title: str, message: str, icon_key: str = 'sparkle') -> None:
        """Show kawaii info dialog"""
        self._create_dialog(title, message, 'info', icon_key, ['OK'])
    
    def show_success(self, title: str, message: str, icon_key: str = 'heart') -> None:
        """Show kawaii success dialog"""
        self._create_dialog(title, message, 'success', icon_key, ['OK'])
    
    def show_warning(self, title: str, message: str, icon_key: str = 'bow') -> None:
        """Show kawaii warning dialog"""
        self._create_dialog(title, message, 'warning', icon_key, ['OK'])
    
    def show_question(self, title: str, message: str, icon_key: str = 'glasses') -> bool:
        """Show kawaii yes/no question dialog"""
        self._create_dialog(title, message, 'question', icon_key, ['Yes', 'No'])
        return self.result == 'Yes'
    
    def show_error(self, title: str, message: str, icon_key: str = 'skull') -> None:
        """Show kawaii error dialog"""
        self._create_dialog(title, message, 'error', icon_key, ['OK'])
    
    def _create_dialog(self, title: str, message: str, dialog_type: str, icon_key: str, buttons: list):
        """Create the actual dialog window"""
        # Create dialog window
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.configure(bg=self.colors['bg'])
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog - smaller size
        dialog.update_idletasks()
        width = 320
        height = 220
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main frame - reduced padding
        main_frame = ttk.Frame(dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon section
        icon_frame = ttk.Frame(main_frame)
        icon_frame.pack(pady=(0, 15))
        
        # Get and display icon
        icon = self.icon_manager.get_icon(icon_key)
        if icon:
            icon_label = ttk.Label(icon_frame, image=icon)
            icon_label.pack()
        
        # Add some kawaii decoration based on type
        kawaii_text = self._get_kawaii_decoration(dialog_type)
        if kawaii_text:
            kawaii_label = ttk.Label(icon_frame, text=kawaii_text, 
                                   foreground=self.colors['magenta'],
                                   font=('Arial', 12))
            kawaii_label.pack(pady=(5, 0))
        
        # Title
        title_label = ttk.Label(main_frame, text=title,
                               font=('Arial', 14, 'bold'),
                               foreground=self.colors['text'])
        title_label.pack(pady=(0, 10))
        
        # Message
        message_label = ttk.Label(main_frame, text=message,
                                 font=('Arial', 9),
                                 foreground=self.colors['text_muted'],
                                 wraplength=280,
                                 justify=tk.CENTER)
        message_label.pack(pady=(0, 15))
        
        # Buttons frame - centered
        button_frame = ttk.Frame(main_frame)
        if len(buttons) == 1:  # For single button, ensure perfect centering
            button_frame.pack(anchor=tk.CENTER, expand=True, fill=tk.X)
        else:
            button_frame.pack(anchor=tk.CENTER)
        
        # Create buttons - smaller and centered with proper spacing
        for i, button_text in enumerate(buttons):
            style = self._get_button_style(button_text, dialog_type)
            btn = ttk.Button(button_frame, text=button_text,
                           style=style, width=10,
                           command=lambda text=button_text: self._on_button_click(dialog, text))
            if len(buttons) == 2:  # For Yes/No dialogs, center both buttons
                btn.pack(side=tk.LEFT, padx=(8 if i > 0 else 8, 8))
            elif len(buttons) == 1:  # For single button dialogs (like OK), center the button
                btn.pack(padx=8, pady=4)
            else:
                btn.pack(side=tk.LEFT, padx=(8 if i > 0 else 0, 0))
        
        # Focus first button
        if buttons:
            dialog.focus_set()
        
        # Wait for dialog to close
        dialog.wait_window()
    
    def _get_kawaii_decoration(self, dialog_type: str) -> str:
        """Get kawaii decoration text based on dialog type"""
        decorations = {
            'success': ['Success!', 'Done!', 'Complete!', 'Great!'],
            'info': ['Info', 'Notice', 'FYI', 'Note'],
            'warning': ['Warning', 'Caution', 'Alert', 'Notice'],
            'error': ['Error', 'Failed', 'Problem', 'Issue'],
            'question': ['Question', 'Confirm', 'Please Choose', 'Decision']
        }
        return random.choice(decorations.get(dialog_type, ['Notice']))
    
    def _get_button_style(self, button_text: str, dialog_type: str) -> str:
        """Get appropriate button style"""
        if button_text in ['OK', 'Yes']:
            if dialog_type == 'success':
                return 'Pastel.Success.TButton'
            elif dialog_type == 'error':
                return 'Pastel.Danger.TButton'
            else:
                return 'Pastel.Primary.TButton'
        elif button_text == 'No':
            return 'Pastel.Secondary.TButton'
        else:
            return 'Pastel.Ghost.TButton'
    
    def _on_button_click(self, dialog: tk.Toplevel, button_text: str):
        """Handle button click"""
        self.result = button_text
        dialog.destroy()


class KawaiiInputDialog:
    """Custom kawaii-styled input dialog"""
    
    def __init__(self, parent, theme_manager, icon_manager):
        self.parent = parent
        self.theme = theme_manager
        self.icon_manager = icon_manager
        self.colors = theme_manager.colors
        self.result = None
    
    def ask_float(self, title: str, prompt: str, initial_value: float = 0.0, 
                  min_value: float = 0.0, max_value: float = float('inf'),
                  icon_key: str = 'folder') -> Optional[float]:
        """Ask for float input with kawaii styling"""
        return self._create_input_dialog(title, prompt, 'float', initial_value, 
                                       min_value, max_value, icon_key)
    
    def ask_string(self, title: str, prompt: str, initial_value: str = "",
                   icon_key: str = 'folder') -> Optional[str]:
        """Ask for string input with kawaii styling"""
        return self._create_input_dialog(title, prompt, 'string', initial_value, 
                                       icon_key=icon_key)
    
    def _create_input_dialog(self, title: str, prompt: str, input_type: str,
                           initial_value=None, min_value: float = 0.0, 
                           max_value: float = float('inf'), icon_key: str = 'folder'):
        """Create input dialog"""
        # Create dialog window
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.configure(bg=self.colors['bg'])
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        width = 400
        height = 250
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main frame - reduced padding
        main_frame = ttk.Frame(dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon section
        icon_frame = ttk.Frame(main_frame)
        icon_frame.pack(pady=(0, 15))
        
        icon = self.icon_manager.get_icon(icon_key)
        if icon:
            icon_label = ttk.Label(icon_frame, image=icon)
            icon_label.pack()
        
        # Kawaii decoration
        kawaii_label = ttk.Label(icon_frame, text='Input Required',
                               foreground=self.colors['magenta'],
                               font=('Arial', 10))
        kawaii_label.pack(pady=(5, 0))
        
        # Title
        title_label = ttk.Label(main_frame, text=title,
                               font=('Arial', 14, 'bold'),
                               foreground=self.colors['text'])
        title_label.pack(pady=(0, 10))
        
        # Prompt
        prompt_label = ttk.Label(main_frame, text=prompt,
                                font=('Arial', 10),
                                foreground=self.colors['text_muted'],
                                wraplength=350)
        prompt_label.pack(pady=(0, 15))
        
        # Input field
        input_var = tk.StringVar()
        if initial_value is not None:
            input_var.set(str(initial_value))
        
        input_entry = ttk.Entry(main_frame, textvariable=input_var, width=30,
                               font=('Arial', 11))
        input_entry.pack(pady=(0, 20))
        input_entry.focus_set()
        input_entry.select_range(0, tk.END)
        
        # Validation function
        def validate_and_submit():
            value = input_var.get().strip()
            if not value:
                self.result = None
                dialog.destroy()
                return
            
            try:
                if input_type == 'float':
                    float_value = float(value)
                    if float_value < min_value or float_value > max_value:
                        # Show error with kawaii dialog
                        error_dlg = KawaiiMessageBox(dialog, self.theme, self.icon_manager)
                        error_dlg.show_error("Invalid Input", 
                                           f"Value must be between {min_value:,.0f} and {max_value:,.0f}")
                        return
                    self.result = float_value
                else:
                    self.result = value
                dialog.destroy()
            except ValueError:
                error_dlg = KawaiiMessageBox(dialog, self.theme, self.icon_manager)
                error_dlg.show_error("Invalid Input", "Please enter a valid number")
        
        # Buttons frame - centered like other dialogs
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(anchor=tk.CENTER)
        
        ok_btn = ttk.Button(button_frame, text="OK",
                          style='Pastel.Success.TButton', width=10,
                          command=validate_and_submit)
        ok_btn.pack(side=tk.LEFT, padx=(8, 8))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel",
                              style='Pastel.Secondary.TButton', width=10,
                              command=lambda: [setattr(self, 'result', None), dialog.destroy()])
        cancel_btn.pack(side=tk.LEFT, padx=(8, 8))
        
        # Bind Enter key
        input_entry.bind('<Return>', lambda e: validate_and_submit())
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return self.result


class TradingHelpDialog:
    """Comprehensive help dialog for mock trading"""
    
    def __init__(self, parent, theme_manager, icon_manager):
        self.parent = parent
        self.theme = theme_manager
        self.icon_manager = icon_manager
        self.colors = theme_manager.colors
    
    def show_help(self):
        """Show the trading help dialog"""
        # Create help window
        help_window = tk.Toplevel(self.parent)
        help_window.title("Mock Trading Help Guide")
        help_window.configure(bg=self.colors['bg'])
        help_window.resizable(True, True)
        help_window.transient(self.parent)
        help_window.grab_set()
        
        # Set window size and center
        width = 700
        height = 600
        x = (help_window.winfo_screenwidth() // 2) - (width // 2)
        y = (help_window.winfo_screenheight() // 2) - (height // 2)
        help_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main frame with padding
        main_frame = ttk.Frame(help_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title section
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Icon
        icon = self.icon_manager.get_icon('glasses')
        if icon:
            icon_label = ttk.Label(title_frame, image=icon)
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = ttk.Label(title_frame, 
                               text="Mock Trading Guide",
                               font=('Arial', 16, 'bold'),
                               foreground=self.colors['magenta'])
        title_label.pack(side=tk.LEFT)
        
        # Create notebook for different help sections
        help_notebook = ttk.Notebook(main_frame)
        help_notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Getting Started tab
        self._create_getting_started_tab(help_notebook)
        
        # How to Trade tab
        self._create_trading_tab(help_notebook)
        
        # Portfolio Management tab
        self._create_portfolio_tab(help_notebook)
        
        # Tips & Tricks tab
        self._create_tips_tab(help_notebook)
        
        # Close button - perfectly centered, bold, and compact
        button_container = ttk.Frame(main_frame)
        button_container.pack(pady=15, fill=tk.X)
        
        # Create centering frame to ensure perfect alignment
        center_frame = ttk.Frame(button_container)
        center_frame.pack(expand=True)
        
        close_btn = ttk.Button(center_frame, text="Got It!",
                             style='Pastel.Primary.TButton',
                             command=help_window.destroy)
        close_btn.pack()
        
        # Configure button styling for bold text and compact size
        close_btn.configure(width=12)  # Reduced width
    
    def _create_getting_started_tab(self, notebook):
        """Create getting started help tab"""
        frame = ttk.Frame(notebook, padding="15")
        notebook.add(frame, text="Getting Started")
        
        # Create scrollable text
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, 
                             bg=self.colors['panel'], fg=self.colors['text'],
                             yscrollcommand=scrollbar.set,
                             font=('Arial', 10), height=20)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        content = """
Welcome to Mock Trading!

Mock Trading is a safe environment where you can practice trading stocks without real money!

STEP 1: Add Stocks to Watch
• Go to the "Trading" tab
• In the "Stock Search" section, type a stock symbol (like AAPL, GOOGL, TSLA)
• Click "Search & Add" - the stock will be added to your watchlist
• You'll see the current price displayed

STEP 2: Select a Stock to Trade
• In the "Watched Stocks" list, double-click any stock
• The stock will be selected for trading (shown in the order form)

STEP 3: Your Virtual Money
• You start with $100,000 virtual cash
• This appears in the "Portfolio Summary" at the top
• You can reset your account anytime with "Reset Portfolio"

STEP 4: Understanding the Interface
• Portfolio Summary: Shows your cash, total value, and profit/loss
• Trading Tab: Where you buy and sell stocks
• Portfolio Tab: Shows all your stock holdings
• History Tab: Shows all your past transactions

Ready to make your first trade? Check the "How to Trade" tab!
"""
        
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
    
    def _create_trading_tab(self, notebook):
        """Create trading help tab"""
        frame = ttk.Frame(notebook, padding="15")
        notebook.add(frame, text="How to Trade")
        
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD,
                             bg=self.colors['panel'], fg=self.colors['text'],
                             yscrollcommand=scrollbar.set,
                             font=('Arial', 10), height=20)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        content = """
HOW TO BUY STOCKS

SELECT A STOCK:
• Double-click a stock from your "Watched Stocks" list
• The stock symbol will appear in the order form

CHOOSE ORDER TYPE:
• Market: Buy at current price immediately
• Limit: Set your own price (good for waiting for better deals)

CHOOSE ACTION:
• Buy: Purchase shares (you need enough cash)
• Sell: Sell shares you own (you need to own them first)

ENTER QUANTITY:
• Type how many shares you want to buy/sell
• Example: "10" means 10 shares

SET LIMIT PRICE (if using Limit orders):
• Only for Limit orders
• Set the maximum price you're willing to pay (buy)
• Or minimum price you're willing to accept (sell)

CHECK ESTIMATED COST:
• The system shows you how much it will cost
• Includes commissions and fees

PLACE ORDER:
• Click "Place Order" button
• If successful, you'll see a confirmation

EXAMPLE TRADE

Let's buy 5 shares of AAPL:
1. Add AAPL to watchlist
2. Double-click AAPL in watched stocks
3. Select "Market" order type
4. Select "Buy" action  
5. Enter "5" for quantity
6. Click "Place Order"
7. Success! You now own 5 AAPL shares

The estimated cost will show before you buy!
"""
        
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
    
    def _create_portfolio_tab(self, notebook):
        """Create portfolio management help tab"""
        frame = ttk.Frame(notebook, padding="15")
        notebook.add(frame, text="Portfolio Management")
        
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD,
                             bg=self.colors['panel'], fg=self.colors['text'],
                             yscrollcommand=scrollbar.set,
                             font=('Arial', 10), height=20)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        content = """
UNDERSTANDING YOUR PORTFOLIO

PORTFOLIO SUMMARY (Top of screen):
• Cash: Money available to buy stocks
• Total Value: Cash + value of all your stocks
• P&L: Profit & Loss (how much you've made/lost)

PORTFOLIO TAB - Your Holdings:
• Symbol: Stock ticker (AAPL, GOOGL, etc.)
• Quantity: How many shares you own
• Avg Price: Average price you paid per share
• Current Price: Current market price per share
• Market Value: Current total value of your position
• P&L: Profit/Loss on this specific stock
• P&L %: Percentage profit/loss

HISTORY TAB - Your Transactions:
• Shows every buy/sell you've made
• Date, stock, quantity, price, fees
• Use this to track your trading activity

AUTOMATIC UPDATES:
• Stock prices update every 5 seconds automatically
• You can also click "Refresh" for manual updates
• Portfolio values update in real-time

READING YOUR PERFORMANCE:
• Green numbers = Profit (good!)
• Red numbers = Loss (learning opportunity!)
• P&L % shows your return rate

PORTFOLIO TIPS:
• Diversify: Don't put all money in one stock
• Watch your cash: Keep some for new opportunities  
• Monitor P&L: Learn from both wins and losses
• Use History tab to review your decisions

RESET PORTFOLIO:
• Click "Reset Portfolio" to start over
• Choose new starting amount
• All positions and history will be cleared
"""
        
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
    
    def _create_tips_tab(self, notebook):
        """Create tips and tricks tab"""
        frame = ttk.Frame(notebook, padding="15")
        notebook.add(frame, text="Tips & Tricks")
        
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD,
                             bg=self.colors['panel'], fg=self.colors['text'],
                             yscrollcommand=scrollbar.set,
                             font=('Arial', 10), height=20)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        content = """
TRADING TIPS & TRICKS

BEGINNER STRATEGIES:
• Start small: Buy just a few shares to learn
• Paper trade first: Practice before using real money
• Keep learning: Watch how your stocks perform
• Don't panic: Stock prices go up and down

UNDERSTANDING ORDERS:
• Market Orders: Instant but price may vary slightly
• Limit Orders: Exact price but may not execute immediately
• Use Limit orders when you want control over price

POPULAR STOCKS TO PRACTICE WITH:
• AAPL (Apple) - Stable tech company
• GOOGL (Google) - Search engine giant  
• TSLA (Tesla) - Electric vehicle leader
• MSFT (Microsoft) - Software giant
• AMZN (Amazon) - E-commerce leader
• NVDA (NVIDIA) - AI/Graphics chips

MONEY MANAGEMENT:
• Don't invest all your cash at once
• Keep 20-30% in cash for opportunities
• Set stop-losses: Sell if stock drops too much
• Take profits: Don't be greedy

PRACTICE SCENARIOS:
1. Buy 10 AAPL shares, watch for a week
2. Try a limit order below current price
3. Practice selling when you're up 5%
4. Experience buying the dip (when stock falls)

COMMON MISTAKES TO AVOID:
• Buying without research
• Putting all money in one stock
• Panic selling during small drops
• FOMO (Fear of Missing Out) buying
• Not setting stop-losses

KEYBOARD SHORTCUTS:
• Double-click stocks to select for trading
• Enter key submits forms
• Tab to move between fields

INTERFACE TIPS:
• Colors: Green = profit, Red = loss
• Refresh button updates all prices
• Portfolio summary shows total performance
• History tab is great for learning from trades

Remember: This is practice! Make mistakes, learn, and have fun!
"""
        
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)