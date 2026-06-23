#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查上传脚本的前置条件和文件状态
"""

import os
import sys

os.chdir(r'e:\lab\台塑生醫旗艦館\FBEDM')

SOURCE_DIR = r"e:\lab\台塑生醫旗艦館\FBEDM\images"
GITHUB_OWNER = "tsunKW"
GITHUB_REPO = "FBEDMDEMO"
TARGET_DIR = "images"

print("=" * 80)
print("GitHub 文件上传工具 - 前置条件检查")
print("=" * 80)
print()

# 检查源目录
print("1️⃣  源目录检查:")
print(f"   路径: {SOURCE_DIR}")
if os.path.exists(SOURCE_DIR):
    print(f"   状态: ✓ 存在")
    files = [f for f in os.listdir(SOURCE_DIR) if os.path.isfile(os.path.join(SOURCE_DIR, f)) and f != "Thumbs.db"]
    print(f"   文件数: {len(files)} 个")
else:
    print(f"   状态: ✗ 不存在")
    sys.exit(1)

print()

# 文件类型统计
print("2️⃣  文件类型统计:")
by_ext = {}
for f in files:
    ext = os.path.splitext(f)[1].lower()
    if ext:
        by_ext[ext] = by_ext.get(ext, 0) + 1

for ext in sorted(by_ext.keys()):
    print(f"   {ext:10} : {by_ext[ext]:3} 个")

print()

# GitHub 配置
print("3️⃣  上传目标配置:")
print(f"   Owner: {GITHUB_OWNER}")
print(f"   Repo: {GITHUB_REPO}")
print(f"   Target Dir: {TARGET_DIR}/")
print(f"   API Endpoint: https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents")

print()

# Token 检查
print("4️⃣  GitHub Token 检查:")
token = os.environ.get('GITHUB_TOKEN')
if token:
    print(f"   状态: ✓ 已设置 GITHUB_TOKEN")
    print(f"   前缀: {token[:6]}...")
else:
    print(f"   状态: ⚠️  GITHUB_TOKEN 未设置")
    print(f"   说明: 脚本运行时会提示输入")

print()

# 采样文件大小
print("5️⃣  采样文件信息 (前5个):")
for f in files[:5]:
    file_path = os.path.join(SOURCE_DIR, f)
    size_kb = os.path.getsize(file_path) / 1024
    print(f"   {f:40} ({size_kb:8.2f} KB)")

print()
print("=" * 80)
print("✅ 所有前置条件检查完成")
print("=" * 80)
print()
print("💡 提示: 已为您准备好运行 simple_upload.py")
print()
