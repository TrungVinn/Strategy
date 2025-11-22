"""Data models for crypto market analysis"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class MarketData:
    """Market data structure"""
    symbol: str
    timestamp: datetime
    price: float
    volume_24h: float
    volume_avg_7d: float
    open_interest: Optional[float] = None
    funding_rate: Optional[float] = None
    ma_20: Optional[float] = None
    ma_50: Optional[float] = None
    ma_200: Optional[float] = None
    high_24h: Optional[float] = None
    low_24h: Optional[float] = None
    liquidations: Optional[Dict] = None
    sentiment_score: Optional[float] = None


@dataclass
class Anomaly:
    """Anomaly detection result"""
    type: str  # 'oi_spike', 'volume_spike', 'whale_transfer', 'liquidation_risk'
    severity: str  # 'low', 'medium', 'high'
    description: str
    value: Optional[float] = None


@dataclass
class MarketAnalysis:
    """Market analysis result"""
    symbol: str
    timestamp: datetime
    trend: str  # 'bullish', 'bearish', 'neutral'
    trend_emoji: str  # '📈', '📉', '➡️'
    trend_description: str
    volume_change_pct: float
    funding_rate_status: str  # 'bình thường', 'cao', 'nguy hiểm'
    volatility_status: str  # 'thấp', 'trung bình', 'mạnh'
    anomalies: List[Anomaly] = field(default_factory=list)
    key_levels: Dict[str, float] = field(default_factory=dict)
    trading_direction: str = ""
    market_data: Optional[MarketData] = None


@dataclass
class AgentState:
    """State for LangGraph agent"""
    symbol: str
    raw_data: Optional[MarketData] = None
    analysis: Optional[MarketAnalysis] = None
    report: str = ""
    error: Optional[str] = None
