#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

os.chdir(r'e:\lab\台塑生醫旗艦館\FBEDM')

# 快速诊断
SOURCE_DIR = r"e:\lab\台塑生醫旗艦館\FBEDM\images"

print("="*80)
print("QUICK DIAGNOSIS")
print("="*80)

if os.path.exists(SOURCE_DIR):
    files = [f for f in os.listdir(SOURCE_DIR) if os.path.isfile(os.path.join(SOURCE_DIR, f)) and f!="Thumbs.db"]
    print(f"✓ Source directory exists: {len(files)} files found")
    
    by_ext = {}
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext:
            by_ext[ext] = by_ext.get(ext,0) + 1
    
    print("\nFile types:")
    for ext in sorted(by_ext.keys()):
        print(f"  {ext}: {by_ext[ext]}")
else:
    print("✗ Source directory not found")

print("\nToken status:")
token = os.environ.get('GITHUB_TOKEN')
if token:
    print(f"✓ GITHUB_TOKEN is set ({len(token)} chars)")
else:
    print("⚠ GITHUB_TOKEN not set - script will prompt for input")

print("\n" + "="*80)
print("Ready to execute simple_upload.py")
print("="*80)
