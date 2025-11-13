import pytest
from httpx import Response, AsyncClient
from pydify_plus import AsyncClient as DifyAsyncClient

@pytest.mark.asyncio
async def test_create_chat_message(respx_mock):
    respx_mock.post("/v1/chat-messages").mock(return_value=Response(200, json={"result": "ok"}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        response = await client.chat.create_chat_message(
            model="claude-2", messages=[{"role": "user", "content": "Hello"}]
        )
        assert response["result"] == "ok"


@pytest.mark.asyncio
async def test_chat_upload_file_bytes(respx_mock):
    respx_mock.post("/v1/files/upload").mock(return_value=Response(200, json={"file_id": "f_1"}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.chat.upload_file_bytes(file_name="a.txt", content=b"hello", content_type="text/plain", purpose="conversation")
        assert resp["file_id"] == "f_1"