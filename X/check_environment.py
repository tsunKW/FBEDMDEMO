#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查脚本 - 验证上传前的准备
"""

import os
import sys
import subprocess

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"✓ Python 版本: {version.major}.{version.minor}.{version.micro} (满足要求 >= 3.6)")
        return True
    else:
        print(f"✗ Python 版本过旧: {version.major}.{version.minor}.{version.micro}")
        print("  需要: Python 3.6 或更高版本")
        return False

def check_requests_library():
    """检查 requests 库"""
    try:
        import requests
        print(f"✓ requests 库已安装 (版本: {requests.__version__})")
        return True
    except ImportError:
        print("✗ requests 库未安装")
        print("  安装方法: pip install requests")
        return False

def check_source_directory():
    """检查源目录"""
    source_dir = r"e:\lab\台塑生醫旗艦館\FBEDM\images"
    if os.path.exists(source_dir):
        files = [f for f in os.listdir(source_dir) if f != "Thumbs.db" and os.path.isfile(os.path.join(source_dir, f))]
        valid_files = [f for f in files if os.path.splitext(f)[1].lower() in {'.jpg', '.png', '.js', '.css', '.min.js', '.min.css'}]
        print(f"✓ 源目录存在: {source_dir}")
        print(f"  - 总文件数: {len(files)}")
        print(f"  - 有效文件: {len(valid_files)}")
        return True
    else:
        print(f"✗ 源目录不存在: {source_dir}")
        return False

def check_script_files():
    """检查必需的脚本文件"""
    scripts = [
        'upload_to_github.py',
        'upload_files_with_token.py',
        'upload.bat',
        'README_UPLOAD.md'
    ]
    
    missing = []
    for script in scripts:
        if os.path.exists(script):
            print(f"✓ {script} 存在")
        else:
            print(f"✗ {script} 缺失")
            missing.append(script)
    
    return len(missing) == 0

def check_network():
    """检查网络连接"""
    try:
        import requests
        response = requests.get('https://github.com', timeout=5)
        if response.status_code != 404:  # GitHub 可能返回不同状态码，但能连接就行
            print("✓ 网络连接正常 (可以访问 GitHub)")
            return True
    except:
        pass
    
    print("✗ 无法连接到 GitHub")
    print("  请检查网络连接")
    return False

def main():
    print("=" * 80)
    print("GitHub 文件上传 - 环境检查")
    print("=" * 80)
    print()
    
    checks = [
        ("Python 版本检查", check_python_version),
        ("Requests 库检查", check_requests_library),
        ("源目录检查", check_source_directory),
        ("脚本文件检查", check_script_files),
        ("网络连接检查", check_network),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ 检查失败: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 80)
    print("检查结果总结")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n总计: {passed}/{total} 检查通过")
    
    if passed == total:
        print("\n✅ 环境准备完成！可以开始上传。")
        print("\n推荐命令:")
        print("  upload.bat your_github_token_here")
        return 0
    else:
        print("\n⚠️ 检查失败，请根据上述提示修复问题后重试。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
