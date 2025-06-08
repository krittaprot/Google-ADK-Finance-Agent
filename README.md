# Financial Agent with YFinance Tools

Adapted from: https://docs.agno.com/examples/agents/finance-agent

A powerful financial analysis assistant built with Google ADK (Agent Development Kit) and integrated with YFinance for real-time market data.

## Features

🔍 **Real-time Stock Data**
- Current stock prices with currency information
- Live market data during trading hours

📊 **Company Analysis**
- Comprehensive company profiles and business information
- Key financial metrics and ratios
- Market capitalization and trading statistics

📈 **Historical Data**
- Historical stock prices with customizable time periods
- Support for different data intervals (daily, weekly, monthly)
- Trend analysis capabilities

💰 **Financial Fundamentals**
- P/E ratios, EPS, and other key metrics
- Debt-to-equity ratios and profitability margins
- Return on equity and assets analysis
- Income statement analysis
- Key financial ratios
- Analyst recommendations
- Technical indicator analysis

📰 **Market News**
- Latest company news and press releases
- Market developments and announcements
- Configurable number of news stories

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root with your OpenRouter API credentials:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

### 3. Verify Installation

Test that yfinance is working:

```python
import yfinance as yf
stock = yf.Ticker("AAPL")
print(stock.info.get("regularMarketPrice"))
```

## Usage

### Basic Usage

You can interact with the financial agent using the ADK CLI for terminal-based conversations or the ADK web UI for a browser-based experience.

#### Run in Terminal

To run the agent in your terminal:

```bash
adk run finance_agent
```

You can then type your queries directly in the terminal. To exit, use `Ctrl+C`.

#### Run in Web UI

To launch the interactive developer UI in your browser:

```bash
adk web
```

Open your browser to `http://localhost:8000` (or the URL provided). In the top-left corner, select your agent (`finance_agent` if you renamed the directory, or the default `agent` name if not explicitly changed) from the dropdown. You can then chat with the agent through the web interface.

### Available Tools

The financial agent has access to these YFinance tools:

#### `get_current_stock_price(symbol: str)`
Get real-time stock price for any symbol.

**Example:** "What's the current price of Tesla stock?"

#### `get_company_info(symbol: str)`
Get comprehensive company information including business summary, financials, and key metrics.

**Example:** "Tell me about Microsoft as a company"

#### `get_historical_stock_prices(symbol: str, period: str, interval: str)`
Get historical price data with customizable periods and intervals.

**Example:** "Show me Apple's stock performance over the last year"

#### `get_stock_fundamentals(symbol: str)`
Get key financial ratios and fundamental analysis data.

**Example:** "What are Google's financial fundamentals?"

#### `get_company_news(symbol: str, num_stories: int)`
Get recent news and press releases for a company.

**Example:** "What's the latest news about Amazon?"

#### `get_income_statements(symbol: str)`
Get income statements for a given stock symbol.

**Example:** "Show me the income statement for Google (GOOGL)"

#### `get_key_financial_ratios(symbol: str)`
Get key financial ratios for a given stock symbol.

**Example:** "What are the key financial ratios for Microsoft (MSFT)?"

#### `get_analyst_recommendations(symbol: str)`
Get analyst recommendations for a given stock symbol.

**Example:** "What are the analyst recommendations for Apple (AAPL)?"

#### `get_technical_indicators(symbol: str, period: str)`
Get technical indicators for a given stock symbol with customizable periods.

**Example:** "Show me the technical indicators for Tesla (TSLA) over the last 3 months"

## Example Queries

Here are some example queries you can try:

1. **Stock Prices**
   - "What's the current stock price of Apple (AAPL)?"
   - "How is Tesla (TSLA) performing today?"

2. **Company Analysis**
   - "Give me detailed information about Microsoft (MSFT)"
   - "What sector is Amazon (AMZN) in and what do they do?"

3. **Historical Data**
   - "Show me Google's (GOOGL) stock performance over the last 6 months"
   - "What was the historical trend for Netflix (NFLX) in 2023?"

4. **Financial Fundamentals**
   - "What are the key financial ratios for Apple (AAPL)?"
   - "How profitable is Microsoft (MSFT) based on its fundamentals?"

5. **Income Statements**
   - "Get the income statement for Amazon (AMZN)."
   - "Can you provide the income statement for Netflix (NFLX)?"

6. **Key Financial Ratios**
   - "What are the key financial ratios for Google (GOOGL)?"
   - "Show me the key financial ratios for Tesla (TSLA)."

7. **Analyst Recommendations**
   - "What are the latest analyst recommendations for Microsoft (MSFT)?"
   - "Are there any analyst recommendations for Apple (AAPL)?"

8. **Technical Indicators**
   - "Show me the technical indicators for Nvidia (NVDA) for the last 6 months."
   - "What are the technical indicators for AMD (AMD)?"

9. **Market News**
   - "What's the latest news about Tesla (TSLA)?"
   - "Are there any recent developments with Amazon (AMZN)?"

## Supported Stock Symbols

The agent works with any valid stock symbol supported by Yahoo Finance, including:

- **US Stocks**: AAPL, GOOGL, MSFT, TSLA, AMZN, META, NVDA, etc.
- **International Stocks**: Use appropriate suffixes (e.g., ASML.AS for European stocks)
- **ETFs**: SPY, QQQ, VTI, etc.
- **Indices**: ^GSPC (S&P 500), ^IXIC (NASDAQ), etc.

## Limitations

- Data is sourced from Yahoo Finance and subject to their terms of service
- Real-time data may have slight delays
- Some international stocks may have limited data availability
- This tool is for educational and research purposes only - not investment advice

## Contributing

Feel free to extend the agent with additional financial tools or improve existing functionality. The modular design makes it easy to add new YFinance capabilities.

## License

This project is for educational purposes. Please respect Yahoo Finance's terms of service when using their data.

---

**Disclaimer**: This financial agent is for educational and informational purposes only. It does not constitute financial advice. Always consult with qualified financial professionals before making investment decisions. 
