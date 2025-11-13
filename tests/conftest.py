"""Pytest configuration and fixtures for Dify Client tests."""

import pytest
import asyncio
from unittest.mock import AsyncMock, Mock
from typing import Dict, Any

from pydify_plus import AsyncClient, Client


@pytest.fixture
def mock_response():
    """Fixture for creating mock HTTP responses."""

    def _create_mock_response(
        status_code: int = 200,
        json_data: Dict[str, Any] = None,
        text: str = None,
        headers: Dict[str, str] = None
    ):
        mock_resp = Mock()
        mock_resp.status_code = status_code
        mock_resp.headers = headers or {}

        if json_data is not None:
            mock_resp.json = Mock(return_value=json_data)
            mock_resp.text = ""
        elif text is not None:
            mock_resp.text = text
            mock_resp.json = Mock(side_effect=ValueError("Not JSON"))

        mock_resp.raise_for_status = Mock()
        if 200 <= status_code < 300:
            mock_resp.raise_for_status.return_value = None
        else:
            mock_resp.raise_for_status.side_effect = Exception(f"HTTP {status_code}")

        return mock_resp

    return _create_mock_response


@pytest.fixture
def async_client():
    """Fixture for creating an AsyncClient instance."""
    return AsyncClient(base_url="https://api.dify.ai", api_key="test-api-key")


@pytest.fixture
def sync_client():
    """Fixture for creating a Client instance."""
    return Client(base_url="https://api.dify.ai", api_key="test-api-key")


@pytest.fixture
def mock_async_client():
    """Fixture for creating a mocked AsyncClient."""
    client = AsyncClient(base_url="https://api.dify.ai", api_key="test-api-key")
    client._cli = AsyncMock()
    return client


@pytest.fixture
def sample_chat_messages():
    """Fixture for sample chat messages."""
    return [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you!"}
    ]


@pytest.fixture
def sample_dataset_data():
    """Fixture for sample dataset data."""
    return {
        "id": "dataset-123",
        "name": "Test Dataset",
        "description": "A test dataset",
        "provider": "user",
        "permission": "only_me",
        "data_source_type": "upload_file",
        "indexing_technique": "high_quality",
        "app_count": 0,
        "document_count": 0,
        "word_count": 0,
        "created_by": "user-123",
        "created_at": 1234567890,
        "updated_at": 1234567890
    }


@pytest.fixture
def sample_document_data():
    """Fixture for sample document data."""
    return {
        "id": "doc-123",
        "dataset_id": "dataset-123",
        "position": 1,
        "data_source_type": "upload_file",
        "data_source_info": {},
        "dataset_process_rule_id": None,
        "name": "test_document.txt",
        "created_from": "upload_file",
        "created_by": "user-123",
        "created_at": 1234567890,
        "tokens": 100,
        "indexing_status": "completed",
        "enabled": True,
        "disabled_at": None,
        "disabled_by": None,
        "archived": False,
        "display_status": "available",
        "word_count": 50,
        "hit_count": 10,
        "segment_count": 5
    }


@pytest.fixture
def sample_workflow_execution_data():
    """Fixture for sample workflow execution data."""
    return {
        "execution_id": "exec-123",
        "total_tokens": 150,
        "status": "succeeded",
        "outputs": {"result": "Hello, World!"},
        "error": None,
        "elapsed_time": 1.5,
        "total_steps": 3,
        "finished_steps": 3,
        "created_at": 1234567890,
        "finished_at": 1234567891
    }


@pytest.fixture
def sample_file_upload_data():
    """Fixture for sample file upload data."""
    return {
        "id": "file-123",
        "name": "test.txt",
        "size": 1024,
        "type": "text/plain",
        "created_at": 1234567890,
        "extension": ".txt",
        "mime_type": "text/plain"
    }


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Test data factories
class TestDataFactory:
    """Factory for creating test data."""

    @staticmethod
    def create_chat_response() -> Dict[str, Any]:
        """Create sample chat response data."""
        return {
            "id": "msg-123",
            "conversation_id": "conv-123",
            "query": "Hello",
            "answer": "Hi there!",
            "message_files": [],
            "created_at": 1234567890
        }

    @staticmethod
    def create_error_response(status_code: int = 400) -> Dict[str, Any]:
        """Create sample error response data."""
        return {
            "code": f"HTTP_{status_code}",
            "message": "An error occurred",
            "status": status_code
        }

    @staticmethod
    def create_paginated_response(data: list, has_more: bool = False) -> Dict[str, Any]:
        """Create sample paginated response data."""
        return {
            "data": data,
            "has_more": has_more,
            "limit": len(data),
            "total": len(data),
            "page": 1
        }
