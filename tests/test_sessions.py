import pytest
from httpx import Response
from pydify_plus import AsyncClient as DifyAsyncClient


@pytest.mark.asyncio
async def test_list_conversations(respx_mock):
    respx_mock.get("/v1/conversations").mock(return_value=Response(200, json={"data": [], "total": 0}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.sessions.list()
        assert resp["total"] == 0


@pytest.mark.asyncio
async def test_conversation_history(respx_mock):
    respx_mock.get("/v1/conversations/c_1/messages").mock(return_value=Response(200, json={"data": []}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.sessions.history("c_1")
        assert isinstance(resp.get("data"), list)