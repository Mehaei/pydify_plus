# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-11

from typing import Any, Dict, Optional

from ..config import API_ENDPOINTS


class TextGenApi:
    """
    Dify 文本生成 API 封装。

    用于非会话型的文本生成（completion）。支持流式与停止响应。
    """

    def __init__(self, client):
        self.client = client

    async def send(self, *, inputs: Dict[str, Any], user: Optional[str] = None) -> Dict[str, Any]:
        """
        发送文本生成请求。

        Args:
            inputs: 生成输入参数（prompt 等）。
            user: 用户标识（可选）。
        """
        payload = {"inputs": inputs}
        if user:
            payload["user"] = user
        return await self.client._arequest("POST", API_ENDPOINTS["COMPLETION_MESSAGES_CREATE"], json=payload)

    async def send_stream(self, *, inputs: Dict[str, Any], user: Optional[str] = None):
        """
        发送流式文本生成请求，返回 SSE 事件迭代器。
        """
        payload = {"inputs": inputs}
        if user:
            payload["user"] = user
        async for event in self.client.stream_request("POST", API_ENDPOINTS["COMPLETION_MESSAGES_STREAM"], json=payload):
            yield event

    async def stop(self, message_id: str) -> Dict[str, Any]:
        """
        停止响应文本生成任务。
        """
        return await self.client._arequest("POST", API_ENDPOINTS["COMPLETION_MESSAGES_STOP"].format(message_id=message_id))