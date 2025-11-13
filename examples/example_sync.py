# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-10 11:11:20
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-12 16:31:02

#!/usr/bin/env python3
"""
同步客户端使用示例

这个示例展示了如何使用同步客户端与 Dify API 进行交互。
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径，以便从本地导入
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pydify_plus import Client
from pydify_plus.errors import (
    DifyAuthError, DifyNotFoundError, DifyRateLimitError,
    DifyValidationError, DifyServerError, DifyConnectionError, DifyTimeoutError
)
from pydify_plus.models import MessageRole

load_dotenv()


def main():
    """主函数，展示同步客户端的各种用法。"""

    # 从环境变量获取配置
    api_key = os.getenv("DIFY_API_KEY")
    base_url = os.getenv("DIFY_BASE_URL", "https://api.dify.ai")

    if not api_key:
        raise ValueError("DIFY_API_KEY environment variable not set")

    print("🚀 初始化同步客户端...")

    # 使用上下文管理器创建客户端
    with Client(
        base_url=base_url,
        api_key=api_key,
        timeout=30.0,
        retries=3,
        retry_backoff_factor=1.0
    ) as client:

        print("✅ 客户端初始化成功")

        try:
            # 示例 1: 创建聊天消息
            print("\n📝 示例 1: 创建聊天消息")
            chat_response = client.chat.create_chat_message(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": MessageRole.USER, "content": "你好，请介绍一下你自己"}
                ],
                conversation_id="test_conversation_123",
                user="example_user",
                stream=False
            )
            print(f"💬 聊天响应: {chat_response}")

            # 示例 2: 流式聊天
            print("\n🌊 示例 2: 流式聊天（如果支持）")
            try:
                for event in client.chat.stream_chat_message_sync(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": MessageRole.USER, "content": "请用流式方式回复"}
                    ],
                    stream=True
                ):
                    print(f"📡 流式事件: {event.event} - {event.data}")
            except Exception as e:
                print(f"⚠️  流式聊天可能不受支持: {e}")

            # 示例 3: 获取应用配置
            print("\n⚙️  示例 3: 获取应用配置")
            app_config = client.app_config.get_app_basic_info()
            print(f"📱 应用配置: {app_config}")

            # 示例 4: 列出数据集
            print("\n📚 示例 4: 列出数据集")
            datasets = client.dataset.list_datasets()
            print(f"📂 数据集列表: {datasets}")

            # 示例 5: 错误处理示例
            print("\n🛡️  示例 5: 错误处理")
            try:
                # 尝试访问不存在的资源
                client.dataset.get_dataset("non_existent_dataset_id")
            except DifyNotFoundError as e:
                print(f"❌ 资源未找到: {e}")
            except DifyAuthError as e:
                print(f"🔐 认证失败: {e}")
            except DifyRateLimitError as e:
                print(f"🚫 速率限制: {e}")
            except DifyValidationError as e:
                print(f"📋 验证错误: {e}")
            except DifyServerError as e:
                print(f"🔧 服务器错误: {e}")
            except DifyConnectionError as e:
                print(f"🌐 连接错误: {e}")
            except DifyTimeoutError as e:
                print(f"⏰ 超时错误: {e}")
            except Exception as e:
                print(f"💥 未知错误: {e}")

        except Exception as e:
            print(f"❌ 示例执行失败: {e}")
            sys.exit(1)

    print("\n✅ 所有示例执行完成！")


if __name__ == "__main__":
    main()