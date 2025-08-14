#!/usr/bin/env python3
"""Recommendations Tab Component - Retro Pastel Style"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading


class RecommendationsTab:
    def __init__(self, notebook, main_app):
        self.notebook = notebook
        self.main_app = main_app
        self.colors = main_app.colors
        self.setup_tab()
        
    def setup_tab(self):
        """Create the recommendations tab"""
        self.frame = ttk.Frame(self.notebook, padding="15")
        icon = self.main_app.icon_manager.get_icon('tab_recommend')
        self.notebook.add(self.frame, text='Recommendations', image=icon, compound='left')
        
        # Configure grid
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Control panel
        self.create_control_panel()
        
        # Recommendations display
        self.create_recommendations_display()
        
    def create_control_panel(self):
        """Create control panel for recommendations"""
        control_frame = ttk.LabelFrame(self.frame, text="Generate Recommendations", padding="15")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Use new icon button system
        if hasattr(self.main_app, 'icon_button'):
            advanced_btn = self.main_app.icon_button(
                control_frame, 'analyze_advanced', 'Advanced Analysis', self.generate_advanced_recommendations
            )
            advanced_btn.grid(row=0, column=0, padx=(0, 10))
            
            quick_btn = self.main_app.icon_button(
                control_frame, 'analyze_quick', 'Quick Analysis', self.generate_basic_recommendations
            )
            quick_btn.grid(row=0, column=1, padx=(0, 10))
            
            save_btn = self.main_app.icon_button(
                control_frame, 'save', 'Save Report', self.export_report
            )
            save_btn.grid(row=0, column=2)
        else:
            # Fallback regular buttons
            ttk.Button(control_frame, text="Advanced Analysis",
                      command=self.generate_advanced_recommendations,
                      style='Pastel.Primary.TButton').grid(row=0, column=0, padx=(0, 10))
            
            ttk.Button(control_frame, text="Quick Analysis",
                      command=self.generate_basic_recommendations,
                      style='Pastel.Primary.TButton').grid(row=0, column=1, padx=(0, 10))
            
            ttk.Button(control_frame, text="Save Report",
                      command=self.export_report,
                      style='Pastel.Primary.TButton').grid(row=0, column=2)
        
    def create_recommendations_display(self):
        """Create display area for recommendations"""
        display_frame = ttk.LabelFrame(self.frame, text="Investment Advice", padding="15")
        display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)
        
        # Text widget for recommendations
        self.recommendations_text = scrolledtext.ScrolledText(
            display_frame, 
            wrap=tk.WORD, 
            height=25,
            font=('Consolas', 11),
            bg=self.colors['panel_alt'],
            fg=self.colors['text'],
            insertbackground=self.colors['periwinkle'],
            selectbackground=self.colors['lavender']
        )
        self.recommendations_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add initial message
        initial_message = """Welcome to Investment Recommendations!

• Click "Advanced Analysis" for comprehensive multi-criteria analysis
• Click "Quick Analysis" for basic technical analysis  
• Use "Save Report" to export your results

Ready to make informed investment decisions?
Choose your analysis type above to get started!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        self.recommendations_text.insert(1.0, initial_message)
        
    def generate_advanced_recommendations(self):
        """Generate advanced multi-criteria recommendations"""
        def generate():
            try:
                self.main_app.update_status("Generating advanced analysis with multiple investment criteria...")
                self.main_app.show_progress()
                
                results = self.main_app.recommendation_engine.analyze_all_magnificent_seven(use_advanced=True)
                report = self.main_app.recommendation_engine.generate_investment_report(results)
                self.main_app.current_recommendations = results
                
                self.main_app.root.after(0, self.update_recommendations_display, report)
                
                
                self.main_app.root.after(0, self.main_app.update_status, "Advanced analysis completed successfully!")
                self.main_app.root.after(0, self.main_app.hide_progress)
                
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"Error generating advanced recommendations: {str(e)}")
                self.main_app.root.after(0, self.main_app.update_status, "Error generating advanced analysis")
                self.main_app.root.after(0, self.main_app.hide_progress)
        
        threading.Thread(target=generate, daemon=True).start()
    
    def generate_basic_recommendations(self):
        """Generate basic recommendations (legacy mode)"""
        def generate():
            try:
                self.main_app.update_status("Generating quick basic analysis...")
                self.main_app.show_progress()
                
                results = self.main_app.recommendation_engine.analyze_all_magnificent_seven(use_advanced=False)
                report = self.main_app.recommendation_engine.generate_investment_report(results)
                self.main_app.current_recommendations = results
                
                self.main_app.root.after(0, self.update_recommendations_display, report)
                
                
                self.main_app.root.after(0, self.main_app.update_status, "Basic analysis completed successfully!")
                self.main_app.root.after(0, self.main_app.hide_progress)
                
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"Error generating basic recommendations: {str(e)}")
                self.main_app.root.after(0, self.main_app.update_status, "Error generating basic analysis")
                self.main_app.root.after(0, self.main_app.hide_progress)
        
        threading.Thread(target=generate, daemon=True).start()
    
    def update_recommendations_display(self, report):
        """Update the recommendations display with new data"""
        try:
            self.recommendations_text.delete(1.0, tk.END)
            self.recommendations_text.insert(1.0, report)
            self.main_app.update_status("Recommendations updated successfully!")
        except Exception as e:
            self.main_app.show_error(f"Error updating display: {str(e)}")
    
    def export_report(self):
        """Export current recommendations to file"""
        try:
            if not hasattr(self.main_app, 'current_recommendations') or not self.main_app.current_recommendations:
                messagebox.showwarning("No Data", "Please generate recommendations first before exporting.")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Recommendations Report"
            )
            
            if filename:
                content = self.recommendations_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.main_app.update_status(f"Report saved to {filename}")
                messagebox.showinfo("Export Successful", f"Recommendations report saved to:\n{filename}")
                
        except Exception as e:
            self.main_app.show_error(f"Error exporting report: {str(e)}")