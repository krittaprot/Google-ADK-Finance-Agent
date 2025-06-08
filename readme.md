# ADK Finance Agent - Full Stack Application

A complete financial analysis application built with Google Agent Development Kit (ADK), featuring a modern Streamlit web interface and a powerful finance agent backend with real-time market data integration.

## 🏗️ Architecture Overview

This project consists of two main components:

### 🎨 **Frontend** (`app.py`)
- **Streamlit Web Interface**: Modern, interactive chat UI
- **Real-time Streaming**: Live streaming of agent responses with visual indicators
- **Tool Execution Visualization**: Chronological display of tool calls with expandable results
- **Session Management**: Create and manage ADK agent sessions
- **Error Handling**: Robust error handling and user feedback

### 🤖 **Backend** (`finance_agent/`)
- **ADK Agent**: Powered by Google Agent Development Kit
- **YFinance Integration**: Real-time market data and financial analysis
- **Comprehensive Tools**: Stock prices, company info, historical data, fundamentals, news
- **OpenRouter LLM**: Advanced language model integration for financial analysis

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** with pip
2. **OpenRouter API Key** (for LLM access)
3. **Internet connection** (for real-time market data)

### Installation

1. **Clone and setup the project**:
   ```bash
   git clone <repository-url>
   cd Google-ADK-Agents
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   Create a `.env` file in the `finance_agent/` directory:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   ```

3. **Verify YFinance installation**:
   ```python
   import yfinance as yf
   stock = yf.Ticker("AAPL")
   print(stock.info.get("regularMarketPrice"))
   ```

### Running the Application

#### Option 1: Full Stack (Recommended)

1. **Start the ADK agent backend**:
   ```bash
   #parent directory
   adk api_server --host 0.0.0.0 --port 8000
   ```

2. **In a new terminal, start the Streamlit frontend**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** to `http://localhost:8501` and start chatting!

#### Option 2: Backend Only (Terminal)

```bash
#parent directory
adk run finance_agent
```

#### Option 3: Backend Only (Web UI)

```bash
#parent directory
adk web
```

## 🎯 Features

### Frontend Features (Streamlit UI)
- 🔄 **Real-time Streaming**: Live streaming of agent responses
- 🛠️ **Tool Execution Visualization**: See tools execute in real-time
- 💬 **Modern Chat Interface**: Clean, responsive chat UI
- 📋 **Copy to Clipboard**: Easily copy agent responses
- 🔧 **Session Management**: Easy session creation and management
- 💰 **Finance-Optimized**: Proper handling of financial symbols and data
- 🎯 **Error Handling**: Comprehensive error handling and user feedback
- 📱 **Responsive Design**: Works on desktop and mobile devices

### Backend Features (Finance Agent)
- 🔍 **Real-time Stock Data**: Current prices with currency information
- 📊 **Company Analysis**: Comprehensive profiles and business information
- 📈 **Historical Data**: Historical prices with customizable time periods
- 💰 **Financial Fundamentals**: P/E ratios, EPS, debt-to-equity, ROE/ROA
- 📰 **Market News**: Latest company news and press releases
- 🔢 **Technical Indicators**: Advanced technical analysis
- 📋 **Income Statements**: Detailed financial statements
- 🎯 **Analyst Recommendations**: Professional analyst insights

## 🛠️ Available Tools

The finance agent provides these powerful tools accessible through the Streamlit interface:

| Tool | Description | Example Query |
|------|-------------|---------------|
| `get_current_stock_price` | Real-time stock prices | "What's Tesla's current price?" |
| `get_company_info` | Company profiles and metrics | "Tell me about Microsoft" |
| `get_historical_stock_prices` | Historical price data | "Apple's performance last year" |
| `get_stock_fundamentals` | Financial ratios and analysis | "Google's financial fundamentals" |
| `get_company_news` | Recent news and developments | "Latest Amazon news" |
| `get_income_statements` | Financial statements | "Netflix income statement" |
| `get_key_financial_ratios` | Key financial metrics | "Microsoft's financial ratios" |
| `get_analyst_recommendations` | Professional recommendations | "Apple analyst recommendations" |
| `get_technical_indicators` | Technical analysis data | "Tesla technical indicators" |

## 💡 Example Queries

Try these queries in the Streamlit interface:

### 📈 **Basic Analysis Prompts**
- "What is Apple's current stock price and recent performance?"
- "Compare the financial performance of Tesla vs Ford over the last year"
- "Analyze Microsoft's quarterly earnings and provide key insights"
- "What are the top 5 performing tech stocks this month?"
- "Explain the recent market trends in the renewable energy sector"
- "What is Amazon's P/E ratio and how does it compare to industry average?"

### 📊 Advanced Analysis Prompts:
- "Create a detailed SWOT analysis for Netflix in the current streaming market"
- "What are the key financial ratios I should look at when evaluating Nvidia's stock?"
- "Analyze the impact of recent Fed interest rate changes on bank stocks"
- "Compare the debt-to-equity ratios of major airlines: Delta, United, and Southwest"

### 🎯 Tips for Better Results:
- **Be specific**: Instead of "How is Apple doing?", try "What was Apple's revenue growth in Q3 2024?"
- **Ask for comparisons**: "Compare X vs Y" often provides valuable insights
- **Request explanations**: Add "explain why" to understand the reasoning behind trends
- **Use timeframes**: Specify periods like "last quarter", "past year", or "since 2020"

## 🔧 Technical Architecture

### Frontend Architecture (Streamlit)
```
Streamlit App (app.py)
├── Session Management
├── ADK API Integration (/run_sse endpoint)
├── Real-time Event Processing
│   ├── Function Calls (Tool Execution)
│   ├── Function Responses (Tool Results)
│   └── Text Streaming (LLM Response)
└── UI Components
    ├── Chat Interface
    ├── Tool Status Displays
    └── Error Handling
```

### Backend Architecture (Finance Agent)
```
Finance Agent (finance_agent/)
├── agent.py (Main agent logic)
├── tools.py (YFinance tool implementations)
├── prompts.py (System prompts and instructions)
└── ADK Integration
    ├── OpenRouter LLM
    ├── Tool Execution Engine
    └── Session Management
```

### Data Flow
1. **User Input** → Streamlit UI
2. **HTTP Request** → ADK Agent API (`/run_sse`)
3. **Tool Execution** → YFinance APIs
4. **LLM Processing** → OpenRouter
5. **Streaming Response** → Server-Sent Events
6. **Real-time Display** → Streamlit UI

## 🎨 Development Learnings

### ✅ What Works Well

#### **Proper SSE Event Handling**
```python
# Process all parts within a single event
if "content" in event and event["content"].get("parts"):
    for part in event["content"]["parts"]:
        if "functionCall" in part:
            # Handle tool start
        elif "functionResponse" in part:
            # Handle tool result  
        elif "text" in part:
            # Handle streaming text
```

#### **Chronological Tool Display**
```python
# Create assistant container FIRST
with st.chat_message("assistant"):
    assistant_container = st.container()
    # All tools created within this container
```

#### **Financial Data Handling**
```python
# Escape dollar signs for Streamlit
def escape_markdown_dollars(text: str) -> str:
    return text.replace('$', '\\$')
```

### ❌ Common Pitfalls

- **Layout Shifts**: Creating tool calls outside assistant container
- **Event Skipping**: Using `elif` instead of processing all parts
- **Text Duplication**: Ignoring `partial` flags in streaming
- **Tool Mismatching**: Not tracking tool IDs properly

## 📁 Project Structure

```
Google-ADK-Agents/
├── app.py                 # Streamlit frontend application
├── readme.md             # This comprehensive guide
├── requirements.txt      # Python dependencies
└── finance_agent/        # ADK agent backend
    ├── agent.py          # Main agent configuration
    ├── tools.py          # YFinance tool implementations
    ├── prompts.py        # System prompts
    ├── README.md         # Backend-specific documentation
    └── __init__.py       # Python package initialization
```

## 🔒 Security & Limitations

### Security Considerations
- **API Keys**: Store OpenRouter API key securely in `.env`
- **Local Only**: Default configuration runs locally only
- **No Authentication**: Current setup has no user authentication

### Data Limitations
- **Yahoo Finance TOS**: Subject to Yahoo Finance terms of service
- **Real-time Delays**: Market data may have slight delays
- **Educational Use**: For educational and research purposes only
- **Not Financial Advice**: This tool does not provide investment advice

## 🚀 Deployment Options

### Local Development
- **Frontend**: `streamlit run app.py`
- **Backend**: `adk api_server`

### Production Deployment
- **Streamlit Cloud**: Deploy frontend to Streamlit Cloud
- **Google Cloud Run**: Deploy ADK agent to Cloud Run
- **Docker**: Containerize both components

## 🤝 Contributing

### Frontend Development
1. Test SSE event handling with real ADK agents
2. Verify chronological order of tool calls
3. Test error scenarios and edge cases
4. Ensure financial data displays correctly

### Backend Development
1. Add new YFinance tools in `tools.py`
2. Update prompts in `prompts.py` for new capabilities
3. Test tool integration with ADK framework
4. Validate financial data accuracy

### Development Guidelines
- Follow ADK best practices for agent development
- Use proper error handling for both frontend and backend
- Test with real market data and various stock symbols
- Maintain backward compatibility with existing tools

## 📚 Documentation References

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Testing Guide](https://google.github.io/adk-docs/get-started/testing/#local-testing)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [YFinance Documentation](https://pypi.org/project/yfinance/)

## 📄 License

This project is for educational purposes. Please respect:
- Yahoo Finance's terms of service
- OpenRouter's usage policies
- Google ADK licensing terms

---

**⚠️ Disclaimer**: This application is for educational and informational purposes only. It does not constitute financial advice. Always consult with qualified financial professionals before making investment decisions.
