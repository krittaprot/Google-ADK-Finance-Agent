#adapted from agno finance agent (https://docs.agno.com/examples/agents/finance-agent)

"""Finance agent for financial market analysis and stock data retrieval.

This module defines the main finance agent that combines prompts and tools
to provide comprehensive financial analysis capabilities using YFinance data.
"""

import os
import litellm
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from .prompts import return_instructions_finance
from .tools import YFinanceTools

# Enable LiteLLM debugging (optional)
litellm._turn_on_debug()

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")

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

# Create the finance agent
root_agent = LlmAgent(
    name="finance_agent",
    model=model,
    instruction=return_instructions_finance(),
    tools=yfinance_tools
)