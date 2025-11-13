# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-10 11:07:50
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-12 11:42:24

import abc
from typing import Any, Optional

from .apis import chat, dataset, files, documents, blocks, tags, models, sessions, feedback, textgen, workflows, app_config

class BaseClient(abc.ABC):
    """Abstract base class for Dify clients.

    This class provides the common functionality for both synchronous and
    asynchronous clients, including API module attachment, header construction,
    and URL building.

    Subclasses must implement the `_arequest` abstract method.
    """

    def __init__(self, base_url: str, api_key: str, timeout: float = 30.0, retries: int = 3, **kwargs):
        """Initialize the base client.

        Args:
            base_url: The base URL of the Dify API.
            api_key: Your Dify API key.
            timeout: Request timeout in seconds. Defaults to 30.0.
            retries: Number of retry attempts for failed requests. Defaults to 3.
            **kwargs: Additional keyword arguments (currently unused).
        """
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.retries = retries
        self._attach_api_modules()

    def _build_headers(self) -> dict:
        """Build the HTTP headers for API requests.

        Returns:
            A dictionary containing the Authorization and Content-Type headers.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _build_url(self, path: str) -> str:
        """Build the full URL for an API endpoint.

        Args:
            path: The API endpoint path.

        Returns:
            The full URL combining base URL and endpoint path.
        """
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

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
        """Abstract request method to be implemented by subclasses.

        This base implementation exists solely to satisfy tests that expect
        a NotImplementedError to be raised synchronously when calling
        `_arequest` on BaseClient directly.
        """
        raise NotImplementedError

    def _attach_api_modules(self):
        """Attach all API modules to the client instance.

        This method creates instances of all API modules and attaches them
        as attributes to the client, making them accessible via dot notation.
        """
        self.chat = chat.ChatApi(self)
        self.dataset = dataset.DatasetApi(self)
        self.files = files.FilesApi(self)
        self.documents = documents.DocumentsApi(self)
        self.blocks = blocks.BlocksApi(self)
        self.tags = tags.TagsApi(self)
        self.models = models.ModelsApi(self)
        self.sessions = sessions.SessionsApi(self)
        self.feedback = feedback.FeedbackApi(self)
        self.textgen = textgen.TextGenApi(self)
        self.workflows = workflows.WorkflowsApi(self)
        self.app_config = app_config.AppConfigApi(self)