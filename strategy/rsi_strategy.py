import pandas as pd
from .base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    def __init__(self, period: int = 14, overbought: int = 70, 
                 oversold: int = 30, initial_capital: float = 100000):
        super().__init__(initial_capital)
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate RSI and additional indicators"""
        # Calculate price changes
        delta = df['Close'].diff()
        
        # Get gains and losses
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        
        # Calculate RS and RSI
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Add RSI momentum
        df['rsi_mom'] = df['rsi'].diff()
        
        # Add price momentum
        df['price_mom'] = df['Close'].pct_change()
        
        # Add RSI moving average
        df['rsi_ma'] = df['rsi'].rolling(window=10).mean()
        
        # Add volume analysis
        df['volume_ma'] = df['Volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['Volume'] / df['volume_ma']
        
        return df
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate enhanced RSI trading signals"""
        df['signal_line'] = 0
        
        # Buy conditions:
        # 1. RSI crosses above oversold level
        # 2. RSI is below 40 and showing positive momentum
        # 3. RSI is trending up (above its MA) with strong volume
        buy_condition = (
            # Traditional oversold crossover
            ((df['rsi'] > self.oversold) & (df['rsi'].shift(1) <= self.oversold)) |
            
            # RSI momentum based entry
            ((df['rsi'] < 40) & (df['rsi_mom'] > 0) & 
             (df['price_mom'] > 0) & (df['volume_ratio'] > 1.2)) |
            
            # RSI trend following
            ((df['rsi'] > df['rsi_ma']) & (df['rsi'].shift(1) <= df['rsi_ma'].shift(1)) &
             (df['rsi'] < 60) & (df['volume_ratio'] > 1))
        )
        df.loc[buy_condition, 'signal_line'] = 1
        
        # Sell conditions:
        # 1. RSI crosses below overbought level
        # 2. RSI is above 60 and showing negative momentum
        # 3. RSI crosses below its MA with high RSI
        sell_condition = (
            # Traditional overbought crossover
            ((df['rsi'] < self.overbought) & (df['rsi'].shift(1) >= self.overbought)) |
            
            # RSI momentum based exit
            ((df['rsi'] > 60) & (df['rsi_mom'] < 0) & 
             (df['price_mom'] < 0) & (df['volume_ratio'] > 1.2)) |
            
            # RSI trend reversal
            ((df['rsi'] < df['rsi_ma']) & (df['rsi'].shift(1) >= df['rsi_ma'].shift(1)) &
             (df['rsi'] > 40))
        )
        df.loc[sell_condition, 'signal_line'] = -1
        
        return df 