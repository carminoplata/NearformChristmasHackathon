import asyncio
import aiohttp
import os

from typing import Optional
from app.utils import RAPIDAPI_API_KEY

ALIBABA_API_URL = "https://aliexpress-datahub.p.rapidapi.com"

async def get_alibaba_deals_by_product(
        item: str,
        max_price: Optional[float] = None,
        sortby: Optional[str] = None):
    headers = {
        "X-RAPIDAPI-KEY": RAPIDAPI_API_KEY
    }
    if max_price:
        params = {
            "q": item,
            "end_price": max_price,
            "country": "IT",
            "sort": "priceAsc",
            "currency": "EUR",
        }
    else:
        params = {
            "q": item,
            "country": "IT",
            "sort": "priceAsc",
            "currency": "EUR",
        }
    search_api = f"{ALIBABA_API_URL}/item_search_4"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(search_api, 
                                   headers=headers,
                                   params=params,
                                   timeout=20) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error = await response.json()
                    print(f"❌ Error Alibaba Search API: {error}")
                    return { "msg": f"No deals has been found for {item}"}
    except Exception as e:
        print(f"❌ Error during call Alibaba Search API: {e}")
        return {}
