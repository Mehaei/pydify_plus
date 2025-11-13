import pytest
from httpx import Response
from pydify_plus import AsyncClient as DifyAsyncClient


@pytest.mark.asyncio
async def test_create_from_text(respx_mock):
    respx_mock.post("/v1/datasets/d_1/documents/text").mock(return_value=Response(200, json={"document_id": "doc_1"}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.documents.create_from_text("d_1", text="hello")
        assert resp["document_id"] == "doc_1"


@pytest.mark.asyncio
async def test_list_documents(respx_mock):
    respx_mock.get("/v1/datasets/d_1/documents").mock(return_value=Response(200, json={"data": [], "total": 0}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.documents.list("d_1")
        assert resp["total"] == 0


@pytest.mark.asyncio
async def test_create_document_from_file_bytes(respx_mock):
    respx_mock.post("/v1/datasets/d_1/documents/file").mock(return_value=Response(200, json={"document_id": "doc_2"}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.documents.create_from_file_bytes("d_1", file_name="a.txt", content=b"hello", content_type="text/plain")
        assert resp["document_id"] == "doc_2"