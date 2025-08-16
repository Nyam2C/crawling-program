#!/usr/bin/env python3
"""Test GUI launch to verify notebook tab addition fix"""

try:
    # Test imports first
    print("Testing imports...")
    from src.gui.gui_app import StockAnalysisGUI
    print("✅ Imports successful!")
    
    # Test GUI initialization (won't run mainloop)
    print("Testing GUI initialization...")
    app = StockAnalysisGUI()
    print("✅ GUI initialized successfully!")
    
    # Test that all tabs are created
    tab_count = app.notebook.index("end")
    print(f"✅ Created {tab_count} tabs successfully!")
    
    # Clean up
    try:
        app.on_closing()
    except:
        pass
    
    print("🎉 All tests passed! The notebook tab error should be fixed.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()