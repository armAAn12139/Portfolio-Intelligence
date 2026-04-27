# FinPlot - Portfolio Intelligence
"""THIS IS AN UNDERGOING PROJECT"""
*Your Smart Portfolio Companion* 

A comprehensive portfolio analysis tool that provides intelligent insights, risk assessment, and optimization recommendations for investors. Built with Python and featuring an interactive Streamlit web interface.

##  Features

### Core Analytics
- **Portfolio Volatility** - Measure market risk using historical data
- **Risk Scoring** - Intelligent risk assessment (0-100 scale)
- **Diversification Analysis** - Evaluate asset allocation balance
- **Performance Tracking** - Monitor returns vs. investments
- **Sector Exposure** - Understand market concentration

### 🤖 AI Insights
- **Market Regime Detection** - Bull/Bear market identification
- **Smart Recommendations** - Personalized investment advice
- **Risk Warnings** - Alerts for high-risk positions
- **Optimization Suggestions** - Optimal portfolio rebalancing

###  Interactive Interface
- **Tabbed Dashboard** - Organized analysis sections
- **Interactive Charts** - Plotly-powered visualizations
- **What-If Scenarios** - Test allocation changes
- **Risk Gauge** - Visual risk meter
- **Real-time Updates** - Live market data integration

##  Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/armAAn12139/Portfolio-Intelligence.git
   cd Portfolio-Intelligence
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

##  Usage

### Web Interface (Recommended)
1. Launch the Streamlit app
2. Enter your portfolio assets in the sidebar
3. Click " Analyze Portfolio"
4. Explore the interactive dashboard:
   - **Overview**: Key metrics and risk gauge
   - **Analysis**: Detailed charts and allocations
   - **What-If**: Test portfolio adjustments
   - **Insights**: AI recommendations

### Command Line
```bash
python main.py
```

### Adding Assets
- **Stocks**: Use symbols like `AAPL`, `GOOGL`, `TSLA`
- **Crypto**: Use pairs like `BTC-USD`, `ETH-USD`
- **Cash**: Use symbol `CASH` with any asset type
- **Current Value**: Your current holding value
- **Purchase Price**: Original investment amount

##  Architecture

```
finplot/
├── app.py                 # Streamlit web interface
├── main.py               # CLI entry point
├── models/               # Data models
│   ├── assets.py        # Asset class
│   └── portfolio.py     # Portfolio class
├── portfolio/           # Core analysis modules
│   ├── metrics.py       # Calculation functions
│   ├── optimizer.py     # Portfolio optimization
│   ├── risk.py          # Risk assessment
│   └── portfolio_analyzer.py  # Main analyzer
├── data/                # Data fetching
│   └── market_data.py   # Yahoo Finance integration
├── market/              # Market analysis
│   └── market_context.py # Regime detection
├── recommendation/      # AI recommendations
│   └── recommendation_engine.py
├── risk/                # Advanced risk modeling
│   └── risk_scoring.py
└── utils/               # Utilities
    └── helpers.py       # Output formatting
```

##  Sample Output

```
------ Portfolio Intelligence Report ------

Total Portfolio Value: ₹425,000
Portfolio Volatility: 2.47%
Portfolio Return: -43.53%
Risk Score: 85 / 100
Risk Level: Very High
Diversification Score: 70/100

AI Insights:
- Portfolio is currently down 43.53% - review underperforming positions
- Well-diversified portfolio across multiple asset classes
- High crypto exposure - monitor closely for volatility
```

##  Configuration

### Environment Variables
- No environment variables required for basic usage

### Data Sources
- **Yahoo Finance** (via yfinance library)
- **Historical data**: 1 year by default
- **Real-time updates**: Available during market hours

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .

##  Acknowledgments

- **yfinance** - Yahoo Finance data API
- **Streamlit** - Web app framework
- **Plotly** - Interactive visualizations
- **NumPy/Pandas** - Data processing
- **SciPy** - Optimization algorithms


**Made with  by the FinPlot Team that includes just me😎**

*Invest smart, analyze better!*
