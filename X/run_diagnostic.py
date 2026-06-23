#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行诊断并执行 simple_upload.py
这个脚本会先检查所有前置条件，然后运行上传脚本
"""

import os
import sys
import subprocess

# 更改工作目录
work_dir = r'e:\lab\台塑生醫旗艦館\FBEDM'
os.chdir(work_dir)
sys.path.insert(0, work_dir)

print("\n" + "=" * 80)
print("GitHub 文件上传工具 - 完整诊断和执行")
print("=" * 80 + "\n")

# ============ 诊断部分 ============

SOURCE_DIR = r"e:\lab\台塑生醫旗艦館\FBEDM\images"

# 检查源目录
print("📍 源目录检查:")
if os.path.exists(SOURCE_DIR):
    files = [f for f in os.listdir(SOURCE_DIR) if os.path.isfile(os.path.join(SOURCE_DIR, f)) and f != "Thumbs.db"]
    print(f"   ✓ 存在，包含 {len(files)} 个文件\n")
else:
    print(f"   ✗ 不存在：{SOURCE_DIR}\n")
    sys.exit(1)

# 文件类型统计
print("📊 文件类型统计:")
by_ext = {}
for f in files:
    ext = os.path.splitext(f)[1].lower()
    if ext:
        by_ext[ext] = by_ext.get(ext, 0) + 1
for ext in sorted(by_ext.keys()):
    print(f"   {ext:8}: {by_ext[ext]:3} 个")
print()

# GitHub 配置
print("🔧 上传配置:")
print(f"   仓库: tsunKW/FBEDMDEMO")
print(f"   目标: images/ 文件夹\n")

# Token 检查
print("🔐 认证检查:")
token = os.environ.get('GITHUB_TOKEN')
if token:
    print(f"   ✓ GITHUB_TOKEN 已设置\n")
    use_env_token = True
else:
    print(f"   ⚠️  GITHUB_TOKEN 未设置（脚本会提示输入）\n")
    use_env_token = False

print("=" * 80)
print("现在执行 simple_upload.py...")
print("=" * 80 + "\n")

# ============ 执行部分 ============

try:
    # 直接调用 simple_upload.py 中的 main 函数
    import importlib.util
    spec = importlib.util.spec_from_file_location("simple_upload", 
                                                   os.path.join(work_dir, "simple_upload.py"))
    simple_upload = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(simple_upload)
    
    # 运行主函数
    simple_upload.main()
    
except KeyboardInterrupt:
    print("\n❌ 用户中断")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ 发生错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
