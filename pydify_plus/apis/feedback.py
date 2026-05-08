# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-11

from typing import Any, Dict, Optional

from ..config import API_ENDPOINTS


class FeedbackApi:
    """
    Dify 消息反馈 API 封装。

    包含消息点赞与获取应用反馈列表（如有权限限制，需在服务端配置 API Key）。
    """

    def __init__(self, client):
        self.client = client

    async def like(self, message_id: str, *, score: int = 1) -> Dict[str, Any]:
        """
        对消息进行反馈（点赞）。

        Args:
            message_id: 目标消息 ID。
            score: 反馈分值，默认 1（点赞）。
        """
        return await self.client._arequest("POST", API_ENDPOINTS["FEEDBACK_LIKE"].format(message_id=message_id), json={"score": score})

    async def list(self, *, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """获取应用的消息点赞和反馈列表。"""
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        return await self.client._arequest("GET", API_ENDPOINTS["FEEDBACK_LIST"], params=params or None)