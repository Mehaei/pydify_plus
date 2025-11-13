# 发布指南

本文档描述了如何发布 Dify Client 包到 PyPI。

## 发布流程

### 1. 准备工作

在发布之前，确保：

- [ ] 所有测试通过 (`pytest`)
- [ ] 代码质量检查通过 (`black`, `flake8`, `mypy`)
- [ ] 更新了 `CHANGELOG.md`
- [ ] 更新了版本号
- [ ] 提交了所有更改

### 2. 设置 PyPI 凭据

#### 获取 PyPI API Token

1. 访问 [PyPI 账户设置](https://pypi.org/manage/account/)
2. 在 "API tokens" 部分创建新的 token
3. 设置 token 范围为整个项目或特定项目
4. 复制 token 值

#### 在 GitHub 中设置 Secrets

1. 进入 GitHub 仓库的 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 添加以下 secrets：
   - `PYPI_API_TOKEN`: PyPI API token

### 3. 发布方式

#### 方式一：使用 GitHub Actions（推荐）

1. **自动发布（GitHub Release）**
   - 在 GitHub 上创建新的 Release
   - 工作流会自动构建并发布到 PyPI

2. **手动发布**
   - 进入 GitHub Actions → Release workflow
   - 点击 "Run workflow"
   - 输入版本号（如 `1.0.0`）
   - 点击 "Run workflow"

#### 方式二：使用本地脚本

```bash
# 安装发布工具
pip install build twine

# 构建包
python -m build

# 检查包
python -m twine check dist/*

# 发布到 Test PyPI（测试用）
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# 发布到 PyPI
python -m twine upload dist/*
```

#### 方式三：使用发布脚本

```bash
# 自动版本管理
python scripts/bump_version.py patch  # 或 minor, major

# 完整发布流程
python scripts/release.py 1.0.0

# 发布到 Test PyPI
python scripts/release.py 1.0.0 --test-pypi

# 跳过测试
python scripts/release.py 1.0.0 --skip-tests
```

### 4. 版本管理

#### 版本号规范

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本号 (MAJOR)**: 不兼容的 API 修改
- **次版本号 (MINOR)**: 向后兼容的功能性新增
- **修订号 (PATCH)**: 向后兼容的问题修正

#### 自动版本管理

```bash
# 自动增加修订号
python scripts/bump_version.py patch

# 自动增加次版本号
python scripts/bump_version.py minor

# 自动增加主版本号
python scripts/bump_version.py major
```

### 5. 发布检查清单

#### 发布前检查

- [ ] 运行完整测试套件
- [ ] 更新 CHANGELOG.md
- [ ] 更新版本号
- [ ] 提交版本变更
- [ ] 创建 Git tag

#### 发布后检查

- [ ] 验证 PyPI 页面显示正确
- [ ] 测试安装：`pip install dify-client`
- [ ] 验证基本功能正常
- [ ] 更新文档（如果需要）

### 6. 故障排除

#### 常见问题

1. **认证失败**
   - 检查 `PYPI_API_TOKEN` 是否正确设置
   - 确保 token 有正确的权限

2. **版本已存在**
   - 确保版本号唯一
   - 删除已存在的 tag（如果需要）

3. **构建失败**
   - 检查 `pyproject.toml` 配置
   - 验证所有依赖项正确声明

4. **上传失败**
   - 检查网络连接
   - 验证包文件完整性

#### 测试发布

建议先在 Test PyPI 进行测试发布：

```bash
# 发布到 Test PyPI
python scripts/release.py 1.0.0 --test-pypi

# 从 Test PyPI 安装测试
pip install --index-url https://test.pypi.org/simple/ dify-client
```

### 7. 自动化配置

#### GitHub Actions 配置

项目已配置以下自动化工作流：

- **CI**: 在每次 push 和 PR 时运行测试和代码检查
- **Release**: 在创建 GitHub Release 时自动发布到 PyPI

#### 环境配置

确保在 GitHub 仓库中配置：

- `PYPI_API_TOKEN`: PyPI API token
- 可选的 `CODECOV_TOKEN`: 用于覆盖率报告

### 8. 最佳实践

1. **版本管理**
   - 每次发布都更新版本号
   - 使用语义化版本规范
   - 及时更新 CHANGELOG.md

2. **测试**
   - 发布前运行完整测试
   - 使用 Test PyPI 进行预发布测试
   - 验证安装和基本功能

3. **文档**
   - 更新 README.md 中的版本信息
   - 确保示例代码正确
   - 更新 API 文档

4. **沟通**
   - 在 Release 中提供清晰的发布说明
   - 通知用户重大变更
   - 及时响应问题反馈

## 支持

如果遇到发布问题：

1. 查看 GitHub Actions 日志
2. 检查 PyPI 错误信息
3. 参考 [PyPI 文档](https://packaging.python.org/)
4. 在项目 Issues 中寻求帮助
