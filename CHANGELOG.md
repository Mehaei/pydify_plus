# 更新日志

所有项目的显著更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.1.0] - 2025-11-11

### 新增

- 初始版本发布
- 支持同步和异步客户端
- 完整的 Dify API 覆盖：
  - 聊天 API
  - 数据集 API
  - 文档 API
  - 文件 API
  - 会话 API
  - 反馈 API
  - 工作流 API
  - 模型 API
  - 标签 API
  - 应用配置 API
- 流式响应支持 (Server-Sent Events)
- 完整的类型注解
- 错误处理机制
- 完整的测试套件
- 使用示例

### 技术特性

- 基于 `httpx` 的 HTTP 客户端
- 支持异步和同步操作
- 自动重试机制
- 超时控制
- 上下文管理器支持

### 文档

- 完整的 README 文档
- API 参考文档
- 使用示例
- 贡献指南

## [未发布]

### 计划功能

- 更完善的错误类型
- 响应数据模型
- 批量操作支持
- 更详细的日志记录
- 性能优化

### 已知问题

- 暂无

---

## 版本说明

### 版本号格式

版本号遵循 `MAJOR.MINOR.PATCH` 格式：

- **MAJOR** - 不兼容的 API 修改
- **MINOR** - 向后兼容的功能性新增
- **PATCH** - 向后兼容的问题修正

### 发布周期

- **主要版本** (`x.0.0`) - 包含重大变更
- **次要版本** (`x.y.0`) - 包含新功能
- **修订版本** (`x.y.z`) - 包含 bug 修复

### 支持策略

- 每个主要版本至少支持 12 个月
- 安全更新会向后移植到受支持的版本
- 弃用功能会在下一个主要版本中移除，并提前通知

## 链接

- [GitHub 仓库](https://github.com/your-username/dify-client)
- [问题追踪](https://github.com/your-username/dify-client/issues)
- [文档](https://github.com/your-username/dify-client#readme)
