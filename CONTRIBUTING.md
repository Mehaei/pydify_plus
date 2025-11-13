# 贡献指南

感谢您考虑为 Dify Client 项目做出贡献！我们欢迎各种形式的贡献，包括但不限于：

- 报告 bug
- 提出新功能建议
- 改进文档
- 提交代码修复或新功能

## 开发环境设置

1. **Fork 仓库**

   首先，在 GitHub 上 fork 这个仓库。

2. **克隆仓库**

   ```bash
   git clone https://github.com/your-username/dify-client.git
   cd dify-client
   ```

3. **安装开发依赖**

   ```bash
   pip install -e ".[dev]"
   ```

4. **安装预提交钩子**

   ```bash
   pre-commit install
   ```

## 开发流程

### 1. 创建分支

为您的功能或修复创建一个新的分支：

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 2. 编写代码

- 遵循现有的代码风格
- 添加适当的类型注解
- 编写清晰的文档字符串
- 为新功能添加测试

### 3. 运行测试

确保所有测试都通过：

```bash
pytest
```

### 4. 代码质量检查

运行代码格式化和检查：

```bash
# 代码格式化
 black pydify_plus tests

# 类型检查
 mypy pydify_plus

# 代码检查
 flake8 pydify_plus
```

### 5. 提交更改

使用描述性的提交信息：

```bash
git add .
git commit -m "feat: add new feature for chat streaming"
```

### 6. 推送并创建 Pull Request

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

## 代码规范

### Python 代码风格

- 使用 **Black** 进行代码格式化
- 使用 **Flake8** 进行代码检查
- 使用 **mypy** 进行类型检查
- 遵循 PEP 8 规范

### 文档字符串

使用 Google 风格的文档字符串：

```python
def create_chat_message(self, *, model: str, messages: list, **kwargs) -> dict:
    """Create a new chat message.

    Args:
        model: The model to use for the chat message.
        messages: A list of messages in the conversation.
        **kwargs: Additional keyword arguments to pass to the API.

    Returns:
        The API response as a dictionary.

    Raises:
        DifyAPIError: If the API request fails.
    """
```

### 提交信息规范

使用约定式提交格式：

- `feat:` - 新功能
- `fix:` - bug 修复
- `docs:` - 文档更新
- `style:` - 代码格式调整（不影响功能）
- `refactor:` - 代码重构
- `test:` - 测试相关
- `chore:` - 构建过程或辅助工具的变动

示例：
```
feat: add support for workflow execution
fix: handle timeout errors in async client
docs: update README with installation instructions
```

## 测试

### 编写测试

- 为新功能编写单元测试
- 测试应该覆盖正常情况和边界情况
- 使用 `pytest` 框架
- 异步代码使用 `pytest-asyncio`

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_chat.py

# 运行测试并生成覆盖率报告
 pytest --cov=pydify_plus

# 运行特定标记的测试
pytest -m "slow"
```

## 报告问题

当报告问题时，请包含以下信息：

1. **问题描述** - 清晰描述问题
2. **复现步骤** - 如何复现这个问题
3. **期望行为** - 您期望发生什么
4. **实际行为** - 实际发生了什么
5. **环境信息** - Python 版本、操作系统等
6. **代码示例** - 如果可能，提供复现代码

## 功能请求

对于新功能请求，请描述：

1. **功能描述** - 您想要什么功能
2. **使用场景** - 这个功能在什么场景下有用
3. **替代方案** - 您考虑过的替代方案

## 代码审查

所有提交的代码都会经过审查。审查者会检查：

- 代码质量
- 测试覆盖
- 文档更新
- 性能影响
- 向后兼容性

## 许可证

通过贡献代码，您同意您的贡献将在 MIT 许可证下发布。

## 获取帮助

如果您在贡献过程中遇到问题：

- 查看现有文档
- 搜索已存在的问题
- 在 GitHub Discussions 中提问
- 创建新的 issue

感谢您的贡献！🎉
