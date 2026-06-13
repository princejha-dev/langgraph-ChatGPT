"""Tools for the chatbot agent"""
import os
import requests
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_tavily import TavilySearch
from config.settings import TAVILY_API_KEY


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage API.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=326SWHIXHEU8ZB5G"
    r = requests.get(url)
    return r.json()

@tool
def web_search(query: str) -> dict:
    """
    Perform a web search for the given query using the Tavily API.  
    Returns structured search results such as snippets, links, and metadata.
    """
    tool = TavilySearch(
        max_results=5,
        topic="general",
        api_key=TAVILY_API_KEY
    )

    result = tool.invoke({"query":query})

    return result


# All available tools
tools = [web_search, get_stock_price]
