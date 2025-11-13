# Dify Client

一个用于与 Dify API 交互的 Python 客户端库，提供同步和异步两种接口。

## 特性

- 🚀 **同步和异步支持** - 同时提供 `Client`（同步）和 `AsyncClient`（异步）两种客户端
- 📚 **完整的 API 覆盖** - 支持 Dify 的所有主要 API 端点
- 🔄 **流式响应** - 支持 Server-Sent Events (SSE) 流式响应
- 🛡️ **类型提示** - 完整的类型注解支持
- 🧪 **测试覆盖** - 包含完整的测试套件
- 📖 **详细文档** - 完整的 API 文档和示例

## 支持的 API

- **聊天** - 创建聊天消息、流式聊天、停止消息等
- **数据集** - 创建、管理、搜索数据集
- **文档** - 上传、管理文档
- **文件** - 文件上传和预览
- **会话** - 对话历史管理
- **反馈** - 消息反馈管理
- **工作流** - 工作流执行和管理
- **模型** - 嵌入模型管理
- **标签** - 知识库类型标签管理
- **应用配置** - 应用基础信息和参数配置

## 安装

### 使用 pip 安装

```bash
pip install dify-client
```

### 从源码安装

```bash
git clone https://github.com/your-username/dify-client.git
cd dify-client
pip install -e .
```

## 快速开始

### 同步客户端

```python
from pydify_plus import Client

# 初始化客户端
client = Client(
    base_url="https://api.dify.ai",
    api_key="your-api-key-here"
)

# 创建聊天消息
response = client.chat.create_chat_message(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

print(response)
```

### 异步客户端

```python
import asyncio
from pydify_plus import AsyncClient

async def main():
    async with AsyncClient(
        base_url="https://api.dify.ai",
        api_key="your-api-key-here"
    ) as client:
        # 创建聊天消息
        response = await client.chat.create_chat_message(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, how are you?"}
            ]
        )
        print(response)

asyncio.run(main())
```

### 流式响应

```python
from pydify_plus import Client

client = Client(
    base_url="https://api.dify.ai",
    api_key="your-api-key-here"
)

# 流式聊天
for event in client.chat.stream_chat_message_sync(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Tell me a story"}
    ]
):
    print(f"Event: {event.event}, Data: {event.data}")
```

## API 参考

### 客户端初始化

#### Client (同步)

```python
from pydify_plus import Client

client = Client(
    base_url="https://api.dify.ai",  # Dify API 基础 URL
    api_key="your-api-key",          # API 密钥
    timeout=30.0,                    # 请求超时时间（秒）
    retries=3                        # 重试次数
)
```

#### AsyncClient (异步)

```python
from pydify_plus import AsyncClient

# 使用上下文管理器
async with AsyncClient(
    base_url="https://api.dify.ai",
    api_key="your-api-key",
    timeout=30.0,
    retries=3
) as client:
    # 使用客户端
    pass

# 或手动管理
client = AsyncClient(
    base_url="https://api.dify.ai",
    api_key="your-api-key"
)
await client.__aenter__()
# 使用客户端
await client.__aexit__(None, None, None)
```

### 可用模块

- `client.chat` - 聊天相关 API
- `client.dataset` - 数据集相关 API
- `client.files` - 文件相关 API
- `client.documents` - 文档相关 API
- `client.blocks` - 文档片段相关 API
- `client.tags` - 标签相关 API
- `client.models` - 模型相关 API
- `client.sessions` - 会话相关 API
- `client.feedback` - 反馈相关 API
- `client.textgen` - 文本生成相关 API
- `client.workflows` - 工作流相关 API
- `client.app_config` - 应用配置相关 API

## 示例

查看 [examples](./examples/) 目录获取更多使用示例：

- [同步示例](./examples/example_sync.py)
- [异步示例](./examples/example_async.py)
- [FastAPI 集成示例](./examples/fastapi_example.py)

## 开发

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/your-username/dify-client.git
cd dify-client

# 安装开发依赖
pip install -r requirements-dev.txt

# 安装预提交钩子
pre-commit install
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_chat.py

# 运行测试并生成覆盖率报告
pytest --cov=pydify_plus
```

### 代码质量

```bash
# 代码格式化
black pydify_plus tests

# 类型检查
mypy pydify_plus

# 代码检查
flake8 pydify_plus
```

## 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解如何参与项目开发。

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](./LICENSE) 文件了解详情。

## 支持

- 文档: [查看文档](./docs/)
- 问题: [GitHub Issues](https://github.com/your-username/dify-client/issues)
- 讨论: [GitHub Discussions](https://github.com/your-username/dify-client/discussions)

## 更新日志

查看 [CHANGELOG.md](./CHANGELOG.md) 了解版本更新信息。
