import pytest
from httpx import Response
from pydify_plus import AsyncClient as DifyAsyncClient


@pytest.mark.asyncio
async def test_list_kb_type_tags(respx_mock):
    respx_mock.get("/v1/metadata/kb-type-tags").mock(return_value=Response(200, json={"data": []}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.tags.list_kb_type_tags()
        assert isinstance(resp.get("data"), list)


@pytest.mark.asyncio
async def test_bind_unbind_dataset(respx_mock):
    respx_mock.post("/v1/metadata/kb-type-tags/t_1/datasets/d_1").mock(return_value=Response(200, json={"ok": True}))
    respx_mock.delete("/v1/metadata/kb-type-tags/t_1/datasets/d_1").mock(return_value=Response(200, json={"ok": True}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp_bind = await client.tags.bind_dataset("t_1", "d_1")
        resp_unbind = await client.tags.unbind_dataset("t_1", "d_1")
        assert resp_bind.get("ok") and resp_unbind.get("ok")