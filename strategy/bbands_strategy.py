import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy

class BBandsStrategy(BaseStrategy):
    def __init__(self, period: int = 20, std_dev: float = 2.0, initial_capital: float = 100000):
        super().__init__(initial_capital)
        self.period = period
        self.std_dev = std_dev
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Bollinger Bands and additional indicators"""
        # Calculate middle band (SMA)
        df['bb_middle'] = df['Close'].rolling(window=self.period).mean()
        
        # Calculate standard deviation
        rolling_std = df['Close'].rolling(window=self.period).std()
        
        # Calculate upper and lower bands
        df['bb_upper'] = df['bb_middle'] + (rolling_std * self.std_dev)
        df['bb_lower'] = df['bb_middle'] - (rolling_std * self.std_dev)
        
        # Calculate %B indicator (position within bands)
        df['bb_b'] = (df['Close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        # Calculate Bandwidth (volatility indicator)
        df['bb_bandwidth'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
        
        # Add momentum indicators
        df['price_mom'] = df['Close'].pct_change()
        df['price_mom_ma'] = df['price_mom'].rolling(window=5).mean()
        
        # Add volume analysis
        df['volume_ma'] = df['Volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['Volume'] / df['volume_ma']
        
        # Add trend direction
        df['trend'] = np.where(df['Close'] > df['bb_middle'], 1, -1)
        
        # Add band touches
        df['upper_touch'] = np.where(df['High'] >= df['bb_upper'], 1, 0)
        df['lower_touch'] = np.where(df['Low'] <= df['bb_lower'], 1, 0)
        
        # Add band compression/expansion
        df['bb_bandwidth_ma'] = df['bb_bandwidth'].rolling(window=10).mean()
        df['bands_expanding'] = df['bb_bandwidth'] > df['bb_bandwidth_ma']
        
        return df
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate enhanced Bollinger Bands trading signals"""
        df['signal_line'] = 0
        
        # Buy conditions:
        buy_condition = (
            # Bounce from lower band
            ((df['Close'] > df['bb_lower']) & 
             (df['Close'].shift(1) <= df['bb_lower'].shift(1)) &
             (df['volume_ratio'] > 1.2) &
             (df['price_mom'] > 0)) |
            
            # Middle band breakout
            ((df['Close'] > df['bb_middle']) &
             (df['Close'].shift(1) <= df['bb_middle'].shift(1)) &
             (df['trend'] == 1) &
             (df['volume_ratio'] > 1)) |
            
            # Squeeze breakout
            ((df['bb_bandwidth'] > df['bb_bandwidth_ma']) &
             (df['bb_bandwidth'].shift(1) <= df['bb_bandwidth_ma'].shift(1)) &
             (df['Close'] > df['bb_middle']) &
             (df['price_mom'] > 0)) |
            
            # Double bottom pattern
            ((df['lower_touch'] == 1) &
             (df['lower_touch'].shift(3) == 1) &
             (df['Close'] > df['Low'].shift(1)) &
             (df['volume_ratio'] > 1.5))
        )
        df.loc[buy_condition, 'signal_line'] = 1
        
        # Sell conditions:
        sell_condition = (
            # Upper band rejection
            ((df['Close'] < df['bb_upper']) &
             (df['Close'].shift(1) >= df['bb_upper'].shift(1)) &
             (df['price_mom'] < 0) &
             (df['volume_ratio'] > 1.2)) |
            
            # Middle band breakdown
            ((df['Close'] < df['bb_middle']) &
             (df['Close'].shift(1) >= df['bb_middle'].shift(1)) &
             (df['trend'] == -1) &
             (df['volume_ratio'] > 1)) |
            
            # Volatility expansion sell
            ((df['bb_bandwidth'] > df['bb_bandwidth_ma']) &
             (df['Close'] < df['bb_middle']) &
             (df['price_mom'] < 0)) |
            
            # Double top pattern
            ((df['upper_touch'] == 1) &
             (df['upper_touch'].shift(3) == 1) &
             (df['Close'] < df['High'].shift(1)) &
             (df['volume_ratio'] > 1.5))
        )
        df.loc[sell_condition, 'signal_line'] = -1
        
        return df 