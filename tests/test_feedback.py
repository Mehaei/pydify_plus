import pytest
from httpx import Response
from pydify_plus import AsyncClient as DifyAsyncClient


@pytest.mark.asyncio
async def test_like_feedback(respx_mock):
    respx_mock.post("/v1/feedbacks/m_1/like").mock(return_value=Response(200, json={"ok": True}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.feedback.like("m_1")
        assert resp.get("ok")


@pytest.mark.asyncio
async def test_list_feedback(respx_mock):
    respx_mock.get("/v1/feedbacks").mock(return_value=Response(200, json={"data": []}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.feedback.list()
        assert isinstance(resp.get("data"), list)