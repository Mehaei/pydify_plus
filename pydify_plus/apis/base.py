from typing import TYPE_CHECKING, Optional, Dict, Any, List, AsyncIterator


if TYPE_CHECKING:
    from ..base import BaseClient


class BaseApi:
    API_KEY_NAME = "DIFY_API_KEY"
    def __init__(self, client: "BaseClient"):
        self._client = client
    async def request(self, *args, **kwargs) -> dict:
        if "api_key_name" not in kwargs:
            kwargs["api_key_name"] = self.API_KEY_NAME
        return await self._client._arequest(*args, **kwargs)

    async def stream_request(self, *args, **kwargs) -> AsyncIterator[dict]:
        if "api_key_name" not in kwargs:
            kwargs["api_key_name"] = self.API_KEY_NAME
        async for event in self._client._stream_request(*args, **kwargs):
            yield event
