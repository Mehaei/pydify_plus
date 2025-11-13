# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-11

from typing import Any, Dict

from ..config import API_ENDPOINTS


class TagsApi:
    """
    Dify 元数据与标签 API 封装。

    包含知识库类型标签的增删改查，以及数据集与标签的绑定/解绑与查询。
    注意：实际路径请参考 Dify 文档，若有差异请调整 `API_ENDPOINTS`。
    """

    def __init__(self, client):
        self.client = client

    async def list_kb_type_tags(self) -> Dict[str, Any]:
        """获取知识库类型标签列表。"""
        return await self.client._arequest("GET", API_ENDPOINTS["KB_TYPE_TAGS_LIST"]) 

    async def create_kb_type_tag(self, name: str) -> Dict[str, Any]:
        """创建新的知识库类型标签。"""
        return await self.client._arequest("POST", API_ENDPOINTS["KB_TYPE_TAGS_CREATE"], json={"name": name})

    async def delete_kb_type_tag(self, tag_id: str) -> Dict[str, Any]:
        """删除知识库类型标签。"""
        return await self.client._arequest("DELETE", API_ENDPOINTS["KB_TYPE_TAGS_DELETE"].format(tag_id=tag_id))

    async def rename_kb_type_tag(self, tag_id: str, new_name: str) -> Dict[str, Any]:
        """修改知识库类型标签名称。"""
        return await self.client._arequest("POST", API_ENDPOINTS["KB_TYPE_TAGS_RENAME"].format(tag_id=tag_id), json={"name": new_name})

    async def bind_dataset(self, tag_id: str, dataset_id: str) -> Dict[str, Any]:
        """将数据集绑定到知识库类型标签。"""
        return await self.client._arequest("POST", API_ENDPOINTS["KB_TYPE_TAGS_BIND_DATASET"].format(tag_id=tag_id, dataset_id=dataset_id))

    async def unbind_dataset(self, tag_id: str, dataset_id: str) -> Dict[str, Any]:
        """解绑数据集和知识库类型标签。"""
        return await self.client._arequest("DELETE", API_ENDPOINTS["KB_TYPE_TAGS_UNBIND_DATASET"].format(tag_id=tag_id, dataset_id=dataset_id))

    async def list_dataset_bound_tags(self, dataset_id: str) -> Dict[str, Any]:
        """查询绑定到数据集的标签。"""
        return await self.client._arequest("GET", API_ENDPOINTS["DATASET_BOUND_TAGS"].format(dataset_id=dataset_id))