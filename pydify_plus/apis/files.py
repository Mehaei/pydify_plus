# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-11

from typing import Any, Dict, Optional

from ..config import API_ENDPOINTS


class FilesApi:
    """
    Dify 文件管理 API 封装。

    提供文件上传与预览能力。支持从本地路径或内存字节流上传，符合 httpx `files` 约定。
    所有方法均为无状态转发，不在本地存储 Dify 数据。
    """

    def __init__(self, client):
        self.client = client

    async def upload_file_path(self, file_path: str, *, purpose: Optional[str] = None) -> Dict[str, Any]:
        """
        通过文件路径上传文件。

        Args:
            file_path: 本地文件路径。
            purpose: 文件用途（可选），如 dataset、workflow 等。

        Returns:
            Dify 返回的文件元数据字典。
        """
        files = {"file": (file_path.split("/")[-1], open(file_path, "rb"))}
        params = {"purpose": purpose} if purpose else None
        return await self.client._arequest(
            "POST",
            API_ENDPOINTS["FILES_UPLOAD"],
            files=files,
            params=params,
        )

    async def upload_file_bytes(self, filename: str, data: bytes, *, content_type: Optional[str] = None, purpose: Optional[str] = None) -> Dict[str, Any]:
        """
        通过内存字节流上传文件。

        Args:
            filename: 文件名。
            data: 二进制数据。
            content_type: MIME 类型（可选）。
            purpose: 文件用途（可选）。

        Returns:
            Dify 返回的文件元数据字典。
        """
        files = {"file": (filename, data, content_type or "application/octet-stream")}
        params = {"purpose": purpose} if purpose else None
        return await self.client._arequest(
            "POST",
            API_ENDPOINTS["FILES_UPLOAD"],
            files=files,
            params=params,
        )

    async def preview(self, file_id: str) -> Dict[str, Any]:
        """
        获取文件预览信息。

        Args:
            file_id: 文件 ID。

        Returns:
            文件预览信息字典。
        """
        return await self.client._arequest(
            "GET",
            API_ENDPOINTS["FILES_PREVIEW"].format(file_id=file_id),
        )