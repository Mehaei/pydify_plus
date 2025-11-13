import pytest
from httpx import Response
from pydify_plus import AsyncClient as DifyAsyncClient


@pytest.mark.asyncio
async def test_send_text_completion(respx_mock):
    respx_mock.post("/v1/completion-messages").mock(return_value=Response(200, json={"id": "msg_1"}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.textgen.send(inputs={"prompt": "hello"})
        assert resp["id"] == "msg_1"