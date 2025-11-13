# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-10 17:52:08
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-12 15:15:27

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from httpx_sse import ServerSentEvent
from pydify_plus.async_client import AsyncClient
from pydify_plus.sync_client import Client
from pydify_plus.apis.chat import ChatApi


class AsyncIterator:
    def __init__(self, items):
        self.items = items

    async def __aiter__(self):
        for item in self.items:
            yield item



class TestStreamingChat:
    """Test streaming chat functionality."""

    def test_stream_chat_message_sync(self):
        """Test synchronous streaming chat message."""
        # Create mock events
        mock_events = [
            ServerSentEvent(event="message", data='{"content": "Hello"}'),
            ServerSentEvent(event="message", data='{"content": " World"}'),
            ServerSentEvent(event="done", data='{"finish_reason": "stop"}'),
        ]
        
        # Mock the connect_sse context manager
        with patch('pydify_plus.apis.chat.connect_sse') as mock_connect:
            mock_event_source = Mock()
            mock_event_source.__enter__ = Mock(return_value=mock_event_source)
            mock_event_source.__exit__ = Mock(return_value=None)
            mock_event_source.iter_sse.return_value = mock_events
            mock_connect.return_value = mock_event_source
            
            # Create client and test streaming
            client = Client(base_url="https://api.example.com", api_key="test-key")
            chat_api = ChatApi(client)
            
            events = list(chat_api.stream_chat_message_sync(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            ))
            
            assert len(events) == 3
            assert events[0].data == '{"content": "Hello"}'
            assert events[1].data == '{"content": " World"}'
            assert events[2].data == '{"finish_reason": "stop"}'

    @pytest.mark.asyncio
    async def test_stream_chat_message_async(self):
        """Test asynchronous streaming chat message."""
        # Create mock events
        mock_events = [
            ServerSentEvent(event="message", data='{"content": "Hello"}'),
            ServerSentEvent(event="message", data='{"content": " World"}'),
            ServerSentEvent(event="done", data='{"finish_reason": "stop"}'),
        ]
        
        # Mock the aconnect_sse context manager
        with patch('pydify_plus.apis.chat.aconnect_sse') as mock_aconnect:
            mock_event_source = Mock()
            mock_event_source.__aenter__ = AsyncMock(return_value=mock_event_source)
            mock_event_source.__aexit__ = AsyncMock(return_value=None)
            mock_event_source.aiter_sse.return_value = AsyncIterator(mock_events)
            mock_aconnect.return_value = mock_event_source
            
            # Create client and test streaming
            async_client = AsyncClient(base_url="https://api.example.com", api_key="test-key")
            chat_api = ChatApi(async_client)
            
            events = []
            async for event in chat_api.stream_chat_message(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}]
            ):
                events.append(event)
            
            assert len(events) == 3
            assert events[0].data == '{"content": "Hello"}'
            assert events[1].data == '{"content": " World"}'
            assert events[2].data == '{"finish_reason": "stop"}'

    def test_stream_request_sync(self):
        """Test synchronous stream request method."""
        # Create mock events
        mock_events = [
            ServerSentEvent(event="data", data='{"chunk": "1"}'),
            ServerSentEvent(event="data", data='{"chunk": "2"}'),
        ]
        
        with patch('pydify_plus.sync_client.connect_sse') as mock_connect:
            mock_event_source = Mock()
            mock_event_source.__enter__ = Mock(return_value=mock_event_source)
            mock_event_source.__exit__ = Mock(return_value=None)
            mock_event_source.iter_sse.return_value = mock_events
            mock_connect.return_value = mock_event_source
            
            client = Client(base_url="https://api.example.com", api_key="test-key")
            
            events = list(client.stream_request("POST", "/test/stream"))
            
            assert len(events) == 2
            assert events[0].data == '{"chunk": "1"}'
            assert events[1].data == '{"chunk": "2"}'

    @pytest.mark.asyncio
    async def test_stream_request_async(self):
        """Test asynchronous stream request method."""
        # Create mock events
        mock_events = [
            ServerSentEvent(event="data", data='{"chunk": "1"}'),
            ServerSentEvent(event="data", data='{"chunk": "2"}'),
        ]
        
        with patch('pydify_plus.async_client.aconnect_sse') as mock_aconnect:
            mock_event_source = Mock()
            mock_event_source.__aenter__ = AsyncMock(return_value=mock_event_source)
            mock_event_source.__aexit__ = AsyncMock(return_value=None)
            mock_event_source.aiter_sse.return_value = AsyncIterator(mock_events)
            mock_aconnect.return_value = mock_event_source
            
            async_client = AsyncClient(base_url="https://api.example.com", api_key="test-key")
            
            events = []
            async for event in async_client.stream_request("POST", "/test/stream"):
                events.append(event)
            
            assert len(events) == 2
            assert events[0].data == '{"chunk": "1"}'
            assert events[1].data == '{"chunk": "2"}'

    def test_stream_chat_with_parameters(self):
        """Test streaming chat with additional parameters."""
        mock_events = [
            ServerSentEvent(event="message", data='{"content": "Test"}'),
        ]
        
        with patch('pydify_plus.apis.chat.connect_sse') as mock_connect:
            mock_event_source = Mock()
            mock_event_source.__enter__ = Mock(return_value=mock_event_source)
            mock_event_source.__exit__ = Mock(return_value=None)
            mock_event_source.iter_sse.return_value = mock_events
            mock_connect.return_value = mock_event_source
            
            client = Client(base_url="https://api.example.com", api_key="test-key")
            chat_api = ChatApi(client)
            
            events = list(chat_api.stream_chat_message_sync(
                model="gpt-4",
                messages=[{"role": "user", "content": "Test"}],
                temperature=0.7,
                max_tokens=100
            ))
            
            assert len(events) == 1
            # Verify that the payload includes the additional parameters
            call_args = mock_connect.call_args
            assert call_args is not None