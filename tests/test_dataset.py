import pytest
from httpx import Response
from pydify_plus import AsyncClient as DifyAsyncClient

@pytest.mark.asyncio
async def test_create_dataset(respx_mock):
    respx_mock.post("/v1/datasets").mock(return_value=Response(200, json={"result": "ok"}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        response = await client.dataset.create_dataset(name="test_dataset")
        assert response["result"] == "ok"


@pytest.mark.asyncio
async def test_dataset_search_payload(respx_mock):
    captured = {}

    def _callback(request):
        import json as _json
        captured["json"] = _json.loads(request.content.decode())
        return Response(200, json={"data": []})

    respx_mock.post("/v1/datasets/d_1/search").mock(side_effect=_callback)
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.dataset.search(dataset_id="d_1", query_content="hello", top_k=3, score_threshold=0.5)
        assert resp["data"] == []
        assert captured["json"]["query"]["content"] == "hello"
        assert captured["json"]["top_k"] == 3
        assert captured["json"]["score_threshold"] == 0.5