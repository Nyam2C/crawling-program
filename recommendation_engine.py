"""
Stock recommendation engine for the Magnificent Seven
"""

from typing import Dict, List
from financial_analyzer import FinancialAnalyzer
from stock_crawler import StockCrawler
import json


class RecommendationEngine:
    """Generates stock buy recommendations based on comprehensive analysis"""
    
    def __init__(self, delay=2):
        self.crawler = StockCrawler(delay)
        self.analyzer = FinancialAnalyzer()
        
    def analyze_single_stock(self, symbol: str) -> Dict:
        """
        Analyze a single stock and generate recommendation
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            dict: Analysis results with recommendation
        """
        stock_data = self.crawler.get_stock_data(symbol)
        
        if not stock_data:
            return {
                'error': f'Failed to retrieve data for {symbol}',
                'symbol': symbol
            }
            
        return self.analyzer.generate_comprehensive_analysis(stock_data)
        
    def analyze_all_magnificent_seven(self) -> Dict:
        """
        Analyze all Magnificent Seven stocks and generate recommendations
        
        Returns:
            dict: Complete analysis for all stocks with rankings
        """
        print("🚀 Analyzing all Magnificent Seven stocks...")
        
        all_analyses = {}
        successful_analyses = []
        
        from config import MAGNIFICENT_SEVEN
        
        for symbol in MAGNIFICENT_SEVEN.keys():
            print(f"📊 Analyzing {symbol}...")
            analysis = self.analyze_single_stock(symbol)
            
            if 'error' not in analysis:
                all_analyses[symbol] = analysis
                successful_analyses.append(analysis)
            else:
                print(f"❌ Failed to analyze {symbol}")
                all_analyses[symbol] = analysis
                
        # Rank stocks by overall score
        successful_analyses.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return {
            'individual_analyses': all_analyses,
            'ranked_recommendations': successful_analyses,
            'summary': self._generate_portfolio_summary(successful_analyses)
        }
        
    def _generate_portfolio_summary(self, analyses: List[Dict]) -> Dict:
        """
        Generate portfolio-level summary and insights
        
        Args:
            analyses (list): List of individual stock analyses
            
        Returns:
            dict: Portfolio summary
        """
        if not analyses:
            return {'error': 'No successful analyses to summarize'}
            
        # Categorize recommendations
        strong_buys = [a for a in analyses if 'STRONG BUY' in a['recommendation']]
        buys = [a for a in analyses if 'BUY' in a['recommendation'] and 'STRONG' not in a['recommendation']]
        holds = [a for a in analyses if 'HOLD' in a['recommendation'] or 'WATCH' in a['recommendation']]
        weak_holds = [a for a in analyses if 'WEAK HOLD' in a['recommendation']]
        avoids = [a for a in analyses if 'AVOID' in a['recommendation']]
        
        # Calculate average score
        avg_score = sum(a['overall_score'] for a in analyses) / len(analyses)
        
        # Top 3 recommendations
        top_picks = analyses[:3]
        
        return {
            'total_analyzed': len(analyses),
            'average_score': round(avg_score, 3),
            'distribution': {
                'strong_buys': len(strong_buys),
                'buys': len(buys), 
                'holds': len(holds),
                'weak_holds': len(weak_holds),
                'avoids': len(avoids)
            },
            'top_3_picks': [
                {
                    'rank': i+1,
                    'symbol': pick['symbol'],
                    'company': pick['company'],
                    'score': pick['overall_score'],
                    'recommendation': pick['recommendation']
                }
                for i, pick in enumerate(top_picks)
            ],
            'market_sentiment': self._assess_market_sentiment(avg_score, analyses)
        }
        
    def _assess_market_sentiment(self, avg_score: float, analyses: List[Dict]) -> Dict:
        """
        Assess overall market sentiment based on analysis results
        
        Args:
            avg_score (float): Average score across all stocks
            analyses (list): Individual analyses
            
        Returns:
            dict: Market sentiment assessment
        """
        # Count positive momentum stocks
        positive_momentum = sum(1 for a in analyses 
                              if a['analysis_breakdown']['momentum']['score'] > 0.6)
        
        # Overall sentiment
        if avg_score >= 0.75:
            sentiment = "🚀 Very Bullish"
            description = "Strong buying opportunities across the board"
        elif avg_score >= 0.6:
            sentiment = "📈 Bullish"
            description = "Good investment climate with selective opportunities"
        elif avg_score >= 0.45:
            sentiment = "➡️ Neutral"
            description = "Mixed signals - careful stock selection recommended"
        elif avg_score >= 0.3:
            sentiment = "📉 Bearish"
            description = "Challenging market conditions - defensive approach advised"
        else:
            sentiment = "⬇️ Very Bearish"
            description = "Poor investment climate - consider waiting"
            
        return {
            'sentiment': sentiment,
            'description': description,
            'positive_momentum_count': positive_momentum,
            'strength_rating': f"{avg_score*100:.1f}%"
        }
        
    def generate_investment_report(self, analysis_results: Dict) -> str:
        """
        Generate a formatted investment report
        
        Args:
            analysis_results (dict): Results from analyze_all_magnificent_seven
            
        Returns:
            str: Formatted report
        """
        if 'error' in analysis_results:
            return f"❌ Error generating report: {analysis_results['error']}"
            
        summary = analysis_results['summary']
        ranked = analysis_results['ranked_recommendations']
        
        report = []
        report.append("=" * 80)
        report.append("📊 MAGNIFICENT SEVEN STOCK ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Market Overview
        report.append("🌟 MARKET OVERVIEW")
        report.append("-" * 50)
        sentiment = summary['market_sentiment']
        report.append(f"Market Sentiment: {sentiment['sentiment']}")
        report.append(f"Overall Strength: {sentiment['strength_rating']}")
        report.append(f"Description: {sentiment['description']}")
        report.append(f"Stocks with Positive Momentum: {sentiment['positive_momentum_count']}/{summary['total_analyzed']}")
        report.append("")
        
        # Recommendation Distribution
        report.append("📈 RECOMMENDATION BREAKDOWN")
        report.append("-" * 50)
        dist = summary['distribution']
        report.append(f"🟢 Strong Buy: {dist['strong_buys']}")
        report.append(f"🔵 Buy: {dist['buys']}")
        report.append(f"🟡 Hold/Watch: {dist['holds']}")
        report.append(f"🟠 Weak Hold: {dist['weak_holds']}")
        report.append(f"🔴 Avoid: {dist['avoids']}")
        report.append("")
        
        # Top 3 Picks
        report.append("🏆 TOP 3 RECOMMENDATIONS")
        report.append("-" * 50)
        for pick in summary['top_3_picks']:
            report.append(f"{pick['rank']}. {pick['symbol']} - {pick['company']}")
            report.append(f"   Score: {pick['score']} | {pick['recommendation']}")
        report.append("")
        
        # Detailed Analysis
        report.append("📋 DETAILED STOCK ANALYSIS")
        report.append("-" * 50)
        
        for analysis in ranked:
            report.append(f"\n{analysis['symbol']} - {analysis['company']}")
            report.append(f"Overall Score: {analysis['overall_score']} | {analysis['recommendation']}")
            report.append(f"Confidence Level: {analysis['confidence']}")
            
            breakdown = analysis['analysis_breakdown']
            report.append("Analysis:")
            report.append(f"  • Momentum: {breakdown['momentum']['analysis']}")
            report.append(f"  • Volume: {breakdown['volume']['analysis']}")
            report.append(f"  • Market Cap: {breakdown['market_cap']['analysis']}")
            report.append(f"  • Volatility: {breakdown['volatility']['analysis']}")
            report.append(f"  • Value: {breakdown['value']['analysis']}")
            
        report.append("")
        report.append("=" * 80)
        report.append("⚠️  DISCLAIMER: This analysis is for educational purposes only.")
        report.append("    Not financial advice. Always do your own research!")
        report.append("=" * 80)
        
        return "\n".join(report)
        
    def close(self):
        """Clean up resources"""
        self.crawler.close()