from typing import TYPE_CHECKING, Optional, Dict, Any, List
from ..config import API_ENDPOINTS
from .base import BaseApi


if TYPE_CHECKING:
    from ..base import BaseClient

class DatasetApi(BaseApi):
    API_KEY_NAME = "DIFY_DATASET_KEY"
    async def create_dataset(self, *, name: str, description: Optional[str] = None, **kwargs) -> dict:
        """Create a new dataset.

        Args:
            name: The name of the dataset.
            description: The description of the dataset.
            permission: The permission of the dataset.

        Returns:
            The API response as a dictionary.
        """
        payload = {"name": name, "description": description, **kwargs}
        return await self.request("POST", API_ENDPOINTS["DATASETS_CREATE"], json=payload)

    async def list_datasets(self, *, keyword: Optional[str] = None, tag_ids: Optional[List[str]] = None, page: int = 1, limit: int = 20, include_all: bool = False) -> dict:
        """List datasets with optional filters.

        Args:
            keyword: Search keyword to filter by dataset name.
            tag_ids: List of tag IDs; dataset must contain all specified tags.
            page: Page number.
            limit: Items per page (1-100).
            include_all: Whether to include all datasets (workspace owner only).

        Returns:
            A paginated list response as a dictionary.
        """
        params: Dict[str, Any] = {"page": page, "limit": limit, "include_all": include_all}
        if keyword:
            params["keyword"] = keyword
        if tag_ids:
            params["tag_ids"] = tag_ids
        return await self.request("GET", API_ENDPOINTS["DATASETS_LIST"], params=params)

    async def get_dataset(self, *, dataset_id: str) -> dict:
        """Get dataset detail by ID.

        Args:
            dataset_id: Dataset ID.

        Returns:
            Dataset detail as a dictionary.
        """
        return await self.request("GET", API_ENDPOINTS["DATASET_DETAIL"].format(dataset_id=dataset_id))

    async def update_dataset(self, *, dataset_id: str, name: Optional[str] = None, description: Optional[str] = None) -> dict:
        """Update dataset fields.

        Args:
            dataset_id: Dataset ID to update.
            name: New name.
            description: New description.

        Returns:
            The updated dataset response as a dictionary.
        """
        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        return await self.request("PATCH", API_ENDPOINTS["DATASET_UPDATE"].format(dataset_id=dataset_id), json=payload)

    async def delete_dataset(self, *, dataset_id: str) -> dict:
        """Delete a dataset by ID.

        Args:
            dataset_id: Dataset ID.

        Returns:
            API response as a dictionary.
        """
        return await self.request("DELETE", API_ENDPOINTS["DATASET_DELETE"].format(dataset_id=dataset_id))

    async def search(
        self,
        *,
        dataset_id: str,
        query_content: str,
        top_k: int = 5,
        score_threshold: Optional[float] = None,
    ) -> dict:
        """Search blocks in a knowledge base (dataset).

        This implements the "Retrieve blocks from knowledge base / Test retrieval" payload
        format, where the query must be wrapped as an object.

        Args:
            dataset_id: The ID of the dataset to search.
            query_content: The search query content string.
            top_k: The number of results to return.
            score_threshold: Optional score threshold for filtering results.

        Returns:
            The API response as a dictionary.
        """
        payload: Dict[str, Any] = {"query": {"content": query_content}, "top_k": top_k}
        if score_threshold is not None:
            payload["score_threshold"] = score_threshold
        return await self.request(
            "POST",
            API_ENDPOINTS["DATASETS_SEARCH"].format(dataset_id=dataset_id),
            json=payload,
        )