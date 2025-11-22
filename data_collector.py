"""Data collection module for crypto market data"""
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import asyncio
import aiohttp
from models import MarketData
import config


class DataCollector:
    """Collects market data from various sources"""
    
    def __init__(self):
        self.exchange = ccxt.binance({
            'apiKey': config.BINANCE_API_KEY,
            'secret': config.BINANCE_API_SECRET,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'  # Use futures for funding rate and OI
            }
        })
        
    async def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 200) -> pd.DataFrame:
        """Fetch OHLCV data"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Error fetching OHLCV for {symbol}: {e}")
            return pd.DataFrame()
    
    async def fetch_funding_rate(self, symbol: str) -> Optional[float]:
        """Fetch current funding rate"""
        try:
            # Convert symbol format for futures
            futures_symbol = symbol.replace('/', '')
            funding = self.exchange.fetch_funding_rate(symbol)
            return funding.get('fundingRate', None)
        except Exception as e:
            print(f"Error fetching funding rate for {symbol}: {e}")
            return None
    
    async def fetch_open_interest(self, symbol: str) -> Optional[float]:
        """Fetch open interest"""
        try:
            oi = self.exchange.fetch_open_interest(symbol)
            return oi.get('openInterestAmount', None)
        except Exception as e:
            print(f"Error fetching open interest for {symbol}: {e}")
            return None
    
    async def fetch_24h_ticker(self, symbol: str) -> Dict:
        """Fetch 24h ticker data"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            print(f"Error fetching ticker for {symbol}: {e}")
            return {}
    
    async def fetch_liquidations(self, symbol: str) -> Optional[Dict]:
        """Fetch liquidation data (using Binance API)"""
        try:
            async with aiohttp.ClientSession() as session:
                futures_symbol = symbol.replace('/', '')
                url = f"https://fapi.binance.com/fapi/v1/allForceOrders?symbol={futures_symbol}&limit=100"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Process liquidation data
                        liq_data = {
                            'total_liquidations': len(data),
                            'long_liquidations': sum(1 for x in data if x['side'] == 'SELL'),
                            'short_liquidations': sum(1 for x in data if x['side'] == 'BUY'),
                        }
                        return liq_data
        except Exception as e:
            print(f"Error fetching liquidations for {symbol}: {e}")
        return None
    
    async def fetch_sentiment(self, symbol: str) -> Optional[float]:
        """Fetch market sentiment (placeholder - can integrate with sentiment API)"""
        # This is a placeholder. In production, integrate with:
        # - LunarCrush API
        # - Fear & Greed Index
        # - Social media sentiment analysis
        try:
            # Return neutral sentiment for now
            return 0.5  # Range: 0 (extreme fear) to 1 (extreme greed)
        except Exception as e:
            print(f"Error fetching sentiment for {symbol}: {e}")
            return None
    
    def calculate_moving_averages(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate moving averages"""
        mas = {}
        for period in config.MA_PERIODS:
            if len(df) >= period:
                mas[f'ma_{period}'] = df['close'].rolling(window=period).mean().iloc[-1]
            else:
                mas[f'ma_{period}'] = None
        return mas
    
    def calculate_volume_avg(self, df: pd.DataFrame, days: int = 7) -> float:
        """Calculate average volume"""
        if len(df) < days * 24:  # hourly data
            return df['volume'].mean()
        return df['volume'].tail(days * 24).mean()
    
    async def collect_market_data(self, symbol: str) -> MarketData:
        """Collect all market data for a symbol"""
        try:
            # Fetch OHLCV data
            df = await self.fetch_ohlcv(symbol, config.TIMEFRAME, limit=200)
            
            if df.empty:
                raise ValueError(f"No OHLCV data available for {symbol}")
            
            # Fetch other data
            ticker = await self.fetch_24h_ticker(symbol)
            funding_rate = await self.fetch_funding_rate(symbol)
            open_interest = await self.fetch_open_interest(symbol)
            liquidations = await self.fetch_liquidations(symbol)
            sentiment = await self.fetch_sentiment(symbol)
            
            # Calculate indicators
            mas = self.calculate_moving_averages(df)
            volume_avg_7d = self.calculate_volume_avg(df, days=7)
            
            # Create MarketData object
            market_data = MarketData(
                symbol=symbol,
                timestamp=datetime.now(),
                price=float(df['close'].iloc[-1]),
                volume_24h=float(ticker.get('quoteVolume', df['volume'].tail(24).sum())),
                volume_avg_7d=float(volume_avg_7d),
                open_interest=float(open_interest) if open_interest else None,
                funding_rate=float(funding_rate) if funding_rate else None,
                ma_20=float(mas.get('ma_20')) if mas.get('ma_20') else None,
                ma_50=float(mas.get('ma_50')) if mas.get('ma_50') else None,
                ma_200=float(mas.get('ma_200')) if mas.get('ma_200') else None,
                high_24h=float(ticker.get('high', df['high'].tail(24).max())),
                low_24h=float(ticker.get('low', df['low'].tail(24).min())),
                liquidations=liquidations,
                sentiment_score=sentiment
            )
            
            return market_data
            
        except Exception as e:
            print(f"Error collecting market data for {symbol}: {e}")
            raise


def get_data_collector() -> DataCollector:
    """Factory function to get DataCollector instance"""
    return DataCollector()
