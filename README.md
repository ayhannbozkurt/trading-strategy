# Trading Strategy Backtester 📈

A backtesting application developed for testing various technical analysis strategies on Borsa Istanbul stocks. The application also helps you learn basic stock market concepts and technical analysis methods with its education mode.

## 🚀 Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ayhannbozkurt/trading-strategy.git
cd trading-strategy
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Start the application:
```bash
streamlit run app.py
```

## 💻 Usage

1. **Strategy Selection**
   - Select your strategy from the sidebar
   - Customize strategy parameters

2. **Stock Selection**
   - Add .IS suffix for Borsa Istanbul stocks (e.g., THYAO.IS)
   - Set time range and period

3. **Results Analysis**
   - View performance metrics
   - Analyze buy/sell signals on charts
   - Review detailed trade history

4. **Education Mode**
   - Enable education mode to learn basic concepts
   - Reinforce concepts with interactive charts

## 📊 Charts and Indicators

### Price Charts
- Candlestick charts (OHLC)
- Moving averages
- Buy/Sell signals
- Volume analysis

### Strategy Indicators
- MACD histogram and signal lines
- RSI and momentum indicators
- Bollinger Bands and bandwidth

### Portfolio Performance
- Portfolio value chart
- Drawdown analysis
- Cumulative returns

## 🛠️ Technical Details

### Project Structure
```
trading-strategy/
├── app.py                 # Main application
├── data_handler.py        # Data processing
├── education_mode.py      # Education mode
├── visualizations.py      # Chart creation
├── requirements.txt       # Dependencies
└── strategy/             # Strategy modules
    ├── base_strategy.py
    ├── macd_strategy.py
    ├── rsi_strategy.py
    ├── bbands_strategy.py
    └── buyhold_strategy.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

