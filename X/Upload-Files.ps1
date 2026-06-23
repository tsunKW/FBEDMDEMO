# GitHub API 上传脚本 - PowerShell 版本

param(
    [string]$Token
)

# 配置
$GITHUB_OWNER = "tsunKW"
$GITHUB_REPO = "FBEDMDEMO"
$TARGET_DIR = "images"
$SOURCE_DIR = "e:\lab\台塑生醫旗艦館\FBEDM\images"

# 获取 Token
if (-not $Token) {
    if ($env:GITHUB_TOKEN) {
        $Token = $env:GITHUB_TOKEN
    } else {
        Write-Host "⚠️  未找到 GITHUB_TOKEN 环境变量" -ForegroundColor Yellow
        $Token = Read-Host "请输入 GitHub Personal Access Token"
    }
}

if (-not $Token) {
    Write-Host "❌ 无法继续，需要 GitHub Token" -ForegroundColor Red
    exit 1
}

$API_BASE = "https://api.github.com/repos/$GITHUB_OWNER/$GITHUB_REPO/contents"

# 文件列表
$FILES = @(
    "00LOGOA.png", "00LOGOB.png", "topBtn.png",
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
    "2000x450.jpg", "2000x450_DFS.jpg", "FBBG.jpg", "FBBGm.jpg",
    "Layout.css", "animate.min.css", "bootstrap.min.css", "bootstrap.bundle.js",
    "body.js", "jquery-3.6.0.min.js", "lazyload.min.js", "navlightN.css",
    "navlightN.js", "owl.carousel.min.js", "style_FB.css", "swiper.min.css",
    "swiper.min.js", "wow.min.js"
)

function ConvertTo-Base64 {
    param([byte[]]$Data)
    [Convert]::ToBase64String($Data)
}

function Get-FileContent {
    param([string]$FilePath)
    
    $bytes = [System.IO.File]::ReadAllBytes($FilePath)
    
    # 检查文件类型
    $ext = [System.IO.Path]::GetExtension($FilePath).ToLower()
    if ($ext -in @(".jpg", ".png")) {
        # 二进制文件
        return ConvertTo-Base64 -Data $bytes
    } else {
        # 文本文件
        $text = [System.Text.Encoding]::UTF8.GetString($bytes)
        $textBytes = [System.Text.Encoding]::UTF8.GetBytes($text)
        return ConvertTo-Base64 -Data $textBytes
    }
}

function Upload-File {
    param(
        [string]$FileName,
        [string]$FilePath
    )
    
    if (-not (Test-Path $FilePath)) {
        Write-Host "❌ 文件不存在: $FileName" -ForegroundColor Red
        return $false
    }
    
    try {
        $content = Get-FileContent -FilePath $FilePath
        $fileSize = (Get-Item $FilePath).Length / 1024
        
        $url = "$API_BASE/$TARGET_DIR/$FileName"
        $headers = @{
            "Authorization" = "token $Token"
            "Accept" = "application/vnd.github.v3+json"
        }
        
        $body = @{
            "message" = "Upload $FileName via PowerShell script"
            "content" = $content
            "branch" = "main"
        } | ConvertTo-Json
        
        $response = Invoke-WebRequest -Uri $url -Method PUT -Headers $headers -Body $body -ContentType "application/json" -ErrorAction SilentlyContinue
        
        if ($response.StatusCode -in @(200, 201)) {
            Write-Host "✓ 上传: $FileName ($('{0:F1}' -f $fileSize) KB)" -ForegroundColor Green
            return $true
        } else {
            Write-Host "❌ 失败: $FileName (状态码: $($response.StatusCode))" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "❌ 错误: $FileName" -ForegroundColor Red
        Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# 主程序
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "GitHub 文件上传工具 - PowerShell 版本" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 源目录: $SOURCE_DIR"
Write-Host "📍 GitHub: $GITHUB_OWNER/$GITHUB_REPO"
Write-Host "📍 目标目录: $TARGET_DIR/"
Write-Host "📦 总文件数: $($FILES.Count)"
Write-Host ""

$successCount = 0
$failedCount = 0

for ($i = 0; $i -lt $FILES.Count; $i++) {
    $file = $FILES[$i]
    $filePath = Join-Path $SOURCE_DIR $file
    
    Write-Host -NoNewline "[$($i + 1)/$($FILES.Count)] "
    
    if (Upload-File -FileName $file -FilePath $filePath) {
        $successCount++
    } else {
        $failedCount++
    }
    
    if ($i -lt $FILES.Count - 1) {
        Start-Sleep -Milliseconds 500
    }
}

# 总结
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "上传完成！" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "✅ 成功: $successCount 个文件" -ForegroundColor Green
Write-Host "❌ 失败: $failedCount 个文件" -ForegroundColor $(if ($failedCount -gt 0) { 'Red' } else { 'Green' })
Write-Host "📊 总计: $($FILES.Count) 个文件" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔗 仓库链接:" -ForegroundColor Cyan
Write-Host "   https://github.com/$GITHUB_OWNER/$GITHUB_REPO" -ForegroundColor Blue
Write-Host ""
Write-Host "📂 查看上传的文件:" -ForegroundColor Cyan
Write-Host "   https://github.com/$GITHUB_OWNER/$GITHUB_REPO/tree/main/$TARGET_DIR" -ForegroundColor Blue
Write-Host ""
