#adapted from agno finance agent (https://docs.agno.com/examples/agents/finance-agent)

"""Finance agent YFinance tools.

This module contains all the tool functions that the finance agent can use
to fetch stock data, company information, and financial metrics using YFinance.
"""

import json
import yfinance as yf

class YFinanceTools:
    def __init__(
        self,
        stock_price: bool = False,
        company_info: bool = False,
        historical_prices: bool = False,
        stock_fundamentals: bool = False,
        company_news: bool = False,
        income_statements: bool = False,
        key_financial_ratios: bool = False,
        analyst_recommendations: bool = False,
        technical_indicators: bool = False,
    ):
        self._enabled_tools = []
        if stock_price:
            self._enabled_tools.append(self.get_current_stock_price)
        if company_info:
            self._enabled_tools.append(self.get_company_info)
        if historical_prices:
            self._enabled_tools.append(self.get_historical_stock_prices)
        if stock_fundamentals:
            self._enabled_tools.append(self.get_stock_fundamentals)
        if company_news:
            self._enabled_tools.append(self.get_company_news)
        if income_statements:
            self._enabled_tools.append(self.get_income_statements)
        if key_financial_ratios:
            self._enabled_tools.append(self.get_key_financial_ratios)
        if analyst_recommendations:
            self._enabled_tools.append(self.get_analyst_recommendations)
        if technical_indicators:
            self._enabled_tools.append(self.get_technical_indicators)

    def __iter__(self):
        return iter(self._enabled_tools)

    def get_current_stock_price(self, symbol: str) -> str:
        """
        Get the current stock price for a given symbol.

        Args:
            symbol (str): The stock symbol (e.g., 'AAPL', 'GOOGL', 'TSLA').

        Returns:
            str: The current stock price or error message.
        """
        try:
            stock = yf.Ticker(symbol.upper())
            info = stock.info
            current_price = info.get("regularMarketPrice", info.get("currentPrice"))
            
            if current_price:
                currency = info.get("currency", "USD")
                return f"Current price of {symbol.upper()}: {current_price:.2f} {currency}"
            else:
                return f"Could not fetch current price for {symbol.upper()}"
        except Exception as e:
            return f"Error fetching current price for {symbol.upper()}: {str(e)}"

    def get_company_info(self, symbol: str) -> str:
        """
        Get comprehensive company information and overview for a given stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., 'AAPL', 'GOOGL', 'TSLA').

        Returns:
            str: JSON string containing company profile and key metrics.
        """
        try:
            stock = yf.Ticker(symbol.upper())
            info = stock.info
            
            if not info:
                return f"Could not fetch company info for {symbol.upper()}"

            company_data = {
                "Name": info.get("shortName", "N/A"),
                "Symbol": info.get("symbol", symbol.upper()),
                "Current Stock Price": f"{info.get('regularMarketPrice', info.get('currentPrice', 'N/A'))} {info.get('currency', 'USD')}",
                "Market Cap": info.get("marketCap", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Industry": info.get("industry", "N/A"),
                "Country": info.get("country", "N/A"),
                "Website": info.get("website", "N/A"),
                "Business Summary": info.get("longBusinessSummary", "N/A"),
                "EPS": info.get("trailingEps", "N/A"),
                "P/E Ratio": info.get("trailingPE", "N/A"),
                "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
                "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
                "50 Day Average": info.get("fiftyDayAverage", "N/A"),
                "200 Day Average": info.get("twoHundredDayAverage", "N/A"),
                "Analyst Recommendation": info.get("recommendationKey", "N/A"),
                "Number Of Analyst Opinions": info.get("numberOfAnalystOpinions", "N/A"),
                "Employees": info.get("fullTimeEmployees", "N/A"),
                "Total Cash": info.get("totalCash", "N/A"),
                "Free Cash Flow": info.get("freeCashflow", "N/A"),
                "EBITDA": info.get("ebitda", "N/A"),
                "Revenue Growth": info.get("revenueGrowth", "N/A"),
                "Gross Margins": info.get("grossMargins", "N/A"),
            }
            
            return json.dumps(company_data, indent=2)
        except Exception as e:
            return f"Error fetching company info for {symbol.upper()}: {str(e)}"

    def get_historical_stock_prices(self, symbol: str, period: str = "1mo", interval: str = "1d") -> str:
        """
        Get historical stock prices for a given symbol.

        Args:
            symbol (str): The stock symbol (e.g., 'AAPL', 'GOOGL', 'TSLA').
            period (str): Time period for historical data. Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max. Defaults to "1mo".
            interval (str): Data interval. Valid intervals: 1d, 5d, 1wk, 1mo, 3mo. Defaults to "1d".

        Returns:
            str: JSON string containing historical price data.
        """
        try:
            stock = yf.Ticker(symbol.upper())
            historical_data = stock.history(period=period, interval=interval)
            
            if historical_data.empty:
                return f"No historical data found for {symbol.upper()}"
            
            # Convert to JSON with readable format
            historical_json = historical_data.to_json(orient="index", date_format="iso")
            return f"Historical data for {symbol.upper()} (Period: {period}, Interval: {interval}):\n{historical_json}"
        except Exception as e:
            return f"Error fetching historical prices for {symbol.upper()}: {str(e)}"

    def get_stock_fundamentals(self, symbol: str) -> str:
        """
        Get fundamental financial data for a given stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., 'AAPL', 'GOOGL', 'TSLA').

        Returns:
            str: JSON string containing fundamental financial metrics.
        """
        try:
            stock = yf.Ticker(symbol.upper())
            info = stock.info
            
            if not info:
                return f"Could not fetch fundamentals for {symbol.upper()}"

            fundamentals = {
                "symbol": symbol.upper(),
                "company_name": info.get("longName", "N/A"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "pe_ratio": info.get("forwardPE", info.get("trailingPE", "N/A")),
                "pb_ratio": info.get("priceToBook", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "eps": info.get("trailingEps", "N/A"),
                "beta": info.get("beta", "N/A"),
                "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
                "revenue_growth": info.get("revenueGrowth", "N/A"),
                "profit_margins": info.get("profitMargins", "N/A"),
                "operating_margins": info.get("operatingMargins", "N/A"),
                "return_on_equity": info.get("returnOnEquity", "N/A"),
                "return_on_assets": info.get("returnOnAssets", "N/A"),
                "debt_to_equity": info.get("debtToEquity", "N/A"),
            }
            
            return json.dumps(fundamentals, indent=2)
        except Exception as e:
            return f"Error fetching fundamentals for {symbol.upper()}: {str(e)}"

    def get_company_news(self, symbol: str, num_stories: int = 5) -> str:
        """
        Get recent news and press releases for a given stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., 'AAPL', 'GOOGL', 'TSLA').
            num_stories (int): Number of news stories to return. Defaults to 5.

        Returns:
            str: JSON string containing recent company news.
        """
        try:
            stock = yf.Ticker(symbol.upper())
            news = stock.news
            
            if not news:
                return f"No recent news found for {symbol.upper()}"
            
            # Limit to requested number of stories and format for readability
            limited_news = news[:num_stories]
            formatted_news = []
            
            for article in limited_news:
                formatted_article = {
                    "title": article.get("title", "N/A"),
                    "publisher": article.get("publisher", "N/A"),
                    "link": article.get("link", "N/A"),
                    "published": article.get("providerPublishTime", "N/A"),
                    "summary": article.get("summary", "N/A")
                }
                formatted_news.append(formatted_article)
            
            return json.dumps(formatted_news, indent=2)
        except Exception as e:
            return f"Error fetching news for {symbol.upper()}: {str(e)}"

    def get_income_statements(self, symbol: str) -> str:
        """Use this function to get income statements for a given stock symbol.

        Args:
            symbol (str): The stock symbol.

        Returns:
            dict: JSON containing income statements or an empty dictionary.
        """
        try:
            stock = yf.Ticker(symbol.upper())
            financials = stock.financials
            return financials.to_json(orient="index")
        except Exception as e:
            return f"Error fetching income statements for {symbol.upper()}: {str(e)}"

    def get_key_financial_ratios(self, symbol: str) -> str:
        """Use this function to get key financial ratios for a given stock symbol.

        Args:
            symbol (str): The stock symbol.

        Returns:
            dict: JSON containing key financial ratios.
        """
        try:
            stock = yf.Ticker(symbol.upper())
            key_ratios = stock.info
            return json.dumps(key_ratios, indent=2)
        except Exception as e:
            return f"Error fetching key financial ratios for {symbol.upper()}: {str(e)}"

    def get_analyst_recommendations(self, symbol: str) -> str:
        """Use this function to get analyst recommendations for a given stock symbol.

        Args:
            symbol (str): The stock symbol.

        Returns:
            str: JSON containing analyst recommendations.
        """
        try:
            stock = yf.Ticker(symbol.upper())
            recommendations = stock.recommendations
            return recommendations.to_json(orient="index")
        except Exception as e:
            return f"Error fetching analyst recommendations for {symbol.upper()}: {str(e)}"

    def get_technical_indicators(self, symbol: str, period: str = "3mo") -> str:
        """Use this function to get technical indicators for a given stock symbol.

        Args:
            symbol (str): The stock symbol.
            period (str): The time period for which to retrieve technical indicators.
                Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max. Defaults to 3mo.

        Returns:
            str: JSON containing technical indicators.
        """
        try:
            indicators = yf.Ticker(symbol.upper()).history(period=period)
            return indicators.to_json(orient="index")
        except Exception as e:
            return f"Error fetching technical indicators for {symbol.upper()}: {str(e)}" 