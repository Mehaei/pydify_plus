import pytest
from httpx import Response
from pydify_plus import AsyncClient as DifyAsyncClient


@pytest.mark.asyncio
async def test_list_embedding_models(respx_mock):
    respx_mock.get("/v1/models/embeddings").mock(return_value=Response(200, json={"models": ["text-embedding-ada-002"]}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.models.list_embedding_models()
        assert "models" in resp