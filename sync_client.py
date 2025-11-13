import anyio
import logging
from typing import Any, Optional, Iterator
from httpx_sse import connect_sse, ServerSentEvent

from .base import BaseClient
from .async_client import AsyncClient

class Client(BaseClient):
    """Synchronous client for interacting with the Dify API.

    This client provides synchronous methods for all Dify API endpoints and supports
    streaming responses using Server-Sent Events. It wraps the AsyncClient internally.

    Example:
        >>> from pydify_plus import Client
        >>>
        >>> with Client(
        ...     base_url="https://api.dify.ai",
        ...     api_key="your-api-key"
        ... ) as client:
        ...     response = client.chat.create_chat_message(
        ...         model="gpt-3.5-turbo",
        ...         messages=[{"role": "user", "content": "Hello!"}]
        ...     )
        ...     print(response)
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        retries: int = 3,
        retry_backoff_factor: float = 1.0,
        logger: Optional[logging.Logger] = None,
        **kwargs
    ):
        """Initialize the synchronous client.

        Args:
            base_url: The base URL of the Dify API (e.g., "https://api.dify.ai").
            api_key: Your Dify API key.
            timeout: Request timeout in seconds. Defaults to 30.0.
            retries: Number of retry attempts for failed requests. Defaults to 3.
            retry_backoff_factor: Backoff factor for retry delays. Defaults to 1.0.
            logger: Custom logger instance. If None, a default logger will be used.
            **kwargs: Additional keyword arguments passed to the base client.
        """
        super().__init__(base_url, api_key, timeout=timeout, retries=retries, **kwargs)
        self._async_client = AsyncClient(
            base_url,
            api_key,
            timeout=timeout,
            retries=retries,
            retry_backoff_factor=retry_backoff_factor,
            logger=logger,
            **kwargs
        )

    def _arequest(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        files: Optional[Any] = None,
        timeout: Optional[float] = None,
        retries: Optional[int] = None,
    ) -> dict:
        return anyio.run(
            self._async_client._arequest,
            method,
            path,
            json=json,
            params=params,
            files=files,
            timeout=timeout,
            retries=retries,
        )

    def __enter__(self):
        anyio.run(self._async_client.__aenter__)
        return self

    def __exit__(self, exc_type, exc, tb):
        anyio.run(self._async_client.__aexit__, exc_type, exc, tb)

    def stream_request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[ServerSentEvent]:
        """Make a streaming request using Server-Sent Events (synchronous version).
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            json: JSON payload for the request
            params: Query parameters
            timeout: Request timeout in seconds
            
        Yields:
            ServerSentEvent objects from the streaming response.
        """
        # Use the async client's httpx client for the connection
        if not self._async_client._cli:
            anyio.run(self._async_client.__aenter__)
        
        url = self._build_url(path)
        headers = self._build_headers()
        _timeout = timeout if timeout is not None else self.timeout

        with connect_sse(
            self._async_client._cli,
            method,
            url,
            headers=headers,
            json=json,
            params=params,
            timeout=_timeout,
        ) as event_source:
            for event in event_source.iter_sse():
                yield event