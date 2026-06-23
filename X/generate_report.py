#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的诊断报告生成脚本
"""

import os
import sys

# 设置工作目录
os.chdir(r'e:\lab\台塑生醫旗艦館\FBEDM')

SOURCE_DIR = r"e:\lab\台塑生醫旗艦館\FBEDM\images"
GITHUB_OWNER = "tsunKW"
GITHUB_REPO = "FBEDMDEMO"

report = []

def add_line(text=""):
    report.append(text)
    print(text)

add_line("=" * 80)
add_line("🚀 GitHub 文件上传工具 - 执行诊断报告")
add_line("=" * 80)
add_line()

# ========== 1. 环境检查 ==========
add_line("1️⃣  系统环境检查")
add_line("-" * 80)

# Python 版本
python_version = sys.version
add_line(f"   Python 版本: {python_version.split()[0]}")

# 工作目录
add_line(f"   工作目录: {os.getcwd()}")

# simple_upload.py 是否存在
script_path = os.path.join(os.getcwd(), 'simple_upload.py')
if os.path.exists(script_path):
    add_line(f"   ✓ simple_upload.py 存在")
else:
    add_line(f"   ✗ simple_upload.py 不存在")

add_line()

# ========== 2. 源目录检查 ==========
add_line("2️⃣  源目录和文件检查")
add_line("-" * 80)

add_line(f"   源目录: {SOURCE_DIR}")

if os.path.exists(SOURCE_DIR):
    add_line(f"   ✓ 源目录存在")
    
    # 获取文件列表
    all_items = os.listdir(SOURCE_DIR)
    files = [f for f in all_items if os.path.isfile(os.path.join(SOURCE_DIR, f))]
    
    add_line(f"   文件总数: {len(files)} 个")
    
    # 统计文件类型
    by_ext = {}
    total_size = 0
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext:
            by_ext[ext] = by_ext.get(ext, 0) + 1
        
        file_path = os.path.join(SOURCE_DIR, f)
        total_size += os.path.getsize(file_path)
    
    add_line()
    add_line("   📊 文件类型分布:")
    for ext in sorted(by_ext.keys()):
        count = by_ext[ext]
        add_line(f"      {ext:10}: {count:3} 个")
    
    add_line()
    add_line(f"   📦 总大小: {total_size / (1024*1024):.2f} MB")
    
else:
    add_line(f"   ✗ 源目录不存在")

add_line()

# ========== 3. GitHub 配置 ==========
add_line("3️⃣  GitHub 上传配置")
add_line("-" * 80)

add_line(f"   仓库所有者: {GITHUB_OWNER}")
add_line(f"   仓库名称: {GITHUB_REPO}")
add_line(f"   目标目录: images/")
add_line(f"   API 端点: https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents")
add_line()

# ========== 4. 认证检查 ==========
add_line("4️⃣  GitHub 认证检查")
add_line("-" * 80)

token = os.environ.get('GITHUB_TOKEN')
if token:
    add_line(f"   ✓ GITHUB_TOKEN 环境变量已设置")
    add_line(f"   Token 前缀: {token[:6]}...")
    add_line(f"   Token 长度: {len(token)} 字符")
else:
    add_line(f"   ⚠️  GITHUB_TOKEN 环境变量未设置")
    add_line(f"   说明: 脚本运行时会提示用户手动输入")

add_line()

# ========== 5. 脚本分析 ==========
add_line("5️⃣  simple_upload.py 脚本分析")
add_line("-" * 80)

# 读取脚本内容分析
try:
    with open(script_path, 'r', encoding='utf-8') as f:
        script_content = f.read()
    
    # 统计函数数量
    import re
    functions = re.findall(r'def\s+(\w+)\s*\(', script_content)
    add_line(f"   脚本函数: {', '.join(functions)}")
    add_line(f"   代码行数: {len(script_content.splitlines())}")
    
except Exception as e:
    add_line(f"   ✗ 无法读取脚本: {e}")

add_line()

# ========== 6. 上传流程预览 ==========
add_line("6️⃣  预期上传流程")
add_line("-" * 80)

add_line("   ✓ 获取 GitHub Token（环境变量或用户输入）")
add_line("   ✓ 扫描源目录中的所有文件")
add_line(f"   ✓ 将 {len(files) if os.path.exists(SOURCE_DIR) else '?'} 个文件准备上传")
add_line("   ✓ 为每个文件进行 Base64 编码（对于二进制文件）")
add_line("   ✓ 通过 GitHub API 上传文件")
add_line("   ✓ 显示上传进度和结果统计")

add_line()

# ========== 7. 后续步骤 ==========
add_line("7️⃣  执行上传的方式")
add_line("-" * 80)

add_line("   方式 A: 交互式运行（推荐）")
add_line("      python simple_upload.py")
add_line("      # 脚本会提示输入 GitHub Token")
add_line()

add_line("   方式 B: 设置环境变量后运行")
add_line("      set GITHUB_TOKEN=your_token_here")
add_line("      python simple_upload.py")
add_line()

add_line("   方式 C: 使用命令行工具")
add_line("      python upload_files_with_token.py ghp_xxx...")
add_line()

# ========== 8. 信息总结 ==========
add_line("=" * 80)
add_line("✅ 诊断报告完成")
add_line("=" * 80)
add_line()

add_line("📝 关键信息总结:")
if os.path.exists(SOURCE_DIR):
    add_line(f"   • 需上传文件: {len(files)} 个")
    add_line(f"   • 总数据量: {total_size / (1024*1024):.2f} MB")
else:
    add_line(f"   • 源目录不存在")

add_line(f"   • 目标仓库: https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}")
add_line(f"   • Token 状态: {'✓ 已设置' if token else '⚠️  需要输入'}")

add_line()

add_line("🚀 现在您可以运行 simple_upload.py 开始上传文件")
add_line()

# 保存报告
report_text = "\n".join(report)

print("\n")
print("报告已生成。现在显示简要信息：")
print()
