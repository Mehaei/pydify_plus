# 项目结构

```
pydify_plus/
├── .github/                    # GitHub 配置
│   └── workflows/              # GitHub Actions 工作流
├── pydify_plus/               # 主包目录
│   ├── __init__.py           # 包初始化
│   ├── base.py               # 基础客户端类
│   ├── async_client.py       # 异步客户端
│   ├── sync_client.py        # 同步客户端
│   ├── config.py             # API 端点配置
│   ├── errors.py             # 自定义异常
│   ├── models.py             # 数据模型
│   ├── utils.py              # 工具函数
│   └── apis/                 # API 模块
│       ├── __init__.py
│       ├── chat.py           # 聊天 API
│       ├── dataset.py        # 数据集 API
│       ├── documents.py      # 文档 API
│       ├── files.py          # 文件 API
│       ├── blocks.py         # 文档片段 API
│       ├── tags.py           # 标签 API
│       ├── models.py         # 模型 API
│       ├── sessions.py       # 会话 API
│       ├── feedback.py       # 反馈 API
│       ├── textgen.py        # 文本生成 API
│       ├── workflows.py      # 工作流 API
│       └── app_config.py     # 应用配置 API
├── tests/                    # 测试目录
│   ├── __init__.py
│   ├── test_async_client.py
│   ├── test_sync_client.py
│   ├── test_base.py
│   ├── test_chat.py
│   ├── test_dataset.py
│   ├── test_documents.py
│   ├── test_files.py
│   ├── test_blocks.py
│   ├── test_tags.py
│   ├── test_models.py
│   ├── test_sessions.py
│   ├── test_feedback.py
│   ├── test_textgen.py
│   ├── test_workflows.py
│   ├── test_app_config.py
│   └── test_streaming.py
├── examples/                 # 使用示例
│   ├── README.md
│   ├── example_sync.py      # 同步客户端示例
│   ├── example_async.py     # 异步客户端示例
│   └── fastapi_example.py   # FastAPI 集成示例
├── docs/                    # 文档目录
├── .gitignore              # Git 忽略文件
├── .pre-commit-config.yaml # 预提交钩子配置
├── pytest.ini              # pytest 配置
├── requirements.txt        # Python 依赖
├── pyproject.toml          # 现代 Python 项目配置
├── README.md               # 项目说明
├── CONTRIBUTING.md         # 贡献指南
├── CHANGELOG.md            # 更新日志
├── LICENSE                 # 许可证
└── PROJECT_STRUCTURE.md    # 项目结构说明
```

## 核心模块说明

### 客户端类

- **BaseClient**: 抽象基类，提供通用功能
- **AsyncClient**: 异步客户端，支持 async/await
- **Client**: 同步客户端，基于 AsyncClient 封装

### API 模块

每个 API 模块对应 Dify 的一个功能领域：

- **chat**: 聊天和对话管理
- **dataset**: 数据集管理
- **documents**: 文档管理
- **files**: 文件上传和预览
- **blocks**: 文档片段管理
- **tags**: 知识库标签管理
- **models**: 模型管理
- **sessions**: 会话管理
- **feedback**: 用户反馈
- **textgen**: 文本生成
- **workflows**: 工作流执行
- **app_config**: 应用配置

### 支持的功能

- ✅ 同步和异步操作
- ✅ 流式响应 (Server-Sent Events)
- ✅ 自动重试机制
- ✅ 超时控制
- ✅ 错误处理
- ✅ 类型注解
- ✅ 完整的测试覆盖
- ✅ 详细的文档

## 开发工作流

1. **代码质量**
   - Black: 代码格式化
   - Flake8: 代码检查
   - mypy: 类型检查
   - pre-commit: 预提交钩子

2. **测试**
   - pytest: 测试框架
   - pytest-asyncio: 异步测试支持
   - pytest-cov: 覆盖率报告

3. **文档**
   - Google 风格文档字符串
   - README 和示例代码
   - API 参考文档

## 依赖管理

- **pyproject.toml**: 现代 Python 项目配置
- **requirements.txt**: 传统依赖管理
- **可选依赖**: 开发和示例依赖

## 发布流程

1. 更新版本号
2. 更新 CHANGELOG.md
3. 运行测试
4. 构建包
5. 发布到 PyPI
