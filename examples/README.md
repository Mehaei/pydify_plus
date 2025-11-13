# 示例代码

这个目录包含了使用 Pydify Plus 客户端的各种示例代码。

## 环境设置

在运行示例之前，请确保设置了必要的环境变量：

```bash
# 创建 .env 文件
echo "DIFY_API_KEY=your-api-key-here" > .env
echo "DIFY_BASE_URL=https://api.dify.ai/v1" >> .env
```

或者直接在环境中设置：

```bash
export DIFY_API_KEY="your-api-key-here"
export DIFY_BASE_URL="https://api.dify.ai/v1"
```

## 示例文件

### [example_sync.py](./example_sync.py)

同步客户端使用示例。展示了如何使用同步客户端进行基本的 API 调用。

运行：
```bash
python examples/example_sync.py
```

### [example_async.py](./example_async.py)

异步客户端使用示例。展示了如何使用异步客户端进行多个 API 调用。

运行：
```bash
python examples/example_async.py
```

### [fastapi_example.py](./fastapi_example.py)

FastAPI 集成示例。展示了如何在 FastAPI 应用中使用 Pydify Plus 客户端。

运行：
```bash
uvicorn examples.fastapi_example:app --reload
```

## 更多示例

### 流式聊天

```python
from pydify_plus import Client

client = Client(base_url="https://api.dify.ai", api_key="your-api-key")

# 流式聊天
for event in client.chat.stream_chat_message_sync(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Tell me a story"}
    ]
):
    print(f"Event: {event.event}, Data: {event.data}")
```

### 数据集操作

```python
import asyncio
from pydify_plus import AsyncClient

async def main():
    async with AsyncClient(base_url="https://api.dify.ai", api_key="your-api-key") as client:
        # 创建数据集
        dataset = await client.dataset.create_dataset(name="My Dataset")

        # 上传文件
        with open("document.pdf", "rb") as f:
            file_response = await client.files.upload_file(file=f)

        # 创建文档
        document = await client.documents.create_document_from_file(
            dataset_id=dataset["id"],
            file_id=file_response["id"]
        )

        print(f"Created dataset: {dataset['id']}")
        print(f"Uploaded file: {file_response['id']}")
        print(f"Created document: {document['id']}")

asyncio.run(main())
```

### 工作流执行

```python
from pydify_plus import Client

client = Client(base_url="https://api.dify.ai", api_key="your-api-key")

# 执行工作流
workflow_response = client.workflows.execute_workflow(
    workflow_id="your-workflow-id",
    inputs={
        "input_variable": "Hello, World!"
    }
)

print(f"Workflow execution ID: {workflow_response['execution_id']}")
```

## 错误处理

所有示例都包含基本的错误处理。在实际应用中，建议使用更详细的错误处理：

```python
from pydify_plus import Client
from pydify_plus.errors import DifyAuthError, DifyNotFoundError, DifyAPIError

client = Client(base_url="https://api.dify.ai", api_key="your-api-key")

try:
    response = client.chat.create_chat_message(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except DifyAuthError as e:
    print(f"Authentication failed: {e}")
except DifyNotFoundError as e:
    print(f"Resource not found: {e}")
except DifyAPIError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 最佳实践

1. **使用环境变量**：不要将 API 密钥硬编码在代码中
2. **错误处理**：总是处理可能的异常
3. **资源管理**：使用上下文管理器确保资源正确释放
4. **超时设置**：根据应用需求调整超时时间
5. **重试机制**：利用内置的重试机制处理临时错误

## 故障排除

如果遇到问题：

1. 检查 API 密钥是否正确
2. 验证 base URL 格式
3. 检查网络连接
4. 查看详细的错误信息
5. 确保安装了所有依赖项
