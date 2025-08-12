"""
Financial analysis engine for stock recommendation system
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class FinancialAnalyzer:
    """Analyzes financial data and generates investment insights"""
    
    def __init__(self):
        self.analysis_weights = {
            'price_momentum': 0.25,      # Recent price performance
            'volume_analysis': 0.15,     # Trading volume trends
            'market_cap_score': 0.20,    # Company size and stability
            'volatility_score': 0.15,    # Price stability
            'value_assessment': 0.25     # Overall value proposition
        }
        
    def parse_financial_value(self, value_str: str) -> float:
        """
        Parse financial values with suffixes (K, M, B, T)
        
        Args:
            value_str (str): Value string like "2.89T" or "45.6B"
            
        Returns:
            float: Numeric value
        """
        if not value_str or value_str == 'N/A':
            return 0.0
            
        # Remove any non-numeric characters except K, M, B, T, ., -, +
        cleaned = re.sub(r'[^\d.KMBT+-]', '', str(value_str).upper())
        
        if not cleaned or cleaned in ['N/A', '--']:
            return 0.0
            
        try:
            # Extract numeric part and suffix
            numeric_part = re.findall(r'[\d.-]+', cleaned)[0]
            suffix = re.findall(r'[KMBT]', cleaned)
            
            value = float(numeric_part)
            
            if suffix:
                multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000, 'T': 1000000000000}
                value *= multipliers.get(suffix[0], 1)
                
            return value
        except (ValueError, IndexError):
            return 0.0
            
    def analyze_price_momentum(self, stock_data: Dict) -> Tuple[float, str]:
        """
        Analyze price momentum based on change percentage
        
        Args:
            stock_data (dict): Stock data dictionary
            
        Returns:
            tuple: (score, analysis_text)
        """
        change_percent = stock_data.get('change_percent', '0')
        
        try:
            # Extract percentage value
            percent_value = float(re.findall(r'[-+]?\d*\.?\d+', str(change_percent))[0])
            
            if percent_value > 3:
                return 0.9, f"🚀 Strong upward momentum (+{abs(percent_value):.1f}%)"
            elif percent_value > 1:
                return 0.7, f"📈 Positive momentum (+{percent_value:.1f}%)"
            elif percent_value > -1:
                return 0.5, f"➡️ Stable price action ({percent_value:.1f}%)"
            elif percent_value > -3:
                return 0.3, f"📉 Minor decline ({percent_value:.1f}%)"
            else:
                return 0.1, f"⬇️ Significant decline ({percent_value:.1f}%)"
                
        except (ValueError, IndexError):
            return 0.5, "❓ Unable to assess momentum"
            
    def analyze_volume(self, stock_data: Dict) -> Tuple[float, str]:
        """
        Analyze trading volume
        
        Args:
            stock_data (dict): Stock data dictionary
            
        Returns:
            tuple: (score, analysis_text)
        """
        volume = self.parse_financial_value(stock_data.get('volume', '0'))
        
        if volume > 100000000:  # > 100M
            return 0.9, f"💪 Very high volume ({volume/1000000:.0f}M)"
        elif volume > 50000000:  # > 50M
            return 0.7, f"📊 High volume ({volume/1000000:.0f}M)"
        elif volume > 20000000:  # > 20M
            return 0.6, f"📈 Good volume ({volume/1000000:.0f}M)"
        elif volume > 5000000:   # > 5M
            return 0.4, f"📉 Moderate volume ({volume/1000000:.0f}M)"
        else:
            return 0.2, f"💤 Low volume ({volume/1000000:.1f}M)"
            
    def analyze_market_cap(self, stock_data: Dict) -> Tuple[float, str]:
        """
        Analyze market capitalization for stability assessment
        
        Args:
            stock_data (dict): Stock data dictionary
            
        Returns:
            tuple: (score, analysis_text)
        """
        market_cap = self.parse_financial_value(stock_data.get('market_cap', '0'))
        
        if market_cap > 2000000000000:  # > $2T
            return 0.95, f"🏛️ Mega-cap leader (${market_cap/1000000000000:.1f}T)"
        elif market_cap > 1000000000000:  # > $1T
            return 0.9, f"🏢 Large-cap giant (${market_cap/1000000000000:.1f}T)"
        elif market_cap > 500000000000:   # > $500B
            return 0.8, f"🏪 Large-cap stock (${market_cap/1000000000:.0f}B)"
        elif market_cap > 100000000000:   # > $100B
            return 0.7, f"🏬 Mid-large cap (${market_cap/1000000000:.0f}B)"
        else:
            return 0.5, f"🏠 Smaller cap (${market_cap/1000000000:.0f}B)"
            
    def assess_value_proposition(self, stock_data: Dict) -> Tuple[float, str]:
        """
        Overall value assessment based on multiple factors
        
        Args:
            stock_data (dict): Stock data dictionary
            
        Returns:
            tuple: (score, analysis_text)
        """
        symbol = stock_data.get('symbol', '')
        current_price = self.parse_financial_value(stock_data.get('current_price', '0'))
        
        # Company-specific value assessments based on historical performance and market position
        value_profiles = {
            'AAPL': {'base_score': 0.85, 'reason': 'Ecosystem dominance & innovation'},
            'MSFT': {'base_score': 0.88, 'reason': 'Cloud leadership & enterprise focus'},
            'GOOGL': {'base_score': 0.82, 'reason': 'Search monopoly & AI advancement'},
            'AMZN': {'base_score': 0.80, 'reason': 'E-commerce & AWS dominance'},
            'NVDA': {'base_score': 0.90, 'reason': 'AI & semiconductor leadership'},
            'TSLA': {'base_score': 0.75, 'reason': 'EV pioneer but high volatility'},
            'META': {'base_score': 0.78, 'reason': 'Social media reach & VR potential'}
        }
        
        profile = value_profiles.get(symbol, {'base_score': 0.6, 'reason': 'Unknown company'})
        
        return profile['base_score'], f"💎 {profile['reason']}"
        
    def calculate_volatility_score(self, stock_data: Dict) -> Tuple[float, str]:
        """
        Assess price volatility and stability
        
        Args:
            stock_data (dict): Stock data dictionary
            
        Returns:
            tuple: (score, analysis_text)
        """
        symbol = stock_data.get('symbol', '')
        
        # Volatility profiles based on historical data patterns
        volatility_profiles = {
            'AAPL': 0.75,  # Moderate volatility
            'MSFT': 0.80,  # Lower volatility  
            'GOOGL': 0.70, # Moderate-high volatility
            'AMZN': 0.65,  # Higher volatility
            'NVDA': 0.45,  # Very high volatility
            'TSLA': 0.30,  # Extremely high volatility
            'META': 0.60   # High volatility
        }
        
        score = volatility_profiles.get(symbol, 0.50)
        
        if score > 0.8:
            return score, "🛡️ Low volatility - stable investment"
        elif score > 0.6:
            return score, "⚖️ Moderate volatility - balanced risk"
        elif score > 0.4:
            return score, "⚡ High volatility - higher risk/reward"
        else:
            return score, "🎢 Very high volatility - speculative"
            
    def generate_comprehensive_analysis(self, stock_data: Dict) -> Dict:
        """
        Generate comprehensive financial analysis
        
        Args:
            stock_data (dict): Stock data dictionary
            
        Returns:
            dict: Complete analysis results
        """
        symbol = stock_data.get('symbol', 'Unknown')
        company = stock_data.get('company', 'Unknown Company')
        
        # Perform individual analyses
        momentum_score, momentum_text = self.analyze_price_momentum(stock_data)
        volume_score, volume_text = self.analyze_volume(stock_data)
        market_cap_score, market_cap_text = self.analyze_market_cap(stock_data)
        volatility_score, volatility_text = self.calculate_volatility_score(stock_data)
        value_score, value_text = self.assess_value_proposition(stock_data)
        
        # Calculate weighted overall score
        overall_score = (
            momentum_score * self.analysis_weights['price_momentum'] +
            volume_score * self.analysis_weights['volume_analysis'] +
            market_cap_score * self.analysis_weights['market_cap_score'] +
            volatility_score * self.analysis_weights['volatility_score'] +
            value_score * self.analysis_weights['value_assessment']
        )
        
        # Generate recommendation
        if overall_score >= 0.8:
            recommendation = "🟢 STRONG BUY"
            confidence = "High"
        elif overall_score >= 0.65:
            recommendation = "🔵 BUY"
            confidence = "Medium-High"
        elif overall_score >= 0.5:
            recommendation = "🟡 HOLD/WATCH"
            confidence = "Medium"
        elif overall_score >= 0.35:
            recommendation = "🟠 WEAK HOLD"
            confidence = "Medium-Low"
        else:
            recommendation = "🔴 AVOID"
            confidence = "Low"
            
        return {
            'symbol': symbol,
            'company': company,
            'overall_score': round(overall_score, 3),
            'recommendation': recommendation,
            'confidence': confidence,
            'analysis_breakdown': {
                'momentum': {'score': round(momentum_score, 2), 'analysis': momentum_text},
                'volume': {'score': round(volume_score, 2), 'analysis': volume_text},
                'market_cap': {'score': round(market_cap_score, 2), 'analysis': market_cap_text},
                'volatility': {'score': round(volatility_score, 2), 'analysis': volatility_text},
                'value': {'score': round(value_score, 2), 'analysis': value_text}
            },
            'timestamp': datetime.now().isoformat()
        }