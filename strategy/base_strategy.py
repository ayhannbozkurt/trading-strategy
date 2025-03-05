from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Tuple, Dict

class BaseStrategy(ABC):
    def __init__(self, initial_capital: float = 100000):
        self.initial_capital = initial_capital
    
    @abstractmethod
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate strategy-specific indicators"""
        pass
    
    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals"""
        pass
    
    def backtest(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Run backtest for the strategy
        Returns: (backtest_results, trades)
        """
        df = df.copy()
        df = self.calculate_indicators(df)
        df = self.generate_signals(df)
        
        # Portfolio columns
        df['position'] = 0
        df['cash'] = self.initial_capital
        df['holdings'] = 0
        df['total_value'] = self.initial_capital
        df['returns'] = 0
        
        trades = []
        current_position = 0  # Positive for long, negative for short
        entry_price = 0
        entry_date = None
        
        for i in range(1, len(df)):
            date = df.index[i]
            price = df['Close'].iloc[i]
            signal = df['signal_line'].iloc[i]
            
            # Carry forward position
            df.iloc[i, df.columns.get_loc('position')] = current_position
            df.iloc[i, df.columns.get_loc('cash')] = df['cash'].iloc[i-1]
            df.iloc[i, df.columns.get_loc('holdings')] = current_position * price
            
            # Close existing position if we have a new signal
            if ((signal == 1 and current_position < 0) or  # Close short on buy signal
                (signal == -1 and current_position > 0)):  # Close long on sell signal
                exit_price = price
                
                # Calculate profit/loss based on position type
                if current_position > 0:  # Long position
                    profit_loss = (exit_price - entry_price) * abs(current_position)
                    profit_loss_pct = (exit_price / entry_price - 1) * 100
                else:  # Short position
                    profit_loss = (entry_price - exit_price) * abs(current_position)
                    profit_loss_pct = (entry_price / exit_price - 1) * 100
                
                trades.append({
                    'entry_date': entry_date,
                    'exit_date': date,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'position_type': 'LONG' if current_position > 0 else 'SHORT',
                    'profit_loss': profit_loss,
                    'profit_loss_pct': profit_loss_pct,
                    'trade_duration': (date - entry_date).days
                })
                
                df.iloc[i, df.columns.get_loc('cash')] += current_position * price
                df.iloc[i, df.columns.get_loc('position')] = 0
                df.iloc[i, df.columns.get_loc('holdings')] = 0
                current_position = 0
            
            # Open new position if we have a signal and no current position
            if current_position == 0:
                shares_to_trade = int(df['cash'].iloc[i] // price)
                
                if signal == 1 and shares_to_trade > 0:  # Long position
                    current_position = shares_to_trade
                    entry_price = price
                    entry_date = date
                    
                    df.iloc[i, df.columns.get_loc('cash')] -= shares_to_trade * price
                    
                elif signal == -1 and shares_to_trade > 0:  # Short position
                    current_position = -shares_to_trade
                    entry_price = price
                    entry_date = date
                    
                    df.iloc[i, df.columns.get_loc('cash')] += shares_to_trade * price
                
                df.iloc[i, df.columns.get_loc('position')] = current_position
                df.iloc[i, df.columns.get_loc('holdings')] = current_position * price
            
            # Update total value and returns
            df.iloc[i, df.columns.get_loc('total_value')] = df['cash'].iloc[i] + df['holdings'].iloc[i]
            df.iloc[i, df.columns.get_loc('returns')] = df['total_value'].iloc[i] / df['total_value'].iloc[i-1] - 1
        
        # Close any remaining position at the end
        if current_position != 0:
            exit_price = df['Close'].iloc[-1]
            
            if current_position > 0:  # Long position
                profit_loss = (exit_price - entry_price) * abs(current_position)
                profit_loss_pct = (exit_price / entry_price - 1) * 100
            else:  # Short position
                profit_loss = (entry_price - exit_price) * abs(current_position)
                profit_loss_pct = (entry_price / exit_price - 1) * 100
            
            trades.append({
                'entry_date': entry_date,
                'exit_date': df.index[-1],
                'entry_price': entry_price,
                'exit_price': exit_price,
                'position_type': 'LONG' if current_position > 0 else 'SHORT',
                'profit_loss': profit_loss,
                'profit_loss_pct': profit_loss_pct,
                'trade_duration': (df.index[-1] - entry_date).days
            })
        
        # Calculate cumulative returns
        df['cumulative_returns'] = (1 + df['returns']).cumprod() - 1
        
        # Create trades DataFrame with Turkish column names
        trades_df = pd.DataFrame(trades)
        trades_df.columns = [
            'Giriş Tarihi',
            'Çıkış Tarihi',
            'Giriş Fiyatı',
            'Çıkış Fiyatı',
            'Pozisyon Tipi',
            'Kar/Zarar',
            'Kar/Zarar %',
            'İşlem Süresi (Gün)'
        ]
        
        return df, trades_df
    
    @staticmethod
    def calculate_performance_metrics(df: pd.DataFrame, trades_df: pd.DataFrame) -> Dict:
        """Calculate trading performance metrics"""
        metrics = {}
        
        # Helper function to add arrow
        def add_arrow(value):
            if isinstance(value, (int, float)):
                return f"{value:.2f} {'↑' if value > 0 else '↓'}"
            return value
        
        # Total return
        metrics['total_return'] = add_arrow(df['cumulative_returns'].iloc[-1] * 100)
        
        # Annual return
        days = (df.index[-1] - df.index[0]).days
        annual_return = ((1 + df['cumulative_returns'].iloc[-1]) ** (365/days) - 1) * 100
        metrics['annual_return'] = add_arrow(annual_return)
        
        # Volatility
        metrics['volatility'] = add_arrow(df['returns'].std() * np.sqrt(252) * 100)
        
        # Sharpe ratio
        risk_free_rate = 0.02
        sharpe = (annual_return/100 - risk_free_rate) / (df['returns'].std() * np.sqrt(252))
        metrics['sharpe_ratio'] = add_arrow(sharpe)
        
        # Maximum drawdown
        df['previous_peak'] = df['total_value'].cummax()
        df['drawdown'] = (df['total_value'] - df['previous_peak']) / df['previous_peak']
        metrics['max_drawdown'] = add_arrow(df['drawdown'].min() * 100)
        
        # Trade metrics
        if len(trades_df) > 0:
            # Pre-calculate profit flags once
            profitable_trades = trades_df['Kar/Zarar'] > 0
            
            metrics['total_trades'] = len(trades_df)
            metrics['winning_trades'] = profitable_trades.sum()
            metrics['losing_trades'] = metrics['total_trades'] - metrics['winning_trades']
            metrics['win_rate'] = add_arrow(metrics['winning_trades'] / metrics['total_trades'] * 100)
            
            # Average profit and loss
            if metrics['winning_trades'] > 0:
                metrics['avg_profit'] = add_arrow(trades_df.loc[profitable_trades, 'Kar/Zarar'].mean())
                metrics['avg_profit_pct'] = add_arrow(trades_df.loc[profitable_trades, 'Kar/Zarar %'].mean())
            else:
                metrics['avg_profit'] = metrics['avg_profit_pct'] = 0
                
            if metrics['losing_trades'] > 0:
                metrics['avg_loss'] = add_arrow(trades_df.loc[~profitable_trades, 'Kar/Zarar'].mean())
                metrics['avg_loss_pct'] = add_arrow(trades_df.loc[~profitable_trades, 'Kar/Zarar %'].mean())
            else:
                metrics['avg_loss'] = metrics['avg_loss_pct'] = 0
            
            # Profit factor
            if metrics['avg_loss'] != 0 and metrics['losing_trades'] > 0:
                profit_factor = abs(float(str(metrics['avg_profit']).split()[0]) * metrics['winning_trades'] / 
                              (float(str(metrics['avg_loss']).split()[0]) * metrics['losing_trades']))
                metrics['profit_factor'] = add_arrow(profit_factor)
            else:
                metrics['profit_factor'] = float('inf')
            
            metrics['avg_trade_duration'] = trades_df['İşlem Süresi (Gün)'].mean()
        else:
            # Default metrics for no trades
            metrics.update({
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'avg_profit': 0,
                'avg_profit_pct': 0,
                'avg_loss': 0,
                'avg_loss_pct': 0,
                'profit_factor': 0,
                'avg_trade_duration': 0
            })
        
        return metrics 