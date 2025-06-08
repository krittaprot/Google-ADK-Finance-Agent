#adapted from agno finance agent (https://docs.agno.com/examples/agents/finance-agent)

"""Finance agent for financial market analysis and stock data retrieval.

This module defines the main finance agent that combines prompts and tools
to provide comprehensive financial analysis capabilities using YFinance data.
"""

import os
import litellm
from dotenv import load_dotenv
from datetime import datetime

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool

from .prompts import return_instructions_finance
from .tools import YFinanceTools

#import langchain tools
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import TavilySearchResults

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize the model
model = LiteLlm(
    model="openrouter/openai/gpt-4.1-nano",
    api_key=OPENROUTER_API_KEY,
    api_base=OPENROUTER_BASE_URL
)

# Configure and initialize YFinanceTools with desired functionalities
yfinance_tools = YFinanceTools(
    stock_price=True,
    company_info=True,
    historical_prices=True,
    stock_fundamentals=True,
    company_news=True,
    income_statements=True,
    key_financial_ratios=True,
    analyst_recommendations=True,
    technical_indicators=True,
)

# Instantiate the LangChain tool
tavily_tool_instance = TavilySearchResults(
    max_results=10,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=False,
    include_images=False,
    time_range="day",
    topic="news",
)

# Wrap it with LangchainTool for ADK
adk_tavily_tool = LangchainTool(tool=tavily_tool_instance)

# Create the finance agent
root_agent = LlmAgent(
    name="root_agent",
    model=model,
    instruction=return_instructions_finance(),
    tools=[*yfinance_tools, adk_tavily_tool]
)

