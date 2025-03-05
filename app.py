import streamlit as st
from datetime import datetime, timedelta
from data_handler import fetch_stock_data
from strategy.macd_strategy import MACDStrategy
from strategy.rsi_strategy import RSIStrategy
from strategy.bbands_strategy import BBandsStrategy
from strategy.buyhold_strategy import BuyHoldStrategy
from strategy.base_strategy import BaseStrategy
from visualizations import (
    create_stock_price_plot,
    create_macd_plot,
    create_rsi_plot,
    create_bbands_plot,
    create_portfolio_plot,
    format_metrics_for_display
)
from education_mode import (
    show_basic_concepts,
    show_technical_analysis_basics
)

@st.cache_data(ttl=3600) 
def cached_fetch_stock_data(symbol, start_date, end_date, interval):
    """
    Streamlit önbellekleme ile veri çekme
    Bu fonksiyon, aynı parametrelerle yapılan istekleri önbellekler
    ve deploy edilen uygulamada performansı artırır
    """
    df = fetch_stock_data(symbol, start_date, end_date, interval)
    if df.empty:
        st.error(f"No data available for {symbol}. Please check the symbol and try again.")
        return df
    return df

# Page config
st.set_page_config(
    page_title="Trading Strategy Backtester",
    page_icon="📈",
    layout="wide"
)

# Education Mode Toggle
education_mode = st.sidebar.toggle("Enable Education Mode", value=False)

# Title and description
if education_mode:
    st.title("📚 Borsa Stratejileri")
else:
    st.title("Trading Strategy Backtester")
    st.markdown("""
    This application allows you to backtest various trading strategies on any stock.
    Choose a strategy, enter a stock symbol and date range to analyze the performance.
    """)

# Sidebar inputs
with st.sidebar:
    st.header("Strategy Parameters")
    
    # Strategy selection
    strategy_type = st.selectbox(
        "Select Strategy",
        options=['MACD', 'RSI', 'Bollinger Bands', 'Buy & Hold'],
        index=0
    )
    
    # Stock selection
    symbol = st.text_input(
        "Stock Symbol",
        value="THYAO.IS",
        help="Enter the stock symbol (add .IS for Borsa Istanbul stocks)"
    )
    
    # Interval selection
    interval = st.selectbox(
        "Time Interval",
        options=['4h', '1h', '1d'],
        index=0,
        help="Select the time interval for the analysis"
    )
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=360),
            max_value=datetime.now()
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    # Strategy-specific parameters
    st.subheader("Strategy Parameters")
    
    if strategy_type == 'MACD':
        if interval == '4h':
            fast_default, slow_default, signal_default = 6, 13, 4
        else:
            fast_default, slow_default, signal_default = 12, 26, 9
        
        fast_period = st.slider("Fast Period", min_value=3, max_value=30, value=fast_default)
        slow_period = st.slider("Slow Period", min_value=5, max_value=50, value=slow_default)
        signal_period = st.slider("Signal Period", min_value=2, max_value=20, value=signal_default)
        
        strategy = MACDStrategy(fast_period, slow_period, signal_period)
    
    elif strategy_type == 'RSI':
        period = st.slider("RSI Period", min_value=5, max_value=30, value=14)
        overbought = st.slider("Overbought Level", min_value=50, max_value=90, value=70)
        oversold = st.slider("Oversold Level", min_value=10, max_value=50, value=30)
        
        strategy = RSIStrategy(period, overbought, oversold)
    
    elif strategy_type == 'Bollinger Bands':
        period = st.slider("Period", min_value=5, max_value=50, value=20)
        std_dev = st.slider("Standard Deviation", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
        
        strategy = BBandsStrategy(period, std_dev)
    
    else:  # Buy & Hold
        strategy = BuyHoldStrategy()
    
    # Initial capital
    initial_capital = st.number_input(
        "Initial Capital (TL)",
        min_value=1000,
        value=100000,
        step=1000
    )
    strategy.initial_capital = initial_capital

# Main content
if education_mode:    
    # Create tabs for different education sections
    tab_basic, tab_technical = st.tabs([
        "🎯 Temel Kavramlar",
        "📊 Teknik Analiz"
    ])
    
    with tab_basic:
        show_basic_concepts()
    
    with tab_technical:
        show_technical_analysis_basics()

else:
    try:
            df = cached_fetch_stock_data(symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), interval)
            
            if df.empty:
                st.error(f"No data found for {symbol} with {interval} interval in the specified date range.")
            else:
                # Run backtest
                backtest_results, trades = strategy.backtest(df)
                metrics = BaseStrategy.calculate_performance_metrics(backtest_results, trades)
                formatted_metrics = format_metrics_for_display(metrics)
                
                # Display metrics
                st.header("Performance Metrics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Return", formatted_metrics['total_return'])
                    st.metric("Annual Return", formatted_metrics['annual_return'])
                    st.metric("Sharpe Ratio", formatted_metrics['sharpe_ratio'])
                
                with col2:
                    st.metric("Total Trades", formatted_metrics['total_trades'])
                    st.metric("Win Rate", formatted_metrics['win_rate'])
                    st.metric("Profit Factor", formatted_metrics['profit_factor'])
                
                with col3:
                    st.metric("Average Profit", formatted_metrics['avg_profit'])
                    st.metric("Average Loss", formatted_metrics['avg_loss'])
                    st.metric("Max Drawdown", formatted_metrics['max_drawdown'])
                
                with col4:
                    st.metric("Winning Trades", formatted_metrics['winning_trades'])
                    st.metric("Losing Trades", formatted_metrics['losing_trades'])
                    st.metric("Avg Trade Duration", formatted_metrics['avg_trade_duration'])
                
                # Display charts
                st.header("Charts")
                
                # Price chart with signals
                st.subheader(f"Stock Price and Trading Signals ({interval} Interval)")
                st.plotly_chart(create_stock_price_plot(backtest_results), use_container_width=True)
                
                # Strategy-specific indicator charts
                if strategy_type == 'MACD':
                    st.subheader("MACD Indicator")
                    st.plotly_chart(create_macd_plot(backtest_results), use_container_width=True)
                elif strategy_type == 'RSI':
                    st.subheader("RSI Indicator")
                    st.plotly_chart(create_rsi_plot(backtest_results), use_container_width=True)
                elif strategy_type == 'Bollinger Bands':
                    st.subheader("Bollinger Bands")
                    st.plotly_chart(create_bbands_plot(backtest_results), use_container_width=True)
                
                # Portfolio value chart
                st.subheader("Portfolio Value and Drawdown")
                st.plotly_chart(create_portfolio_plot(backtest_results), use_container_width=True)
                
                # Trade list
                if not trades.empty:
                    st.header("Trade History")
                    st.dataframe(
                        trades.style.format({
                            'entry_price': '₺{:.2f}',
                            'exit_price': '₺{:.2f}',
                            'profit_loss': '₺{:.2f}',
                            'profit_loss_pct': '{:.2f}%'
                        })
                    )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}") 