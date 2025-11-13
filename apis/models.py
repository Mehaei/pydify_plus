# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-11

from typing import Any, Dict

from ..config import API_ENDPOINTS


class ModelsApi:
    """
    Dify 模型相关 API 封装。

    目前提供嵌入模型列表查询。
    """

    def __init__(self, client):
        self.client = client

    async def list_embedding_models(self) -> Dict[str, Any]:
        """获取可用的嵌入模型列表。"""
        return await self.client._arequest("GET", API_ENDPOINTS["EMBEDDING_MODELS_LIST"])