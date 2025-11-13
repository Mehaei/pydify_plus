# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-11

from typing import Any, Dict, Optional

from ..config import API_ENDPOINTS


class SessionsApi:
    """
    Dify 会话（Conversation）管理 API 封装。

    包含获取会话列表、历史消息、删除、重命名、获取会话变量等能力。
    """

    def __init__(self, client):
        self.client = client

    async def list(self, *, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """获取会话列表。"""
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        return await self.client._arequest("GET", API_ENDPOINTS["CONVERSATIONS_LIST"], params=params or None)

    async def history(self, conversation_id: str, *, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """获取会话历史消息。"""
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        return await self.client._arequest(
            "GET",
            API_ENDPOINTS["CONVERSATION_HISTORY"].format(conversation_id=conversation_id),
            params=params or None,
        )

    async def delete(self, conversation_id: str) -> Dict[str, Any]:
        """删除会话。"""
        return await self.client._arequest("DELETE", API_ENDPOINTS["CONVERSATION_DELETE"].format(conversation_id=conversation_id))

    async def rename(self, conversation_id: str, *, name: str) -> Dict[str, Any]:
        """会话重命名。"""
        return await self.client._arequest("POST", API_ENDPOINTS["CONVERSATION_RENAME"].format(conversation_id=conversation_id), json={"name": name})

    async def variables(self, conversation_id: str) -> Dict[str, Any]:
        """获取对话变量。"""
        return await self.client._arequest("GET", API_ENDPOINTS["CONVERSATION_VARIABLES"].format(conversation_id=conversation_id))