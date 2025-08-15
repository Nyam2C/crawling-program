#!/usr/bin/env python3
"""Scoreboard Tab Component - Arcade Style Leaderboard"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Optional

from src.trading.scoreboard_manager import ScoreboardManager
from src.trading.scoreboard_models import ScoreRecord
from src.gui.components.dialogs import KawaiiMessageBox


class ScoreboardTab:
    def __init__(self, notebook, main_app):
        self.notebook = notebook
        self.main_app = main_app
        self.colors = main_app.colors
        
        # 스코어보드 매니저 초기화
        self.scoreboard_manager = ScoreboardManager()
        
        # Initialize kawaii message box
        self.kawaii_msg = KawaiiMessageBox(self.main_app.root, self.main_app.theme_manager, self.main_app.icon_manager)
        
        self.setup_tab()
        self.refresh_scoreboard()
        
        # 주기적 새로고침 (30초마다)
        self.schedule_refresh()
    
    def setup_tab(self):
        """Create the scoreboard tab"""
        self.frame = ttk.Frame(self.notebook, padding="15")
        icon = self.main_app.icon_manager.get_icon('tab_scoreboard')
        if icon:
            self.notebook.add(self.frame, text='Scoreboard', image=icon, compound='left')
        else:
            self.notebook.add(self.frame, text='Scoreboard')
        
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
        """Create scoreboard header with arcade styling"""
        header_frame = ttk.Frame(self.frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Arcade style title
        title_label = ttk.Label(header_frame, 
                               text="KAWAII STOCK TRADING SCOREBOARD",
                               font=('Arial', 16, 'bold'),
                               foreground=self.colors['magenta'])
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                  text="✨ Hall of Fame - Top Trading Legends ✨",
                                  font=('Arial', 12),
                                  foreground=self.colors['lavender'])
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 15))
        
        # Control buttons
        refresh_btn = self.main_app.icon_button(header_frame, 'refresh', 'Refresh', 
                                               self.refresh_scoreboard,
                                               style='Pastel.Primary.TButton')
        refresh_btn.grid(row=2, column=0, padx=(0, 10), sticky=tk.W)
        
        export_btn = self.main_app.icon_button(header_frame, 'export', 'Export CSV',
                                              self.export_scoreboard,
                                              style='Pastel.Secondary.TButton')
        export_btn.grid(row=2, column=1, padx=(0, 10), sticky=tk.W)
        
        clear_btn = self.main_app.icon_button(header_frame, 'reset', 'Clear All',
                                             self.clear_scoreboard,
                                             style='Pastel.Danger.TButton')
        clear_btn.grid(row=2, column=2, padx=(0, 10), sticky=tk.W)
    
    def create_main_content(self):
        """Create main scoreboard content"""
        main_frame = ttk.Frame(self.frame)
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Leaderboard table
        self.create_leaderboard_table(main_frame)
        
        # Statistics panel
        self.create_statistics_panel(main_frame)
    
    def create_leaderboard_table(self, parent):
        """Create the main leaderboard table"""
        table_frame = ttk.LabelFrame(parent, text="🎮 Leaderboard", padding="10")
        table_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview for scoreboard
        columns = ('rank', 'nickname', 'date', 'return_rate', 'profit_loss', 
                  'holding_period', 'best_stock', 'grade', 'trades')
        
        self.scoreboard_tree = ttk.Treeview(table_frame, columns=columns, 
                                           show='headings', height=15,
                                           style='Pastel.Treeview')
        
        # Define column headings and widths
        column_config = {
            'rank': ('#', 40),
            'nickname': ('Nickname', 100),
            'date': ('Date', 80),
            'return_rate': ('Return %', 80),
            'profit_loss': ('P&L', 100),
            'holding_period': ('Days', 60),
            'best_stock': ('Best Stock', 80),
            'grade': ('Grade', 50),
            'trades': ('Trades', 60)
        }
        
        for col, (heading, width) in column_config.items():
            self.scoreboard_tree.heading(col, text=heading)
            self.scoreboard_tree.column(col, width=width, anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", 
                                   command=self.scoreboard_tree.yview,
                                   style='Pastel.Vertical.TScrollbar')
        self.scoreboard_tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", 
                                   command=self.scoreboard_tree.xview,
                                   style='Pastel.Horizontal.TScrollbar')
        self.scoreboard_tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.scoreboard_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Double-click binding for details
        self.scoreboard_tree.bind('<Double-1>', self.show_record_details)
    
    def create_statistics_panel(self, parent):
        """Create statistics panel"""
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding="10")
        stats_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Statistics content will be created dynamically
        self.stats_content_frame = ttk.Frame(stats_frame)
        self.stats_content_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_footer(self):
        """Create footer with additional info"""
        footer_frame = ttk.Frame(self.frame)
        footer_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(15, 0))
        
        # Info label
        info_text = "💡 Tip: Double-click any record to view detailed information"
        info_label = ttk.Label(footer_frame, text=info_text,
                              foreground=self.colors['text_muted'],
                              font=('Arial', 9))
        info_label.pack(side=tk.LEFT)
        
        # Last updated info
        self.last_updated_label = ttk.Label(footer_frame, text="",
                                           foreground=self.colors['text_muted'],
                                           font=('Arial', 9))
        self.last_updated_label.pack(side=tk.RIGHT)
    
    def refresh_scoreboard(self):
        """Refresh the scoreboard display"""
        # Reload data from file first
        self.scoreboard_manager.load_data()
        
        # Clear current items
        for item in self.scoreboard_tree.get_children():
            self.scoreboard_tree.delete(item)
        
        # Get leaderboard data
        records = self.scoreboard_manager.get_leaderboard(50)  # Top 50
        
        # Populate table
        for rank, record in enumerate(records, 1):
            # Color coding based on performance
            if record.return_rate >= 20:
                tags = ('excellent',)
            elif record.return_rate >= 10:
                tags = ('good',)
            elif record.return_rate >= 0:
                tags = ('neutral',)
            else:
                tags = ('poor',)
            
            self.scoreboard_tree.insert('', 'end', tags=tags, values=(
                rank,
                record.nickname[:12],  # Truncate long nicknames
                record.date.strftime('%m/%d'),
                f"{record.return_rate:.1f}%",
                f"${record.profit_loss:,.0f}",
                f"{record.holding_period_days}d",
                record.best_stock[:6],  # Truncate long symbols
                record.grade,
                record.total_trades
            ))
        
        # Configure row colors
        self.scoreboard_tree.tag_configure('excellent', background='#E8F5E8', foreground='#2E7D2E')
        self.scoreboard_tree.tag_configure('good', background='#E8F0FF', foreground='#1E40AF')
        self.scoreboard_tree.tag_configure('neutral', background='#FFFEF0', foreground='#92400E')
        self.scoreboard_tree.tag_configure('poor', background='#FEE8E8', foreground='#DC2626')
        
        # Update statistics
        self.update_statistics_panel()
        
        # Update footer
        self.last_updated_label.configure(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    def update_statistics_panel(self):
        """Update statistics panel"""
        # Clear current stats
        for widget in self.stats_content_frame.winfo_children():
            widget.destroy()
        
        # Get statistics
        stats = self.scoreboard_manager.get_statistics()
        
        # Create stats display
        stats_data = [
            ("Total Records", f"{stats['total_records']}"),
            ("Average Return", f"{stats['average_return']:.1f}%"),
            ("Best Return", f"{stats['best_return']:.1f}%"),
            ("Worst Return", f"{stats['worst_return']:.1f}%"),
            ("Success Rate", f"{stats['profitable_ratio']:.1f}%")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            label_widget = ttk.Label(self.stats_content_frame, text=f"{label}:",
                                    font=('Arial', 10))
            label_widget.grid(row=i, column=0, sticky=tk.W, padx=(0, 10), pady=2)
            
            value_widget = ttk.Label(self.stats_content_frame, text=value,
                                    font=('Arial', 10, 'bold'),
                                    foreground=self.colors['magenta'])
            value_widget.grid(row=i, column=1, sticky=tk.W, pady=2)
        
        # Grade distribution if available
        if 'grade_distribution' in stats and stats['grade_distribution']:
            ttk.Separator(self.stats_content_frame, orient='horizontal').grid(
                row=len(stats_data), column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 5))
            
            grade_label = ttk.Label(self.stats_content_frame, text="Grade Distribution:",
                                   font=('Arial', 10, 'bold'))
            grade_label.grid(row=len(stats_data)+1, column=0, columnspan=2, sticky=tk.W, pady=(5, 5))
            
            for i, (grade, count) in enumerate(stats['grade_distribution'].items()):
                grade_text = f"{grade}: {count}"
                grade_widget = ttk.Label(self.stats_content_frame, text=grade_text,
                                       font=('Arial', 9))
                grade_widget.grid(row=len(stats_data)+2+i, column=0, columnspan=2, 
                                 sticky=tk.W, padx=(10, 0), pady=1)
    
    def show_record_details(self, event):
        """Show detailed information for selected record"""
        selection = self.scoreboard_tree.selection()
        if not selection:
            return
        
        item = self.scoreboard_tree.item(selection[0])
        values = item['values']
        
        if not values:
            return
        
        # Get the actual record data
        rank = int(values[0])
        records = self.scoreboard_manager.get_leaderboard(50)
        
        if rank <= len(records):
            record = records[rank - 1]
            self._show_record_detail_dialog(record, rank)
    
    def _show_record_detail_dialog(self, record: ScoreRecord, rank: int):
        """Show detailed record information dialog"""
        dialog = tk.Toplevel(self.main_app.root)
        dialog.title(f"Score Details - {record.nickname}")
        dialog.configure(bg=self.colors['bg'])
        dialog.resizable(False, False)
        dialog.transient(self.main_app.root)
        
        # Center dialog
        dialog.update_idletasks()
        width = 400
        height = 500
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Safe grab_set
        try:
            dialog.grab_set()
        except tk.TclError:
            pass
        
        # Content frame
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text=f"#{rank} - {record.nickname}",
                               font=('Arial', 16, 'bold'),
                               foreground=self.colors['magenta'])
        title_label.pack(pady=(0, 20))
        
        # Details
        details = [
            ("Date Recorded", record.date.strftime('%Y-%m-%d %H:%M')),
            ("Grade", f"{record.grade}"),
            ("", ""),  # Separator
            ("Initial Balance", f"${record.initial_balance:,.2f}"),
            ("Final Balance", f"${record.final_balance:,.2f}"),
            ("Profit/Loss", f"${record.profit_loss:,.2f}"),
            ("Return Rate", f"{record.return_rate:.2f}%"),
            ("", ""),  # Separator
            ("Holding Period", f"{record.holding_period_days} days"),
            ("Total Trades", f"{record.total_trades} trades"),
            ("Best Stock", f"{record.best_stock}"),
            ("Best Stock Return", f"{record.best_stock_return:.2f}%"),
            ("", ""),  # Separator
            ("Rank Score", f"{record.rank_score:.2f}"),
            ("Result Type", record.result_type.value.replace('_', ' ').title()),
        ]
        
        for label_text, value_text in details:
            if not label_text:  # Separator
                ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=5)
                continue
            
            detail_frame = ttk.Frame(main_frame)
            detail_frame.pack(fill=tk.X, pady=2)
            
            label = ttk.Label(detail_frame, text=f"{label_text}:", 
                             font=('Arial', 10))
            label.pack(side=tk.LEFT)
            
            value = ttk.Label(detail_frame, text=value_text, 
                             font=('Arial', 10, 'bold'),
                             foreground=self.colors['text_accent'])
            value.pack(side=tk.RIGHT)
        
        # Close button
        close_btn = ttk.Button(main_frame, text="Close",
                              style='Pastel.Primary.TButton',
                              command=dialog.destroy)
        close_btn.pack(pady=(20, 0))
    
    def export_scoreboard(self):
        """Export scoreboard to CSV"""
        try:
            # Ask for file location
            filename = filedialog.asksaveasfilename(
                title="Export Scoreboard",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialname=f"scoreboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if filename:
                exported_file = self.scoreboard_manager.export_to_csv(filename)
                if exported_file:
                    messagebox.showinfo("Export Successful", 
                                       f"Scoreboard exported successfully to:\n{exported_file}")
                else:
                    messagebox.showerror("Export Failed", "Failed to export scoreboard.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting scoreboard: {str(e)}")
    
    def clear_scoreboard(self):
        """Clear all scoreboard records (with confirmation)"""
        result = self.kawaii_msg.show_question(
            "Clear Scoreboard",
            "Are you sure you want to clear ALL scoreboard records?\n\n"
            "This action cannot be undone!",
            'skull'
        )
        
        if result:
            self.scoreboard_manager.clear_all_records()
            self.refresh_scoreboard()
            self.kawaii_msg.show_success("Scoreboard Cleared", 
                               "All scoreboard records have been cleared.", 'sparkle')
    
    def schedule_refresh(self):
        """Schedule automatic refresh"""
        self.main_app.root.after(30000, self.auto_refresh)  # 30 seconds
    
    def auto_refresh(self):
        """Auto refresh scoreboard"""
        try:
            self.refresh_scoreboard()
        except Exception as e:
            print(f"Auto refresh error: {e}")
        finally:
            self.schedule_refresh()  # Schedule next refresh