#!/usr/bin/env python3
"""
Advanced Technical Analysis Engine - 고급 기술적 분석 엔진
머신러닝과 고급 수학적 모델을 활용한 주식 기술적 분석
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import logging
import warnings

# Suppress sklearn warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.model_selection import train_test_split
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class TrendDirection(Enum):
    """트렌드 방향"""
    STRONG_BULLISH = "strong_bullish"
    BULLISH = "bullish"
    NEUTRAL = "neutral"
    BEARISH = "bearish"
    STRONG_BEARISH = "strong_bearish"

class SupportResistanceLevel(Enum):
    """지지/저항 레벨 강도"""
    VERY_STRONG = "very_strong"
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"

@dataclass
class TechnicalIndicator:
    """기술적 지표 결과"""
    name: str
    value: float
    signal: str  # BUY, SELL, HOLD
    confidence: float  # 0-1
    description: str

@dataclass
class PriceLevel:
    """가격 레벨 (지지/저항)"""
    price: float
    level_type: str  # 'support' or 'resistance'
    strength: SupportResistanceLevel
    touches: int  # 몇 번 터치되었는지
    last_touch_date: datetime

@dataclass
class TrendAnalysis:
    """트렌드 분석 결과"""
    direction: TrendDirection
    strength: float  # 0-1
    duration_days: int
    slope: float
    confidence: float
    key_levels: List[PriceLevel]

@dataclass
class PredictionResult:
    """가격 예측 결과"""
    predicted_price: float
    confidence_interval: Tuple[float, float]
    model_accuracy: float
    prediction_horizon_days: int
    features_importance: Dict[str, float]

class AdvancedTechnicalAnalyzer:
    """고급 기술적 분석기"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        
    def get_stock_price_history(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """주식 가격 히스토리 데이터 가져오기"""
        try:
            import yfinance as yf
            
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                raise ValueError(f"No data available for {symbol}")
            
            return hist
            
        except Exception as e:
            self.logger.error(f"Error fetching price history for {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_advanced_indicators(self, price_data: pd.DataFrame) -> Dict[str, TechnicalIndicator]:
        """고급 기술적 지표 계산"""
        indicators = {}
        
        if price_data.empty:
            return indicators
        
        try:
            # 기본 가격 데이터
            close = price_data['Close']
            high = price_data['High']
            low = price_data['Low']
            volume = price_data['Volume']
            
            # 1. Bollinger Bands
            bb_result = self._calculate_bollinger_bands(close)
            indicators['bollinger_bands'] = bb_result
            
            # 2. RSI (Relative Strength Index)
            rsi_result = self._calculate_rsi(close)
            indicators['rsi'] = rsi_result
            
            # 3. MACD (Moving Average Convergence Divergence)
            macd_result = self._calculate_macd(close)
            indicators['macd'] = macd_result
            
            # 4. Stochastic Oscillator
            stoch_result = self._calculate_stochastic(high, low, close)
            indicators['stochastic'] = stoch_result
            
            # 5. Williams %R
            williams_result = self._calculate_williams_r(high, low, close)
            indicators['williams_r'] = williams_result
            
            # 6. Average True Range (ATR)
            atr_result = self._calculate_atr(high, low, close)
            indicators['atr'] = atr_result
            
            # 7. On-Balance Volume (OBV)
            obv_result = self._calculate_obv(close, volume)
            indicators['obv'] = obv_result
            
            # 8. Fibonacci Retracement Levels
            fib_result = self._calculate_fibonacci_levels(high, low)
            indicators['fibonacci'] = fib_result
            
        except Exception as e:
            self.logger.error(f"Error calculating indicators: {e}")
        
        return indicators
    
    def _calculate_bollinger_bands(self, close: pd.Series, window: int = 20, num_std: int = 2) -> TechnicalIndicator:
        """볼린저 밴드 계산"""
        rolling_mean = close.rolling(window=window).mean()
        rolling_std = close.rolling(window=window).std()
        
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)
        
        current_price = close.iloc[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        current_middle = rolling_mean.iloc[-1]
        
        # 신호 생성
        if current_price >= current_upper:
            signal = "SELL"
            confidence = 0.8
        elif current_price <= current_lower:
            signal = "BUY"
            confidence = 0.8
        else:
            signal = "HOLD"
            confidence = 0.5
        
        position = (current_price - current_lower) / (current_upper - current_lower)
        
        return TechnicalIndicator(
            name="Bollinger Bands",
            value=position,
            signal=signal,
            confidence=confidence,
            description=f"Price position: {position:.2%} between bands"
        )
    
    def _calculate_rsi(self, close: pd.Series, window: int = 14) -> TechnicalIndicator:
        """RSI 계산"""
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        # 신호 생성
        if current_rsi >= 70:
            signal = "SELL"
            confidence = min((current_rsi - 70) / 10, 1.0)
        elif current_rsi <= 30:
            signal = "BUY"
            confidence = min((30 - current_rsi) / 10, 1.0)
        else:
            signal = "HOLD"
            confidence = 0.5
        
        return TechnicalIndicator(
            name="RSI",
            value=current_rsi,
            signal=signal,
            confidence=confidence,
            description=f"RSI: {current_rsi:.1f} ({'Overbought' if current_rsi > 70 else 'Oversold' if current_rsi < 30 else 'Neutral'})"
        )
    
    def _calculate_macd(self, close: pd.Series, fast: int = 12, slow: int = 26, signal_period: int = 9) -> TechnicalIndicator:
        """MACD 계산"""
        exp1 = close.ewm(span=fast).mean()
        exp2 = close.ewm(span=slow).mean()
        macd_line = exp1 - exp2
        signal_line = macd_line.ewm(span=signal_period).mean()
        histogram = macd_line - signal_line
        
        current_macd = macd_line.iloc[-1]
        current_signal = signal_line.iloc[-1]
        current_histogram = histogram.iloc[-1]
        prev_histogram = histogram.iloc[-2] if len(histogram) > 1 else 0
        
        # 신호 생성
        if current_macd > current_signal and prev_histogram < 0 < current_histogram:
            signal = "BUY"
            confidence = 0.8
        elif current_macd < current_signal and prev_histogram > 0 > current_histogram:
            signal = "SELL"
            confidence = 0.8
        else:
            signal = "HOLD"
            confidence = 0.5
        
        return TechnicalIndicator(
            name="MACD",
            value=current_histogram,
            signal=signal,
            confidence=confidence,
            description=f"MACD: {current_macd:.4f}, Signal: {current_signal:.4f}, Histogram: {current_histogram:.4f}"
        )
    
    def _calculate_stochastic(self, high: pd.Series, low: pd.Series, close: pd.Series, k_window: int = 14, d_window: int = 3) -> TechnicalIndicator:
        """스토캐스틱 오실레이터 계산"""
        lowest_low = low.rolling(window=k_window).min()
        highest_high = high.rolling(window=k_window).max()
        
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_window).mean()
        
        current_k = k_percent.iloc[-1]
        current_d = d_percent.iloc[-1]
        
        # 신호 생성
        if current_k >= 80 and current_d >= 80:
            signal = "SELL"
            confidence = 0.7
        elif current_k <= 20 and current_d <= 20:
            signal = "BUY"
            confidence = 0.7
        else:
            signal = "HOLD"
            confidence = 0.5
        
        return TechnicalIndicator(
            name="Stochastic",
            value=current_k,
            signal=signal,
            confidence=confidence,
            description=f"Stochastic %K: {current_k:.1f}, %D: {current_d:.1f}"
        )
    
    def _calculate_williams_r(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> TechnicalIndicator:
        """Williams %R 계산"""
        highest_high = high.rolling(window=window).max()
        lowest_low = low.rolling(window=window).min()
        
        williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low))
        current_wr = williams_r.iloc[-1]
        
        # 신호 생성
        if current_wr >= -20:
            signal = "SELL"
            confidence = 0.7
        elif current_wr <= -80:
            signal = "BUY"
            confidence = 0.7
        else:
            signal = "HOLD"
            confidence = 0.5
        
        return TechnicalIndicator(
            name="Williams %R",
            value=current_wr,
            signal=signal,
            confidence=confidence,
            description=f"Williams %R: {current_wr:.1f}"
        )
    
    def _calculate_atr(self, high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> TechnicalIndicator:
        """Average True Range 계산"""
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(window=window).mean()
        current_atr = atr.iloc[-1]
        
        # ATR은 변동성 지표이므로 직접적인 매매 신호는 제공하지 않음
        signal = "HOLD"
        confidence = 0.5
        
        return TechnicalIndicator(
            name="ATR",
            value=current_atr,
            signal=signal,
            confidence=confidence,
            description=f"Average True Range: {current_atr:.2f} (Volatility measure)"
        )
    
    def _calculate_obv(self, close: pd.Series, volume: pd.Series) -> TechnicalIndicator:
        """On-Balance Volume 계산"""
        obv = (np.sign(close.diff()) * volume).fillna(0).cumsum()
        current_obv = obv.iloc[-1]
        
        # OBV 트렌드 분석
        obv_ma = obv.rolling(window=10).mean()
        if current_obv > obv_ma.iloc[-1]:
            signal = "BUY"
            confidence = 0.6
        elif current_obv < obv_ma.iloc[-1]:
            signal = "SELL"
            confidence = 0.6
        else:
            signal = "HOLD"
            confidence = 0.5
        
        return TechnicalIndicator(
            name="OBV",
            value=current_obv,
            signal=signal,
            confidence=confidence,
            description=f"On-Balance Volume: {current_obv:.0f}"
        )
    
    def _calculate_fibonacci_levels(self, high: pd.Series, low: pd.Series) -> TechnicalIndicator:
        """피보나치 되돌림 레벨 계산"""
        max_price = high.max()
        min_price = low.min()
        
        diff = max_price - min_price
        levels = {
            0.236: max_price - 0.236 * diff,
            0.382: max_price - 0.382 * diff,
            0.500: max_price - 0.500 * diff,
            0.618: max_price - 0.618 * diff,
            0.786: max_price - 0.786 * diff
        }
        
        current_price = high.iloc[-1]  # 종가 대신 고가 사용
        
        # 현재 가격이 어느 피보나치 레벨 근처에 있는지 확인
        signal = "HOLD"
        confidence = 0.5
        closest_level = min(levels.values(), key=lambda x: abs(x - current_price))
        
        return TechnicalIndicator(
            name="Fibonacci",
            value=closest_level,
            signal=signal,
            confidence=confidence,
            description=f"Fibonacci levels: {levels}"
        )
    
    def analyze_trend(self, price_data: pd.DataFrame) -> TrendAnalysis:
        """트렌드 분석"""
        if price_data.empty:
            return TrendAnalysis(
                direction=TrendDirection.NEUTRAL,
                strength=0.0,
                duration_days=0,
                slope=0.0,
                confidence=0.0,
                key_levels=[]
            )
        
        close = price_data['Close']
        high = price_data['High']
        low = price_data['Low']
        
        # 이동평균 기반 트렌드 분석
        ma_short = close.rolling(window=20).mean()
        ma_long = close.rolling(window=50).mean()
        
        # 현재 트렌드 방향
        current_price = close.iloc[-1]
        current_ma_short = ma_short.iloc[-1]
        current_ma_long = ma_long.iloc[-1]
        
        # 선형 회귀를 통한 트렌드 강도 계산
        x = np.arange(len(close))
        coeffs = np.polyfit(x, close, 1)
        slope = coeffs[0]
        
        # 트렌드 방향 결정
        if current_price > current_ma_short > current_ma_long and slope > 0:
            if slope > close.std() * 0.1:
                direction = TrendDirection.STRONG_BULLISH
                strength = min(slope / (close.std() * 0.1), 1.0)
            else:
                direction = TrendDirection.BULLISH
                strength = 0.7
        elif current_price < current_ma_short < current_ma_long and slope < 0:
            if abs(slope) > close.std() * 0.1:
                direction = TrendDirection.STRONG_BEARISH
                strength = min(abs(slope) / (close.std() * 0.1), 1.0)
            else:
                direction = TrendDirection.BEARISH
                strength = 0.7
        else:
            direction = TrendDirection.NEUTRAL
            strength = 0.5
        
        # 지지/저항 레벨 찾기
        key_levels = self._find_support_resistance_levels(high, low, close)
        
        # 트렌드 지속 기간 계산
        duration_days = self._calculate_trend_duration(close, ma_short)
        
        # 신뢰도 계산
        confidence = min(strength * 0.8 + 0.2, 1.0)
        
        return TrendAnalysis(
            direction=direction,
            strength=strength,
            duration_days=duration_days,
            slope=slope,
            confidence=confidence,
            key_levels=key_levels
        )
    
    def _find_support_resistance_levels(self, high: pd.Series, low: pd.Series, close: pd.Series) -> List[PriceLevel]:
        """지지/저항 레벨 찾기"""
        levels = []
        
        # 지지선 찾기 (최근 저점들)
        local_mins = []
        for i in range(5, len(low) - 5):
            if low.iloc[i] == low.iloc[i-5:i+5].min():
                local_mins.append((i, low.iloc[i]))
        
        # 저항선 찾기 (최근 고점들)
        local_maxs = []
        for i in range(5, len(high) - 5):
            if high.iloc[i] == high.iloc[i-5:i+5].max():
                local_maxs.append((i, high.iloc[i]))
        
        # 지지선 레벨 생성
        for idx, price in local_mins[-3:]:  # 최근 3개 지지선
            levels.append(PriceLevel(
                price=price,
                level_type='support',
                strength=SupportResistanceLevel.MODERATE,
                touches=1,
                last_touch_date=datetime.now() - timedelta(days=len(low)-idx)
            ))
        
        # 저항선 레벨 생성
        for idx, price in local_maxs[-3:]:  # 최근 3개 저항선
            levels.append(PriceLevel(
                price=price,
                level_type='resistance',
                strength=SupportResistanceLevel.MODERATE,
                touches=1,
                last_touch_date=datetime.now() - timedelta(days=len(high)-idx)
            ))
        
        return levels
    
    def _calculate_trend_duration(self, close: pd.Series, ma: pd.Series) -> int:
        """트렌드 지속 기간 계산"""
        if len(close) < 2 or len(ma) < 2:
            return 0
        
        # 현재 트렌드 방향 확인
        current_above_ma = close.iloc[-1] > ma.iloc[-1]
        
        duration = 0
        for i in range(len(close) - 1, 0, -1):
            if (close.iloc[i] > ma.iloc[i]) == current_above_ma:
                duration += 1
            else:
                break
        
        return duration
    
    def predict_price_ml(self, price_data: pd.DataFrame, days_ahead: int = 5) -> Optional[PredictionResult]:
        """머신러닝을 활용한 가격 예측"""
        if not SKLEARN_AVAILABLE:
            self.logger.warning("Scikit-learn not available. Price prediction skipped.")
            return None
        
        if price_data.empty or len(price_data) < 50:
            return None
        
        try:
            # 특성 엔지니어링
            features = self._create_ml_features(price_data)
            
            if features.empty:
                return None
            
            # 타겟 변수 (다음 날 종가)
            target = price_data['Close'].shift(-1).dropna()
            
            # 데이터 정렬
            min_len = min(len(features), len(target))
            features = features.iloc[:min_len]
            target = target.iloc[:min_len]
            
            # 훈련/테스트 데이터 분할
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, test_size=0.2, random_state=42, shuffle=False
            )
            
            # 데이터 스케일링
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # 모델 훈련 (Random Forest)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
            
            # 모델 평가
            y_pred = model.predict(X_test_scaled)
            accuracy = r2_score(y_test, y_pred)
            
            # 미래 가격 예측
            last_features = features.iloc[-1:].values
            last_features_scaled = scaler.transform(last_features)
            predicted_price = model.predict(last_features_scaled)[0]
            
            # 신뢰구간 계산 (간단한 방법)
            prediction_error = np.sqrt(mean_squared_error(y_test, y_pred))
            confidence_interval = (
                predicted_price - 1.96 * prediction_error,
                predicted_price + 1.96 * prediction_error
            )
            
            # 특성 중요도
            feature_importance = dict(zip(features.columns, model.feature_importances_))
            
            return PredictionResult(
                predicted_price=predicted_price,
                confidence_interval=confidence_interval,
                model_accuracy=accuracy,
                prediction_horizon_days=days_ahead,
                features_importance=feature_importance
            )
            
        except Exception as e:
            self.logger.error(f"Error in ML price prediction: {e}")
            return None
    
    def _create_ml_features(self, price_data: pd.DataFrame) -> pd.DataFrame:
        """머신러닝을 위한 특성 생성"""
        features = pd.DataFrame(index=price_data.index)
        
        close = price_data['Close']
        high = price_data['High']
        low = price_data['Low']
        volume = price_data['Volume']
        
        # 기본 특성
        features['close'] = close
        features['high'] = high
        features['low'] = low
        features['volume'] = volume
        
        # 이동평균
        features['ma_5'] = close.rolling(5).mean()
        features['ma_10'] = close.rolling(10).mean()
        features['ma_20'] = close.rolling(20).mean()
        features['ma_50'] = close.rolling(50).mean()
        
        # 가격 변화율
        features['price_change'] = close.pct_change()
        features['price_change_5'] = close.pct_change(5)
        features['price_change_10'] = close.pct_change(10)
        
        # 변동성
        features['volatility_5'] = close.rolling(5).std()
        features['volatility_20'] = close.rolling(20).std()
        
        # 거래량 관련
        features['volume_ma_10'] = volume.rolling(10).mean()
        features['volume_ratio'] = volume / features['volume_ma_10']
        
        # RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        features['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = close.ewm(span=12).mean()
        exp2 = close.ewm(span=26).mean()
        features['macd'] = exp1 - exp2
        features['macd_signal'] = features['macd'].ewm(span=9).mean()
        
        # 볼린저 밴드
        rolling_mean = close.rolling(20).mean()
        rolling_std = close.rolling(20).std()
        features['bb_upper'] = rolling_mean + (rolling_std * 2)
        features['bb_lower'] = rolling_mean - (rolling_std * 2)
        features['bb_position'] = (close - features['bb_lower']) / (features['bb_upper'] - features['bb_lower'])
        
        # NaN 값 제거
        features = features.dropna()
        
        return features
    
    def generate_comprehensive_analysis(self, symbol: str) -> Dict[str, Any]:
        """종합 분석 리포트 생성"""
        try:
            # 가격 데이터 가져오기
            price_data = self.get_stock_price_history(symbol, period="1y")
            
            if price_data.empty:
                return {"error": f"No data available for {symbol}"}
            
            # 기술적 지표 계산
            indicators = self.calculate_advanced_indicators(price_data)
            
            # 트렌드 분석
            trend_analysis = self.analyze_trend(price_data)
            
            # 머신러닝 예측
            ml_prediction = self.predict_price_ml(price_data)
            
            # 종합 점수 계산
            overall_score = self._calculate_overall_score(indicators, trend_analysis)
            
            # 추천 생성
            recommendation = self._generate_recommendation(overall_score, indicators, trend_analysis)
            
            return {
                "symbol": symbol,
                "analysis_date": datetime.now().isoformat(),
                "technical_indicators": {name: {
                    "value": ind.value,
                    "signal": ind.signal,
                    "confidence": ind.confidence,
                    "description": ind.description
                } for name, ind in indicators.items()},
                "trend_analysis": {
                    "direction": trend_analysis.direction.value,
                    "strength": trend_analysis.strength,
                    "duration_days": trend_analysis.duration_days,
                    "slope": trend_analysis.slope,
                    "confidence": trend_analysis.confidence,
                    "key_levels_count": len(trend_analysis.key_levels)
                },
                "ml_prediction": {
                    "predicted_price": ml_prediction.predicted_price if ml_prediction else None,
                    "confidence_interval": ml_prediction.confidence_interval if ml_prediction else None,
                    "model_accuracy": ml_prediction.model_accuracy if ml_prediction else None,
                    "prediction_horizon_days": ml_prediction.prediction_horizon_days if ml_prediction else None
                } if ml_prediction else None,
                "overall_score": overall_score,
                "recommendation": recommendation
            }
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive analysis for {symbol}: {e}")
            return {"error": str(e)}
    
    def _calculate_overall_score(self, indicators: Dict[str, TechnicalIndicator], trend_analysis: TrendAnalysis) -> float:
        """전체 점수 계산 (0-100)"""
        if not indicators:
            return 50.0
        
        # 매수 신호 가중치
        buy_signals = 0
        sell_signals = 0
        total_confidence = 0
        
        for indicator in indicators.values():
            if indicator.signal == "BUY":
                buy_signals += indicator.confidence
            elif indicator.signal == "SELL":
                sell_signals += indicator.confidence
            total_confidence += indicator.confidence
        
        # 트렌드 가중치
        trend_weight = 0.3
        if trend_analysis.direction in [TrendDirection.BULLISH, TrendDirection.STRONG_BULLISH]:
            trend_score = 70 + (trend_analysis.strength * 30)
        elif trend_analysis.direction in [TrendDirection.BEARISH, TrendDirection.STRONG_BEARISH]:
            trend_score = 30 - (trend_analysis.strength * 30)
        else:
            trend_score = 50
        
        # 지표 가중치
        indicator_weight = 0.7
        if total_confidence > 0:
            indicator_score = 50 + ((buy_signals - sell_signals) / total_confidence) * 50
        else:
            indicator_score = 50
        
        overall_score = (trend_score * trend_weight) + (indicator_score * indicator_weight)
        return max(0, min(100, overall_score))
    
    def _generate_recommendation(self, overall_score: float, indicators: Dict[str, TechnicalIndicator], trend_analysis: TrendAnalysis) -> Dict[str, Any]:
        """추천 생성"""
        if overall_score >= 70:
            action = "STRONG BUY"
            reason = "Multiple bullish indicators and strong upward trend"
        elif overall_score >= 60:
            action = "BUY"
            reason = "Positive technical indicators suggest upward momentum"
        elif overall_score >= 40:
            action = "HOLD"
            reason = "Mixed signals, wait for clearer direction"
        elif overall_score >= 30:
            action = "SELL"
            reason = "Negative technical indicators suggest downward pressure"
        else:
            action = "STRONG SELL"
            reason = "Multiple bearish indicators and strong downward trend"
        
        # 주요 지지/저항 레벨
        key_levels = []
        for level in trend_analysis.key_levels[:3]:  # 상위 3개
            key_levels.append({
                "price": level.price,
                "type": level.level_type,
                "strength": level.strength.value
            })
        
        return {
            "action": action,
            "confidence": min(max(overall_score, 10), 90) / 100,
            "reason": reason,
            "key_levels": key_levels,
            "risk_level": "High" if abs(overall_score - 50) > 30 else "Medium" if abs(overall_score - 50) > 15 else "Low"
        }

# 전역 인스턴스
advanced_technical_analyzer = AdvancedTechnicalAnalyzer()