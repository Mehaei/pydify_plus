# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-10 11:09:03
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-26 10:01:57

from typing import TYPE_CHECKING, List, AsyncIterator, Iterator
from httpx_sse import aconnect_sse, connect_sse, ServerSentEvent

from ..config import API_ENDPOINTS
from .base import BaseApi

if TYPE_CHECKING:
    from ..base import BaseClient

class ChatApi(BaseApi):
    API_KEY_NAME = "DIFY_APP_KEY"
    async def create_chat_message(self, *, model: str, messages: list, **kwargs) -> dict:
        """Create a new chat message.

        Args:
            model: The model to use for the chat message.
            messages: A list of messages in the conversation.
            **kwargs: Additional keyword arguments to pass to the API.

        Returns:
            The API response as a dictionary.
        """
        payload = {"model": model, "messages": messages, **kwargs}
        return await self.request("POST", API_ENDPOINTS["CHAT_MESSAGES_CREATE"], json=payload)

    async def get_chat_message(self, message_id: str) -> dict:
        """Get a chat message by its ID.

        Args:
            message_id: The ID of the message to retrieve.

        Returns:
            The API response as a dictionary.
        """
        return await self.request("GET", API_ENDPOINTS["CHAT_MESSAGES_GET"].format(conversation_id=message_id))

    async def upload_file_bytes(self, *, file_name: str, content: bytes, content_type: str = "application/octet-stream", user: str = "abc-123") -> dict:
        """Upload a file to be used in chat (file-based conversations).

        Args:
            file_name: The filename to send to the server.
            content: File content as bytes.
            content_type: MIME type, defaults to application/octet-stream.
            purpose: Optional file purpose (e.g., "conversation").

        Returns:
            The API response as a dictionary containing file metadata (e.g., file_id).
        """
        files = {"file": (file_name, content, content_type)}
        payload = { "user": user }
        return await self.request("POST", API_ENDPOINTS["FILES_UPLOAD"], files=files, json=payload)

    async def preview_file(self, file_id: str, as_attachment: bool = False) -> dict[str, any]:
        """
        获取文件预览信息。

        Args:
            file_id: 文件 ID。

        Returns:
            文件预览信息字典。
        """
        querystring = {"as_attachment": as_attachment}

        return await self.request(
            "GET",
            API_ENDPOINTS["FILES_PREVIEW"].format(file_id=file_id),
            params=querystring
        )

    async def upload_file_path(self, *, file_path: str, user: str = "abc-123") -> dict:
        """Upload a local file to be used in chat.

        Args:
            file_path: Local file path to upload.
            user: Optional user ID (e.g., "abc-123").

        Returns:
            The API response as a dictionary containing file metadata (e.g., file_id).
        """
        file_name = file_path.split("/")[-1]
        files = {"file": (file_name, open(file_path, "rb"))}
        payload = { "user": user }
        return await self.request("POST", API_ENDPOINTS["FILES_UPLOAD"], files=files, json=payload)

    async def stop_chat_message(self, task_id: str, user: str = "abc-123") -> dict:
        """Stop a streaming chat message.

        Args:
            task_id: The ID of the task to stop.

        Returns:
            The API response as a dictionary.
        """
        payload = {"user": user}
        return await self.request("POST", API_ENDPOINTS["CHAT_MESSAGES_STOP"].format(task_id=task_id), json=payload)

    async def stream_chat_message(
        self,
        *,
        model: str,
        messages: list,
        **kwargs,
    ) -> AsyncIterator[ServerSentEvent]:
        """Create a streaming chat message using Server-Sent Events.

        Args:
            model: The model to use for the chat message.
            messages: A list of messages in the conversation.
            **kwargs: Additional keyword arguments to pass to the API.

        Yields:
            ServerSentEvent objects from the streaming response.
        """
        import httpx

        url = self._client._build_url(API_ENDPOINTS["CHAT_MESSAGES_STREAM"])
        headers = self._client._build_headers(api_key_name=self.API_KEY_NAME)
        payload = {"model": model, "messages": messages, **kwargs}

        httpx_client = getattr(self._client, "_cli", None)
        close_client = False
        if httpx_client is None:
            httpx_client = httpx.AsyncClient(base_url=self._client.base_url, timeout=self._client.timeout)
            close_client = True

        try:
            async with aconnect_sse(
                httpx_client,
                "POST",
                url,
                headers=headers,
                json=payload,
            ) as event_source:
                async for event in event_source.aiter_sse():
                    yield event
        finally:
            if close_client:
                await httpx_client.aclose()

    def stream_chat_message_sync(
        self,
        *,
        model: str,
        messages: list,
        **kwargs,
    ) -> Iterator[ServerSentEvent]:
        """Create a streaming chat message using Server-Sent Events (synchronous version).

        Args:
            model: The model to use for the chat message.
            messages: A list of messages in the conversation.
            **kwargs: Additional keyword arguments to pass to the API.

        Yields:
            ServerSentEvent objects from the streaming response.
        """
        import httpx

        url = self._client._build_url(API_ENDPOINTS["CHAT_MESSAGES_STREAM"])
        headers = self._client._build_headers(api_key_name=self.API_KEY_NAME)
        payload = {"model": model, "messages": messages, **kwargs}

        with httpx.Client(base_url=self._client.base_url, timeout=self._client.timeout) as httpx_client:
            with connect_sse(
                httpx_client,
                "POST",
                url,
                headers=headers,
                json=payload,
            ) as event_source:
                for event in event_source.iter_sse():
                    yield event

    def chat_message(self, *, model: str, messages: list, **kwargs) -> Iterator[ServerSentEvent]:
        for event in self.stream_chat_message_sync(model=model, messages=messages, **kwargs):
            yield event
