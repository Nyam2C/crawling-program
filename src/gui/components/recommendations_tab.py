#!/usr/bin/env python3
"""Recommendations Tab Component - Cool Kuromi Style"""

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
        self.notebook.add(self.frame, text="٩(ˊᗜˋ*)و̵ Recommendations")
        
        # Configure grid
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Control panel
        self.create_control_panel()
        
        # Recommendations display
        self.create_recommendations_display()
        
    def create_control_panel(self):
        """Create control panel for recommendations"""
        control_frame = ttk.LabelFrame(self.frame, text="( ˶ˆᗜˆ˵ ) Generate Recommendations", padding="15")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Button(control_frame, text="°ʚ(*´꒳`*)ɞ° Advanced Analysis",
                  command=self.generate_advanced_recommendations,
                  style='Kuromi.Gold.TButton').grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(control_frame, text="( ˶ˆᗜˆ˵ ) Quick Analysis",
                  command=self.generate_basic_recommendations,
                  style='Kuromi.Primary.TButton').grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(control_frame, text="ฅ^•ﻌ•^ฅ Save Report",
                  command=self.export_report,
                  style='Kuromi.Gold.TButton').grid(row=0, column=2)
        
    def create_recommendations_display(self):
        """Create display area for recommendations"""
        display_frame = ttk.LabelFrame(self.frame, text="( ˶ˆᗜˆ˵ ) Investment Advice", padding="15")
        display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)
        
        # Cute text widget for recommendations
        self.recommendations_text = scrolledtext.ScrolledText(
            display_frame, 
            wrap=tk.WORD, 
            height=25,
            font=('Consolas', 11),
            bg=self.colors['kuromi_light'],
            fg=self.colors['kuromi_text'],
            insertbackground=self.colors['kuromi_accent'],
            selectbackground=self.colors['kuromi_primary']
        )
        self.recommendations_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add cute initial message
        initial_message = """×~☆𝑲𝒖𝒓𝒐𝒎𝒊☆~× Welcome to Kuromi's Investment Recommendations! ×~☆𝑲𝒖𝒓𝒐𝒎𝒊☆~×

( ˶ˆᗜˆ˵ ) Click "Advanced Analysis" for comprehensive multi-criteria analysis
( ˶ˆᗜˆ˵ ) Click "Quick Analysis" for basic technical analysis
ฅ^•ﻌ•^ฅ Use "Save Report" to export your results

Ready to make some magical investment decisions? ( ˶ˆᗜˆ˵ )
Choose your analysis type above to get started! ( ˶ˆ꒳ˆ˵ )

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        self.recommendations_text.insert(1.0, initial_message)
        
    def generate_advanced_recommendations(self):
        """Generate advanced multi-criteria recommendations"""
        def generate():
            try:
                self.main_app.update_status("🌟 Generating advanced analysis with multiple investment criteria...")
                self.main_app.show_progress()
                
                results = self.main_app.recommendation_engine.analyze_all_magnificent_seven(use_advanced=True)
                report = self.main_app.recommendation_engine.generate_investment_report(results)
                self.main_app.current_recommendations = results
                
                self.main_app.root.after(0, self.update_recommendations_display, report)
                
                # Update charts with real data if available
                if hasattr(self.main_app, 'charts_frame') and self.main_app.charts_frame:
                    self.main_app.root.after(0, self.main_app.charts_frame.update_with_real_data, results)
                
                self.main_app.root.after(0, self.main_app.update_status, "✅ Advanced analysis completed successfully!")
                self.main_app.root.after(0, self.main_app.hide_progress)
                
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"Error generating advanced recommendations: {str(e)}")
                self.main_app.root.after(0, self.main_app.update_status, "❌ Error generating advanced analysis")
                self.main_app.root.after(0, self.main_app.hide_progress)
        
        threading.Thread(target=generate, daemon=True).start()
    
    def generate_basic_recommendations(self):
        """Generate basic recommendations (legacy mode)"""
        def generate():
            try:
                self.main_app.update_status("⚡ Generating quick basic analysis...")
                self.main_app.show_progress()
                
                results = self.main_app.recommendation_engine.analyze_all_magnificent_seven(use_advanced=False)
                report = self.main_app.recommendation_engine.generate_investment_report(results)
                self.main_app.current_recommendations = results
                
                self.main_app.root.after(0, self.update_recommendations_display, report)
                
                # Update charts with real data if available
                if hasattr(self.main_app, 'charts_frame') and self.main_app.charts_frame:
                    self.main_app.root.after(0, self.main_app.charts_frame.update_with_real_data, results)
                
                self.main_app.root.after(0, self.main_app.update_status, "✅ Basic analysis completed successfully!")
                self.main_app.root.after(0, self.main_app.hide_progress)
                
            except Exception as e:
                self.main_app.root.after(0, self.main_app.show_error, f"Error generating basic recommendations: {str(e)}")
                self.main_app.root.after(0, self.main_app.update_status, "❌ Error generating basic analysis")
                self.main_app.root.after(0, self.main_app.hide_progress)
        
        threading.Thread(target=generate, daemon=True).start()
        
    def update_recommendations_display(self, report):
        """Update the recommendations text display"""
        self.recommendations_text.delete(1.0, tk.END)
        
        # Add cute header
        cute_header = """💖✨ KUROMI'S MAGICAL STOCK ANALYSIS RESULTS ✨💖
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        self.recommendations_text.insert(1.0, cute_header + report)
        
    def export_report(self):
        """Export recommendations report"""
        if not hasattr(self.main_app, 'current_recommendations') or not self.main_app.current_recommendations:
            messagebox.showwarning("Warning", "No recommendations to export. Generate recommendations first! 💝")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Kuromi's Investment Report 💾"
        )
        
        if filename:
            try:
                report = self.main_app.recommendation_engine.generate_investment_report(self.main_app.current_recommendations)
                with open(filename, 'w', encoding='utf-8') as f:
                    # Add cute header to saved file
                    cute_header = """💖✨ KUROMI'S MAGICAL STOCK ANALYSIS REPORT ✨💖
Generated with love and magic! 🌸
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
                    f.write(cute_header + report)
                messagebox.showinfo("Success", f"✅ Report saved successfully to {filename}! 💝")
            except Exception as e:
                messagebox.showerror("Error", f"❌ Failed to save report: {str(e)}")