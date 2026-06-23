#!/bin/bash

# GitHub API 上传脚本
# 使用 curl 和 base64 上传文件到 GitHub

GITHUB_OWNER="tsunKW"
GITHUB_REPO="FBEDMDEMO"
TARGET_DIR="images"
SOURCE_DIR="e:\\lab\\台塑生醫旗艦館\\FBEDM\\images"

# 获取 GitHub Token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  未找到 GITHUB_TOKEN 环境变量"
    read -p "请输入 GitHub Personal Access Token: " GITHUB_TOKEN
    if [ -z "$GITHUB_TOKEN" ]; then
        echo "❌ 无法继续，需要 GitHub Token"
        exit 1
    fi
fi

API_BASE="https://api.github.com/repos/$GITHUB_OWNER/$GITHUB_REPO/contents"

# 文件列表
declare -a FILES=(
    "00LOGOA.png" "00LOGOB.png" "topBtn.png"
    "00swiper_BioLead.jpg" "00swiper_BioLeadm.jpg" "00swiper_DFH.jpg"
    "00swiper_DFS.jpg" "00swiper_DFSm.jpg" "00swiper_DHFm.jpg"
    "00swiper_FORTE.jpg" "00swiper_FORTEm.jpg"
    "02bonus01.png" "02bonus02.png" "02bonus03.png" "02bonus04.png" "02bonus_title.png"
    "03BOM01.png" "03BOM02.png" "03BOM03.png" "03BOM04.png" "03BOM_title.png"
    "04swiper01.jpg" "04swiper01m.jpg" "04swiper02.jpg" "04swiper02m.jpg"
    "04swiper03.jpg" "04swiper03m.jpg" "04swiper05.jpg" "04swiper05m.jpg"
    "04swiper06.jpg" "04swiper06m.jpg" "04swiper07.jpg" "04swiper07m.jpg"
    "05A1.jpg" "05A2.jpg" "05A3.jpg" "05A4.jpg"
    "05B1.jpg" "05B2.jpg" "05B3.jpg" "05B4.jpg"
    "05BNA.jpg" "05BNB.jpg" "05BNC.jpg" "05BND.jpg" "05BNE.jpg" "05BNF.jpg"
    "05C1.jpg" "05C2.jpg" "05C3.jpg" "05C4.jpg"
    "05D1.jpg" "05D2.jpg" "05D3.jpg" "05D4.jpg"
    "05E1.jpg" "05E2.jpg" "05E3.jpg" "05E4.jpg"
    "05F1.jpg" "05F2.jpg" "05F3.jpg" "05F4.jpg"
    "2000x450.jpg" "2000x450_DFS.jpg" "FBBG.jpg" "FBBGm.jpg"
    "Layout.css" "animate.min.css" "bootstrap.min.css" "bootstrap.bundle.js"
    "body.js" "jquery-3.6.0.min.js" "lazyload.min.js" "navlightN.css"
    "navlightN.js" "owl.carousel.min.js" "style_FB.css" "swiper.min.css"
    "swiper.min.js" "wow.min.js"
)

echo "========================================================================"
echo "GitHub 文件上传工具"
echo "========================================================================"
echo ""
echo "📍 源目录: $SOURCE_DIR"
echo "📍 GitHub: $GITHUB_OWNER/$GITHUB_REPO"
echo "📍 目标目录: $TARGET_DIR/"
echo "📦 总文件数: ${#FILES[@]}"
echo ""

SUCCESS_COUNT=0
FAILED_COUNT=0

for FILE in "${FILES[@]}"; do
    FILE_PATH="$SOURCE_DIR/$FILE"
    URL="$API_BASE/$TARGET_DIR/$FILE"
    
    # 检查文件是否存在
    if [ ! -f "$FILE_PATH" ]; then
        echo "❌ 文件不存在: $FILE"
        ((FAILED_COUNT++))
        continue
    fi
    
    # 获取文件大小
    FILE_SIZE=$(stat -c%s "$FILE_PATH" 2>/dev/null || stat -f%z "$FILE_PATH" 2>/dev/null)
    FILE_SIZE_KB=$((FILE_SIZE / 1024))
    
    # 检查文件类型
    if [[ $FILE == *.jpg ]] || [[ $FILE == *.png ]]; then
        # 二进制文件 - Base64 编码
        CONTENT=$(base64 -w 0 "$FILE_PATH")
    else
        # 文本文件
        CONTENT=$(cat "$FILE_PATH" | base64 -w 0)
    fi
    
    # 准备 JSON 数据
    JSON_DATA=$(cat <<EOF
{
  "message": "Upload $FILE via upload script",
  "content": "$CONTENT",
  "branch": "main"
}
EOF
)
    
    # 上传文件
    RESPONSE=$(curl -s -X PUT \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "$JSON_DATA" \
        "$URL")
    
    # 检查响应
    if echo "$RESPONSE" | grep -q "\"sha\""; then
        echo "✓ 上传: $FILE (${FILE_SIZE_KB} KB)"
        ((SUCCESS_COUNT++))
    else
        echo "❌ 失败: $FILE"
        ((FAILED_COUNT++))
    fi
    
    # 延迟以避免 API 限制
    sleep 0.5
done

echo ""
echo "========================================================================"
echo "上传完成！"
echo "========================================================================"
echo "✅ 成功: $SUCCESS_COUNT 个文件"
echo "❌ 失败: $FAILED_COUNT 个文件"
echo "📊 总计: ${#FILES[@]} 个文件"
echo ""
echo "🔗 仓库链接: https://github.com/$GITHUB_OWNER/$GITHUB_REPO"
echo "📂 查看文件: https://github.com/$GITHUB_OWNER/$GITHUB_REPO/tree/main/$TARGET_DIR"
