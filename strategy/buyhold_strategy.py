import pandas as pd
from .base_strategy import BaseStrategy

class BuyHoldStrategy(BaseStrategy):
    def __init__(self, initial_capital: float = 100000):
        super().__init__(initial_capital)
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """No indicators needed for buy & hold"""
        return df
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate buy & hold signals"""
        df['signal_line'] = 0
        
        # Buy at the first opportunity
        df.iloc[1, df.columns.get_loc('signal_line')] = 1
        
        # Sell at the last day
        df.iloc[-1, df.columns.get_loc('signal_line')] = -1
        
        return df 