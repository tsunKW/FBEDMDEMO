#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式上传脚本：获取GitHub Token并上传文件
"""

import os
import sys
import getpass

# 提示用户输入 GitHub Token
print("=" * 80)
print("GitHub 文件上传工具 - 令牌输入")
print("=" * 80)
print("\n您需要提供 GitHub Personal Access Token 来上传文件。")
print("请输入您的 GitHub Token（输入将不会显示）：\n")

try:
    github_token = getpass.getpass("GitHub Token: ").strip()
    if not github_token:
        print("❌ 错误：未提供 Token")
        sys.exit(1)
    
    # 设置环境变量并执行主脚本
    os.environ['GITHUB_TOKEN'] = github_token
    
    # 现在执行主上传脚本
    import subprocess
    result = subprocess.run([sys.executable, 'upload_to_github.py'], cwd=os.path.dirname(os.path.abspath(__file__)))
    sys.exit(result.returncode)
    
except KeyboardInterrupt:
    print("\n❌ 用户取消")
    sys.exit(1)
except Exception as e:
    print(f"❌ 错误：{e}")
    sys.exit(1)
