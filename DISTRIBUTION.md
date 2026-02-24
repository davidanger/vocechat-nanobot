# VoceChat Integration v1.0 分发指南

> 如何将 VoceChat 集成安装到其他 nanobot 实例

---

## 📦 分发包信息

**文件名**: `vocechat-v1.0.tar.gz`  
**大小**: ~33KB（压缩后）  
**内容**: 完整的 VoceChat 集成技能（14 个文件）  
**适用**: nanobot v0.1.4+

### 分发包内容

```
vocechat-v1.0.tar.gz
└── vocechat/
    ├── 核心代码 (3 个 Python 文件)
    │   ├── vocechat_channel.py     (14K)
    │   ├── vocechat_bot.py         (17K)
    │   └── send_message.py         (4.4K)
    │
    ├── 文档 (8 个 Markdown 文件)
    │   ├── QUICKSTART.md           (5.0K)
    │   ├── README.md               (9.0K)
    │   ├── SKILL.md                (9.6K)
    │   ├── VERSION.md              (5.6K)
    │   ├── RELEASE_NOTES.md        (8.4K)
    │   ├── CHECKLIST.md            (9.0K)
    │   ├── SUMMARY.md              (11K)
    │   ├── RELEASE_ANNOUNCEMENT.md (8.5K)
    │   └── INSTALLATION.md         (6.6K)
    │
    ├── 工具 (2 个脚本)
    │   ├── install.sh              (5.1K)
    │   └── verify.sh               (4.0K)
    │
    └── 配置
        └── .gitignore              (548B)
```

**总计**: 15 个文件，~93KB（解压后）

---

## 🚀 分发方式

### 方式 1: 直接传输压缩包（推荐）

**适用场景**: 
- 一对一分发
- 内网部署
- 离线环境

**步骤**:

1. **准备分发包**
   ```bash
   # 在源服务器上
   cd /root/.nanobot/workspace/skills
   ls -lh vocechat-v1.0.tar.gz
   ```

2. **传输到目标服务器**
   ```bash
   # 使用 scp
   scp vocechat-v1.0.tar.gz user@target-server:/tmp/
   
   # 或使用 rsync
   rsync -avz vocechat-v1.0.tar.gz user@target-server:/tmp/
   
   # 或使用其他文件传输工具
   ```

3. **在目标服务器上安装**
   ```bash
   # 登录目标服务器
   ssh user@target-server
   
   # 解压到技能目录
   cd /root/.nanobot/workspace/skills
   tar -xzf /tmp/vocechat-v1.0.tar.gz
   
   # 验证安装
   cd vocechat
   bash verify.sh
   
   # 配置 nanobot
   nano /root/.nanobot/config.json
   
   # 重启 nanobot
   sudo systemctl restart nanobot
   ```

---

### 方式 2: 创建下载链接

**适用场景**: 
- 多人分发
- 公开分享
- 远程安装

**步骤**:

1. **上传到文件服务器**
   ```bash
   # 上传到 Web 服务器
   scp vocechat-v1.0.tar.gz webserver:/var/www/downloads/
   
   # 或上传到云存储（AWS S3、阿里云 OSS 等）
   aws s3 cp vocechat-v1.0.tar.gz s3://your-bucket/vocechat-v1.0.tar.gz
   ```

2. **生成下载链接**
   ```
   https://your-domain.com/downloads/vocechat-v1.0.tar.gz
   ```

3. **分发下载链接**
   
   提供安装说明：
   ```bash
   # 下载安装
   cd /root/.nanobot/workspace/skills
   wget https://your-domain.com/downloads/vocechat-v1.0.tar.gz
   
   # 解压
   tar -xzf vocechat-v1.0.tar.gz
   
   # 验证
   cd vocechat && bash verify.sh
   
   # 配置并重启
   # ... (见 INSTALLATION.md)
   ```

---

### 方式 3: Git 仓库分发

**适用场景**: 
- 版本控制
- 持续更新
- 团队协作

**步骤**:

1. **创建 Git 仓库**
   ```bash
   cd /root/.nanobot/workspace/skills/vocechat
   git init
   git add .
   git commit -m "VoceChat Integration v1.0"
   git tag v1.0
   
   # 推送到远程仓库
   git remote add origin <repository-url>
   git push origin main --tags
   ```

2. **在其他服务器安装**
   ```bash
   cd /root/.nanobot/workspace/skills
   git clone <repository-url> vocechat
   cd vocechat
   git checkout v1.0
   
   # 后续步骤同上
   ```

---

### 方式 4: 发布到 ClawHub（如果可用）

**适用场景**: 
- 社区分享
- 自动更新
- 技能市场

**步骤**:

1. **准备技能包**
   ```bash
   # 确保 SKILL.md 包含正确的元数据
   cat /root/.nanobot/workspace/skills/vocechat/SKILL.md | head -10
   ```

2. **发布到 ClawHub**
   ```bash
   cd /root/.nanobot/workspace/skills/vocechat
   nanobot skill publish
   ```

3. **其他用户安装**
   ```bash
   nanobot skill search vocechat
   nanobot skill install vocechat
   ```

---

## 📋 分发前检查清单

在分发前，确认：

### 文件完整性

- [ ] 压缩包已创建
- [ ] 所有文件都包含在内
- [ ] 没有包含 `__pycache__` 等缓存文件
- [ ] 验证脚本可以运行

```bash
# 验证压缩包内容
tar -tzf vocechat-v1.0.tar.gz | wc -l
# 应返回 15（文件数）

# 检查压缩包大小
ls -lh vocechat-v1.0.tar.gz
# 应 ~33KB
```

### 功能验证

- [ ] 在源服务器上运行正常
- [ ] 验证脚本通过所有检查
- [ ] 文档完整且准确
- [ ] 安装脚本测试通过

### 文档准备

- [ ] INSTALLATION.md 包含完整安装说明
- [ ] QUICKSTART.md 提供快速开始指南
- [ ] README.md 包含详细使用说明
- [ ] 故障排查指南完整

---

## 📦 创建分发包

### 方法 A: 使用提供的脚本

```bash
cd /root/.nanobot/workspace/skills
bash -c 'tar -czf vocechat-v1.0.tar.gz --exclude="__pycache__" vocechat/'
```

### 方法 B: 手动创建

```bash
cd /root/.nanobot/workspace/skills

# 清理缓存
find vocechat -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# 创建压缩包
tar -czf vocechat-v1.0.tar.gz vocechat/
```

### 方法 C: 使用 Git archive

```bash
cd /root/.nanobot/workspace/skills/vocechat
git archive --format=tar.gz --prefix=vocechat/ v1.0 > ../vocechat-v1.0.tar.gz
```

---

## 🧪 测试分发

### 在测试环境验证

1. **创建测试环境**
   ```bash
   # 使用 Docker 或虚拟机创建测试环境
   docker run -it debian:latest bash
   ```

2. **安装 nanobot**
   ```bash
   # 在测试环境中安装 nanobot
   # ... (略)
   ```

3. **安装 VoceChat 技能**
   ```bash
   cd /root/.nanobot/workspace/skills
   tar -xzf /tmp/vocechat-v1.0.tar.gz
   cd vocechat && bash verify.sh
   ```

4. **配置并测试**
   ```bash
   # 配置 nanobot
   # 重启服务
   # 测试功能
   ```

---

## 📊 分发统计

### 文件大小

| 文件 | 大小 | 说明 |
|------|------|------|
| `vocechat-v1.0.tar.gz` | ~33KB | 压缩分发包 |
| 解压后 | ~93KB | 完整技能目录 |

### 系统要求

| 要求 | 最低 | 推荐 |
|------|------|------|
| nanobot | v0.1.4 | v0.1.4+ |
| Python | 3.10 | 3.11+ |
| 内存 | 100MB | 500MB |
| 磁盘 | 1MB | 10MB |
| 网络 | 可选 | 用于下载 |

---

## 📞 支持其他用户安装

### 提供安装文档

将以下文档一并提供给用户：

1. **INSTALLATION.md** - 详细安装指南
2. **QUICKSTART.md** - 快速开始（5 分钟）
3. **README.md** - 完整使用说明

### 提供安装脚本

用户只需运行：

```bash
# 下载并解压
cd /root/.nanobot/workspace/skills
tar -xzf vocechat-v1.0.tar.gz

# 运行安装脚本
cd vocechat
sudo bash install.sh

# 按提示配置
```

### 提供验证工具

```bash
# 验证安装
bash verify.sh
```

---

## 🔄 更新分发

### 发布更新版本

1. **更新版本号**
   ```bash
   # 修改 VERSION.md 和 SKILL.md 中的版本号
   # 例如：v1.0 → v1.1
   ```

2. **创建新版本压缩包**
   ```bash
   tar -czf vocechat-v1.1.tar.gz --exclude="__pycache__" vocechat/
   ```

3. **通知用户更新**
   ```bash
   # 提供更新说明
   # 提供下载链接
   ```

### 用户更新方法

```bash
# 备份配置
cp /root/.nanobot/config.json /root/.nanobot/config.json.backup

# 停止 nanobot
sudo systemctl stop nanobot

# 删除旧版本
rm -rf /root/.nanobot/workspace/skills/vocechat

# 解压新版本
cd /root/.nanobot/workspace/skills
tar -xzf /tmp/vocechat-v1.1.tar.gz

# 重启 nanobot
sudo systemctl restart nanobot
```

---

## 📝 分发记录模板

记录分发给谁：

```markdown
## VoceChat v1.0 分发记录

| 日期 | 接收方 | 服务器 | 状态 | 备注 |
|------|--------|--------|------|------|
| 2026-02-24 | 用户 A | server1.example.com | ✅ 已安装 | 运行正常 |
| 2026-02-24 | 用户 B | server2.example.com | ⏳ 安装中 | - |
| 2026-02-25 | 用户 C | server3.example.com | ❌ 失败 | 端口冲突 |
```

---

## 🔐 安全提示

### 分发安全

- ✅ 使用加密传输（SCP、HTTPS）
- ✅ 提供文件校验和（SHA256）
- ✅ 验证接收方身份
- ⚠️ 不要在公开场合分享 API Key

### 生成校验和

```bash
# 生成 SHA256 校验和
sha256sum vocechat-v1.0.tar.gz > vocechat-v1.0.tar.gz.sha256

# 用户验证
sha256sum -c vocechat-v1.0.tar.gz.sha256
```

---

## 📚 相关文档

- **INSTALLATION.md** - 详细安装指南
- **QUICKSTART.md** - 5 分钟快速开始
- **README.md** - 完整使用说明
- **SKILL.md** - 技能文档
- **VERSION.md** - 版本说明

---

## ✅ 分发检查清单

分发前确认：

- [ ] 压缩包已创建且验证通过
- [ ] 所有必要文件都包含
- [ ] 文档完整且准确
- [ ] 安装脚本测试通过
- [ ] 验证脚本可用
- [ ] 提供安装说明
- [ ] 提供技术支持联系方式
- [ ] （可选）生成文件校验和
- [ ] （可选）创建下载链接
- [ ] （可选）准备更新计划

---

**版本**: v1.0  
**发布日期**: 2026-02-24  
**维护者**: nanobot 🐈 Team

**开始分发**: 将 `vocechat-v1.0.tar.gz` 传输到目标服务器，按照 INSTALLATION.md 安装！
