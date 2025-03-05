import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(symbol: str, start_date: str, end_date: str, interval: str = '4h') -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance
    Args:
        symbol: Stock symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        interval: Data interval ('1h', '4h', '1d', etc.)
    """
    # Convert dates to datetime
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    # If end date is future or today, set to yesterday
    if end >= datetime.now():
        end = datetime.now() - timedelta(days=1)
    
    
    # Update date strings
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')
    
    # For 4h interval
    if interval == '4h':
        # Get 1h data and resample to 4h
        data = yf.download(
            symbol,
            start=start_str,
            end=end_str,
            interval='1h',
            progress=False,
            threads=False
        )
        
        # Handle MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        # Ensure index is datetime
        data.index = pd.to_datetime(data.index)
        
        # Resample to 4h
        if not data.empty:
            data = data.resample('4H').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()
        
    else:
        # For other intervals, download directly
        data = yf.download(
            symbol,
            start=start_str,
            end=end_str,
            interval=interval,
            progress=False,
            threads=False
        )
        
        # Handle MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        # Ensure index is datetime
        data.index = pd.to_datetime(data.index)
    
    # Basic cleaning
    data = data.dropna(subset=['Close'])
    
    return data