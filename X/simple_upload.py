#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接上传文件到 GitHub 的 Python 脚本
"""

import os
import sys
import base64
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

# 配置
GITHUB_OWNER = "tsunKW"
GITHUB_REPO = "FBEDMDEMO"
TARGET_DIR = "images"
SOURCE_DIR = r"e:\lab\台塑生醫旗艦館\FBEDM\images"

def get_github_token():
    """获取 GitHub Token"""
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        return token
    
    print("⚠️  未找到 GITHUB_TOKEN 环境变量")
    print("请输入你的 GitHub Personal Access Token：")
    try:
        token = input().strip()
        if not token:
            print("❌ 无法继续，需要 GitHub Token")
            sys.exit(1)
        return token
    except KeyboardInterrupt:
        print("\n❌ 用户中断")
        sys.exit(1)

def get_files_to_upload():
    """获取需要上传的文件列表"""
    files = []
    
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ 源目录不存在: {SOURCE_DIR}")
        return files
    
    try:
        for file in os.listdir(SOURCE_DIR):
            if file == "Thumbs.db":
                continue
            
            file_path = os.path.join(SOURCE_DIR, file)
            if os.path.isfile(file_path):
                files.append((file, file_path))
        
        return sorted(files)
    except Exception as e:
        print(f"❌ 读取目录出错: {e}")
        return files

def is_binary_file(filename):
    """判断是否为二进制文件"""
    ext = os.path.splitext(filename.lower())[1]
    return ext in {'.jpg', '.png'}

def upload_file(filename, file_path, token, api_base):
    """上传单个文件到 GitHub"""
    url = f"{api_base}/{TARGET_DIR}/{filename}"
    
    try:
        # 读取文件内容
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # 编码内容
        if is_binary_file(filename):
            content = base64.b64encode(file_content).decode('utf-8')
        else:
            try:
                content = file_content.decode('utf-8')
            except:
                content = base64.b64encode(file_content).decode('utf-8')
            content = base64.b64encode(file_content.decode('utf-8', errors='ignore').encode('utf-8')).decode('utf-8')
        
        # 获取文件大小
        file_size_kb = len(file_content) / 1024
        
        # 准备请求数据
        data = {
            "message": f"Upload {filename} via Python script",
            "content": content,
            "branch": "main"
        }
        
        body = json.dumps(data).encode('utf-8')
        
        # 创建请求
        req = urllib.request.Request(url, data=body, method='PUT')
        req.add_header('Authorization', f'token {token}')
        req.add_header('Accept', 'application/vnd.github.v3+json')
        req.add_header('Content-Type', 'application/json')
        
        # 发送请求
        try:
            response = urllib.request.urlopen(req, timeout=30)
            status_code = response.status
            
            if status_code in [200, 201]:
                print(f"✓ 上传: {filename:40} ({file_size_kb:.1f} KB)")
                return True
            else:
                print(f"❌ 失败: {filename} (状态码: {status_code})")
                return False
        except urllib.error.HTTPError as e:
            if e.code in [200, 201]:
                print(f"✓ 上传: {filename:40} ({file_size_kb:.1f} KB)")
                return True
            else:
                print(f"❌ 失败: {filename} (状态码: {e.code})")
                try:
                    error_msg = json.loads(e.read().decode('utf-8'))
                    print(f"   错误: {error_msg.get('message', 'Unknown error')}")
                except:
                    pass
                return False
    except FileNotFoundError:
        print(f"❌ 文件不存在: {filename}")
        return False
    except Exception as e:
        print(f"❌ 错误: {filename}")
        print(f"   {str(e)[:100]}")
        return False

def main():
    # 获取 Token
    token = get_github_token()
    api_base = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents"
    
    print("=" * 80)
    print("GitHub 文件上传工具")
    print("=" * 80)
    print(f"\n📍 源目录: {SOURCE_DIR}")
    print(f"📍 GitHub: {GITHUB_OWNER}/{GITHUB_REPO}")
    print(f"📍 目标目录: {TARGET_DIR}/")
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
        print(f"[{idx:2}/{len(files)}] ", end="", flush=True)
        if upload_file(filename, file_path, token, api_base):
            success_count += 1
        else:
            failed_count += 1
            failed_files.append(filename)
        
        # 延迟以避免 API 限制
        if idx < len(files):
            time.sleep(0.5)
    
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
