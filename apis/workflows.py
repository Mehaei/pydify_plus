# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-11

from typing import Any, Dict, Optional

from ..config import API_ENDPOINTS
from .base import BaseApi


class WorkflowsApi(BaseApi):
    """
    Dify 工作流执行 API 封装。

    包含执行 workflow、查询执行状态、停止任务、获取日志、上传工作流文件等能力。
    """
    API_KEY_NAME = "DIFY_WORKFLOW_KEY"

    def __init__(self, client):
        self.client = client

    async def execute(self, workflow_id: str, *, inputs: Dict[str, Any], user: Optional[str] = None) -> Dict[str, Any]:
        """
        执行 workflow。
        """
        payload = {"inputs": inputs}
        if user:
            payload["user"] = user
        return await self.request("POST", API_ENDPOINTS["WORKFLOW_EXECUTE"].format(workflow_id=workflow_id), json=payload)

    async def execution_status(self, workflow_id: str, execution_id: str) -> Dict[str, Any]:
        """
        获取 workflow 执行情况。
        """
        return await self.request("GET", API_ENDPOINTS["WORKFLOW_EXECUTION_STATUS"].format(workflow_id=workflow_id, execution_id=execution_id))

    async def stop_task(self, workflow_id: str, execution_id: str) -> Dict[str, Any]:
        """
        停止响应 workflow task。
        """
        return await self.request("POST", API_ENDPOINTS["WORKFLOW_STOP_TASK"].format(workflow_id=workflow_id, execution_id=execution_id))

    async def logs(self, workflow_id: str, execution_id: str) -> Dict[str, Any]:
        """
        获取 workflow 日志。
        """
        return await self.request("GET", API_ENDPOINTS["WORKFLOW_LOGS"].format(workflow_id=workflow_id, execution_id=execution_id))

    async def upload_file(self, workflow_id: str, file_path: str) -> Dict[str, Any]:
        """
        上传文件（workflow）。
        """
        files = {"file": (file_path.split("/")[-1], open(file_path, "rb"))}
        return await self.request("POST", API_ENDPOINTS["WORKFLOW_FILES_UPLOAD"].format(workflow_id=workflow_id), files=files)