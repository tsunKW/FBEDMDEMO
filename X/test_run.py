#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：检查 simple_upload.py 的前置条件
"""

import os
import sys

# 设置工作目录
os.chdir(r'e:\lab\台塑生醫旗艦館\FBEDM')

# 导入 simple_upload 模块
sys.path.insert(0, r'e:\lab\台塑生醫旗艦館\FBEDM')

print("=" * 80)
print("GitHub 文件上传工具 - 执行前检查")
print("=" * 80)
print()

# 检查 1: 源目录
SOURCE_DIR = r"e:\lab\台塑生醫旗艦館\FBEDM\images"
print(f"✓ 源目录: {SOURCE_DIR}")
if os.path.exists(SOURCE_DIR):
    print(f"  状态: 存在 ✓")
    files = [f for f in os.listdir(SOURCE_DIR) if os.path.isfile(os.path.join(SOURCE_DIR, f))]
    print(f"  文件数: {len(files)}")
else:
    print(f"  状态: 不存在 ✗")

print()

# 检查 2: 文件类型统计
print("📊 文件类型分布:")
files = [f for f in os.listdir(SOURCE_DIR) if os.path.isfile(os.path.join(SOURCE_DIR, f)) and f != "Thumbs.db"]
by_ext = {}
for f in files:
    ext = os.path.splitext(f)[1].lower()
    if ext:
        by_ext[ext] = by_ext.get(ext, 0) + 1

for ext in sorted(by_ext.keys()):
    print(f"  {ext:10} : {by_ext[ext]:3} 个")

print()

# 检查 3: GitHub 配置
print("🔧 上传配置:")
print(f"  GitHub Owner: tsunKW")
print(f"  GitHub Repo: FBEDMDEMO")
print(f"  Target Dir: images/")

print()

# 检查 4: Token 状态
token = os.environ.get('GITHUB_TOKEN')
print("🔐 GitHub Token 状态:")
if token:
    print(f"  ✓ 已设置 (前20字符: {token[:20]}...)")
else:
    print(f"  ⚠️  未设置环境变量")
    print(f"     脚本将提示用户手动输入")

print()
print("=" * 80)
print("现在运行 simple_upload.py...")
print("=" * 80)
print()

# 导入并执行
try:
    from simple_upload import main
    main()
except KeyboardInterrupt:
    print("\n❌ 用户中断")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
