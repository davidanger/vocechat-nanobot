#!/bin/bash
# VoceChat Integration GitHub 发布脚本
# 自动初始化 Git 仓库并推送到 GitHub

set -e

echo "=========================================="
echo "VoceChat Integration GitHub 发布脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SKILL_DIR="/root/.nanobot/workspace/skills/vocechat"
cd "$SKILL_DIR"

# 检查 Git 是否安装
if ! command -v git &> /dev/null; then
    echo -e "${RED}错误：Git 未安装${NC}"
    echo "请运行：apt-get install git"
    exit 1
fi

echo -e "${GREEN}✓ Git 已安装${NC}"

# 检查是否已初始化
if [ -d ".git" ]; then
    echo -e "${YELLOW}警告：Git 仓库已存在${NC}"
    read -p "是否重新初始化？(y/N): " confirm
    if [ "$confirm" != "y" ]; then
        echo "跳过初始化"
        git_status="existing"
    else
        rm -rf .git
        git_status="new"
    fi
else
    git_status="new"
fi

# 初始化 Git 仓库
if [ "$git_status" = "new" ]; then
    echo ""
    echo "初始化 Git 仓库..."
    git init
    echo -e "${GREEN}✓ Git 仓库已初始化${NC}"
fi

# 配置 Git 用户（如果需要）
if [ -z "$(git config user.name)" ]; then
    echo ""
    read -p "请输入 Git 用户名: " git_user
    git config user.name "$git_user"
fi

if [ -z "$(git config user.email)" ]; then
    read -p "请输入 Git 邮箱: " git_email
    git config user.email "$git_email"
fi

echo -e "${GREEN}✓ Git 用户已配置${NC}"

# 添加所有文件
echo ""
echo "添加文件到 Git..."
git add .
echo -e "${GREEN}✓ 文件已添加${NC}"

# 提交
echo ""
read -p "输入提交信息 (默认: Initial release: VoceChat Integration v1.0): " commit_msg
commit_msg=${commit_msg:-"Initial release: VoceChat Integration v1.0"}

git commit -m "$commit_msg"
echo -e "${GREEN}✓ 提交完成${NC}"

# 创建标签
echo ""
read -p "是否创建 v1.0.0 标签？(Y/n): " create_tag
if [ "$create_tag" != "n" ]; then
    git tag -a v1.0.0 -m "VoceChat Integration v1.0 Stable Release"
    echo -e "${GREEN}✓ 标签 v1.0.0 已创建${NC}"
fi

# 添加远程仓库
echo ""
read -p "是否添加远程仓库？(y/N): " add_remote
if [ "$add_remote" = "y" ]; then
    read -p "输入 GitHub 仓库地址 (例如：https://github.com/username/vocechat-nanobot.git): " remote_url
    
    # 检查是否已存在
    if git remote | grep -q "^origin$"; then
        echo -e "${YELLOW}远程仓库已存在${NC}"
        read -p "是否更新？(y/N): " update_remote
        if [ "$update_remote" = "y" ]; then
            git remote set-url origin "$remote_url"
        fi
    else
        git remote add origin "$remote_url"
    fi
    
    echo -e "${GREEN}✓ 远程仓库已配置${NC}"
    
    # 推送
    echo ""
    read -p "是否推送到 GitHub？(y/N): " push_now
    if [ "$push_now" = "y" ]; then
        echo "推送代码到 GitHub..."
        git push -u origin main
        
        echo ""
        echo "推送标签到 GitHub..."
        git push origin --tags
        
        echo -e "${GREEN}✓ 推送完成${NC}"
        
        # 创建 Release 提示
        echo ""
        echo "=========================================="
        echo -e "${GREEN}发布到 GitHub 完成！${NC}"
        echo "=========================================="
        echo ""
        echo "下一步:"
        echo "1. 访问 https://github.com/$(echo $remote_url | cut -d'/' -f4)/$(echo $remote_url | cut -d'/' -f5 | sed 's/.git$//')/releases/new"
        echo "2. 创建 Release v1.0.0"
        echo "3. 上传以下文件:"
        echo "   - /root/.nanobot/workspace/skills/vocechat-v1.0.tar.gz"
        echo "   - /root/.nanobot/workspace/skills/vocechat-v1.0.tar.gz.sha256"
        echo "4. 使用 GITHUB_RELEASE.md 中的模板填写发布说明"
        echo ""
    else
        echo "跳过推送"
        echo ""
        echo "手动推送命令:"
        echo "  git push -u origin main"
        echo "  git push origin --tags"
    fi
else
    echo ""
    echo "=========================================="
    echo -e "${GREEN}本地 Git 仓库已准备就绪！${NC}"
    echo "=========================================="
    echo ""
    echo "下一步:"
    echo "1. 在 GitHub 创建空仓库"
    echo "2. 运行以下命令:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/vocechat-nanobot.git"
    echo "   git push -u origin main"
    echo "   git push origin --tags"
    echo ""
fi

# 显示统计信息
echo ""
echo "=========================================="
echo "统计信息"
echo "=========================================="
echo "文件数量：$(find . -type f -not -path './.git/*' | wc -l)"
echo "代码行数：$(wc -l *.py *.md 2>/dev/null | tail -1 | awk '{print $1}')"
echo "提交数量：$(git log --oneline | wc -l)"
echo "标签：$(git tag | tail -1)"
echo ""

echo -e "${GREEN}发布脚本完成！${NC}"
