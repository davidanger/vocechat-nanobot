# VoceChat v1.0 快速开始指南 ⚡

> 5 分钟快速安装和配置 VoceChat 集成

---

## 📋 前置要求

- ✅ nanobot v0.1.4+ 已安装并运行
- ✅ VoceChat 服务器访问权限（管理员）
- ✅ Python 3.10+
- ✅ root 或 sudo 权限

---

## 🚀 5 步快速安装

### 步骤 1: 在 VoceChat 创建 Bot (2 分钟)

1. 登录 VoceChat 服务器管理面板
2. 进入 `Settings => Bot&Webhook`
3. 点击 `New` 创建新 Bot
4. 设置名称：`nanobot`
5. 设置 Webhook URL: `http://你的服务器IP:8080/`
6. 创建 API Key 并**立即复制保存**
7. 记录 Bot ID（在 Bot 信息页面查看）

### 步骤 2: 运行安装脚本 (30 秒)

```bash
cd /root/.nanobot/workspace/skills/vocechat
sudo bash install.sh
```

安装脚本会自动：
- ✓ 检查 nanobot 安装
- ✓ 验证配置文件
- ✓ 检查端口占用
- ✓ 提供配置说明

### 步骤 3: 配置 nanobot (1 分钟)

编辑配置文件：

```bash
nano /root/.nanobot/config.json
```

添加或修改 VoceChat 配置：

```json
{
  "channels": {
    "vocechat": {
      "enabled": true,
      "serverUrl": "https://your-vocechat-server.com",
      "apiKey": "你的 API_KEY",
      "botId": "你的 BOT_ID",
      "webhookPort": 8080,
      "allowFrom": []
    }
  }
}
```

**保存并退出**: `Ctrl+O` → `Enter` → `Ctrl+X`

### 步骤 4: 重启 nanobot (30 秒)

```bash
# 如果使用 systemd
sudo systemctl restart nanobot

# 检查状态
sudo systemctl status nanobot
```

### 步骤 5: 验证运行 (1 分钟)

```bash
# 1. 检查进程
ps aux | grep nanobot

# 2. 检查端口
ss -tlnp | grep 8080

# 3. 查看日志
tail -f /tmp/vocechat_webhook.log
```

**期望输出**:
```
✅ VoceChat 连接成功！Bot 在 X 个频道中
🚀 Webhook 服务器运行在 http://0.0.0.0:8080/
✅ 消息处理器已启动
```

---

## 🧪 测试

### 测试 1: Webhook 服务器

```bash
curl http://localhost:8080/
# 应返回：VoceChat Webhook is running!
```

### 测试 2: API 连接

```bash
curl -H "x-api-key: 你的 API_KEY" \
     https://your-vocechat-server.com/api/bot
# 应返回 Bot 信息 JSON
```

### 测试 3: 发送消息

```bash
cd /root/.nanobot/workspace/skills/vocechat
python3 send_message.py
```

### 测试 4: 实际聊天

1. 打开 VoceChat
2. 找到 nanobot
3. 发送消息：`你好`
4. 应该收到 AI 回复

---

## 🔧 故障排查

### 问题 1: 端口被占用

```bash
# 查看占用进程
ss -tlnp | grep 8080

# 修改配置文件中的 webhookPort
nano /root/.nanobot/config.json
```

### 问题 2: Webhook 不接收消息

检查清单:
- [ ] Webhook URL 是否正确
- [ ] 防火墙是否开放 8080 端口
- [ ] VoceChat 服务器能否访问你的服务器

```bash
# 检查防火墙
ufw status

# 开放端口（如果需要）
ufw allow 8080/tcp
```

### 问题 3: 没有自动回复

```bash
# 重启 nanobot
sudo systemctl restart nanobot

# 查看详细日志
journalctl -u nanobot --since "5 minutes ago" | grep vocechat
```

### 问题 4: API Key 无效

```bash
# 测试 API Key
curl -H "x-api-key: 你的 API_KEY" \
     https://your-vocechat-server.com/api/bot

# 如果返回错误，在 VoceChat 重新创建 API Key
```

---

## 📚 下一步

### 阅读完整文档

- **README.md** - 详细使用指南
- **SKILL.md** - 技能文档
- **VERSION.md** - 版本说明
- **RELEASE_NOTES.md** - 发布说明

### 高级配置

#### 限制允许的用户

```json
{
  "channels": {
    "vocechat": {
      "enabled": true,
      "allowFrom": ["1", "2", "3"]  // 只允许这些用户 ID
    }
  }
}
```

#### 自定义 Webhook 端口

```json
{
  "channels": {
    "vocechat": {
      "webhookPort": 9000  // 使用 9000 端口
    }
  }
}
```

#### 使用 HTTPS（推荐生产环境）

配置 nginx 反向代理：

```nginx
server {
    listen 443 ssl;
    server_name vocechat.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

然后在 VoceChat 更新 Webhook URL 为: `https://vocechat.yourdomain.com/`

---

## 📞 获取帮助

### 日志文件

- **Webhook 日志**: `/tmp/vocechat_webhook.log`
- **nanobot 日志**: `journalctl -u nanobot -f`

### 验证工具

```bash
# 运行完整验证
bash verify.sh
```

### 文档位置

```bash
# 所有文档
ls -lh /root/.nanobot/workspace/skills/vocechat/*.md
```

---

## ✅ 检查清单

安装完成后，确认以下各项:

- [ ] nanobot 进程正常运行
- [ ] 端口 8080 正在监听
- [ ] Webhook 服务器响应正常
- [ ] VoceChat Bot 配置正确
- [ ] 能够发送消息到 VoceChat
- [ ] 能够接收 VoceChat 消息
- [ ] 自动回复工作正常
- [ ] 日志记录正常

---

## 🎉 完成！

如果以上所有检查都通过，恭喜你成功安装 VoceChat Integration v1.0！

现在可以在 VoceChat 中享受 nanobot 的智能聊天功能了！🦞🤖💬

---

**版本**: v1.0  
**更新**: 2026-02-24  
**支持**: 查看 README.md 获取详细帮助
