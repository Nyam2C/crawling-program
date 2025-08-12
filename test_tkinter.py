#!/usr/bin/env python3
"""
Simple tkinter test script to verify GUI functionality
"""

def test_tkinter():
    """Test if tkinter is working properly"""
    try:
        import tkinter as tk
        from tkinter import messagebox, ttk
        
        print("✅ tkinter imported successfully")
        
        # Create test window
        root = tk.Tk()
        root.title("🧪 tkinter Test - Magnificent Seven Stock Analysis")
        root.geometry("500x400")
        root.resizable(True, True)
        
        # Create widgets to test functionality
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, 
                              text="🧪 tkinter Functionality Test", 
                              font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Test basic widgets
        ttk.Label(main_frame, text="Basic Label:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text="✅ Working", foreground="green").grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Test button
        def button_test():
            messagebox.showinfo("Success", "✅ Button and messagebox working!")
            
        ttk.Label(main_frame, text="Button Test:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="🔘 Click Me", command=button_test).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Test entry
        ttk.Label(main_frame, text="Text Entry:").grid(row=3, column=0, sticky=tk.W, pady=5)
        test_entry = ttk.Entry(main_frame, width=20)
        test_entry.insert(0, "Type here...")
        test_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Test combobox
        ttk.Label(main_frame, text="Combobox:").grid(row=4, column=0, sticky=tk.W, pady=5)
        test_combo = ttk.Combobox(main_frame, values=["AAPL", "MSFT", "GOOGL"], state="readonly")
        test_combo.set("AAPL")
        test_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Test progress bar
        ttk.Label(main_frame, text="Progress Bar:").grid(row=5, column=0, sticky=tk.W, pady=5)
        progress = ttk.Progressbar(main_frame, length=200, mode='determinate')
        progress['value'] = 75
        progress.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Test notebook (tabs)
        ttk.Label(main_frame, text="Notebook Tabs:").grid(row=6, column=0, sticky=tk.W, pady=5)
        notebook = ttk.Notebook(main_frame, width=250, height=100)
        
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Tab 1")
        ttk.Label(tab1, text="📊 Stock Data").pack(pady=20)
        
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Tab 2") 
        ttk.Label(tab2, text="💡 Recommendations").pack(pady=20)
        
        notebook.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # Status
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        ttk.Label(status_frame, 
                 text="🎉 All tkinter components are working correctly!", 
                 foreground="green",
                 font=('Arial', 10, 'bold')).pack()
        
        # Configure grid weights
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Close button
        def close_app():
            print("✅ tkinter test completed successfully!")
            root.destroy()
            
        close_button = ttk.Button(main_frame, text="🏁 Close Test", command=close_app)
        close_button.grid(row=8, column=0, columnspan=2, pady=(20, 0))
        
        print("🎉 tkinter test window created successfully!")
        print("💡 Close the window to complete the test.")
        
        # Start the GUI
        root.mainloop()
        
        return True
        
    except ImportError as e:
        print(f"❌ tkinter import failed: {e}")
        print("\n📦 Install tkinter:")
        print("   Linux: sudo apt-get install python3-tk")
        print("   Windows/macOS: tkinter should be included with Python")
        return False
        
    except Exception as e:
        print(f"❌ tkinter test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing tkinter functionality...")
    print("=" * 50)
    
    if test_tkinter():
        print("✅ tkinter is fully functional!")
        print("🚀 You can now run the GUI application: python run_gui.py")
    else:
        print("❌ tkinter test failed")
        print("📋 Check INSTALL_TKINTER.md for installation instructions")