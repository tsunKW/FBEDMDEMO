#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 images 文件夹中的所有文件推送到 GitHub 仓库
"""

import os
import base64
import requests
import json
from pathlib import Path
from datetime import datetime

# 配置
GITHUB_OWNER = "tsunKW"
GITHUB_REPO = "FBEDMDEMO"
TARGET_DIR = "images"
SOURCE_DIR = r"e:\lab\台塑生醫旗艦館\FBEDM\images"

# 获取 GitHub Token (从环境变量或提示输入)
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("⚠️  未找到 GITHUB_TOKEN 环境变量")
    print("请输入你的 GitHub Personal Access Token（或按 Enter 跳过）:")
    GITHUB_TOKEN = input().strip()
    if not GITHUB_TOKEN:
        print("❌ 无法继续，需要 GitHub Token")
        exit(1)

# GitHub API 基础 URL
API_BASE = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents"

# 需要推送的文件类型
EXTENSIONS = {'.jpg', '.png', '.js', '.css', '.min.js', '.min.css'}

def get_files_to_upload():
    """获取需要上传的文件列表"""
    files = []
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ 源目录不存在: {SOURCE_DIR}")
        return files
    
    for file in os.listdir(SOURCE_DIR):
        if file == "Thumbs.db":
            continue
        
        file_path = os.path.join(SOURCE_DIR, file)
        if os.path.isfile(file_path):
            # 检查文件扩展名
            _, ext = os.path.splitext(file)
            if ext.lower() in EXTENSIONS:
                files.append((file, file_path))
    
    return sorted(files)

def is_binary_file(filename):
    """判断是否为二进制文件"""
    _, ext = os.path.splitext(filename.lower())
    return ext in {'.jpg', '.png'}

def get_file_sha(filename):
    """获取 GitHub 上该文件的 SHA（如果存在）"""
    url = f"{API_BASE}/{TARGET_DIR}/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get('sha')
    except:
        pass
    
    return None

def upload_file(filename, file_path):
    """上传单个文件到 GitHub"""
    url = f"{API_BASE}/{TARGET_DIR}/{filename}"
    
    # 读取文件内容
    with open(file_path, 'rb') as f:
        file_content = f.read()
    
    # 编码内容
    if is_binary_file(filename):
        content = base64.b64encode(file_content).decode('utf-8')
    else:
        content = file_content.decode('utf-8')
    
    # 获取文件大小
    file_size_kb = len(file_content) / 1024
    
    # 获取该文件在 GitHub 上的 SHA（用于更新）
    sha = get_file_sha(filename)
    
    # 准备请求数据
    data = {
        "message": f"Upload {filename} via script",
        "content": content,
        "branch": "main"
    }
    
    if sha:
        data["sha"] = sha
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.put(url, json=data, headers=headers, timeout=30)
        
        if response.status_code in [200, 201]:
            status = "✓ 更新" if sha else "✓ 上传"
            print(f"{status}: {filename:40} ({file_size_kb:.1f} KB)")
            return True
        else:
            print(f"❌ 失败: {filename} (状态码: {response.status_code})")
            try:
                error_msg = response.json()
                print(f"   错误信息: {error_msg.get('message', 'Unknown error')}")
            except:
                print(f"   响应: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ 错误: {filename}")
        print(f"   {str(e)}")
        return False

def main():
    print("=" * 70)
    print("GitHub 图片文件推送工具")
    print("=" * 70)
    print(f"\n📍 源目录: {SOURCE_DIR}")
    print(f"📍 GitHub: {GITHUB_OWNER}/{GITHUB_REPO}")
    print(f"📍 目标目录: {TARGET_DIR}/")
    if GITHUB_TOKEN:
        print(f"📍 Token: {GITHUB_TOKEN[:10]}...")
    else:
        print("⚠️  未设置 Token")
    print()
    
    # 获取文件列表
    files = get_files_to_upload()
    
    if not files:
        print("❌ 没有找到需要上传的文件")
        return
    
    print(f"📦 找到 {len(files)} 个文件\n")
    
    # 按类型分类显示
    by_type = {}
    for filename, _ in files:
        ext = os.path.splitext(filename)[1].lower()
        if ext not in by_type:
            by_type[ext] = 0
        by_type[ext] += 1
    
    print("文件类型分布:")
    for ext in sorted(by_type.keys()):
        print(f"  {ext:10} : {by_type[ext]:3} 个")
    
    print("\n" + "=" * 70)
    print("开始上传...\n")
    
    # 上传文件
    success_count = 0
    failed_count = 0
    
    for filename, file_path in files:
        if upload_file(filename, file_path):
            success_count += 1
        else:
            failed_count += 1
    
    print("\n" + "=" * 70)
    print("上传完成！")
    print("=" * 70)
    print(f"✓ 成功: {success_count} 个文件")
    print(f"❌ 失败: {failed_count} 个文件")
    print(f"📊 总计: {len(files)} 个文件")
    print(f"🔗 仓库链接: https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}")
    print()

if __name__ == "__main__":
    main()
