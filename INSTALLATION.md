# VoceChat Integration 安装指南

> 适用于其他 nanobot 实例的安装说明

## 📦 安装方法

### 方法 A: 从 GitHub 下载（推荐）

```bash
# 1. 下载
cd /root/.nanobot/workspace/skills
wget https://github.com/davidanger/vocechat-nanobot/releases/download/v1.0.0/vocechat-v1.0.tar.gz

# 2. 解压
tar -xzf vocechat-v1.0.tar.gz

# 3. 验证
cd vocechat
bash verify.sh
```

### 方法 B: 从压缩包安装

```bash
# 1. 传输压缩包到服务器
scp vocechat-v1.0.tar.gz user@target-server:/tmp/

# 2. 解压
cd /root/.nanobot/workspace/skills
tar -xzf /tmp/vocechat-v1.0.tar.gz

# 3. 验证
cd vocechat && bash verify.sh
```

### 方法 C: 克隆仓库

```bash
cd /root/.nanobot/workspace/skills
git clone https://github.com/davidanger/vocechat-nanobot.git vocechat
cd vocechat
bash install.sh
```

## 🔧 配置

编辑 `/root/.nanobot/config.json`：

```json
{
  "channels": {
    "vocechat": {
      "enabled": true,
      "serverUrl": "https://your-vocechat-server.com",
      "apiKey": "your_api_key_here",
      "botId": "your_bot_id",
      "webhookPort": 8080,
      "allowFrom": []
    }
  }
}
```

### 配置项说明

| 配置项 | 说明 |
|--------|------|
| `enabled` | 是否启用 |
| `serverUrl` | VoceChat 服务器地址 |
| `apiKey` | Bot API Key |
| `botId` | Bot 用户 ID |
| `webhookPort` | Webhook 端口（默认 8080） |
| `allowFrom` | 允许的用户列表（空=全部） |

## 🚀 启动

```bash
# 重启 nanobot
sudo systemctl restart nanobot

# 验证运行
ps aux | grep nanobot
ss -tlnp | grep 8080
tail -f /tmp/vocechat_webhook.log
```

## ✅ 验证

### 1. 运行验证脚本

```bash
cd /root/.nanobot/workspace/skills/vocechat
bash verify.sh
```

### 2. 测试聊天

在 VoceChat 中给 nanobot 发送消息，应该收到 AI 回复。

## 🔧 故障排查

### Webhook 不工作

```bash
# 检查端口
ss -tlnp | grep 8080

# 检查日志
tail -f /tmp/vocechat_webhook.log
```

### 消息发送失败

```bash
# 测试 API
curl -H "x-api-key: YOUR_API_KEY" \
     https://your-vocechat-server.com/api/bot

# 检查日志
journalctl -u nanobot -f
```

### 依赖缺失

```bash
pip3 install requests loguru
```

## 📚 相关文档

- [README.md](./README.md) - 主文档
- [QUICKSTART.md](./QUICKSTART.md) - 快速开始
- [VERSION.md](./VERSION.md) - 版本说明

---

**作者**: davidanger with nanobot-354345126  
**版本**: v1.0  
**GitHub**: https://github.com/davidanger/vocechat-nanobot
