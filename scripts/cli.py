"""
Command line interface for the Stock Analysis & Recommendation System
"""

import json
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.stock_crawler import StockCrawler
from src.analysis.recommendation_engine import RecommendationEngine
from src.core.config import MAGNIFICENT_SEVEN


class StockAnalysisCLI:
    """Command line interface for stock analysis and recommendations"""
    
    def __init__(self):
        self.crawler = StockCrawler()
        self.recommendation_engine = RecommendationEngine()
        
    def show_menu(self):
        """Display the main menu"""
        # Kuromi ASCII Art
        kuromi_art = """
⡤⠲⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡎⢑
⠑⢲⠷⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠶⠚⡟⠉
⠀⠸⡇⠀⠈⠙⠲⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠚⠉⠀⠀⠀⡇⠀
⠀⠀⡇⠀⠀⠀⠀⠀⠈⠙⣲⣀⠄⠠⠄⠒⠢⠤⠠⢴⠋⠁⠀⠀⠀⠀⠀⢸⠇⠀
⠀⠀⣧⠀⠀⠀⠀⠀⣀⠏⠀⠀⠀⠀⠀⠀⢀⠀⠀⠈⠉⢳⡀⠀⠀⠀⠀⢸⠀⠀
⠀⠀⢸⠀⠀⠀⣠⣾⠀⠀⠀⣂⡠⠤⢤⣤⠬⠤⢄⣰⠀⠀⠈⣷⡀⠀⠀⡾⠀⠀
⠀⠀⠸⢦⣀⣼⠋⢏⢀⡜⠊⠁⢠⣾⣿⣿⣿⣦⠀⠈⠑⠶⡀⣹⠹⡦⠖⠃⠀⠀
⠀⠀⠀⠀⢸⠃⠀⠀⠉⠀⠀⠀⠸⣁⣼⣿⣇⡸⠀⠀⠀⠀⠈⠁⠀⢻⡀⠀⠀⠀
⠀⠀⠀⠀⣾⠀⠀⠀⣠⡴⠒⠉⠓⠲⢼⣈⠯⠒⠋⠙⠲⣄⠀⠀⠀⢸⡇⠀⠀⠀
⠀⠀⠀⠀⢹⠀⠀⣰⠋⢲⣤⡀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠋⢳⠀⠀⢸⠃⠀⠀⠀
⠀⠀⠀⠀⠈⣧⠀⣏⠀⢸⣿⠏⠀⠀⢀⣀⠀⠀⠀⢿⡿⠀⠈⡇⢠⠏⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠳⣿⡀⠀⠀⠀⠀⠀⢌⣂⠅⠀⠀⠀⠀⢀⣼⡶⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡀⣀⠽⠓⠲⠤⢤⣤⣤⣤⣤⣤⡤⠤⠶⢯⡁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠣⠸⠛⠒⠒⢲⡀⠀⣀⡤⠦⣄⠀⢠⠖⠒⠒⠻⣀⠇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢔⢑⠋⠁⠀⠀⠀⢹⠉⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀
        """
        
        print(kuromi_art)
        print()
        print("×~☆𝑲𝒖𝒓𝒐𝒎𝒊☆~× Magnificent Seven Stock Analysis & Recommendation System ( ˶ˆᗜˆ˵ )")
        print("=" * 80)
        print("Choose option:")
        print("1. ⸜(｡˃ ᵕ ˂ )⸝♡ Get stock data (all Magnificent Seven)")
        print("2. Get stock data (specific stock)")
        print("3. ── ୨୧ ──── Get buy recommendations (all stocks)")
        print("4. ﮩ٨ـﮩﮩ٨ـ♡ﮩ٨ـﮩﮩ٨ـ Analyze specific stock")
        print("5. ⋆.˚✮🎧✮˚.⋆ General web crawling")
        
    def get_user_choice(self):
        """Get user menu choice"""
        return input("Enter choice (1-5): ").strip()
        
    def crawl_all_stocks(self):
        """Handle crawling all stocks"""
        print("\n⸜(｡˃ ᵕ ˂ )⸝♡ Crawling all Magnificent Seven stocks...")
        results = self.crawler.get_all_stocks_data()
        print(json.dumps(results, indent=2))
        
    def crawl_specific_stock(self):
        """Handle crawling a specific stock"""
        print(f"\nAvailable stocks: {', '.join(MAGNIFICENT_SEVEN.keys())}")
        symbol = input("Enter stock symbol: ").upper().strip()
        
        if symbol in MAGNIFICENT_SEVEN:
            result = self.crawler.get_stock_data(symbol)
            if result:
                print(json.dumps(result, indent=2))
            else:
                print(f"Failed to get data for {symbol}")
        else:
            print("Invalid symbol. Please choose from the Magnificent Seven.")
            
    def get_all_recommendations(self):
        """Handle getting recommendations for all stocks"""
        print("\n── ୨୧ ──── Generating buy recommendations for all Magnificent Seven stocks...")
        print("( ˶ˆᗜˆ˵ ) This may take a moment as we analyze each stock...")
        
        results = self.recommendation_engine.analyze_all_magnificent_seven()
        report = self.recommendation_engine.generate_investment_report(results)
        print(report)
        
    def analyze_specific_stock(self):
        """Handle analyzing a specific stock"""
        print(f"\nﮩ٨ـﮩﮩ٨ـ♡ﮩ٨ـﮩﮩ٨ـ Available stocks: {', '.join(MAGNIFICENT_SEVEN.keys())}")
        symbol = input("Enter stock symbol to analyze: ").upper().strip()
        
        if symbol in MAGNIFICENT_SEVEN:
            print(f"\n( ˶ˆᗜˆ˵ ) Analyzing {symbol}...")
            analysis = self.recommendation_engine.analyze_single_stock(symbol)
            
            if 'error' in analysis:
                print(f"{analysis['error']}")
                return
                
            print(f"\n˃̵ᴗ˂ ANALYSIS RESULT FOR {symbol}")
            print("-" * 50)
            print(f"Company: {analysis['company']}")
            print(f"Overall Score: {analysis['overall_score']}")
            print(f"Recommendation: {analysis['recommendation']}")
            print(f"Confidence: {analysis['confidence']}")
            print("\n⸜(｡˃ ᵕ ˂ )⸝♡ Detailed Breakdown:")
            
            breakdown = analysis['analysis_breakdown']
            print(f"  • Momentum: {breakdown['momentum']['analysis']} (Score: {breakdown['momentum']['score']})")
            print(f"  • Volume: {breakdown['volume']['analysis']} (Score: {breakdown['volume']['score']})")
            print(f"  • Market Cap: {breakdown['market_cap']['analysis']} (Score: {breakdown['market_cap']['score']})")
            print(f"  • Volatility: {breakdown['volatility']['analysis']} (Score: {breakdown['volatility']['score']})")
            print(f"  • Value: {breakdown['value']['analysis']} (Score: {breakdown['value']['score']})")
            
        else:
            print("Invalid symbol. Please choose from the Magnificent Seven.")
            
    def crawl_general_url(self):
        """Handle general web crawling"""
        url = input("Enter URL to crawl: ").strip()
        result = self.crawler.crawl_general_url(url)
        
        if result:
            print(json.dumps(result, indent=2))
        else:
            print("Failed to crawl the URL")
            
    def run(self):
        """Run the CLI application"""
        try:
            self.show_menu()
            choice = self.get_user_choice()
            
            if choice == "1":
                self.crawl_all_stocks()
            elif choice == "2":
                self.crawl_specific_stock()
            elif choice == "3":
                self.get_all_recommendations()
            elif choice == "4":
                self.analyze_specific_stock()
            elif choice == "5":
                self.crawl_general_url()
            else:
                print("Invalid choice.")
                
        finally:
            self.crawler.close()
            self.recommendation_engine.close()