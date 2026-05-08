# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-12-18 11:42:24
import json as JSON
from typing import Any, Dict, Optional
from .base import BaseApi

from ..config import API_ENDPOINTS


class DocumentsApi(BaseApi):
    """
    Dify 文档管理 API 封装。

    面向知识库（数据集）下的文档增删改查与状态查询。
    支持从文本或文件创建/更新文档。
    """
    API_KEY_NAME = "DIFY_DATASET_KEY"

    async def create_from_text(self, dataset_id: str, *, text: str, title: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        通过文本创建文档。

        Args:
            dataset_id: 知识库 ID。
            text: 文档文本内容。
            title: 文档标题（可选）。
            metadata: 文档元数据（可选）。

        Returns:
            创建后的文档信息字典。
        """
        payload = {"text": text}
        if title:
            payload["title"] = title
        if metadata:
            payload["metadata"] = metadata
        return await self.request(
            "POST",
            API_ENDPOINTS["DOCUMENTS_CREATE_TEXT"].format(dataset_id=dataset_id),
            json=payload,
        )

    async def create_from_file_path(self, dataset_id: str, *, file_path: str, title: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        通过文件创建文档（文件路径）。

        Args:
            dataset_id: 知识库 ID。
            file_path: 本地文件路径。
            title: 文档标题（可选）。
            metadata: 文档元数据（可选）。

        Returns:
            创建后的文档信息字典。
        """
        files = {"file": (file_path.split("/")[-1], open(file_path, "rb"))}
        data: Dict[str, Any] = {}
        if title:
            data["title"] = title
        if metadata:
            data["metadata"] = metadata
        return await self.request(
            "POST",
            API_ENDPOINTS["DOCUMENTS_CREATE_FILE"].format(dataset_id=dataset_id),
            files=files,
            json=data if data else None,
        )

    async def create_from_file_bytes(self, dataset_id: str, *, file_name: str, content: bytes, content_type: str = "application/octet-stream", doc_language: str = "Chinese Simplified", remove_extra_spaces: bool = True, remove_urls_emails: bool = True, segmentation_max_tokens: int = 520, segmentation_chunk_overlap: int = 50, metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        通过文件创建文档（内存字节流）。

        Args:
            dataset_id: 知识库 ID。
            file: 上传的异步文件对象。
            content_type: MIME 类型，默认 application/octet-stream。
            doc_language = "Chinese Simplified"
            remove_extra_spaces = True
            remove_urls_emails = True
            segmentation_max_tokens = 520
            segmentation_chunk_overlap = 50
            metadata: 文档元数据（可选）。

        Returns:
            创建后的文档信息字典。
        """
        files = {"file": (file_name, content, content_type)}
        document_data = {
            "indexing_technique": "economy",
            "process_rule": {
                "rules": {
                    "pre_processing_rules": [
                        {
                            "id": "remove_extra_spaces",
                            "enabled": remove_extra_spaces,
                        },
                        {
                            "id": "remove_urls_emails",
                            "enabled": remove_urls_emails,
                        }
                    ],
                    "segmentation": {
                        "separator": "\n\n",
                        "max_tokens": segmentation_max_tokens,
                        "chunk_overlap": segmentation_chunk_overlap
                    }
                },
                "mode": "custom"
            },
            "doc_form": "text_model",
            "doc_language": doc_language,
            "retrieval_model": {
                "search_method": "hybrid_search",
                "reranking_enable": False,
                "reranking_mode": "weighted_score",
                "reranking_model": {
                    "reranking_provider_name": "",
                    "reranking_model_name": ""
                },
                "weights": {
                    "weight_type": "customized",
                    "vector_setting": {
                        "vector_weight": 0.7,
                        "embedding_provider_name": "",
                        "embedding_model_name": ""
                    },
                    "keyword_setting": {
                        "keyword_weight": 0.3
                    }
                },
                "top_k": 2,
                "score_threshold_enabled": False,
                "score_threshold": None
            },
            "embedding_model": "",
            "embedding_model_provider": ""
        }
        if metadata and isinstance(metadata, dict):
            document_data.update(metadata)
        data = {"data": JSON.dumps(document_data)}
        return await self.request(
            "POST",
            API_ENDPOINTS["DOCUMENTS_CREATE_FILE"].format(dataset_id=dataset_id),
            files=files,
            data=data
        )

    async def update_text(self, dataset_id: str, document_id: str, *, text: str, title: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        用文本更新文档。

        Args:
            dataset_id: 知识库 ID。
            document_id: 文档 ID。
            text: 新文本内容。
            title: 文档标题（可选）。
            metadata: 文档元数据（可选）。

        Returns:
            更新后的文档信息字典。
        """
        payload = {"text": text}
        if title:
            payload["title"] = title
        if metadata:
            payload["metadata"] = metadata
        return await self.request(
            "POST",
            API_ENDPOINTS["DOCUMENTS_UPDATE_TEXT"].format(dataset_id=dataset_id, document_id=document_id),
            json=payload,
        )

    async def update_file_path(self, dataset_id: str, document_id: str, *, file_path: str, title: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        用文件更新文档（文件路径）。

        Args:
            dataset_id: 知识库 ID。
            document_id: 文档 ID。
            file_path: 本地文件路径。
            title: 文档标题（可选）。
            metadata: 文档元数据（可选）。

        Returns:
            更新后的文档信息字典。
        """
        files = {"file": (file_path.split("/")[-1], open(file_path, "rb"))}
        data: Dict[str, Any] = {}
        if title:
            data["title"] = title
        if metadata:
            data["metadata"] = metadata
        return await self.request(
            "POST",
            API_ENDPOINTS["DOCUMENTS_UPDATE_FILE"].format(dataset_id=dataset_id, document_id=document_id),
            files=files,
            json=data if data else None,
        )

    async def update_file_bytes(self, dataset_id: str, document_id: str, *, file_name: str, content: bytes, content_type: str = "application/octet-stream", title: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        用文件更新文档（内存字节流）。

        Args:
            dataset_id: 知识库 ID。
            document_id: 文档 ID。
            file_name: 文件名。
            content: 文件字节内容。
            content_type: MIME 类型，默认 application/octet-stream。
            title: 文档标题（可选）。
            metadata: 文档元数据（可选）。

        Returns:
            更新后的文档信息字典。
        """
        files = {"file": (file_name, content, content_type)}
        data: Dict[str, Any] = {}
        if title:
            data["title"] = title
        if metadata:
            data["metadata"] = metadata
        return await self.request(
            "POST",
            API_ENDPOINTS["DOCUMENTS_UPDATE_FILE"].format(dataset_id=dataset_id, document_id=document_id),
            files=files,
            json=data if data else None,
        )

    async def embedding_status(self, dataset_id: str, batch_id: str) -> Dict[str, Any]:
        """
        获取文档嵌入状态（进度）。
        """
        return await self.request(
            "GET",
            API_ENDPOINTS["DOCUMENTS_EMBED_STATUS"].format(dataset_id=dataset_id, batch_id=document_id),
        )

    async def detail(self, dataset_id: str, document_id: str) -> Dict[str, Any]:
        """
        获取文档详情。
        """
        return await self.request(
            "GET",
            API_ENDPOINTS["DOCUMENTS_DETAIL"].format(dataset_id=dataset_id, document_id=document_id),
        )

    async def delete(self, dataset_id: str, document_id: str) -> Dict[str, Any]:
        """
        删除文档。
        """
        return await self.request(
            "DELETE",
            API_ENDPOINTS["DOCUMENTS_DELETE"].format(dataset_id=dataset_id, document_id=document_id),
        )

    async def list(self, dataset_id: str, *, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        获取知识库的文档列表。
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        return await self.request(
            "GET",
            API_ENDPOINTS["DOCUMENTS_LIST"].format(dataset_id=dataset_id),
            params=params or None,
        )

    async def update_status(self, dataset_id: str, document_id: str, *, status: str) -> Dict[str, Any]:
        """
        更新文档状态。

        Args:
            status: 文档状态，如 enabled/disabled 等。
        """
        payload = {"status": status}
        return await self.request(
            "POST",
            API_ENDPOINTS["DOCUMENTS_UPDATE_STATUS"].format(dataset_id=dataset_id, document_id=document_id),
            json=payload,
        )