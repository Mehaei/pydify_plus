# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-10 11:09:03
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-10 18:16:16

from typing import TYPE_CHECKING, List, AsyncIterator, Iterator
from httpx_sse import aconnect_sse, connect_sse, ServerSentEvent

from ..config import API_ENDPOINTS

if TYPE_CHECKING:
    from ..base import BaseClient

class ChatApi:
    def __init__(self, client: "BaseClient"):
        self._client = client

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
        return await self._client._arequest("POST", API_ENDPOINTS["CHAT_MESSAGES_CREATE"], json=payload)

    async def get_chat_message(self, message_id: str) -> dict:
        """Get a chat message by its ID.

        Args:
            message_id: The ID of the message to retrieve.

        Returns:
            The API response as a dictionary.
        """
        return await self._client._arequest("GET", API_ENDPOINTS["CHAT_MESSAGES_GET"].format(conversation_id=message_id))

    async def upload_file_bytes(self, *, file_name: str, content: bytes, content_type: str = "application/octet-stream", purpose: str | None = None) -> dict:
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
        params = {"purpose": purpose} if purpose else None
        return await self._client._arequest("POST", API_ENDPOINTS["FILES_UPLOAD"], files=files, params=params)

    async def upload_file_path(self, *, file_path: str, purpose: str | None = None) -> dict:
        """Upload a local file to be used in chat.

        Args:
            file_path: Local file path to upload.
            purpose: Optional file purpose (e.g., "conversation").

        Returns:
            The API response as a dictionary containing file metadata (e.g., file_id).
        """
        file_name = file_path.split("/")[-1]
        files = {"file": (file_name, open(file_path, "rb"))}
        params = {"purpose": purpose} if purpose else None
        return await self._client._arequest("POST", API_ENDPOINTS["FILES_UPLOAD"], files=files, params=params)

    async def stream_chat_message(self, *, model: str, messages: list, **kwargs) -> AsyncIterator[ServerSentEvent]:
        """Create a streaming chat message using Server-Sent Events.

        Args:
            model: The model to use for the chat message.
            messages: A list of messages in the conversation.
            **kwargs: Additional keyword arguments to pass to the API.

        Yields:
            ServerSentEvent objects from the streaming response.
        """
        payload = {"model": model, "messages": messages, "stream": True, **kwargs}
        
        async with aconnect_sse(
            self._client._cli,
            "POST",
            API_ENDPOINTS["CHAT_MESSAGES_STREAM"],
            json=payload,
            timeout=self._client.timeout
        ) as event_source:
            async for event in event_source.aiter_sse():
                yield event

    def stream_chat_message_sync(self, *, model: str, messages: list, **kwargs) -> Iterator[ServerSentEvent]:
        """Create a streaming chat message using Server-Sent Events (synchronous version).

        Args:
            model: The model to use for the chat message.
            messages: A list of messages in the conversation.
            **kwargs: Additional keyword arguments to pass to the API.

        Yields:
            ServerSentEvent objects from the streaming response.
        """
        payload = {"model": model, "messages": messages, "stream": True, **kwargs}
        
        with connect_sse(
            self._client._async_client._cli,
            "POST",
            API_ENDPOINTS["CHAT_MESSAGES_STREAM"],
            json=payload,
            timeout=self._client.timeout
        ) as event_source:
            for event in event_source.iter_sse():
                yield event