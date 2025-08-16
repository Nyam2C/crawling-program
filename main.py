#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📚 StockEdu - 종합 주식 교육 플랫폼
Main entry point for Stock Education Platform
실전 주식 투자를 위한 올인원 교육 및 실습 플랫폼 🎓📈
"""

import sys
import os

# Add the project root to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """StockEdu 메인 함수 - 교육 플랫폼 GUI 실행"""
    try:
        from scripts.run_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Failed to import GUI components: {e}")
        print("\nPlease install missing dependencies:")
        print("   pip install -r requirements.txt")
        print("\nNote: This platform only supports GUI mode.")
        sys.exit(1)

if __name__ == "__main__":
    main()