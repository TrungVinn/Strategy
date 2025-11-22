"""Configuration file for Crypto Market Analysis Agent"""

# API Configuration
BINANCE_API_KEY = ""  # User needs to set this
BINANCE_API_SECRET = ""  # User needs to set this

# Default symbols to analyze
DEFAULT_SYMBOLS = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT"]

# Analysis parameters
MA_PERIODS = [20, 50, 200]
VOLUME_LOOKBACK = 7  # days
FUNDING_RATE_THRESHOLD = 0.01  # 1%
OI_SPIKE_THRESHOLD = 0.15  # 15% increase
VOLUME_SPIKE_THRESHOLD = 0.30  # 30% increase

# Data refresh interval (seconds)
REFRESH_INTERVAL = 60

# OpenAI API Key (for LangGraph - optional, can work without it)
OPENAI_API_KEY = ""  # User can set this for enhanced analysis

# Analysis timeframe
TIMEFRAME = "1h"  # candlestick timeframe
