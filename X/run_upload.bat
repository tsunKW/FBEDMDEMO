@echo off
REM 设置编码为 UTF-8
chcp 65001 >nul

cd /d "e:\lab\台塑生醫旗艦館\FBEDM"

REM 检查 Python 是否可用
where python >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装或不在 PATH 中
    exit /b 1
)

REM 运行上传脚本
echo 正在启动文件上传...
echo.
python upload_to_github.py

if errorlevel 1 (
    echo.
    echo ❌ 上传过程中出现错误
    exit /b 1
)

echo.
echo ✓ 上传脚本执行完成
pause
