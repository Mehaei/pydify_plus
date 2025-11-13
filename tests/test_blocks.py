import pytest
from httpx import Response
from pydify_plus import AsyncClient as DifyAsyncClient


@pytest.mark.asyncio
async def test_list_segments(respx_mock):
    respx_mock.get("/v1/datasets/d_1/documents/doc_1/segments").mock(return_value=Response(200, json={"data": [], "total": 0}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.blocks.list("d_1", "doc_1")
        assert resp["total"] == 0


@pytest.mark.asyncio
async def test_add_segment(respx_mock):
    respx_mock.post("/v1/datasets/d_1/documents/doc_1/segments").mock(return_value=Response(200, json={"segment_id": "seg_1"}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.blocks.add("d_1", "doc_1", content="abc")
        assert resp["segment_id"] == "seg_1"