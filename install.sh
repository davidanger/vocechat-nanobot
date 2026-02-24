#!/bin/bash
# VoceChat Integration v1.0 安装脚本
# 自动配置 VoceChat 通道到 nanobot

set -e

echo "=========================================="
echo "VoceChat Integration v1.0 安装脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否以 root 运行
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}错误：请以 root 用户运行此脚本${NC}"
    exit 1
fi

# 检查 nanobot 是否已安装
if ! command -v nanobot &> /dev/null; then
    echo -e "${RED}错误：nanobot 未安装${NC}"
    echo "请先安装 nanobot: https://github.com/nanobot-ai/nanobot"
    exit 1
fi

echo -e "${GREEN}✓ nanobot 已安装${NC}"

# 检查 VoceChat 技能目录
SKILL_DIR="/root/.nanobot/workspace/skills/vocechat"
if [ ! -d "$SKILL_DIR" ]; then
    echo -e "${RED}错误：VoceChat 技能目录不存在${NC}"
    echo "请确保技能文件已下载到：$SKILL_DIR"
    exit 1
fi

echo -e "${GREEN}✓ VoceChat 技能目录存在${NC}"

# 检查配置文件
CONFIG_FILE="/root/.nanobot/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}警告：nanobot 配置文件不存在${NC}"
    echo "将创建默认配置文件..."
    mkdir -p /root/.nanobot
    cat > "$CONFIG_FILE" << 'EOF'
{
  "channels": {
    "telegram": {
      "enabled": false
    },
    "vocechat": {
      "enabled": true,
      "serverUrl": "https://vc.fn.lssv.cc:8443",
      "apiKey": "YOUR_API_KEY_HERE",
      "botId": "YOUR_BOT_ID",
      "webhookPort": 8080,
      "allowFrom": []
    }
  },
  "providers": {
    "custom": {}
  }
}
EOF
    echo -e "${GREEN}✓ 已创建默认配置文件${NC}"
    echo -e "${YELLOW}请编辑 $CONFIG_FILE 并填入你的 VoceChat API Key 和 Bot ID${NC}"
    echo ""
fi

# 检查配置是否已包含 vocechat
if grep -q "vocechat" "$CONFIG_FILE"; then
    echo -e "${GREEN}✓ VoceChat 通道已在配置文件中${NC}"
else
    echo -e "${YELLOW}警告：配置文件中未找到 VoceChat 配置${NC}"
    echo "正在添加 VoceChat 配置..."
    
    # 备份原配置
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d%H%M%S)"
    echo -e "${GREEN}✓ 已备份原配置文件${NC}"
    
    # 这里可以添加自动插入配置的逻辑
    # 为安全起见，建议手动编辑
    echo -e "${YELLOW}请手动编辑 $CONFIG_FILE 添加 VoceChat 配置${NC}"
fi

# 检查端口占用
WEBHOOK_PORT=8080
if ss -tlnp | grep -q ":$WEBHOOK_PORT "; then
    echo -e "${YELLOW}警告：端口 $WEBHOOK_PORT 已被占用${NC}"
    echo "占用进程:"
    ss -tlnp | grep ":$WEBHOOK_PORT "
    echo ""
    echo -e "${YELLOW}如果需要，请修改配置文件中的 webhookPort${NC}"
else
    echo -e "${GREEN}✓ 端口 $WEBHOOK_PORT 可用${NC}"
fi

# 检查 Python 依赖
echo ""
echo "检查 Python 依赖..."
python3 -c "import requests" 2>/dev/null && echo -e "${GREEN}✓ requests 已安装${NC}" || echo -e "${YELLOW}⚠ requests 未安装${NC}"
python3 -c "import loguru" 2>/dev/null && echo -e "${GREEN}✓ loguru 已安装${NC}" || echo -e "${YELLOW}⚠ loguru 未安装${NC}"

# 提供配置说明
echo ""
echo "=========================================="
echo "配置说明"
echo "=========================================="
echo ""
echo "1. 在 VoceChat 服务器创建 Bot:"
echo "   - 访问你的 VoceChat 服务器管理面板"
echo "   - 进入 Settings => Bot&Webhook"
echo "   - 点击 New 创建 Bot"
echo "   - 创建 API Key 并保存"
echo ""
echo "2. 编辑配置文件:"
echo "   nano $CONFIG_FILE"
echo ""
echo "3. 填入以下信息:"
echo '   "vocechat": {'
echo '     "enabled": true,'
echo '     "serverUrl": "https://your-vocechat-server.com",'
echo '     "apiKey": "your_api_key_here",'
echo '     "botId": "your_bot_id",'
echo '     "webhookPort": 8080,'
echo '     "allowFrom": []'
echo '   }'
echo ""
echo "4. 重启 nanobot:"
echo "   sudo systemctl restart nanobot"
echo ""
echo "5. 验证运行:"
echo "   ps aux | grep nanobot"
echo "   ss -tlnp | grep 8080"
echo "   tail -f /tmp/vocechat_webhook.log"
echo ""

# 提供测试命令
echo "=========================================="
echo "测试命令"
echo "=========================================="
echo ""
echo "# 测试 Webhook 服务器"
echo "curl http://localhost:8080/"
echo ""
echo "# 测试 API 连接"
echo "curl -H \"x-api-key: YOUR_API_KEY\" https://your-server/api/bot"
echo ""
echo "# 发送测试消息"
echo "cd $SKILL_DIR && python3 send_message.py"
echo ""

echo "=========================================="
echo -e "${GREEN}安装脚本完成！${NC}"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 按照上述说明配置 VoceChat Bot"
echo "2. 编辑配置文件填入 API Key 和 Bot ID"
echo "3. 重启 nanobot"
echo "4. 在 VoceChat 中给 nanobot 发消息测试"
echo ""
echo "文档位置:"
echo "  - README.md: $SKILL_DIR/README.md"
echo "  - VERSION.md: $SKILL_DIR/VERSION.md"
echo "  - RELEASE_NOTES.md: $SKILL_DIR/RELEASE_NOTES.md"
echo ""
echo "如有问题，请查看日志："
echo "  tail -f /tmp/vocechat_webhook.log"
echo "  journalctl -u nanobot -f"
echo ""
