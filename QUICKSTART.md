# VoceChat v1.0 快速开始指南 ⚡

> 5 分钟快速安装和配置 VoceChat 集成  
> **作者**: davidanger with nanobot-354345126

---

## 🚀 5 步快速安装

### 步骤 1: 在 VoceChat 创建 Bot (2 分钟)

1. 登录 VoceChat 管理面板
2. 进入 `Settings => Bot&Webhook`
3. 创建新 Bot，设置 Webhook URL: `http://你的服务器 IP:8080/`
4. 创建 API Key 并**立即保存**
5. 记录 Bot ID

### 步骤 2: 运行安装脚本

```bash
cd /root/.nanobot/workspace/skills/vocechat
sudo bash install.sh
```

### 步骤 3: 配置 nanobot

编辑 `/root/.nanobot/config.json`：

```json
{
  "channels": {
    "vocechat": {
      "enabled": true,
      "serverUrl": "https://your-vocechat-server.com",
      "apiKey": "你的 API_KEY",
      "botId": "你的 BOT_ID",
      "webhookPort": 8080
    }
  }
}
```

### 步骤 4: 重启 nanobot

```bash
sudo systemctl restart nanobot
```

### 步骤 5: 验证

```bash
ss -tlnp | grep 8080
tail -f /tmp/vocechat_webhook.log
```

---

## 🧪 测试

1. **Webhook 服务器**: `curl http://localhost:8080/`
2. **API 连接**: `curl -H "x-api-key: YOUR_API_KEY" https://your-server.com/api/bot`
3. **实际聊天**: 在 VoceChat 中发送 "你好"，应收到 AI 回复

---

## 🔧 故障排查

### 端口被占用
```bash
ss -tlnp | grep 8080
# 修改 config.json 中的 webhookPort
```

### Webhook 不工作
```bash
tail -f /tmp/vocechat_webhook.log
```

### 没有自动回复
```bash
sudo systemctl restart nanobot
journalctl -u nanobot -f | grep vocechat
```

---

## 📚 更多文档

- [README.md](./README.md) - 主文档
- [INSTALLATION.md](./INSTALLATION.md) - 详细安装指南
- [VERSION.md](./VERSION.md) - 版本说明

---

**作者**: davidanger with nanobot-354345126  
**版本**: v1.0  
**GitHub**: https://github.com/davidanger/vocechat-nanobot
