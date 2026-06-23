#!/usr/bin/env python3
import os

SOURCE_DIR = r"e:\lab\台塑生醫旗艦館\FBEDM\images"
files = []

if os.path.exists(SOURCE_DIR):
    for file in os.listdir(SOURCE_DIR):
        if file == "Thumbs.db":
            continue
        file_path = os.path.join(SOURCE_DIR, file)
        if os.path.isfile(file_path):
            files.append(file)

print(f"Total files: {len(files)}")
print("\nFirst 20 files:")
for f in sorted(files)[:20]:
    print(f"  {f}")

if len(files) > 20:
    print(f"\n  ... and {len(files) - 20} more files")
