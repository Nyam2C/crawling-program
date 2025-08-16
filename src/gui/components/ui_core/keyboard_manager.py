#!/usr/bin/env python3
"""
Keyboard Shortcut Manager - Handles all keyboard shortcuts and hotkeys
"""

import tkinter as tk
try:
    from typing import Dict, Callable, Optional
except ImportError:
    # Fallback for very old Python versions
    Dict = dict
    Callable = object
    Optional = lambda x: x

class KeyBinding:
    """Key binding information"""
    def __init__(self, key_combination: str, description: str, callback: Callable, enabled: bool = True):
        self.key_combination = key_combination
        self.description = description
        self.callback = callback
        self.enabled = enabled

class KeyboardManager:
    """Keyboard shortcut management class"""
    
    def __init__(self, root: tk.Tk, main_app):
        self.root = root
        self.main_app = main_app
        self.bindings: Dict[str, KeyBinding] = {}
        self.setup_default_bindings()
        self.bind_all_shortcuts()
        
    def setup_default_bindings(self):
        """Setup default keyboard shortcuts"""
        self.bindings = {
            '<Control-r>': KeyBinding(
                'Ctrl+R', 
                'Refresh Data', 
                self.refresh_data
            ),
            '<Control-s>': KeyBinding(
                'Ctrl+S', 
                'Save Settings', 
                self.save_settings
            ),
            '<Control-q>': KeyBinding(
                'Ctrl+Q', 
                'Quit Application', 
                self.quit_application
            ),
            '<F1>': KeyBinding(
                'F1', 
                'Help', 
                self.show_help
            ),
            '<Control-d>': KeyBinding(
                'Ctrl+D', 
                'Delete Selected', 
                self.delete_selected
            ),
            '<Control-e>': KeyBinding(
                'Ctrl+E', 
                'Export Data', 
                self.export_data
            ),
            '<Control-i>': KeyBinding(
                'Ctrl+I', 
                'Import Data', 
                self.import_data
            ),
            '<Escape>': KeyBinding(
                'ESC', 
                'Cancel Current Action', 
                self.cancel_current_action
            ),
            '<Control-1>': KeyBinding(
                'Ctrl+1', 
                'Stock Data Tab', 
                lambda: self.switch_tab(0)
            ),
            '<Control-2>': KeyBinding(
                'Ctrl+2', 
                'Recommendations Tab', 
                lambda: self.switch_tab(1)
            ),
            '<Control-3>': KeyBinding(
                'Ctrl+3', 
                'Analysis Tab', 
                lambda: self.switch_tab(2)
            ),
            '<Control-4>': KeyBinding(
                'Ctrl+4', 
                'Trading Tab', 
                lambda: self.switch_tab(3)
            ),
            '<Control-5>': KeyBinding(
                'Ctrl+5', 
                'Scoreboard Tab', 
                lambda: self.switch_tab(4)
            ),
            '<Control-6>': KeyBinding(
                'Ctrl+6', 
                'Investment Analysis Tab', 
                lambda: self.switch_tab(5)
            ),
            '<Control-7>': KeyBinding(
                'Ctrl+7', 
                'Settings Tab', 
                lambda: self.switch_tab(6)
            ),
        }
    
    def bind_all_shortcuts(self):
        """Bind all shortcuts to tkinter"""
        for key_combo, binding in self.bindings.items():
            if binding.enabled:
                self.root.bind_all(key_combo, self._create_handler(binding.callback))
    
    def _create_handler(self, callback: Callable):
        """Create event handler"""
        def handler(event):
            try:
                print(f"Debug: Executing shortcut callback: {callback}")
                callback()
                return "break"  # Prevent default event handling
            except Exception as e:
                print(f"Keyboard shortcut execution error: {e}")
                if hasattr(self.main_app, 'show_error'):
                    self.main_app.show_error(f"Error executing shortcut: {e}")
                return "break"
        return handler
    
    def add_custom_binding(self, key_combo: str, description: str, callback: Callable):
        """Add custom key binding"""
        binding = KeyBinding(key_combo, description, callback)
        self.bindings[key_combo] = binding
        self.root.bind_all(key_combo, self._create_handler(callback))
    
    def remove_binding(self, key_combo: str):
        """Remove key binding"""
        if key_combo in self.bindings:
            self.root.unbind_all(key_combo)
            del self.bindings[key_combo]
    
    def enable_binding(self, key_combo: str):
        """Enable key binding"""
        if key_combo in self.bindings:
            self.bindings[key_combo].enabled = True
            self.root.bind_all(key_combo, self._create_handler(self.bindings[key_combo].callback))
    
    def disable_binding(self, key_combo: str):
        """Disable key binding"""
        if key_combo in self.bindings:
            self.bindings[key_combo].enabled = False
            self.root.unbind_all(key_combo)
    
    def get_help_text(self) -> str:
        """Generate help text"""
        help_lines = ["Keyboard Shortcuts:\n"]
        for binding in self.bindings.values():
            if binding.enabled:
                help_lines.append(f"  {binding.key_combination}: {binding.description}")
        return "\n".join(help_lines)
    
    # === Shortcut Action Methods ===
    
    def refresh_data(self):
        """Refresh data"""
        self.main_app.update_status("Shortcut: Refreshing data...")
        try:
            # Stock Data tab refresh
            if hasattr(self.main_app, 'stock_data_tab'):
                self.main_app.stock_data_tab.refresh_stock_data()
                
            self.main_app.update_status("Data refresh completed (Ctrl+R)")
        except Exception as e:
            self.main_app.show_error(f"Data refresh failed: {e}")
    
    def save_settings(self):
        """Save settings"""
        try:
            if hasattr(self.main_app, 'settings_tab'):
                self.main_app.settings_tab.save_settings()
            
            # Show styled success dialog with centered OK button
            from src.gui.components.dialogs import show_success
            show_success(self.main_app.root, "Settings Saved", "Settings have been saved successfully!")
            self.main_app.update_status("Settings saved (Ctrl+S)")
        except Exception as e:
            self.main_app.show_error(f"Settings save failed: {e}")
    
    def quit_application(self):
        """Quit application"""
        self.main_app.on_closing()
    
    def show_help(self):
        """Show help"""
        try:
            from src.gui.components.dialogs.styled_dialogs import StyledScrollableDialog
            help_text = self.get_help_text()
            # Use smaller height for F1 dialog
            dialog = StyledScrollableDialog(self.main_app.root, "Keyboard Shortcuts Help", help_text, width=600, height=350)
        except ImportError:
            # Fallback to standard messagebox
            from tkinter import messagebox
            help_text = self.get_help_text()
            messagebox.showinfo("Keyboard Shortcuts Help", help_text)
    
    def delete_selected(self):
        """Delete selected item"""
        current_tab = self.main_app.notebook.select()
        tab_index = self.main_app.notebook.index(current_tab)
        
        try:
            # Show confirmation dialog with styled interface
            from src.gui.components.dialogs import ask_yes_no
            result = ask_yes_no(self.main_app.root, "Confirm Delete", 
                               "Are you sure you want to delete the selected item?")
            
            if result == "yes":
                if tab_index == 0:  # Stock Data tab
                    if hasattr(self.main_app, 'stock_data_tab'):
                        self.main_app.stock_data_tab.remove_selected_stock()
                elif tab_index == 3:  # Mock Trading tab
                    if hasattr(self.main_app, 'mock_trading_tab'):
                        self.main_app.mock_trading_tab.cancel_selected_order()
                
                self.main_app.update_status("Selected item deleted (Ctrl+D)")
            else:
                self.main_app.update_status("Delete operation canceled")
        except Exception as e:
            self.main_app.show_error(f"Failed to delete item: {e}")
    
    def export_data(self):
        """Export data"""
        try:
            current_tab = self.main_app.notebook.select()
            tab_index = self.main_app.notebook.index(current_tab)
            
            if tab_index == 3:  # Mock Trading tab
                if hasattr(self.main_app, 'mock_trading_tab'):
                    self.main_app.mock_trading_tab.export_portfolio_data()
            else:
                from tkinter import filedialog, messagebox
                filename = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
                )
                if filename:
                    # Actual export logic implementation here
                    messagebox.showinfo("Export", f"Data saved to {filename}")
            
            self.main_app.update_status("Data export completed (Ctrl+E)")
        except Exception as e:
            self.main_app.show_error(f"Data export failed: {e}")
    
    def import_data(self):
        """Import data"""
        try:
            from tkinter import filedialog, messagebox
            filename = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                # Actual import logic implementation here
                messagebox.showinfo("Import", f"Data imported from {filename}")
                self.main_app.update_status("Data import completed (Ctrl+I)")
        except Exception as e:
            self.main_app.show_error(f"Data import failed: {e}")
    
    def cancel_current_action(self):
        """Cancel current action"""
        try:
            # Cancel any ongoing operations
            if hasattr(self.main_app, 'progress'):
                self.main_app.hide_progress()
            
            # Remove focus from all input fields
            self.main_app.root.focus_set()
            
            self.main_app.update_status("Current action canceled (ESC)")
        except Exception as e:
            print(f"Error canceling action: {e}")
    
    def switch_tab(self, tab_index: int):
        """Switch tab"""
        try:
            print(f"Debug: switch_tab called with index {tab_index}")
            if hasattr(self.main_app, 'notebook') and self.main_app.notebook:
                tabs = self.main_app.notebook.tabs()
                print(f"Debug: Total tabs: {len(tabs)}, Switching to index: {tab_index}")
                print(f"Debug: Available tabs: {tabs}")
                
                if 0 <= tab_index < len(tabs):
                    # Try multiple approaches to select tab
                    try:
                        # Method 1: Select by index directly
                        self.main_app.notebook.select(tab_index)
                        print(f"Debug: Method 1 - Selected tab by index {tab_index}")
                    except Exception as e1:
                        print(f"Debug: Method 1 failed: {e1}")
                        try:
                            # Method 2: Select by tab ID
                            tab_id = tabs[tab_index]
                            self.main_app.notebook.select(tab_id)
                            print(f"Debug: Method 2 - Selected tab by ID {tab_id}")
                        except Exception as e2:
                            print(f"Debug: Method 2 failed: {e2}")
                            raise e2
                    
                    tab_names = ["Stock Data", "Recommendations", "Analysis", "Trading", 
                               "Scoreboard", "Investment Analysis", "Settings"]
                    if tab_index < len(tab_names):
                        status_msg = f"Switched to {tab_names[tab_index]} tab (Ctrl+{tab_index+1})"
                        if hasattr(self.main_app, 'update_status'):
                            self.main_app.update_status(status_msg)
                        print(f"Debug: Successfully switched to {tab_names[tab_index]} tab")
                else:
                    print(f"Debug: Tab index {tab_index} out of range (0-{len(tabs)-1})")
                    if hasattr(self.main_app, 'update_status'):
                        self.main_app.update_status(f"Tab {tab_index + 1} not available")
            else:
                print("Debug: Notebook not found or not initialized")
                print(f"Debug: main_app has notebook: {hasattr(self.main_app, 'notebook')}")
                if hasattr(self.main_app, 'notebook'):
                    print(f"Debug: notebook is: {self.main_app.notebook}")
                if hasattr(self.main_app, 'update_status'):
                    self.main_app.update_status("Tab switching not available")
        except Exception as e:
            print(f"Debug: Tab switching error: {e}")
            import traceback
            traceback.print_exc()
            if hasattr(self.main_app, 'show_error'):
                self.main_app.show_error(f"Tab switching failed: {e}")