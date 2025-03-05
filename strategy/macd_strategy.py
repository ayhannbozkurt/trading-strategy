import pandas as pd
from .base_strategy import BaseStrategy

class MACDStrategy(BaseStrategy):
    def __init__(self, fast_period: int = 12, slow_period: int = 26, 
                 signal_period: int = 9, initial_capital: float = 100000):
        super().__init__(initial_capital)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate MACD indicators"""
        # Fast EMA
        df['ema_fast'] = df['Close'].ewm(span=self.fast_period, adjust=False).mean()
        
        # Slow EMA
        df['ema_slow'] = df['Close'].ewm(span=self.slow_period, adjust=False).mean()
        
        # MACD Line
        df['macd'] = df['ema_fast'] - df['ema_slow']
        
        # Signal Line
        df['signal'] = df['macd'].ewm(span=self.signal_period, adjust=False).mean()
        
        # MACD Histogram
        df['histogram'] = df['macd'] - df['signal']
        
        return df
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate MACD trading signals"""
        df['signal_line'] = 0
        
        # Buy when MACD crosses above signal line
        buy_condition = (df['macd'] > df['signal']) & (df['macd'].shift(1) <= df['signal'].shift(1))
        df.loc[buy_condition, 'signal_line'] = 1
        
        # Sell when MACD crosses below signal line
        sell_condition = (df['macd'] < df['signal']) & (df['macd'].shift(1) >= df['signal'].shift(1))
        df.loc[sell_condition, 'signal_line'] = -1
        
        return df 