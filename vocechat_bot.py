#!/usr/bin/env python3
"""
VoceChat Bot Integration for nanobot
- 接收 Webhook 消息
- 调用 nanobot 核心处理消息
- 发送智能回复到 VoceChat
"""

import os
import sys
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import threading
import time

# 配置
VOCECHAT_SERVER_URL = os.getenv("VOCECHAT_SERVER_URL", "https://vc.fn.lssv.cc:8443")
VOCECHAT_API_KEY = os.getenv("VOCECHAT_API_KEY", "")
VOCECHAT_BOT_ID = os.getenv("VOCECHAT_BOT_ID", "")
WEBHOOK_PORT = int(os.getenv("VOCECHAT_WEBHOOK_PORT", "8080"))

# 添加 nanobot 到路径
sys.path.insert(0, '/root/nanobot')

class VoceChatBot:
    """VoceChat Bot 客户端"""
    
    def __init__(self, server_url: str, api_key: str):
        self.server_url = server_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': api_key,
            'User-Agent': 'nanobot-vocechat/1.0'
        })
    
    def send_text_to_user(self, uid: int, text: str) -> dict:
        """发送文本消息给用户"""
        url = f"{self.server_url}/api/bot/send_to_user/{uid}"
        try:
            response = self.session.post(
                url,
                data=text.encode('utf-8'),
                headers={'content-type': 'text/plain'},
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def send_markdown_to_user(self, uid: int, markdown: str) -> dict:
        """发送 Markdown 消息给用户"""
        url = f"{self.server_url}/api/bot/send_to_user/{uid}"
        try:
            response = self.session.post(
                url,
                data=markdown.encode('utf-8'),
                headers={'content-type': 'text/markdown'},
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def send_text_to_group(self, gid: int, text: str) -> dict:
        """发送文本消息到频道"""
        url = f"{self.server_url}/api/bot/send_to_group/{gid}"
        try:
            response = self.session.post(
                url,
                data=text.encode('utf-8'),
                headers={'content-type': 'text/plain'},
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def send_markdown_to_group(self, gid: int, markdown: str) -> dict:
        """发送 Markdown 消息到频道"""
        url = f"{self.server_url}/api/bot/send_to_group/{gid}"
        try:
            response = self.session.post(
                url,
                data=markdown.encode('utf-8'),
                headers={'content-type': 'text/markdown'},
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def get_bot_channels(self) -> dict:
        """获取 Bot 所在的所有频道"""
        url = f"{self.server_url}/api/bot"
        response = self.session.get(url, timeout=10)
        return response.json()
    
    def get_user_info(self, uid: int) -> dict:
        """获取用户信息"""
        url = f"{self.server_url}/api/bot/user/{uid}"
        response = self.session.get(url, timeout=10)
        return response.json()
    
    def get_group_info(self, gid: int) -> dict:
        """获取频道信息"""
        url = f"{self.server_url}/api/bot/group/{gid}"
        response = self.session.get(url, timeout=10)
        return response.json()
    
    def upload_file(self, file_path: str) -> dict:
        """上传文件"""
        url = f"{self.server_url}/api/bot/file/upload"
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(url, files=files, timeout=10)
        return response.json()
    
    def send_file_to_user(self, uid: int, file_path: str) -> dict:
        """发送文件给用户"""
        upload_result = self.upload_file(file_path)
        if 'path' in upload_result:
            file_path_in_server = upload_result['path']
            url = f"{self.server_url}/api/bot/send_to_user/{uid}"
            response = self.session.post(
                url,
                json={'path': file_path_in_server},
                headers={'content-type': 'vocechat/file'},
                timeout=10
            )
            return response.json()
        return upload_result


class VoceChatMessageHandler:
    """VoceChat 消息处理器 - 集成 nanobot 核心"""
    
    def __init__(self, bot_instance: VoceChatBot):
        self.bot = bot_instance
        self.user_sessions = {}  # 简单的会话管理
    
    def process_message(self, from_uid: int, content: str, is_group: bool = False, target_id: int = None) -> str:
        """
        处理消息并生成回复
        
        Args:
            from_uid: 发送者 UID
            content: 消息内容
            is_group: 是否来自群组
            target_id: 群组 ID 或用户 ID
        
        Returns:
            回复内容
        """
        # 特殊命令处理
        if content.strip() == '/help':
            return self._format_response(
                "🐈 **nanobot 帮助**\n\n"
                "我可以使用自然语言交流，帮你：\n"
                "- 🌤️ 查询天气\n"
                "- ⏰ 设置提醒\n"
                "- 📝 记录笔记\n"
                "- 🔍 搜索信息\n"
                "- 💬 聊天解闷\n\n"
                "直接问我问题就好！"
            )
        
        if content.strip() == '/ping':
            return self._format_response(f"🏓 Pong! 延迟：{int(time.time() * 1000) % 1000}ms")
        
        # 调用 nanobot 核心处理（简化版本）
        # 实际应该调用 nanobot 的 agent 处理逻辑
        response = self._call_nanobot_core(from_uid, content)
        
        return self._format_response(response)
    
    def _call_nanobot_core(self, user_id: int, message: str) -> str:
        """
        调用 nanobot 核心处理逻辑
        
        这里使用简化实现，实际应该：
        1. 创建或获取用户会话
        2. 调用 nanobot agent 处理消息
        3. 返回处理结果
        """
        # TODO: 集成真实的 nanobot agent
        # 目前使用简单的规则回复
        
        message_lower = message.lower().strip()
        
        # 天气查询
        if '天气' in message or 'weather' in message_lower:
            return "🌤️ 我可以帮你查询天气！请告诉我城市名称，例如：`北京天气`"
        
        # 时间查询
        if '时间' in message or '几点' in message:
            now = datetime.now()
            return f"🕐 当前时间是：{now.strftime('%Y-%m-%d %H:%M:%S')}"
        
        # 日期查询
        if '日期' in message or '今天' in message:
            now = datetime.now()
            return f"📅 今天是：{now.strftime('%Y年%m月%d日 %A')}"
        
        # 自我介绍
        if '你是谁' in message or '介绍一下' in message:
            return (
                "🐈 我是 **nanobot**，一个智能 AI 助手！\n\n"
                "我可以帮助你：\n"
                "- 回答问题和查询信息\n"
                "- 设置提醒和待办事项\n"
                "- 聊天和提供建议\n"
                "- 执行各种实用任务\n\n"
                "有什么可以帮你的吗？"
            )
        
        # 默认回复 - 简单的对话逻辑
        if '你好' in message or 'hello' in message_lower or 'hi' in message_lower:
            return "你好！👋 我是 nanobot，有什么可以帮你的吗？"
        
        if '谢谢' in message or 'thank' in message_lower:
            return "不客气！😊 随时为你服务！"
        
        if '再见' in message or 'bye' in message_lower:
            return "再见！👋 有需要随时找我！"
        
        # 默认：表示收到消息并提供进一步帮助的提示
        return (
            f"收到你的消息了！💬\n\n"
            f"你说的是：*{message}*\n\n"
            "我可以帮你查询信息、设置提醒、或者 просто 聊聊天。\n"
            "输入 `/help` 查看更多功能。"
        )
    
    def _format_response(self, text: str) -> str:
        """格式化回复为 Markdown"""
        return text


class WebhookHandler(BaseHTTPRequestHandler):
    """Webhook 请求处理器"""
    
    bot_instance = None
    message_handler = None
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {args[0]}")
    
    def do_GET(self):
        """健康检查"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'VoceChat Webhook is running!')
    
    def do_POST(self):
        """处理 Webhook 消息"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            message = json.loads(post_data.decode('utf-8'))
            self.handle_message(message)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode('utf-8'))
        except Exception as e:
            print(f"❌ 处理消息失败：{e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
    
    def handle_message(self, message: dict):
        """处理接收到的消息"""
        print(f"\n📥 收到消息:")
        print(json.dumps(message, indent=2, ensure_ascii=False))
        
        # 解析消息
        detail = message.get('detail', {})
        from_uid = message.get('from_uid', 0)
        target = message.get('target', {})
        
        content = detail.get('content', '')
        content_type = detail.get('content_type', 'text/plain')
        msg_type = detail.get('type', 'normal')
        
        # 跳过非文本消息和机器人自己的消息
        if content_type not in ['text/plain', 'text/markdown']:
            print("⏭️  跳过非文本消息")
            return
        
        if not from_uid or from_uid == int(VOCECHAT_BOT_ID or 0):
            print("⏭️  跳过机器人自己的消息")
            return
        
        # 根据消息类型处理
        if msg_type == 'normal':
            self.handle_new_message(from_uid, target, content, content_type)
        elif msg_type == 'reply':
            self.handle_reply(from_uid, target, content, detail.get('mid'))
        elif msg_type == 'reaction':
            reaction_detail = detail.get('detail', {})
            reaction_type = reaction_detail.get('type', '')
            if reaction_type == 'edit':
                self.handle_edit(from_uid, target, reaction_detail.get('content'))
            elif reaction_type == 'delete':
                self.handle_delete(from_uid, target, reaction_detail.get('mid'))
    
    def handle_new_message(self, from_uid: int, target: dict, content: str, content_type: str):
        """处理新消息"""
        if content == 'newuser':
            # 新用户注册
            print(f"🎉 新用户注册：UID={from_uid}")
            if self.bot_instance:
                welcome_msg = (
                    "🎉 **欢迎加入！**\n\n"
                    "我是 **nanobot** 🐈，你的智能 AI 助手！\n\n"
                    "我可以帮你：\n"
                    "- 🌤️ 查询天气\n"
                    "- ⏰ 设置提醒\n"
                    "- 📝 记录笔记\n"
                    "- 🔍 搜索信息\n"
                    "- 💬 聊天解闷\n\n"
                    "输入 `/help` 查看更多功能，或者直接问我问题！"
                )
                result = self.bot_instance.send_markdown_to_user(from_uid, welcome_msg)
                print(f"✅ 发送欢迎消息：{result}")
        else:
            # 普通消息
            target_id = target.get('uid') or target.get('gid')
            is_group = 'gid' in target
            
            print(f"💬 来自 {'频道' if is_group else '用户'} {target_id}: {content}")
            
            if not self.message_handler:
                print("⚠️  消息处理器未初始化")
                return
            
            # 处理消息并生成回复
            response = self.message_handler.process_message(
                from_uid=from_uid,
                content=content,
                is_group=is_group,
                target_id=target_id
            )
            
            # 发送回复
            if is_group and target.get('gid'):
                print(f"📤 发送回复到频道 {target['gid']}")
                result = self.bot_instance.send_markdown_to_group(target['gid'], response)
            else:
                print(f"📤 发送回复给用户 {from_uid}")
                result = self.bot_instance.send_markdown_to_user(from_uid, response)
            
            print(f"✅ 回复结果：{result}")
    
    def handle_reply(self, from_uid: int, target: dict, content: str, reply_to_mid: int):
        """处理回复消息"""
        print(f"💬 回复消息 (回复到 #{reply_to_mid}): {content}")
        
        if self.message_handler and self.bot_instance:
            response = self.message_handler.process_message(from_uid, content)
            result = self.bot_instance.send_markdown_to_user(from_uid, response)
            print(f"✅ 回复结果：{result}")
    
    def handle_edit(self, from_uid: int, target: dict, new_content: str):
        """处理编辑消息"""
        print(f"✏️ 消息被编辑为：{new_content}")
        # TODO: 实现编辑逻辑
    
    def handle_delete(self, from_uid: int, target: dict, mid: int):
        """处理删除消息"""
        print(f"🗑️ 消息 #{mid} 被删除")
        # TODO: 实现删除逻辑


def start_webhook_server(port: int, bot: VoceChatBot, handler: VoceChatMessageHandler):
    """启动 Webhook 服务器"""
    WebhookHandler.bot_instance = bot
    WebhookHandler.message_handler = handler
    
    server = HTTPServer(('0.0.0.0', port), WebhookHandler)
    print(f"🚀 Webhook 服务器启动在端口 {port}")
    print(f"📡 Webhook URL: http://你的服务器IP:{port}/")
    server.serve_forever()


def main():
    """主函数"""
    if not VOCECHAT_API_KEY:
        print("❌ 错误：请设置 VOCECHAT_API_KEY 环境变量")
        print("使用方法:")
        print("  export VOCECHAT_API_KEY=your_api_key")
        print("  export VOCECHAT_SERVER_URL=https://your-vocechat-server.com")
        print("  python3 vocechat_bot.py")
        return
    
    # 创建 Bot 实例
    bot = VoceChatBot(VOCECHAT_SERVER_URL, VOCECHAT_API_KEY)
    
    print(f"🤖 VoceChat Bot 初始化完成")
    print(f"   服务器：{VOCECHAT_SERVER_URL}")
    print(f"   API Key: {VOCECHAT_API_KEY[:10]}...")
    
    # 测试连接
    try:
        channels = bot.get_bot_channels()
        channel_count = len(channels) if isinstance(channels, list) else 'N/A'
        print(f"✅ 连接成功！Bot 在 {channel_count} 个频道中")
    except Exception as e:
        print(f"⚠️ 连接测试失败：{e}")
    
    # 创建消息处理器
    handler = VoceChatMessageHandler(bot)
    
    # 启动 Webhook 服务器（在新线程中）
    webhook_thread = threading.Thread(
        target=start_webhook_server,
        args=(WEBHOOK_PORT, bot, handler),
        daemon=True
    )
    webhook_thread.start()
    
    print("\n✨ VoceChat Bot 已就绪，等待消息...")
    print("📄 日志文件：`/tmp/vocechat_webhook.log`")
    print("🛑 按 Ctrl+C 停止\n")
    
    # 主线程保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 正在关闭...")


if __name__ == '__main__':
    main()
