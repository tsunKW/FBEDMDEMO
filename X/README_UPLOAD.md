# GitHub 文件上传指南

## 📋 概述

本项目包含工具和脚本，用于将 `images/` 目录中的所有文件上传到 GitHub 仓库 `tsunKW/FBEDMDEMO`。

## 🎯 上传目标

- **仓库**: https://github.com/tsunKW/FBEDMDEMO
- **所有者**: tsunKW
- **仓库名**: FBEDMDEMO
- **目标目录**: `images/`
- **源目录**: `e:\lab\台塑生醫旗艦館\FBEDM\images\`
- **文件数量**: 约 88 个文件
- **文件类型**: `.jpg`, `.png`, `.js`, `.css`

## 📝 准备工作

### 1. 获取 GitHub Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token"
3. 选择 "Generate new token (classic)"
4. 配置 Token 权限：
   - 勾选 ✅ `repo` (完整的仓库访问)
   - 勾选 ✅ `workflow` (GitHub Actions)
5. 点击 "Generate token" 并复制 Token
6. ⚠️ **重要**: Token 只会显示一次，请妥善保管

### 2. 验证 Python 环境

确保已安装 Python 3 和必要的库:

```bash
python --version
pip install requests
```

## 🚀 执行上传

有三种方式执行上传脚本：

### 方式 1: 使用批处理文件（推荐 Windows 用户）

```bash
cd e:\lab\台塑生醫旗艦館\FBEDM
upload.bat your_github_token_here
```

### 方式 2: 直接使用 Python 脚本

```bash
cd e:\lab\台塑生醫旗艦館\FBEDM
python upload_files_with_token.py your_github_token_here
```

### 方式 3: 使用环境变量

```bash
set GITHUB_TOKEN=your_github_token_here
python upload_to_github.py
```

或在 PowerShell 中:

```powershell
$env:GITHUB_TOKEN = "your_github_token_here"
python upload_to_github.py
```

## 📊 上传过程

脚本将会：

1. ✓ 验证 GitHub Token
2. ✓ 扫描 `images/` 目录
3. ✓ 对每个文件进行分类处理：
   - 图片文件 (`.jpg`, `.png`): Base64 编码后上传
   - 脚本文件 (`.js`, `.css`): 文本方式上传
4. ✓ 检查文件是否已存在于 GitHub（如果存在则更新）
5. ✓ 显示实时上传进度
6. ✓ 生成上传报告

## ✅ 预期输出

上传完成后，您将看到：

```
================================================================================
上传完成！
================================================================================
✅ 成功: 88 个文件
📊 总计: 88 个文件

🔗 仓库链接:
   https://github.com/tsunKW/FBEDMDEMO

📂 查看上传的文件:
   https://github.com/tsunKW/FBEDMDEMO/tree/main/images
```

## 📂 查看上传结果

上传完成后，访问以下链接查看文件：

- **仓库主页**: https://github.com/tsunKW/FBEDMDEMO
- **images 文件夹**: https://github.com/tsunKW/FBEDMDEMO/tree/main/images
- **单个文件**: https://github.com/tsunKW/FBEDMDEMO/blob/main/images/filename.jpg

## 🔧 脚本说明

### 提供的脚本文件：

1. **upload_to_github.py** - 主上传脚本（从环境变量读取 Token）
2. **upload_files_with_token.py** - 改进版脚本（从命令行参数获取 Token）
3. **run_upload.py** - 交互式脚本（提示用户输入 Token）
4. **upload.bat** - Windows 批处理文件（调用 Python 脚本）

### 关键功能：

- ✅ 自动检测文件类型并选择合适的编码方式
- ✅ 支持文件更新（如果文件已存在）
- ✅ 重试机制（处理 API 冲突）
- ✅ 速率限制保护（请求间延迟 0.5 秒）
- ✅ 详细的进度反馈和错误报告
- ✅ 中文界面友好

## ⚠️ 常见问题

### 1. Token 认证失败

**症状**: 出现 "401 Unauthorized"

**解决方案**:
- 检查 Token 是否正确复制（无空格、完整）
- 确认 Token 尚未过期
- 确认 Token 具有 `repo` 权限

### 2. 文件已存在

**症状**: 显示 "✓ 更新" 而不是 "✓ 上传"

**说明**: 这是正常行为，表示文件已在 GitHub 上存在，脚本将其更新为最新版本

### 3. API 速率限制

**症状**: 频繁出现 422 或 403 错误

**解决方案**:
- 脚本已内置延迟机制，应该不会遇到此问题
- 如果问题持续，等待 1 小时后重新运行

### 4. 编码错误

**症状**: 文件上传后内容乱码

**解决方案**:
- 对于 JavaScript 和 CSS 文件，确保源文件为 UTF-8 编码
- 脚本会自动处理大多数编码问题

## 🛡️ 安全提示

⚠️ **重要安全建议**:

1. **不要在代码中硬编码 Token**
2. **不要在公共仓库中提交 Token**
3. **定期更新 Token 权限检查**
4. **如果 Token 泄露，立即在 GitHub 设置中删除它**
5. **使用环境变量或命令行参数传递 Token（不要在脚本中硬编码）**

## 📞 支持信息

如有问题，请检查：

1. Python 版本是否 >= 3.6
2. `requests` 库是否已安装
3. 网络连接是否正常
4. GitHub Token 权限是否正确
5. 源目录路径是否正确

## 📄 相关资源

- [GitHub API 文档](https://docs.github.com/en/rest/reference/repos#create-or-update-file-contents)
- [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [base64 编码说明](https://en.wikipedia.org/wiki/Base64)

---

**最后更新**: 2024 年
**脚本版本**: 1.0
**兼容性**: Python 3.6+, Windows/Linux/macOS
