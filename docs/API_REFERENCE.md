# API 参考文档

本文档提供了 Dify Client 的完整 API 参考。

## 客户端类

### AsyncClient

异步客户端，支持所有 Dify API 端点。

#### 初始化

```python
from pydify_plus import AsyncClient

# 基本用法
client = AsyncClient(
    base_url="https://api.dify.ai",
    api_key="your-api-key"
)

# 高级配置
client = AsyncClient(
    base_url="https://api.dify.ai",
    api_key="your-api-key",
    timeout=30.0,              # 请求超时时间（秒）
    retries=3,                 # 重试次数
    retry_backoff_factor=1.0,  # 重试退避因子
    logger=custom_logger       # 自定义日志记录器
)
```

#### 上下文管理器

```python
async with AsyncClient(base_url="https://api.dify.ai", api_key="your-api-key") as client:
    # 使用客户端
    response = await client.chat.create_chat_message(...)
```

#### 方法

- `_arequest(method, path, **kwargs)`: 内部请求方法
- `stream_request(method, path, **kwargs)`: 流式请求
- `aclose()`: 关闭客户端连接

### Client

同步客户端，基于 AsyncClient 封装。

#### 初始化

```python
from pydify_plus import Client

# 基本用法
client = Client(
    base_url="https://api.dify.ai",
    api_key="your-api-key"
)

# 高级配置
client = Client(
    base_url="https://api.dify.ai",
    api_key="your-api-key",
    timeout=30.0,              # 请求超时时间（秒）
    retries=3,                 # 重试次数
    retry_backoff_factor=1.0,  # 重试退避因子
    logger=custom_logger       # 自定义日志记录器
)
```

#### 上下文管理器

```python
with Client(base_url="https://api.dify.ai", api_key="your-api-key") as client:
    # 使用客户端
    response = client.chat.create_chat_message(...)
```

## API 模块

### Chat API

聊天相关功能。

#### 方法

- `create_chat_message(model, messages, **kwargs)`: 创建聊天消息
- `get_chat_message(message_id)`: 获取聊天消息
- `stream_chat_message(model, messages, **kwargs)`: 流式聊天（异步）
- `stream_chat_message_sync(model, messages, **kwargs)`: 流式聊天（同步）

#### 示例

```python
# 创建聊天消息
response = await client.chat.create_chat_message(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello"}
    ],
    conversation_id="conv_123",
    user="user_123",
    stream=False
)

# 流式聊天
for event in client.chat.stream_chat_message_sync(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}],
    stream=True
):
    print(f"Event: {event.event}, Data: {event.data}")
```

### Dataset API

数据集管理功能。

#### 方法

- `create_dataset(name, **kwargs)`: 创建数据集
- `list_datasets(**kwargs)`: 列出数据集
- `get_dataset(dataset_id)`: 获取数据集详情
- `update_dataset(dataset_id, **kwargs)`: 更新数据集
- `delete_dataset(dataset_id)`: 删除数据集
- `search_dataset(dataset_id, query, **kwargs)`: 搜索数据集

#### 示例

```python
# 创建数据集
dataset = await client.dataset.create_dataset(
    name="My Dataset",
    description="A test dataset",
    permission="only_me",
    indexing_technique="high_quality"
)

# 搜索数据集
results = await client.dataset.search_dataset(
    dataset_id="dataset_123",
    query="search query",
    top_k=10,
    score_threshold=0.8
)
```

### Files API

文件上传和管理功能。

#### 方法

- `upload_file(file, **kwargs)`: 上传文件
- `get_file_preview(file_id)`: 获取文件预览

#### 示例

```python
# 上传文件
with open("document.pdf", "rb") as f:
    file_response = await client.files.upload_file(
        file=f,
        user="user_123"
    )
```

### Documents API

文档管理功能。

#### 方法

- `create_document_from_text(dataset_id, name, text, **kwargs)`: 从文本创建文档
- `create_document_from_file(dataset_id, name, file_id, **kwargs)`: 从文件创建文档
- `list_documents(dataset_id, **kwargs)`: 列出文档
- `get_document(dataset_id, document_id)`: 获取文档详情
- `update_document(dataset_id, document_id, **kwargs)`: 更新文档
- `delete_document(dataset_id, document_id)`: 删除文档
- `get_document_embedding_status(dataset_id, document_id)`: 获取文档嵌入状态

#### 示例

```python
# 从文本创建文档
document = await client.documents.create_document_from_text(
    dataset_id="dataset_123",
    name="My Document",
    text="This is the document content.",
    indexing_technique="high_quality"
)
```

### Workflows API

工作流执行功能。

#### 方法

- `execute_workflow(workflow_id, inputs, **kwargs)`: 执行工作流
- `get_execution_status(workflow_id, execution_id)`: 获取执行状态
- `stop_execution(workflow_id, execution_id)`: 停止执行
- `get_execution_logs(workflow_id, execution_id)`: 获取执行日志
- `upload_workflow_file(workflow_id, file_path)`: 上传工作流文件

#### 示例

```python
# 执行工作流
execution = await client.workflows.execute_workflow(
    workflow_id="workflow_123",
    inputs={
        "input_variable": "Hello, World!"
    },
    user="user_123"
)

# 获取执行状态
status = await client.workflows.get_execution_status(
    workflow_id="workflow_123",
    execution_id="execution_123"
)
```

### Sessions API

会话管理功能。

#### 方法

- `list_conversations(**kwargs)`: 列出会话
- `delete_conversation(conversation_id)`: 删除会话
- `rename_conversation(conversation_id, name)`: 重命名会话
- `get_conversation_messages(conversation_id, **kwargs)`: 获取会话消息
- `get_conversation_variables(conversation_id)`: 获取会话变量

#### 示例

```python
# 列出会话
conversations = await client.sessions.list_conversations(
    limit=20,
    last_id=None,
    pinned=False
)
```

### Models API

模型管理功能。

#### 方法

- `list_embedding_models()`: 列出嵌入模型

#### 示例

```python
# 列出嵌入模型
models = await client.models.list_embedding_models()
```

### Feedback API

反馈管理功能。

#### 方法

- `like_message(message_id)`: 点赞消息
- `list_feedbacks(**kwargs)`: 列出反馈

#### 示例

```python
# 点赞消息
await client.feedback.like_message("message_123")
```

### TextGen API

文本生成功能。

#### 方法

- `create_completion_message(model, prompt, **kwargs)`: 创建补全消息
- `stream_completion_message(model, prompt, **kwargs)`: 流式补全（异步）
- `stream_completion_message_sync(model, prompt, **kwargs)`: 流式补全（同步）

#### 示例

```python
# 创建补全消息
response = await client.textgen.create_completion_message(
    model="gpt-3.5-turbo",
    prompt="Complete this sentence: The weather today is",
    user="user_123"
)
```

### AppConfig API

应用配置功能。

#### 方法

- `get_app_basic_info()`: 获取应用基础信息
- `get_app_parameters()`: 获取应用参数
- `get_app_meta()`: 获取应用元数据
- `get_webapp_settings()`: 获取 WebApp 设置

#### 示例

```python
# 获取应用基础信息
app_info = await client.app_config.get_app_basic_info()
```

### Tags API

标签管理功能。

#### 方法

- `list_kb_type_tags()`: 列出知识库类型标签
- `create_kb_type_tag(name)`: 创建知识库类型标签
- `delete_kb_type_tag(tag_id)`: 删除知识库类型标签
- `rename_kb_type_tag(tag_id, name)`: 重命名知识库类型标签
- `bind_dataset_to_tag(tag_id, dataset_id)`: 绑定数据集到标签
- `unbind_dataset_from_tag(tag_id, dataset_id)`: 从标签解绑数据集
- `get_dataset_bound_tags(dataset_id)`: 获取数据集绑定的标签

#### 示例

```python
# 列出标签
tags = await client.tags.list_kb_type_tags()

# 创建标签
new_tag = await client.tags.create_kb_type_tag("Important Documents")
```

### Blocks API

文档片段管理功能。

#### 方法

- `list_segments(dataset_id, document_id, **kwargs)`: 列出文档片段
- `add_segment(dataset_id, document_id, content, **kwargs)`: 添加文档片段
- `get_segment(dataset_id, document_id, segment_id)`: 获取文档片段
- `update_segment(dataset_id, document_id, segment_id, content, **kwargs)`: 更新文档片段
- `delete_segment(dataset_id, document_id, segment_id)`: 删除文档片段
- `list_segment_children(dataset_id, document_id, segment_id)`: 列出子片段
- `create_segment_child(dataset_id, document_id, segment_id, content, **kwargs)`: 创建子片段
- `delete_segment_child(dataset_id, document_id, segment_id, child_id)`: 删除子片段
- `update_segment_child(dataset_id, document_id, segment_id, child_id, content, **kwargs)`: 更新子片段

#### 示例

```python
# 列出文档片段
segments = await client.blocks.list_segments(
    dataset_id="dataset_123",
    document_id="document_123"
)
```

## 数据模型

### ChatMessage

聊天消息模型。

```python
from pydify_plus.models import ChatMessage, MessageRole

message = ChatMessage(
    role=MessageRole.USER,
    content="Hello, how are you?"
)
```

### CreateChatMessageRequest

创建聊天消息请求模型。

```python
from pydify_plus.models import CreateChatMessageRequest, ChatMessage, MessageRole

request = CreateChatMessageRequest(
    model="gpt-3.5-turbo",
    messages=[
        ChatMessage(role=MessageRole.USER, content="Hello")
    ],
    conversation_id="conv_123",
    user="user_123",
    stream=False
)
```

### DatasetResponse

数据集响应模型。

```python
from pydify_plus.models import DatasetResponse

# 通常从 API 响应自动创建
dataset = DatasetResponse(**api_response)
```

### WorkflowExecutionResponse

工作流执行响应模型。

```python
from pydify_plus.models import WorkflowExecutionResponse, WorkflowExecutionStatus

# 通常从 API 响应自动创建
execution = WorkflowExecutionResponse(**api_response)
```

## 错误处理

### 异常类

- `DifyError`: 基础异常类
- `DifyAPIError`: API 错误
- `DifyAuthError`: 认证错误 (401)
- `DifyNotFoundError`: 资源未找到错误 (404)
- `DifyRateLimitError`: 速率限制错误 (429)
- `DifyValidationError`: 验证错误 (422)
- `DifyServerError`: 服务器错误 (5xx)
- `DifyConnectionError`: 连接错误
- `DifyTimeoutError`: 超时错误

### 错误处理示例

```python
from pydify_plus.errors import (
    DifyAuthError, DifyNotFoundError, DifyRateLimitError,
    DifyValidationError, DifyServerError, DifyConnectionError, DifyTimeoutError
)

try:
    response = await client.chat.create_chat_message(...)
except DifyAuthError as e:
    print(f"认证失败: {e}")
except DifyNotFoundError as e:
    print(f"资源未找到: {e}")
except DifyRateLimitError as e:
    print(f"速率限制: {e}")
    # 可以在这里实现退避重试逻辑
except DifyValidationError as e:
    print(f"验证错误: {e}")
except DifyServerError as e:
    print(f"服务器错误: {e}")
except DifyConnectionError as e:
    print(f"连接错误: {e}")
except DifyTimeoutError as e:
    print(f"超时错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

## 配置

### 环境变量

```bash
# .env 文件示例
DIFY_API_KEY=your-api-key-here
DIFY_BASE_URL=https://api.dify.ai
```

### 日志配置

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 使用自定义日志记录器
client = AsyncClient(
    base_url="https://api.dify.ai",
    api_key="your-api-key",
logger=logging.getLogger("pydify_plus")
)
```

## 最佳实践

### 1. 使用上下文管理器

```python
# 推荐：自动管理连接
async with AsyncClient(base_url="https://api.dify.ai", api_key="your-api-key") as client:
    response = await client.chat.create_chat_message(...)

# 不推荐：手动管理连接
client = AsyncClient(base_url="https://api.dify.ai", api_key="your-api-key")
await client.__aenter__()
try:
    response = await client.chat.create_chat_message(...)
finally:
    await client.__aexit__(None, None, None)
```

### 2. 错误处理

```python
try:
    response = await client.chat.create_chat_message(...)
except DifyRateLimitError:
    # 实现退避重试逻辑
    await asyncio.sleep(60)
    response = await client.chat.create_chat_message(...)
except (DifyConnectionError, DifyTimeoutError):
    # 网络问题，可以重试
    pass
```

### 3. 资源管理

```python
# 及时关闭文件句柄
with open("large_file.pdf", "rb") as f:
    file_response = await client.files.upload_file(file=f)

# 文件上传后立即关闭
```

### 4. 性能优化

```python
# 使用适当的超时和重试设置
client = AsyncClient(
    base_url="https://api.dify.ai",
    api_key="your-api-key",
    timeout=30.0,      # 根据网络状况调整
    retries=3,         # 根据 API 稳定性调整
    retry_backoff_factor=1.0  # 指数退避
)
```

## 常见问题

### Q: 如何处理大文件上传？

A: 使用流式上传，避免内存问题：

```python
with open("large_file.pdf", "rb") as f:
    file_response = await client.files.upload_file(file=f)
```

### Q: 如何调试请求？

A: 启用调试日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Q: 如何处理速率限制？

A: 捕获 `DifyRateLimitError` 并实现退避重试：

```python
try:
    response = await client.chat.create_chat_message(...)
except DifyRateLimitError:
    await asyncio.sleep(60)  # 等待 1 分钟
    response = await client.chat.create_chat_message(...)
```

### Q: 如何测试 API 连接？

A: 使用简单的 API 调用测试连接：

```python
try:
    app_info = await client.app_config.get_app_basic_info()
    print("✅ API 连接正常")
except Exception as e:
    print(f"❌ API 连接失败: {e}")
