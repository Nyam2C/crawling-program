#!/usr/bin/env python3
"""
Styled Dialog Components - Professional Theme Compatible
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk
import os
try:
    from typing import Optional, Callable
except ImportError:
    # Fallback for very old Python versions
    Optional = lambda x: x
    Callable = object


class StyledDialog:
    """Base class for styled dialogs that match the application theme"""
    
    def __init__(self, parent, title: str, width: int = 400, height: int = 300):
        self.parent = parent
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry(f"{width}x{height}")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Apply theme colors
        self.colors = {
            'background': '#1F144A',
            'panel': '#2B1E6B',
            'lavender': '#C4B5FD',
            'periwinkle': '#A78BFA',
            'pink': '#FBCFE8',
            'text': '#F8F8FF'
        }
        
        self.dialog.configure(bg=self.colors['background'])
        
        # Center dialog on parent
        self.center_dialog()
        
        # Setup content
        self.setup_content()
        
        # Focus and wait
        self.dialog.focus_set()
        self.dialog.wait_window()
    
    def center_dialog(self):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        
        # Get parent position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate center position
        dialog_width = self.dialog.winfo_reqwidth()
        dialog_height = self.dialog.winfo_reqheight()
        
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        self.dialog.geometry(f"+{x}+{y}")
    
    def setup_content(self):
        """Override in subclasses to setup dialog content"""
        pass
    
    def close_dialog(self, result=None):
        """Close dialog with optional result"""
        self.result = result
        self.dialog.destroy()


class StyledMessageBox(StyledDialog):
    """Styled message box dialog"""
    
    def __init__(self, parent, title: str, message: str, dialog_type: str = "info", width: int = 450, height: int = 200):
        self.message = message
        self.dialog_type = dialog_type
        super().__init__(parent, title, width, height)
    
    def setup_content(self):
        """Setup message box content"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon and message frame
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon - try to load image first, fallback to text
        icon_image = self.get_icon_image()
        if icon_image:
            icon_label = tk.Label(content_frame, image=icon_image, bg=self.colors['background'])
            icon_label.image = icon_image  # Keep a reference to prevent garbage collection
        else:
            icon_text = self.get_icon_text()
            icon_label = tk.Label(content_frame, text=icon_text, font=("Arial", 24), 
                                 fg=self.colors['lavender'], bg=self.colors['background'])
        icon_label.pack(side=tk.LEFT, padx=(0, 15), pady=10)
        
        # Message
        message_label = tk.Label(content_frame, text=self.message, font=("Arial", 11),
                                fg=self.colors['text'], bg=self.colors['background'],
                                wraplength=350, justify=tk.LEFT)
        message_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # OK Button - centered
        ok_button = tk.Button(button_frame, text="OK", font=("Arial", 10, "bold"),
                             bg=self.colors['lavender'], fg=self.colors['background'],
                             activebackground=self.colors['periwinkle'],
                             relief=tk.RAISED, bd=2, padx=20, pady=5,
                             command=lambda: self.close_dialog("ok"))
        ok_button.pack(expand=True)
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.close_dialog("ok"))
        self.dialog.bind('<Escape>', lambda e: self.close_dialog("cancel"))
    
    def get_icon_image(self):
        """Get icon image based on dialog type"""
        icon_mapping = {
            "info": "mail.png",
            "warning": "level_3.png", 
            "error": "skull.png",
            "question": "glasses.png",
            "success": "heart.png"
        }
        
        icon_file = icon_mapping.get(self.dialog_type, "mail.png")
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                "assets", "pixel_icons", icon_file)
        
        try:
            if os.path.exists(icon_path):
                return tk.PhotoImage(file=icon_path)
        except Exception as e:
            print(f"Error loading icon {icon_path}: {e}")
        
        return None
    
    def get_icon_text(self) -> str:
        """Get icon text based on dialog type (fallback)"""
        icons = {
            "info": "ℹ",
            "warning": "⚠",
            "error": "✗",
            "question": "?",
            "success": "✓"
        }
        return icons.get(self.dialog_type, "ℹ")


class StyledConfirmDialog(StyledDialog):
    """Styled confirmation dialog"""
    
    def __init__(self, parent, title: str, message: str, width: int = 450, height: int = 180):
        self.message = message
        super().__init__(parent, title, width, height)
    
    def get_question_icon(self):
        """Get question icon image"""
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                "assets", "pixel_icons", "glasses.png")
        
        try:
            if os.path.exists(icon_path):
                return tk.PhotoImage(file=icon_path)
        except Exception as e:
            print(f"Error loading question icon {icon_path}: {e}")
        
        return None
    
    def setup_content(self):
        """Setup confirmation dialog content"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon and message frame
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon - use question icon for confirmation dialogs
        icon_image = self.get_question_icon()
        if icon_image:
            icon_label = tk.Label(content_frame, image=icon_image, bg=self.colors['background'])
            icon_label.image = icon_image  # Keep a reference to prevent garbage collection
        else:
            icon_label = tk.Label(content_frame, text="?", font=("Arial", 24),
                                 fg=self.colors['lavender'], bg=self.colors['background'])
        icon_label.pack(side=tk.LEFT, padx=(0, 15), pady=10)
        
        # Message
        message_label = tk.Label(content_frame, text=self.message, font=("Arial", 11),
                                fg=self.colors['text'], bg=self.colors['background'],
                                wraplength=350, justify=tk.LEFT)
        message_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # No Button
        no_button = tk.Button(button_frame, text="No", font=("Arial", 10),
                             bg=self.colors['panel'], fg=self.colors['text'],
                             activebackground=self.colors['background'],
                             relief=tk.RAISED, bd=2, padx=20, pady=5,
                             command=lambda: self.close_dialog("no"))
        no_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Yes Button
        yes_button = tk.Button(button_frame, text="Yes", font=("Arial", 10, "bold"),
                              bg=self.colors['lavender'], fg=self.colors['background'],
                              activebackground=self.colors['periwinkle'],
                              relief=tk.RAISED, bd=2, padx=20, pady=5,
                              command=lambda: self.close_dialog("yes"))
        yes_button.pack(side=tk.RIGHT)
        
        # Bind keys
        self.dialog.bind('<Return>', lambda e: self.close_dialog("yes"))
        self.dialog.bind('<Escape>', lambda e: self.close_dialog("no"))


def show_info(parent, title: str, message: str) -> str:
    """Show styled info dialog"""
    dialog = StyledMessageBox(parent, title, message, "info")
    return dialog.result


def show_warning(parent, title: str, message: str) -> str:
    """Show styled warning dialog"""
    dialog = StyledMessageBox(parent, title, message, "warning")
    return dialog.result


def show_error(parent, title: str, message: str) -> str:
    """Show styled error dialog"""
    dialog = StyledMessageBox(parent, title, message, "error")
    return dialog.result


def show_success(parent, title: str, message: str) -> str:
    """Show styled success dialog"""
    dialog = StyledMessageBox(parent, title, message, "success")
    return dialog.result


def ask_yes_no(parent, title: str, message: str) -> str:
    """Show styled yes/no confirmation dialog"""
    dialog = StyledConfirmDialog(parent, title, message)
    return dialog.result


class StyledScrollableDialog(StyledDialog):
    """Styled scrollable dialog for long text content"""
    
    def __init__(self, parent, title: str, content: str, width: int = 600, height: int = 500):
        self.content = content
        super().__init__(parent, title, width, height)
    
    def setup_content(self):
        """Setup scrollable dialog content"""
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable text area
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Text widget with scrollbar
        self.text_widget = tk.Text(text_frame, 
                                  font=("Consolas", 11),
                                  bg=self.colors['panel'],
                                  fg=self.colors['text'],
                                  selectbackground=self.colors['lavender'],
                                  selectforeground=self.colors['background'],
                                  relief=tk.FLAT,
                                  padx=15, pady=15,
                                  wrap=tk.WORD)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Pack text and scrollbar
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert content
        self.text_widget.insert(tk.END, self.content)
        self.text_widget.configure(state=tk.DISABLED)  # Make read-only
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Close button
        close_button = tk.Button(button_frame, text="Close", font=("Arial", 10, "bold"),
                                bg=self.colors['lavender'], fg=self.colors['background'],
                                activebackground=self.colors['periwinkle'],
                                relief=tk.RAISED, bd=2, padx=25, pady=8,
                                command=lambda: self.close_dialog("close"))
        close_button.pack(side=tk.RIGHT)
        
        # Bind keys
        self.dialog.bind('<Return>', lambda e: self.close_dialog("close"))
        self.dialog.bind('<Escape>', lambda e: self.close_dialog("close"))


def show_scrollable_info(parent, title: str, content: str) -> str:
    """Show styled scrollable info dialog"""
    dialog = StyledScrollableDialog(parent, title, content)
    return dialog.result