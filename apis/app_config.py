# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-11

from typing import Any, Dict

from ..config import API_ENDPOINTS


class AppConfigApi:
    """
    Dify 应用配置相关 API 封装。

    包含获取应用基本信息、参数、Meta 信息、WebApp 设置，以及 Workflow 版本的对应接口。
    """

    def __init__(self, client):
        self.client = client

    async def basic_info(self) -> Dict[str, Any]:
        """获取应用基本信息。"""
        return await self.client._arequest("GET", API_ENDPOINTS["APP_BASIC_INFO"]) 

    async def parameters(self) -> Dict[str, Any]:
        """获取应用参数。"""
        return await self.client._arequest("GET", API_ENDPOINTS["APP_PARAMETERS"]) 

    async def meta(self) -> Dict[str, Any]:
        """获取应用 meta 信息。"""
        return await self.client._arequest("GET", API_ENDPOINTS["APP_META"]) 

    async def webapp_settings(self) -> Dict[str, Any]:
        """获取应用 WebApp 设置。"""
        return await self.client._arequest("GET", API_ENDPOINTS["APP_WEBAPP_SETTINGS"]) 

    async def workflow_basic_info(self) -> Dict[str, Any]:
        """获取应用基本信息（Workflow 版本）。"""
        return await self.client._arequest("GET", API_ENDPOINTS["WORKFLOW_APP_BASIC_INFO"]) 

    async def workflow_parameters(self) -> Dict[str, Any]:
        """获取应用参数（Workflow 版本）。"""
        return await self.client._arequest("GET", API_ENDPOINTS["WORKFLOW_APP_PARAMETERS"]) 

    async def workflow_webapp_settings(self) -> Dict[str, Any]:
        """获取应用 WebApp 设置（Workflow 版本）。"""
        return await self.client._arequest("GET", API_ENDPOINTS["WORKFLOW_APP_WEBAPP_SETTINGS"])