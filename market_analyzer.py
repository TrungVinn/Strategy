"""Market analysis module"""
import numpy as np
from typing import List, Dict, Tuple
from models import MarketData, MarketAnalysis, Anomaly
from datetime import datetime
import config


class MarketAnalyzer:
    """Analyzes market data and detects anomalies"""
    
    def __init__(self):
        pass
    
    def analyze_trend(self, data: MarketData) -> Tuple[str, str, str]:
        """
        Analyze market trend based on moving averages
        Returns: (trend, emoji, description)
        """
        price = data.price
        ma_20 = data.ma_20
        ma_50 = data.ma_50
        ma_200 = data.ma_200
        
        # Check if we have enough data
        if not ma_20 or not ma_50:
            return "neutral", "➡️", "Chưa đủ dữ liệu để xác định xu hướng"
        
        # Determine trend
        if price > ma_20 and ma_20 > ma_50:
            if ma_200 and price > ma_200:
                return "bullish", "📈", "Xu hướng tăng mạnh, giá trên các MA chính"
            return "bullish", "📈", "Xu hướng tăng ngắn hạn, giá trên MA20 và MA50"
        elif price < ma_20 and ma_20 < ma_50:
            if ma_200 and price < ma_200:
                return "bearish", "📉", "Xu hướng giảm mạnh, giá dưới các MA chính"
            return "bearish", "📉", "Xu hướng giảm ngắn hạn, giá dưới MA20 và MA50"
        else:
            return "neutral", "➡️", "Thị trường đang sideway, chưa có xu hướng rõ ràng"
    
    def calculate_volume_change(self, data: MarketData) -> float:
        """Calculate volume change percentage"""
        if data.volume_avg_7d == 0:
            return 0.0
        return ((data.volume_24h - data.volume_avg_7d) / data.volume_avg_7d) * 100
    
    def analyze_funding_rate(self, data: MarketData) -> str:
        """Analyze funding rate status"""
        if data.funding_rate is None:
            return "không có dữ liệu"
        
        fr = abs(data.funding_rate)
        
        if fr < config.FUNDING_RATE_THRESHOLD * 0.5:
            return "bình thường"
        elif fr < config.FUNDING_RATE_THRESHOLD:
            return "cao"
        else:
            return "nguy hiểm"
    
    def calculate_volatility(self, data: MarketData) -> str:
        """Calculate volatility status"""
        if not data.high_24h or not data.low_24h:
            return "không xác định"
        
        volatility_pct = ((data.high_24h - data.low_24h) / data.low_24h) * 100
        
        if volatility_pct < 3:
            return "thấp"
        elif volatility_pct < 7:
            return "trung bình"
        else:
            return "mạnh"
    
    def detect_anomalies(self, data: MarketData) -> List[Anomaly]:
        """Detect market anomalies"""
        anomalies = []
        
        # 1. Volume spike detection
        volume_change = self.calculate_volume_change(data)
        if volume_change > config.VOLUME_SPIKE_THRESHOLD * 100:
            anomalies.append(Anomaly(
                type="volume_spike",
                severity="high" if volume_change > 50 else "medium",
                description=f"Volume tăng đột biến {volume_change:.1f}% so với trung bình",
                value=volume_change
            ))
        
        # 2. Funding rate extreme
        if data.funding_rate and abs(data.funding_rate) > config.FUNDING_RATE_THRESHOLD:
            anomalies.append(Anomaly(
                type="funding_extreme",
                severity="high",
                description=f"Funding rate {'dương' if data.funding_rate > 0 else 'âm'} cực đoan, nguy cơ squeeze",
                value=data.funding_rate
            ))
        
        # 3. Open Interest spike (if we have historical OI, compare)
        # For now, we'll skip this as we need historical data
        
        # 4. Liquidation risk
        if data.liquidations:
            total_liq = data.liquidations.get('total_liquidations', 0)
            if total_liq > 50:  # Threshold for high liquidations
                long_liq = data.liquidations.get('long_liquidations', 0)
                short_liq = data.liquidations.get('short_liquidations', 0)
                
                if long_liq > short_liq * 2:
                    desc = f"Thanh lý long cao ({long_liq}), áp lực giảm mạnh"
                elif short_liq > long_liq * 2:
                    desc = f"Thanh lý short cao ({short_liq}), áp lực tăng mạnh"
                else:
                    desc = f"Thanh lý lớn cả 2 chiều ({total_liq} vị thế)"
                
                anomalies.append(Anomaly(
                    type="liquidation_risk",
                    severity="medium",
                    description=desc,
                    value=float(total_liq)
                ))
        
        return anomalies
    
    def calculate_key_levels(self, data: MarketData) -> Dict[str, float]:
        """Calculate key price levels"""
        levels = {}
        
        # Support and resistance from 24h high/low
        if data.high_24h and data.low_24h:
            levels['support'] = data.low_24h
            levels['resistance'] = data.high_24h
        
        # MA levels as key levels
        if data.ma_50:
            levels['ma_50'] = data.ma_50
        if data.ma_200:
            levels['ma_200'] = data.ma_200
        
        return levels
    
    def generate_trading_direction(self, analysis: MarketAnalysis) -> str:
        """Generate trading direction suggestion"""
        trend = analysis.trend
        funding_status = analysis.funding_rate_status
        volume_change = analysis.volume_change_pct
        volatility = analysis.volatility_status
        anomalies = analysis.anomalies
        
        directions = []
        
        # Trend-based direction
        if trend == "bullish":
            if volume_change > 20:
                directions.append("Momentum tăng đang mạnh")
            else:
                directions.append("Xu hướng tăng có thể chưa bền vững")
        elif trend == "bearish":
            if volume_change > 20:
                directions.append("Áp lực bán đang tăng cao")
            else:
                directions.append("Xu hướng giảm có thể sắp đảo chiều")
        else:
            directions.append("Thị trường đang sideway, nên chờ tín hiệu rõ ràng")
        
        # Funding rate consideration
        if funding_status == "nguy hiểm":
            directions.append("Cẩn trọng với khả năng short squeeze hoặc long squeeze")
        
        # Volatility consideration
        if volatility == "mạnh":
            directions.append("Biến động cao, quản lý rủi ro chặt chẽ")
        
        # Anomaly consideration
        for anomaly in anomalies:
            if anomaly.severity == "high":
                if anomaly.type == "volume_spike":
                    directions.append("Có dấu hiệu bất thường về volume, quan sát thêm")
                elif anomaly.type == "funding_extreme":
                    directions.append("Funding rate cực đoan, có thể đảo chiều bất ngờ")
        
        # Return best direction or default
        if directions:
            return directions[0]
        return "Chờ tín hiệu xác nhận trước khi hành động"
    
    def analyze_market(self, data: MarketData) -> MarketAnalysis:
        """Perform complete market analysis"""
        # Analyze trend
        trend, emoji, trend_desc = self.analyze_trend(data)
        
        # Calculate volume change
        volume_change = self.calculate_volume_change(data)
        
        # Analyze funding rate
        funding_status = self.analyze_funding_rate(data)
        
        # Calculate volatility
        volatility = self.calculate_volatility(data)
        
        # Detect anomalies
        anomalies = self.detect_anomalies(data)
        
        # Calculate key levels
        key_levels = self.calculate_key_levels(data)
        
        # Create analysis object
        analysis = MarketAnalysis(
            symbol=data.symbol,
            timestamp=datetime.now(),
            trend=trend,
            trend_emoji=emoji,
            trend_description=trend_desc,
            volume_change_pct=volume_change,
            funding_rate_status=funding_status,
            volatility_status=volatility,
            anomalies=anomalies,
            key_levels=key_levels,
            trading_direction="",
            market_data=data
        )
        
        # Generate trading direction
        analysis.trading_direction = self.generate_trading_direction(analysis)
        
        return analysis


def get_market_analyzer() -> MarketAnalyzer:
    """Factory function to get MarketAnalyzer instance"""
    return MarketAnalyzer()
