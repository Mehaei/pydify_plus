# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-11

from typing import Any, Dict, Optional

from ..config import API_ENDPOINTS


class BlocksApi:
    """
    Dify 文档块（Segment） API 封装。

    面向文档的块增删改查以及子块管理。
    """

    def __init__(self, client):
        self.client = client

    async def list(self, dataset_id: str, document_id: str, *, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        从文档获取块列表。
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        return await self.client._arequest(
            "GET",
            API_ENDPOINTS["SEGMENTS_LIST"].format(dataset_id=dataset_id, document_id=document_id),
            params=params or None,
        )

    async def add(self, dataset_id: str, document_id: str, *, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        向文档添加块。
        """
        payload = {"content": content}
        if metadata:
            payload["metadata"] = metadata
        return await self.client._arequest(
            "POST",
            API_ENDPOINTS["SEGMENTS_ADD"].format(dataset_id=dataset_id, document_id=document_id),
            json=payload,
        )

    async def detail(self, dataset_id: str, document_id: str, segment_id: str) -> Dict[str, Any]:
        """
        获取文档中的块详情。
        """
        return await self.client._arequest(
            "GET",
            API_ENDPOINTS["SEGMENT_DETAIL"].format(dataset_id=dataset_id, document_id=document_id, segment_id=segment_id),
        )

    async def update(self, dataset_id: str, document_id: str, segment_id: str, *, content: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        更新文档中的块。
        """
        payload: Dict[str, Any] = {}
        if content is not None:
            payload["content"] = content
        if metadata is not None:
            payload["metadata"] = metadata
        return await self.client._arequest(
            "POST",
            API_ENDPOINTS["SEGMENT_UPDATE"].format(dataset_id=dataset_id, document_id=document_id, segment_id=segment_id),
            json=payload or None,
        )

    async def delete(self, dataset_id: str, document_id: str, segment_id: str) -> Dict[str, Any]:
        """
        删除文档中的块。
        """
        return await self.client._arequest(
            "DELETE",
            API_ENDPOINTS["SEGMENT_DELETE"].format(dataset_id=dataset_id, document_id=document_id, segment_id=segment_id),
        )

    async def list_children(self, dataset_id: str, document_id: str, segment_id: str) -> Dict[str, Any]:
        """
        获取子块列表。
        """
        return await self.client._arequest(
            "GET",
            API_ENDPOINTS["SEGMENT_CHILDREN_LIST"].format(dataset_id=dataset_id, document_id=document_id, segment_id=segment_id),
        )

    async def create_child(self, dataset_id: str, document_id: str, segment_id: str, *, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        创建子块。
        """
        payload = {"content": content}
        if metadata:
            payload["metadata"] = metadata
        return await self.client._arequest(
            "POST",
            API_ENDPOINTS["SEGMENT_CHILD_CREATE"].format(dataset_id=dataset_id, document_id=document_id, segment_id=segment_id),
            json=payload,
        )

    async def delete_child(self, dataset_id: str, document_id: str, segment_id: str, child_id: str) -> Dict[str, Any]:
        """
        删除子块。
        """
        return await self.client._arequest(
            "DELETE",
            API_ENDPOINTS["SEGMENT_CHILD_DELETE"].format(dataset_id=dataset_id, document_id=document_id, segment_id=segment_id, child_id=child_id),
        )

    async def update_child(self, dataset_id: str, document_id: str, segment_id: str, child_id: str, *, content: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        更新子块。
        """
        payload: Dict[str, Any] = {}
        if content is not None:
            payload["content"] = content
        if metadata is not None:
            payload["metadata"] = metadata
        return await self.client._arequest(
            "POST",
            API_ENDPOINTS["SEGMENT_CHILD_UPDATE"].format(dataset_id=dataset_id, document_id=document_id, segment_id=segment_id, child_id=child_id),
            json=payload or None,
        )