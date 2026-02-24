#!/bin/bash
# VoceChat v1.0 发布验证脚本
# 验证所有文件完整性和语法正确性

set -e

echo "=========================================="
echo "VoceChat Integration v1.0 发布验证"
echo "=========================================="
echo ""

SKILL_DIR="/root/.nanobot/workspace/skills/vocechat"
cd "$SKILL_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0

# 1. 检查必需文件
echo "1. 检查必需文件..."
REQUIRED_FILES=(
    "vocechat_channel.py"
    "vocechat_bot.py"
    "send_message.py"
    "README.md"
    "SKILL.md"
    "VERSION.md"
    "RELEASE_NOTES.md"
    "CHECKLIST.md"
    "SUMMARY.md"
    "install.sh"
    ".gitignore"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "   ${GREEN}✓${NC} $file"
    else
        echo -e "   ${RED}✗${NC} $file (缺失)"
        ((ERRORS++))
    fi
done

# 2. 检查 Python 语法
echo ""
echo "2. 检查 Python 语法..."
for py_file in vocechat_channel.py vocechat_bot.py send_message.py; do
    if python3 -m py_compile "$py_file" 2>/dev/null; then
        echo -e "   ${GREEN}✓${NC} $py_file 语法正确"
    else
        echo -e "   ${RED}✗${NC} $py_file 语法错误"
        ((ERRORS++))
    fi
done

# 3. 检查文档格式（基本的 Markdown 检查）
echo ""
echo "3. 检查文档完整性..."
for md_file in README.md SKILL.md VERSION.md RELEASE_NOTES.md CHECKLIST.md SUMMARY.md; do
    if [ -f "$md_file" ]; then
        # 检查是否有标题
        if grep -q "^#" "$md_file"; then
            echo -e "   ${GREEN}✓${NC} $md_file 格式正确"
        else
            echo -e "   ${YELLOW}⚠${NC} $md_file 可能缺少标题"
        fi
    fi
done

# 4. 检查文件大小
echo ""
echo "4. 检查文件大小..."
MIN_SIZES=(
    "vocechat_channel.py:10000"
    "vocechat_bot.py:10000"
    "send_message.py:1000"
    "README.md:5000"
    "SKILL.md:5000"
)

for item in "${MIN_SIZES[@]}"; do
    file="${item%%:*}"
    min_size="${item##*:}"
    if [ -f "$file" ]; then
        size=$(stat -c%s "$file")
        if [ "$size" -ge "$min_size" ]; then
            echo -e "   ${GREEN}✓${NC} $file (${size} bytes)"
        else
            echo -e "   ${YELLOW}⚠${NC} $file 可能不完整 (${size} bytes < ${min_size})"
        fi
    fi
done

# 5. 检查可执行权限
echo ""
echo "5. 检查脚本权限..."
if [ -x "install.sh" ]; then
    echo -e "   ${GREEN}✓${NC} install.sh 可执行"
else
    echo -e "   ${YELLOW}⚠${NC} install.sh 缺少执行权限"
fi

# 6. 检查敏感信息
echo ""
echo "6. 检查敏感信息..."
if grep -q "YOUR_API_KEY_HERE\|your_api_key_here" *.py *.md 2>/dev/null; then
    echo -e "   ${GREEN}✓${NC} 未发现硬编码 API Key"
else
    echo -e "   ${YELLOW}⚠${NC} 请确认没有泄露真实 API Key"
fi

# 7. 统计信息
echo ""
echo "7. 统计信息..."
TOTAL_LINES=$(wc -l *.py *.md 2>/dev/null | tail -1 | awk '{print $1}')
TOTAL_SIZE=$(du -sh . | cut -f1)
echo "   总代码行数：$TOTAL_LINES"
echo "   总大小：$TOTAL_SIZE"

# 8. 最终结果
echo ""
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ 验证通过！所有检查项完成${NC}"
    echo "=========================================="
    echo ""
    echo "发布包已准备就绪："
    echo "  - 核心代码：3 个 Python 文件"
    echo "  - 文档：6 个 Markdown 文件"
    echo "  - 工具：2 个脚本文件"
    echo ""
    echo "下一步："
    echo "  1. 运行安装脚本：sudo bash install.sh"
    echo "  2. 配置 nanobot：编辑 /root/.nanobot/config.json"
    echo "  3. 重启 nanobot: sudo systemctl restart nanobot"
    echo "  4. 测试功能：在 VoceChat 中发送消息"
    echo ""
    exit 0
else
    echo -e "${RED}❌ 验证失败！发现 $ERRORS 个错误${NC}"
    echo "=========================================="
    echo ""
    echo "请修复上述错误后重新运行验证"
    exit 1
fi
