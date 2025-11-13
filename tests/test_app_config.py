import pytest
from httpx import Response
from pydify_plus import AsyncClient as DifyAsyncClient


@pytest.mark.asyncio
async def test_app_basic_info(respx_mock):
    respx_mock.get("/v1/app/basic-info").mock(return_value=Response(200, json={"name": "demo"}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.app_config.basic_info()
        assert resp["name"] == "demo"