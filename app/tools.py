from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(query: str):
    response = tavily.search(query=query, max_results=3)

    results = []

    for r in response["results"]:
        results.append(r["content"])

    return "\n".join(results)