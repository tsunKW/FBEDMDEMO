@echo off
REM GitHub 文件上传批处理脚本
REM 使用方法: run_upload.bat <github_token>

setlocal enabledelayedexpansion

if "%1"=="" (
    echo.
    echo ================================
    echo GitHub 文件上传工具
    echo ================================
    echo.
    echo 使用方法: run_upload.bat ^<github_token^>
    echo.
    echo 示例: run_upload.bat ghp_xxxxxxxxxxxxxxxxxxxx
    echo.
    echo 获取 Token:
    echo   1. 访问 https://github.com/settings/tokens
    echo   2. 点击 "Generate new token"
    echo   3. 选择 "Generate new token (classic)"
    echo   4. 勾选 "repo" 和 "workflow" 权限
    echo   5. 生成 Token 并复制
    echo.
    pause
    exit /b 1
)

set GITHUB_TOKEN=%1

echo.
echo 开始上传...
echo.

cd /d "%~dp0"
python upload_files_with_token.py %GITHUB_TOKEN%

pause
