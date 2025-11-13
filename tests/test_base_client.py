"""Tests for base client functionality."""

import pytest
from unittest.mock import Mock, patch

from pydify_plus.base import BaseClient
from pydify_plus.errors import DifyError


class TestBaseClient:
    """Test cases for BaseClient."""

    def test_init(self):
        """Test BaseClient initialization."""
        client = BaseClient.__new__(BaseClient)
        client.__init__(
            base_url="https://api.dify.ai",
            api_key="test-api-key",
            timeout=30.0,
            retries=3
        )

        assert client.base_url == "https://api.dify.ai"
        assert client.api_key == "test-api-key"
        assert client.timeout == 30.0
        assert client.retries == 3

        # Check that API modules are attached
        assert hasattr(client, 'chat')
        assert hasattr(client, 'dataset')
        assert hasattr(client, 'files')
        assert hasattr(client, 'documents')
        assert hasattr(client, 'blocks')
        assert hasattr(client, 'tags')
        assert hasattr(client, 'models')
        assert hasattr(client, 'sessions')
        assert hasattr(client, 'feedback')
        assert hasattr(client, 'textgen')
        assert hasattr(client, 'workflows')
        assert hasattr(client, 'app_config')

    def test_build_headers(self):
        """Test header construction."""
        client = BaseClient.__new__(BaseClient)
        client.__init__(
            base_url="https://api.dify.ai",
            api_key="test-api-key"
        )

        headers = client._build_headers()

        assert headers == {
            "Authorization": "Bearer test-api-key",
            "Content-Type": "application/json"
        }

    def test_build_url(self):
        """Test URL construction."""
        client = BaseClient.__new__(BaseClient)
        client.__init__(
            base_url="https://api.dify.ai",
            api_key="test-api-key"
        )

        # Test with base URL having trailing slash
        url1 = client._build_url("/v1/chat-messages")
        assert url1 == "https://api.dify.ai/v1/chat-messages"

        # Test with path having leading slash
        url2 = client._build_url("v1/chat-messages")
        assert url2 == "https://api.dify.ai/v1/chat-messages"

        # Test with base URL without trailing slash
        client.base_url = "https://api.dify.ai"
        url3 = client._build_url("v1/chat-messages")
        assert url3 == "https://api.dify.ai/v1/chat-messages"

    def test_abstract_method(self):
        """Test that _arequest is abstract."""
        client = BaseClient.__new__(BaseClient)
        client.__init__(
            base_url="https://api.dify.ai",
            api_key="test-api-key"
        )

        # _arequest should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            client._arequest("GET", "/test")

    def test_custom_parameters(self):
        """Test initialization with custom parameters."""
        client = BaseClient.__new__(BaseClient)
        client.__init__(
            base_url="https://custom.dify.ai",
            api_key="custom-key",
            timeout=60.0,
            retries=5
        )

        assert client.base_url == "https://custom.dify.ai"
        assert client.api_key == "custom-key"
        assert client.timeout == 60.0
        assert client.retries == 5
