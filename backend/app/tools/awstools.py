import asyncio
import aiohttp
import os

from typing import Optional
from app.utils import RAPIDAPI_API_KEY

AMAZON_API_URL = "https://real-time-amazon-data.p.rapidapi.com"

async def get_amazon_deals_by_product(
        item: str,
        max_price: Optional[float] = None,
        sortby: Optional[str] = None):
    headers = {
        "X-RAPIDAPI-KEY": RAPIDAPI_API_KEY
    }
    print(f"RAPID_API_KEY {search_api} with params {params}")
    if max_price:
        params = {
            "query": item,
            "max_price": max_price,
            "country": "IT",
            "sort_by": sortby if sortby else "RELEVANCE",
            "deals_and_discounts": "ALL_DISCOUNTS",
            "language": "IT"
        }
    else:
        params = {
            "query": item,
            "country": "IT",
            "sort_by": sortby if sortby else "RELEVANCE",
            "deals_and_discounts": "ALL_DISCOUNTS",
            "language": "it_IT"
        }
    search_api = f"{AMAZON_API_URL}/search"
    print(f"call Search API at {search_api} with params {params}")
    print(f"API-KEY {RAPIDAPI_API_KEY}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(search_api, 
                                   headers=headers,
                                   params=params,
                                   timeout=20) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"❌ Error AWS Search API: {await response.json()}")
                    return { "msg": f"No deals has been found for {item}"}
    except Exception as e:
        print(f"❌ Error during call at AWS Search API: {e}")
        return {}
