#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 images 文件夹中的所有文件推送到 GitHub 仓库
使用 GitHub API v3 进行上传
"""

import os
import sys
import base64
import json
import time
import requests
from pathlib import Path
from datetime import datetime

# 配置
GITHUB_OWNER = "tsunKW"
GITHUB_REPO = "FBEDMDEMO"
TARGET_DIR = "images"
SOURCE_DIR = r"e:\lab\台塑生醫旗艦館\FBEDM\images"

# 获取 GitHub Token
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("⚠️  未找到 GITHUB_TOKEN 环境变量")
    print("请输入你的 GitHub Personal Access Token：")
    GITHUB_TOKEN = input().strip()
    if not GITHUB_TOKEN:
        print("❌ 无法继续，需要 GitHub Token")
        sys.exit(1)

# GitHub API 基础 URL
API_BASE = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents"

# 需要推送的文件类型
EXTENSIONS = {'.jpg', '.png', '.js', '.css', '.min.js', '.min.css'}

# 添加延迟以避免 API 限制
DELAY_BETWEEN_UPLOADS = 0.5  # 秒

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
            _, ext = os.path.splitext(file)
            if ext.lower() in EXTENSIONS:
                files.append((file, file_path))
    
    return sorted(files)

def is_binary_file(filename):
    """判断是否为二进制文件"""
    _, ext = os.path.splitext(filename.lower())
    return ext in {'.jpg', '.png'}

def get_file_sha(filename):
    """获取 GitHub 上该文件的 SHA"""
    url = f"{API_BASE}/{TARGET_DIR}/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get('sha')
    except Exception as e:
        pass
    
    return None

def upload_file(filename, file_path, retry_count=0, max_retries=3):
    """上传单个文件到 GitHub"""
    url = f"{API_BASE}/{TARGET_DIR}/{filename}"
    
    try:
        # 读取文件内容
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # 编码内容
        if is_binary_file(filename):
            content = base64.b64encode(file_content).decode('utf-8')
        else:
            content = file_content.decode('utf-8', errors='ignore')
        
        # 获取文件大小
        file_size_kb = len(file_content) / 1024
        
        # 获取该文件在 GitHub 上的 SHA
        sha = get_file_sha(filename)
        
        # 准备请求数据
        data = {
            "message": f"Upload {filename} via upload script",
            "content": content,
            "branch": "main"
        }
        
        if sha:
            data["sha"] = sha
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # 发送请求
        response = requests.put(url, json=data, headers=headers, timeout=30)
        
        if response.status_code in [200, 201]:
            status = "✓ 更新" if sha else "✓ 上传"
            print(f"{status}: {filename:40} ({file_size_kb:.1f} KB)")
            return True
        elif response.status_code == 422 and retry_count < max_retries:
            # 处理冲突 - 重试
            print(f"⚠️  冲突: {filename} (重试 {retry_count + 1}/{max_retries})")
            time.sleep(1)
            return upload_file(filename, file_path, retry_count + 1, max_retries)
        else:
            print(f"❌ 失败: {filename} (状态码: {response.status_code})")
            try:
                error_msg = response.json()
                error_text = error_msg.get('message', 'Unknown error')
                if error_msg.get('errors'):
                    error_text += " - " + str(error_msg['errors'])
                print(f"   错误: {error_text[:100]}")
            except:
                print(f"   响应: {response.text[:200]}")
            return False
    except FileNotFoundError:
        print(f"❌ 文件不存在: {filename}")
        return False
    except Exception as e:
        print(f"❌ 错误: {filename}")
        print(f"   {str(e)[:100]}")
        return False

def main():
    print("=" * 80)
    print("GitHub 图片和资源文件上传工具")
    print("=" * 80)
    print(f"\n📍 源目录: {SOURCE_DIR}")
    print(f"📍 GitHub 仓库: {GITHUB_OWNER}/{GITHUB_REPO}")
    print(f"📍 目标目录: {TARGET_DIR}/")
    if GITHUB_TOKEN:
        masked_token = GITHUB_TOKEN[:7] + "*" * (len(GITHUB_TOKEN) - 14) + GITHUB_TOKEN[-7:]
        print(f"📍 Token: {masked_token}")
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
    
    print("📊 文件类型分布:")
    for ext in sorted(by_type.keys()):
        print(f"  {ext:10} : {by_type[ext]:3} 个")
    
    print("\n" + "=" * 80)
    print("开始上传...\n")
    
    # 上传文件
    success_count = 0
    failed_count = 0
    failed_files = []
    
    for idx, (filename, file_path) in enumerate(files, 1):
        print(f"[{idx:2}/{len(files)}] ", end="")
        if upload_file(filename, file_path):
            success_count += 1
        else:
            failed_count += 1
            failed_files.append(filename)
        
        # 添加延迟以避免 API 限制
        if idx < len(files):
            time.sleep(DELAY_BETWEEN_UPLOADS)
    
    # 输出总结
    print("\n" + "=" * 80)
    print("上传完成！")
    print("=" * 80)
    print(f"✅ 成功: {success_count} 个文件")
    if failed_count > 0:
        print(f"❌ 失败: {failed_count} 个文件")
        if len(failed_files) <= 10:
            for f in failed_files:
                print(f"   - {f}")
        else:
            for f in failed_files[:5]:
                print(f"   - {f}")
            print(f"   ... 和其他 {len(failed_files) - 5} 个文件")
    print(f"📊 总计: {len(files)} 个文件")
    print()
    print("🔗 仓库链接:")
    print(f"   https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}")
    print()
    print("📂 查看上传的文件:")
    print(f"   https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/tree/main/{TARGET_DIR}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ 用户中断上传")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
