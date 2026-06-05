"""Tools for the chatbot agent"""
import requests
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults

# Search Tool
search_tool = DuckDuckGoSearchResults(region="us-en")


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage API.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()


# All available tools
tools = [search_tool, get_stock_price]
