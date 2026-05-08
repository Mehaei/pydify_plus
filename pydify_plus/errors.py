# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-10 11:07:34
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-11 16:38:03

class DifyError(Exception):
    """Base exception for pydify_plus.

    All custom exceptions in this library inherit from this class.
    """
    pass


class DifyAPIError(DifyError):
    """Raised when the Dify API returns an error.

    This exception is raised for HTTP status codes in the 4xx or 5xx range,
    excluding authentication and not found errors which have their own
    specific exception classes.

    Attributes:
        status_code: The HTTP status code from the API response.
        body: The response body from the API, either as a dict or string.
        request_id: The request ID from the API response headers, if available.
    """

    def __init__(self, status_code: int, body: dict | str = "", request_id: str | None = None):
        self.status_code = status_code
        self.body = body
        self.request_id = request_id
        message = f"API request failed with status {status_code}"
        if request_id:
            message += f" (request_id: {request_id})"
        message += f": {body}"
        super().__init__(message)


class DifyAuthError(DifyAPIError):
    """Raised for authentication errors (401).

    This exception is raised when the API returns a 401 Unauthorized status,
    typically indicating an invalid or missing API key.
    """
    pass


class DifyNotFoundError(DifyAPIError):
    """Raised for not found errors (404).

    This exception is raised when the API returns a 404 Not Found status,
    indicating that the requested resource does not exist.
    """
    pass


class DifyRateLimitError(DifyAPIError):
    """Raised for rate limiting errors (429).

    This exception is raised when the API returns a 429 Too Many Requests status,
    indicating that the rate limit has been exceeded.
    """
    pass


class DifyValidationError(DifyAPIError):
    """Raised for validation errors (422).

    This exception is raised when the API returns a 422 Unprocessable Entity status,
    indicating that the request data is invalid.
    """
    pass


class DifyServerError(DifyAPIError):
    """Raised for server errors (5xx).

    This exception is raised when the API returns a 5xx status code,
    indicating a server-side error.
    """
    pass


class DifyConnectionError(DifyError):
    """Raised for connection-related errors.

    This exception is raised when there are network connectivity issues
    or the server cannot be reached.
    """
    pass


class DifyTimeoutError(DifyError):
    """Raised for timeout errors.

    This exception is raised when a request times out.
    """
    pass
