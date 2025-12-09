import pytest
from app.tools.awstools import get_amazon_deals_by_product

@pytest.mark.asyncio
async def test_get_amazon_deals_by_product():
    """Test Amazon API integration"""
    result = await get_amazon_deals_by_product("laptop")
    assert result is not None
    assert isinstance(result, dict)

@pytest.mark.asyncio
async def test_get_amazon_deals_with_max_price():
    """Test Amazon API with max price filter"""
    result = await get_amazon_deals_by_product("laptop", max_price=500.0)
    assert result is not None
    assert isinstance(result, dict)
