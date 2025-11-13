# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-10 11:08:09
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-13 14:10:28

import asyncio
import json as JSON
import httpx
import logging
from typing import Optional, Any, AsyncIterator
from httpx_sse import aconnect_sse, ServerSentEvent

from .base import BaseClient
from .errors import (
    DifyAPIError, DifyAuthError, DifyNotFoundError, DifyRateLimitError,
    DifyValidationError, DifyServerError, DifyConnectionError, DifyTimeoutError
)

class AsyncClient(BaseClient):
    """Asynchronous client for interacting with the Dify API.

    This client provides async methods for all Dify API endpoints and supports
    streaming responses using Server-Sent Events.

    Example:
        >>> import asyncio
        >>> from pydify_plus import AsyncClient
        >>>
        >>> async def main():
        ...     async with AsyncClient(
        ...         base_url="https://api.dify.ai",
        ...         api_key="your-api-key"
        ...     ) as client:
        ...         response = await client.chat.create_chat_message(
        ...             model="gpt-3.5-turbo",
        ...             messages=[{"role": "user", "content": "Hello!"}]
        ...         )
        ...         print(response)
        ...
        >>> asyncio.run(main())
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
        """Initialize the async client.

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
        self.retry_backoff_factor = retry_backoff_factor
        self.logger = logger or logging.getLogger(__name__)
        self._cli: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._cli = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.aclose()

    async def aclose(self):
        if self._cli:
            await self._cli.aclose()
            self._cli = None

    async def _arequest(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        files: Optional[Any] = None,
        timeout: Optional[float] = None,
        retries: Optional[int] = None,
    ) -> dict:
        """Make an asynchronous HTTP request to the Dify API.

        This is the internal method used by all API modules. It handles
        authentication, retries, and error handling.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            path: API endpoint path.
            json: JSON payload for the request.
            params: Query parameters.
            files: Files to upload (for multipart/form-data requests).
            timeout: Request timeout in seconds. Overrides client default.
            retries: Number of retry attempts. Overrides client default.

        Returns:
            The API response as a dictionary or string.

        Raises:
            DifyAuthError: If authentication fails (401).
            DifyNotFoundError: If resource not found (404).
            DifyRateLimitError: If rate limit exceeded (429).
            DifyValidationError: If request validation fails (422).
            DifyServerError: For server errors (5xx).
            DifyConnectionError: For connection errors.
            DifyTimeoutError: For timeout errors.
        """
        if not self._cli:
            self._cli = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

        url = self._build_url(path)
        headers = self._build_headers()
        if files:
            headers.pop("Content-Type", None)

        _timeout = timeout if timeout is not None else self.timeout
        _retries = retries if retries is not None else self.retries
        
        last_exc = None

        for attempt in range(_retries + 1):
            try:
                self.logger.debug(f"Making {method} request to {url} (attempt {attempt + 1}/{_retries + 1})")

                resp = await self._cli.request(
                    method,
                    url,
                    headers=headers,
                    json=json,
                    data=data,
                    params=params,
                    files=files,
                    timeout=_timeout,
                )

                # Extract request ID from headers for better error reporting
                request_id = resp.headers.get("x-request-id")

                resp.raise_for_status()

                self.logger.debug(f"Request successful (status: {resp.status_code})")

                try:
                    return resp.json()
                except Exception:
                    return resp.text

            except httpx.TimeoutException as e:
                last_exc = DifyTimeoutError(f"Request timed out after {_timeout} seconds")
                self.logger.warning(f"Request timeout (attempt {attempt + 1}/{_retries + 1})")

            except httpx.ConnectError as e:
                last_exc = DifyConnectionError(f"Connection error: {e}")
                self.logger.warning(f"Connection error (attempt {attempt + 1}/{_retries + 1}): {e}")

            except httpx.HTTPStatusError as e:
                request_id = e.response.headers.get("x-request-id") if e.response else None
            
                try:
                    data = e.response.json()
                except Exception:
                    data = e.response.text
        
                status_code = e.response.status_code

                if status_code == 401:
                    raise DifyAuthError(status_code=status_code, body=data, request_id=request_id) from e
                elif status_code == 404:
                    raise DifyNotFoundError(status_code=status_code, body=data, request_id=request_id) from e
                elif status_code == 429:
                    raise DifyRateLimitError(status_code=status_code, body=data, request_id=request_id) from e
                elif status_code == 422:
                    raise DifyValidationError(status_code=status_code, body=data, request_id=request_id) from e
                elif 500 <= status_code < 600:
                    raise DifyServerError(status_code=status_code, body=data, request_id=request_id) from e
                else:
                    raise DifyAPIError(status_code=status_code, body=data, request_id=request_id) from e

            # If we have an exception and there are retries left, wait before retrying
            if last_exc and attempt < _retries:
                delay = self.retry_backoff_factor * (2 ** attempt)
                self.logger.info(f"Retrying in {delay:.2f} seconds...")
                await asyncio.sleep(delay)

        # If we've exhausted all retries, raise the last exception
        if last_exc:
            raise last_exc

        # This should never happen, but just in case
        raise DifyAPIError("Request failed after retries")

    async def stream_request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[ServerSentEvent]:
        """Make a streaming request using Server-Sent Events.
        
        This method is used for endpoints that support streaming responses,
        such as chat completions and text generation.

        Args:
            method: HTTP method (GET, POST, etc.).
            path: API endpoint path.
            json: JSON payload for the request.
            params: Query parameters.
            timeout: Request timeout in seconds. Overrides client default.
            
        Yields:
            ServerSentEvent objects from the streaming response.

        Raises:
            DifyAuthError: If authentication fails (401).
            DifyNotFoundError: If resource not found (404).
            DifyAPIError: For other API errors (4xx, 5xx).
            httpx.TimeoutException: If request times out.
            httpx.ConnectError: If connection fails.

        Example:
            >>> async for event in client.stream_request( 
            ...     "POST",
            ...     "/v1/chat-messages/stream",
            ...     json={"model": "gpt-3.5-turbo", "messages": [...]}
            ... ):
            ...     print(f"Event: {event.event}, Data: {event.data}")
        """
        if not self._cli:
            self._cli = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

        url = self._build_url(path)
        headers = self._build_headers()
        _timeout = timeout if timeout is not None else self.timeout

        async with aconnect_sse(
            self._cli,
            method,
            url,
            headers=headers,
            json=json,
            params=params,
            timeout=_timeout,
        ) as event_source:
            async for event in event_source.aiter_sse():
                yield event