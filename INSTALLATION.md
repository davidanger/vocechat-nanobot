# VoceChat Integration v1.0 安装指南

> 适用于其他 nanobot 实例的安装说明

## 📦 分发形式

VoceChat Integration v1.0 提供以下分发方式：

### 方式 1: 压缩包分发（推荐）

**文件**: `vocechat-v1.0.tar.gz` (~50KB)

**适用场景**: 
- 离线安装
- 内网部署
- 快速分发

### 方式 2: Git 仓库

**仓库**: （可选，如需创建 Git 仓库）

**适用场景**:
- 版本控制
- 团队协作
- 持续更新

### 方式 3: ClawHub 技能市场

**技能 ID**: `vocechat`

**适用场景**:
- 在线安装
- 自动更新
- 社区分享

---

## 🚀 安装方法

### 方法 A: 从压缩包安装（推荐）

#### 1. 传输压缩包到目标服务器

```bash
# 使用 scp 传输
scp vocechat-v1.0.tar.gz user@target-server:/tmp/

# 或使用其他方式传输（U 盘、网盘等）
```

#### 2. 解压到技能目录

```bash
# 在目标服务器上
cd /root/.nanobot/workspace/skills
tar -xzf /tmp/vocechat-v1.0.tar.gz
```

#### 3. 验证安装

```bash
cd /root/.nanobot/workspace/skills/vocechat
bash verify.sh
```

#### 4. 配置 nanobot

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

#### 5. 重启 nanobot

```bash
sudo systemctl restart nanobot
```

#### 6. 验证运行

```bash
# 检查进程
ps aux | grep nanobot

# 检查端口
ss -tlnp | grep 8080

# 查看日志
tail -f /tmp/vocechat_webhook.log
```

---

### 方法 B: 从 Git 仓库安装

#### 1. 克隆仓库

```bash
cd /root/.nanobot/workspace/skills
git clone <repository-url> vocechat
```

#### 2. 切换到稳定版本

```bash
cd vocechat
git checkout v1.0
```

#### 3. 后续步骤

同方法 A 的步骤 3-6

---

### 方法 C: 使用 ClawHub（如果可用）

```bash
# 搜索技能
nanobot skill search vocechat

# 安装技能
nanobot skill install vocechat

# 配置
nano /root/.nanobot/config.json

# 重启
sudo systemctl restart nanobot
```

---

## 📋 安装前检查清单

在目标服务器上执行：

```bash
# 1. 检查 nanobot 版本
nanobot --version
# 需要 v0.1.4+

# 2. 检查 Python 版本
python3 --version
# 需要 Python 3.10+

# 3. 检查依赖
python3 -c "import requests; import loguru"
# 无错误表示依赖已安装

# 4. 检查端口
ss -tlnp | grep 8080
# 确保 8080 端口未被占用

# 5. 检查磁盘空间
df -h /root/.nanobot
# 确保有足够空间（需要 ~1MB）
```

---

## 🔧 配置说明

### 必需配置

在 `/root/.nanobot/config.json` 中添加：

```json
{
  "channels": {
    "vocechat": {
      "enabled": true,              // 是否启用
      "serverUrl": "https://...",   // VoceChat 服务器地址
      "apiKey": "your_api_key",     // Bot API Key
      "botId": "4",                 // Bot 用户 ID
      "webhookPort": 8080,          // Webhook 端口
      "allowFrom": []               // 允许的用户列表（空=全部）
    }
  }
}
```

### 配置项说明

| 配置项 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| `enabled` | boolean | ✅ | 是否启用 VoceChat 通道 |
| `serverUrl` | string | ✅ | VoceChat 服务器 URL |
| `apiKey` | string | ✅ | Bot API Key（从 VoceChat 获取） |
| `botId` | string | ✅ | Bot 的用户 ID |
| `webhookPort` | integer | ❌ | Webhook 端口（默认 8080） |
| `allowFrom` | array | ❌ | 允许的用户 ID 列表（空=全部） |

### 环境变量（可选）

也可以通过环境变量配置：

```bash
export VOCECHAT_SERVER_URL="https://your-server.com"
export VOCECHAT_API_KEY="your_api_key"
export VOCECHAT_BOT_ID="4"
export VOCECHAT_WEBHOOK_PORT="8080"
```

---

## 📦 分发包内容

```
vocechat-v1.0.tar.gz
└── vocechat/
    ├── 核心代码
    │   ├── vocechat_channel.py     (14K, 351 行)
    │   ├── vocechat_bot.py         (17K, 444 行)
    │   └── send_message.py         (4.4K, 134 行)
    │
    ├── 文档
    │   ├── QUICKSTART.md           (5.0K)
    │   ├── README.md               (9.0K)
    │   ├── SKILL.md                (9.6K)
    │   ├── VERSION.md              (5.6K)
    │   ├── RELEASE_NOTES.md        (8.4K)
    │   ├── CHECKLIST.md            (9.0K)
    │   ├── SUMMARY.md              (11K)
    │   └── RELEASE_ANNOUNCEMENT.md (8.5K)
    │
    ├── 工具
    │   ├── install.sh              (5.1K)
    │   ├── verify.sh               (4.0K)
    │   └── .gitignore              (548B)
    │
    └── __pycache__/               (可忽略)
```

**总计**: 14 个文件，~50KB（压缩后）

---

## 🧪 安装后验证

### 1. 运行验证脚本

```bash
cd /root/.nanobot/workspace/skills/vocechat
bash verify.sh
```

**期望输出**:
```
✅ 验证通过！所有检查项完成
```

### 2. 功能测试

```bash
# 测试 Webhook 服务器
curl http://localhost:8080/
# 应返回：VoceChat Webhook is running!

# 测试 API 连接
curl -H "x-api-key: YOUR_API_KEY" \
     https://your-vocechat-server.com/api/bot
# 应返回 Bot 信息 JSON

# 发送测试消息
python3 send_message.py
```

### 3. 实际聊天测试

1. 打开 VoceChat
2. 找到 nanobot
3. 发送：`你好`
4. 应收到 AI 回复

---

## 🔧 故障排查

### 问题 1: 技能未加载

**症状**: nanobot 启动后没有 VoceChat 相关日志

**解决**:
```bash
# 检查文件是否存在
ls -la /root/.nanobot/workspace/skills/vocechat/

# 检查配置文件
cat /root/.nanobot/config.json | grep -A 10 vocechat

# 查看详细日志
journalctl -u nanobot --since "5 minutes ago" | grep vocechat
```

### 问题 2: 端口被占用

**症状**: `Address already in use` 错误

**解决**:
```bash
# 查看占用进程
ss -tlnp | grep 8080

# 方案 1: 停止占用进程
kill <PID>

# 方案 2: 修改配置使用其他端口
nano /root/.nanobot/config.json
# 修改 webhookPort: 9000
```

### 问题 3: 依赖缺失

**症状**: `ModuleNotFoundError: No module named 'requests'`

**解决**:
```bash
# 安装依赖
pip3 install requests loguru
```

### 问题 4: API Key 无效

**症状**: `401 Unauthorized` 错误

**解决**:
1. 在 VoceChat 重新创建 API Key
2. 更新配置文件
3. 重启 nanobot

---

## 📚 文档说明

安装后，文档位于：

```
/root/.nanobot/workspace/skills/vocechat/
├── QUICKSTART.md              # 5 分钟快速开始（首选）
├── README.md                  # 详细使用指南
├── SKILL.md                   # 技能文档
├── VERSION.md                 # 版本说明
├── RELEASE_NOTES.md           # 发布说明
├── SUMMARY.md                 # 完整总结
└── INSTALLATION.md            # 本文件
```

**推荐阅读顺序**:
1. **QUICKSTART.md** - 快速上手
2. **README.md** - 详细指南
3. **SKILL.md** - 技术文档

---

## 🔄 更新方法

### 从压缩包更新

```bash
# 1. 备份配置
cp /root/.nanobot/config.json /root/.nanobot/config.json.backup

# 2. 停止 nanobot
sudo systemctl stop nanobot

# 3. 删除旧版本
rm -rf /root/.nanobot/workspace/skills/vocechat

# 4. 解压新版本
cd /root/.nanobot/workspace/skills
tar -xzf /tmp/vocechat-v1.0.tar.gz

# 5. 恢复配置（如果需要）
# 配置文件在 /root/.nanobot/config.json，不需要恢复

# 6. 重启 nanobot
sudo systemctl restart nanobot
```

### 从 Git 更新

```bash
cd /root/.nanobot/workspace/skills/vocechat
git pull
git checkout v1.0
sudo systemctl restart nanobot
```

---

## 📞 获取帮助

### 日志文件

- **Webhook 日志**: `/tmp/vocechat_webhook.log`
- **nanobot 日志**: `journalctl -u nanobot -f`

### 验证工具

```bash
bash verify.sh
```

### 文档

- 快速开始：`QUICKSTART.md`
- 详细指南：`README.md`
- 故障排查：`README.md` 的"故障排查"章节

---

## 📊 系统要求

| 要求 | 最低 | 推荐 |
|------|------|------|
| nanobot | v0.1.4 | v0.1.4+ |
| Python | 3.10 | 3.11+ |
| 内存 | 100MB | 500MB |
| 磁盘 | 1MB | 10MB |
| 端口 | 8080 | 8080 或自定义 |

---

## ✅ 安装检查清单

安装完成后，确认：

- [ ] 技能文件已解压到正确位置
- [ ] 验证脚本通过所有检查
- [ ] 配置文件已正确编辑
- [ ] nanobot 已重启
- [ ] 端口 8080 正在监听
- [ ] Webhook 服务器响应正常
- [ ] 能够发送消息到 VoceChat
- [ ] 能够接收 VoceChat 消息
- [ ] 自动回复工作正常

---

**版本**: v1.0  
**更新日期**: 2026-02-24  
**支持**: 查看 README.md 获取详细帮助
