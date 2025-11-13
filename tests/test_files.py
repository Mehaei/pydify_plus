# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11 16:14:16
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-12 16:23:40

import pytest
from httpx import Response
from pydify_plus import AsyncClient as DifyAsyncClient


@pytest.mark.asyncio
async def test_upload_file_bytes(respx_mock):
    respx_mock.post("/v1/files/upload").mock(return_value=Response(200, json={"file_id": "f_1"}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.files.upload_file_bytes("test.txt", b"hello", content_type="text/plain")
        assert resp["file_id"] == "f_1"


@pytest.mark.asyncio
async def test_preview_file(respx_mock):
    respx_mock.get("/v1/files/f_1/preview").mock(return_value=Response(200, json={"url": "http://preview"}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.files.preview("f_1")
        assert resp["url"] == "http://preview"