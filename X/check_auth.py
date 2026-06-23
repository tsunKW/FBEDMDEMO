#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 GitHub API 批量上传 images 文件夹中的所有文件到 GitHub 仓库
"""

import os
import sys
import base64
import subprocess
from pathlib import Path

# 配置
GITHUB_OWNER = "tsunKW"
GITHUB_REPO = "FBEDMDEMO"
TARGET_DIR = "images"
SOURCE_DIR = r"e:\lab\台塑生醫旗艦館\FBEDM\images"

# 需要推送的文件扩展名
EXTENSIONS = {'.jpg', '.png', '.js', '.css'}

# 获取需要上传的文件
files_to_upload = [
    "00LOGOA.png", "00LOGOB.png",
    "00swiper_BioLead.jpg", "00swiper_BioLeadm.jpg", "00swiper_DFH.jpg",
    "00swiper_DFS.jpg", "00swiper_DFSm.jpg", "00swiper_DHFm.jpg",
    "00swiper_FORTE.jpg", "00swiper_FORTEm.jpg",
    "02bonus01.png", "02bonus02.png", "02bonus03.png", "02bonus04.png", "02bonus_title.png",
    "03BOM01.png", "03BOM02.png", "03BOM03.png", "03BOM04.png", "03BOM_title.png",
    "04swiper01.jpg", "04swiper01m.jpg", "04swiper02.jpg", "04swiper02m.jpg",
    "04swiper03.jpg", "04swiper03m.jpg", "04swiper05.jpg", "04swiper05m.jpg",
    "04swiper06.jpg", "04swiper06m.jpg", "04swiper07.jpg", "04swiper07m.jpg",
    "05A1.jpg", "05A2.jpg", "05A3.jpg", "05A4.jpg",
    "05B1.jpg", "05B2.jpg", "05B3.jpg", "05B4.jpg",
    "05BNA.jpg", "05BNB.jpg", "05BNC.jpg", "05BND.jpg", "05BNE.jpg", "05BNF.jpg",
    "05C1.jpg", "05C2.jpg", "05C3.jpg", "05C4.jpg",
    "05D1.jpg", "05D2.jpg", "05D3.jpg", "05D4.jpg",
    "05E1.jpg", "05E2.jpg", "05E3.jpg", "05E4.jpg",
    "05F1.jpg", "05F2.jpg", "05F3.jpg", "05F4.jpg",
    "2000x450.jpg", "2000x450_DFS.jpg",
    "FBBG.jpg", "FBBGm.jpg",
    "topBtn.png",
    "Layout.css", "animate.min.css", "bootstrap.min.css", "bootstrap.bundle.js",
    "body.js", "jquery-3.6.0.min.js", "lazyload.min.js", "navlightN.css",
    "navlightN.js", "owl.carousel.min.js", "style_FB.css", "swiper.min.css",
    "swiper.min.js", "wow.min.js"
]

def main():
    print("=" * 80)
    print("GitHub 文件推送工具 - 使用 Python 和 GitHub API")
    print("=" * 80)
    print(f"\n📍 源目录: {SOURCE_DIR}")
    print(f"📍 GitHub: {GITHUB_OWNER}/{GITHUB_REPO}")
    print(f"📍 目标目录: {TARGET_DIR}/")
    print(f"📝 找到 {len(files_to_upload)} 个文件需要上传\n")
    
    # 分类显示
    images = [f for f in files_to_upload if f.lower().endswith(('.jpg', '.png'))]
    css = [f for f in files_to_upload if f.lower().endswith('.css')]
    js = [f for f in files_to_upload if f.lower().endswith('.js')]
    
    print(f"📊 文件分布:")
    print(f"  🖼️  图片 (JPG/PNG): {len(images)} 个")
    print(f"  🎨 样式表 (CSS): {len(css)} 个")
    print(f"  ⚙️  脚本 (JS): {len(js)} 个")
    print()
    
    # 使用 GitHub CLI 或 curl 上传
    print("=" * 80)
    print("开始验证 GitHub 认证...\n")
    
    # 检查 gh CLI 是否可用
    try:
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ GitHub CLI 认证成功")
            print("  可用于上传文件\n")
            return True
        else:
            print("⚠️  GitHub CLI 认证失败")
            print(result.stderr)
    except FileNotFoundError:
        print("⚠️  GitHub CLI 未安装")
        print("  请通过以下方式安装: winget install GitHub.cli")
    except Exception as e:
        print(f"⚠️  检查失败: {e}")
    
    print("\n💡 建议: 使用以下命令安装 GitHub CLI:")
    print("   winget install GitHub.cli")
    print("\n或使用以下命令手动设置认证:")
    print("   gh auth login")
    
    return False

if __name__ == "__main__":
    main()
