import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict

def create_stock_price_plot(df: pd.DataFrame) -> go.Figure:
    """
    Create an advanced interactive stock price plot with multiple indicators
    """
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, 
                       shared_xaxes=True,
                       vertical_spacing=0.03,
                       subplot_titles=('Price Action', 'Volume'),
                       row_heights=[0.7, 0.3])

    # Add candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ),
        row=1, col=1
    )

    # Add 20-day moving average
    ma20 = df['Close'].rolling(window=20).mean()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=ma20,
            name='20-day MA',
            line=dict(color='rgba(255, 255, 255, 0.5)', width=1)
        ),
        row=1, col=1
    )

    # Add volume bars
    colors = ['red' if row['Open'] > row['Close'] else 'green' for index, row in df.iterrows()]
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.5
        ),
        row=2, col=1
    )

    # Add buy signals
    buy_signals = df[df['signal_line'] == 1]
    if not buy_signals.empty:
        fig.add_trace(
            go.Scatter(
                x=buy_signals.index,
                y=buy_signals['Close'],
                mode='markers',
                marker=dict(
                    symbol='triangle-up',
                    size=12,
                    color='#26a69a',
                    line=dict(color='#000000', width=1)
                ),
                name='Buy Signal'
            ),
            row=1, col=1
        )

    # Add sell signals
    sell_signals = df[df['signal_line'] == -1]
    if not sell_signals.empty:
        fig.add_trace(
            go.Scatter(
                x=sell_signals.index,
                y=sell_signals['Close'],
                mode='markers',
                marker=dict(
                    symbol='triangle-down',
                    size=12,
                    color='#ef5350',
                    line=dict(color='#000000', width=1)
                ),
                name='Sell Signal'
            ),
            row=1, col=1
        )

    # Update layout
    fig.update_layout(
        title='Advanced Price Analysis',
        yaxis_title='Price',
        xaxis_title='Date',
        template='plotly_dark',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        height=800
    )

    # Update y-axes labels
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    return fig

def create_macd_plot(df: pd.DataFrame) -> go.Figure:
    """
    Create an advanced MACD plot with price action
    """
    fig = make_subplots(rows=2, cols=1, 
                       shared_xaxes=True,
                       vertical_spacing=0.03,
                       subplot_titles=('Price with EMA', 'MACD'),
                       row_heights=[0.6, 0.4])

    # Add price line
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Close'],
            name='Close Price',
            line=dict(color='#B6B6B6', width=1)
        ),
        row=1, col=1
    )

    # Add EMAs used in MACD calculation
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=ema12,
            name='EMA 12',
            line=dict(color='#26a69a', width=1)
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=ema26,
            name='EMA 26',
            line=dict(color='#ef5350', width=1)
        ),
        row=1, col=1
    )

    # Add MACD
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['macd'],
            name='MACD',
            line=dict(color='#2962FF', width=1.5)
        ),
        row=2, col=1
    )

    # Add Signal line
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['signal'],
            name='Signal',
            line=dict(color='#FF6D00', width=1.5)
        ),
        row=2, col=1
    )


    # Update layout
    fig.update_layout(
        title='MACD Analysis',
        template='plotly_dark',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        height=800
    )

    # Update y-axes labels
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="MACD", row=2, col=1)

    return fig

def create_rsi_plot(df: pd.DataFrame) -> go.Figure:
    """
    Create an advanced RSI plot with price action and momentum
    """
    fig = make_subplots(rows=3, cols=1,
                       shared_xaxes=True,
                       vertical_spacing=0.03,
                       subplot_titles=('Price Action', 'RSI', 'RSI Momentum'),
                       row_heights=[0.5, 0.25, 0.25])

    # Add price action
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Close'],
            name='Close Price',
            line=dict(color='#B6B6B6', width=1)
        ),
        row=1, col=1
    )

    # Add RSI
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['rsi'],
            name='RSI',
            line=dict(color='#2962FF', width=1.5)
        ),
        row=2, col=1
    )

    # Add RSI moving average if available
    if 'rsi_ma' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['rsi_ma'],
                name='RSI MA',
                line=dict(color='#FF6D00', width=1, dash='dash')
            ),
            row=2, col=1
        )

    # Add RSI momentum if available
    if 'rsi_mom' in df.columns:
        colors = ['#26a69a' if val >= 0 else '#ef5350' for val in df['rsi_mom']]
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['rsi_mom'],
                name='RSI Momentum',
                marker_color=colors,
                opacity=0.5
            ),
            row=3, col=1
        )

    # Add overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    fig.add_hline(y=50, line_dash="dash", line_color="white", 
                 line_width=0.5, opacity=0.5, row=2, col=1)

    # Update layout
    fig.update_layout(
        title='RSI Analysis',
        template='plotly_dark',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        height=900
    )

    # Update y-axes labels and ranges
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)
    fig.update_yaxes(title_text="Momentum", row=3, col=1)

    return fig

def create_bbands_plot(df: pd.DataFrame) -> go.Figure:
    """
    Create an advanced Bollinger Bands plot with additional indicators
    """
    fig = make_subplots(rows=3, cols=1,
                       shared_xaxes=True,
                       vertical_spacing=0.03,
                       subplot_titles=('Price and Bollinger Bands', 'Bandwidth', '%B Indicator'),
                       row_heights=[0.6, 0.2, 0.2])

    # Add price and bands
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ),
        row=1, col=1
    )

    # Add Bollinger Bands
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['bb_upper'],
            name='Upper Band',
            line=dict(color='rgba(255, 255, 255, 0.5)', width=1, dash='dash')
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['bb_middle'],
            name='Middle Band',
            line=dict(color='#FF6D00', width=1, dash='dash')
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['bb_lower'],
            name='Lower Band',
            line=dict(color='rgba(255, 255, 255, 0.5)', width=1, dash='dash'),
            fill='tonexty'
        ),
        row=1, col=1
    )

    # Add Bandwidth
    colors = ['#26a69a' if val else '#ef5350' for val in df['bands_expanding']]
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['bb_bandwidth'],
            name='Bandwidth',
            marker_color=colors,
            opacity=0.5
        ),
        row=2, col=1
    )

    # Add %B indicator
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['bb_b'],
            name='%B',
            line=dict(color='#2962FF', width=1.5)
        ),
        row=3, col=1
    )

    # Add reference lines for %B
    fig.add_hline(y=1, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=0.5, line_dash="dash", line_color="white", 
                 line_width=0.5, opacity=0.5, row=3, col=1)
    fig.add_hline(y=0, line_dash="dash", line_color="green", row=3, col=1)

    # Update layout
    fig.update_layout(
        title='Bollinger Bands Analysis',
        template='plotly_dark',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        height=900
    )

    # Update y-axes labels
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Bandwidth", row=2, col=1)
    fig.update_yaxes(title_text="%B", row=3, col=1)

    return fig

def create_portfolio_plot(df: pd.DataFrame) -> go.Figure:
    """
    Create an advanced portfolio performance plot
    """
    fig = make_subplots(rows=2, cols=1,
                       shared_xaxes=True,
                       vertical_spacing=0.03,
                       subplot_titles=('Portfolio Value', 'Drawdown Analysis'),
                       row_heights=[0.7, 0.3])

    # Calculate additional metrics
    df['daily_returns'] = df['total_value'].pct_change()
    df['cumulative_returns'] = (1 + df['daily_returns']).cumprod()
    drawdown = (df['total_value'] - df['total_value'].cummax()) / df['total_value'].cummax() * 100

    # Add portfolio value line
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['total_value'],
            name='Portfolio Value',
            line=dict(color='#2962FF', width=2)
        ),
        row=1, col=1
    )

    # Add moving average of portfolio value
    ma20 = df['total_value'].rolling(window=20).mean()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=ma20,
            name='20-day MA',
            line=dict(color='#FF6D00', width=1, dash='dash')
        ),
        row=1, col=1
    )

    # Add drawdown
    colors = ['#ef5350' if val < 0 else '#26a69a' for val in drawdown]
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=drawdown,
            name='Drawdown %',
            marker_color=colors,
            opacity=0.5
        ),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        title='Portfolio Performance Analysis',
        template='plotly_dark',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        height=800
    )

    # Update y-axes labels
    fig.update_yaxes(title_text="Portfolio Value (₺)", row=1, col=1)
    fig.update_yaxes(title_text="Drawdown %", row=2, col=1)

    return fig

def format_metrics_for_display(metrics: Dict) -> Dict[str, str]:
    """
    Format metrics for display with enhanced styling
    """
    formatted_metrics = {}
    
    # Helper function to add arrow
    def add_arrow(value):
        if isinstance(value, (int, float)):
            arrow = "↑" if value > 0 else "↓"
            return f"{value:.2f} {arrow}"
        elif isinstance(value, str) and ' ' in value:
            try:
                val = float(value.split()[0])
                arrow = "↑" if val > 0 else "↓"
                return f"{val:.2f} {arrow}"
            except:
                return value
        return value
    
    # Format all numeric metrics with arrows
    numeric_metrics = [
        'total_return', 'annual_return', 'volatility', 'win_rate',
        'max_drawdown', 'avg_profit', 'avg_loss', 'avg_profit_pct',
        'avg_loss_pct', 'sharpe_ratio', 'profit_factor'
    ]
    
    for key in numeric_metrics:
        if key in metrics and metrics[key] != 0:
            formatted_metrics[key] = add_arrow(metrics[key])
        else:
            formatted_metrics[key] = metrics.get(key, 0)
    
    # Format count metrics
    count_metrics = ['total_trades', 'winning_trades', 'losing_trades']
    for key in count_metrics:
        if key in metrics:
            formatted_metrics[key] = metrics[key]
    
    # Format duration metric
    if 'avg_trade_duration' in metrics:
        formatted_metrics['avg_trade_duration'] = f"{metrics['avg_trade_duration']:.1f} gün"
    
    return formatted_metrics 