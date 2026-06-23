#!/usr/bin/env python3
import subprocess
import sys
import os

os.chdir(r'e:\lab\台塑生醫旗艦館\FBEDM')

# 直接调用 Python 执行 simple_upload.py
result = subprocess.run([sys.executable, 'simple_upload.py'], 
                       cwd=r'e:\lab\台塑生醫旗艦館\FBEDM',
                       capture_output=False,
                       text=True)

sys.exit(result.returncode)
