#!/usr/bin/env python3
"""
VoceChat Channel for nanobot
- 完全集成 nanobot 核心架构
- 使用消息总线 (MessageBus) 通信
- 支持异步消息处理
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import requests
from loguru import logger

from nanobot.bus.events import InboundMessage, OutboundMessage
from nanobot.bus.queue import MessageBus
from nanobot.channels.base import BaseChannel


class VoceChatConfig:
    """VoceChat 配置类"""
    def __init__(
        self,
        server_url: str,
        api_key: str,
        bot_id: str = "",
        webhook_port: int = 8080,
        allow_from: list[str] | None = None,
    ):
        self.server_url = server_url
        self.api_key = api_key
        self.bot_id = bot_id
        self.webhook_port = webhook_port
        self.allow_from = allow_from or []


class VoceChatAPI:
    """VoceChat API 客户端"""
    
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
        return self._send_message(f"/api/bot/send_to_user/{uid}", text, 'text/plain')
    
    def send_markdown_to_user(self, uid: int, markdown: str) -> dict:
        """发送 Markdown 消息给用户"""
        return self._send_message(f"/api/bot/send_to_user/{uid}", markdown, 'text/markdown')
    
    def send_text_to_group(self, gid: int, text: str) -> dict:
        """发送文本消息到频道"""
        return self._send_message(f"/api/bot/send_to_group/{gid}", text, 'text/plain')
    
    def send_markdown_to_group(self, gid: int, markdown: str) -> dict:
        """发送 Markdown 消息到频道"""
        return self._send_message(f"/api/bot/send_to_group/{gid}", markdown, 'text/markdown')
    
    def _send_message(self, endpoint: str, content: str, content_type: str) -> dict:
        """发送消息的通用方法"""
        url = f"{self.server_url}{endpoint}"
        try:
            response = self.session.post(
                url,
                data=content.encode('utf-8'),
                headers={'content-type': content_type},
                timeout=10
            )
            return response.json()
        except Exception as e:
            logger.error(f"发送消息失败：{e}")
            return {'error': str(e)}
    
    def get_bot_channels(self) -> list:
        """获取 Bot 所在的所有频道"""
        url = f"{self.server_url}/api/bot"
        response = self.session.get(url, timeout=10)
        return response.json() if response.status_code == 200 else []
    
    def get_user_info(self, uid: int) -> dict:
        """获取用户信息"""
        url = f"{self.server_url}/api/bot/user/{uid}"
        response = self.session.get(url, timeout=10)
        return response.json() if response.status_code == 200 else {}
    
    def get_group_info(self, gid: int) -> dict:
        """获取频道信息"""
        url = f"{self.server_url}/api/bot/group/{gid}"
        response = self.session.get(url, timeout=10)
        return response.json() if response.status_code == 200 else {}


class VoceChatChannel(BaseChannel):
    """
    VoceChat Channel 实现
    
    使用 Webhook 接收消息，通过 MessageBus 与 nanobot 核心通信
    """
    
    name = "vocechat"
    
    def __init__(
        self,
        config: VoceChatConfig,
        bus: MessageBus,
    ):
        super().__init__(config, bus)
        self.config: VoceChatConfig = config
        self.api = VoceChatAPI(config.server_url, config.api_key)
        self._webhook_server = None
        self._webhook_task = None
    
    async def start(self) -> None:
        """启动 VoceChat Webhook 服务器"""
        if not self.config.api_key:
            logger.error("VoceChat API Key 未配置")
            return
        
        self._running = True
        
        logger.info(f"初始化 VoceChat 连接：{self.config.server_url}")
        
        # 测试连接
        try:
            channels = self.api.get_bot_channels()
            logger.info(f"✅ VoceChat 连接成功！Bot 在 {len(channels)} 个频道中")
        except Exception as e:
            logger.warning(f"⚠️ VoceChat 连接测试失败：{e}")
        
        # 启动 Webhook 服务器
        logger.info(f"启动 VoceChat Webhook 服务器 (端口 {self.config.webhook_port})...")
        
        # 在后台线程中运行 HTTP 服务器
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import threading
        import queue
        
        channel_instance = self
        message_queue = queue.Queue()
        
        # 保存事件循环引用（在启动服务器之前）
        self._loop = asyncio.get_event_loop()
        
        class WebhookHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                logger.debug(f"Webhook: {args[0]}")
            
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
                    # 将消息放入队列，由主线程处理
                    message_queue.put(message)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'ok'}).encode('utf-8'))
                except Exception as e:
                    logger.error(f"处理 Webhook 消息失败：{e}")
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        
        # 创建 HTTP 服务器
        self._webhook_server = HTTPServer(('0.0.0.0', self.config.webhook_port), WebhookHandler)
        
        # 在独立线程中运行服务器
        def run_server():
            logger.info(f"🚀 Webhook 服务器运行在 http://0.0.0.0:{self.config.webhook_port}/")
            while self._running:
                self._webhook_server.handle_request()
        
        self._webhook_thread = threading.Thread(target=run_server, daemon=True)
        self._webhook_thread.start()
        
        # 启动消息处理循环
        async def process_webhook_messages():
            """处理 Webhook 消息队列"""
            while self._running:
                try:
                    # 非阻塞方式检查队列
                    try:
                        message = message_queue.get_nowait()
                        logger.debug(f"📥 从队列获取消息")
                        await channel_instance._handle_webhook_message(message)
                    except queue.Empty:
                        await asyncio.sleep(0.1)
                except Exception as e:
                    logger.error(f"处理队列消息失败：{e}")
        
        # 创建消息处理任务
        self._message_processor_task = asyncio.create_task(process_webhook_messages())
        logger.info(f"✅ 消息处理器已启动")
        
        # 保持运行
        while self._running:
            await asyncio.sleep(1)
    
    async def stop(self) -> None:
        """停止 VoceChat Webhook 服务器"""
        self._running = False
        
        # 停止消息处理器
        if hasattr(self, '_message_processor_task'):
            self._message_processor_task.cancel()
            try:
                await self._message_processor_task
            except asyncio.CancelledError:
                pass
        
        if self._webhook_server:
            logger.info("停止 VoceChat Webhook 服务器...")
            self._webhook_server.shutdown()
            self._webhook_server = None
    
    async def send(self, msg: OutboundMessage) -> None:
        """发送消息到 VoceChat"""
        try:
            # 解析 chat_id
            chat_info = json.loads(msg.chat_id) if isinstance(msg.chat_id, str) and msg.chat_id.startswith('{') else msg.chat_id
            
            if isinstance(chat_info, dict):
                uid = chat_info.get('uid')
                gid = chat_info.get('gid')
                
                if gid:
                    # 发送到群组
                    result = self.api.send_markdown_to_group(gid, msg.content)
                    logger.info(f"📤 发送消息到群组 {gid}: {result}")
                elif uid:
                    # 发送给用户
                    result = self.api.send_markdown_to_user(uid, msg.content)
                    logger.info(f"📤 发送消息给用户 {uid}: {result}")
            else:
                # 尝试直接解析为 UID
                try:
                    uid = int(msg.chat_id)
                    result = self.api.send_markdown_to_user(uid, msg.content)
                    logger.info(f"📤 发送消息给用户 {uid}: {result}")
                except ValueError:
                    logger.error(f"无法解析 chat_id: {msg.chat_id}")
        except Exception as e:
            logger.error(f"发送 VoceChat 消息失败：{e}")
    
    async def _handle_webhook_message(self, message: dict) -> None:
        """处理接收到的 Webhook 消息"""
        logger.debug(f"📥 收到 VoceChat 消息：{json.dumps(message, ensure_ascii=False)[:200]}")
        
        detail = message.get('detail', {})
        from_uid = message.get('from_uid', 0)
        target = message.get('target', {})
        
        content = detail.get('content', '')
        content_type = detail.get('content_type', 'text/plain')
        msg_type = detail.get('type', 'normal')
        
        # 跳过非文本消息
        if content_type not in ['text/plain', 'text/markdown']:
            logger.debug(f"⏭️ 跳过非文本消息：{content_type}")
            return
        
        # 跳过机器人自己的消息
        bot_uid = int(self.config.bot_id) if self.config.bot_id else 0
        if not from_uid or from_uid == bot_uid:
            logger.debug(f"⏭️ 跳过机器人消息")
            return
        
        # 处理新用户注册
        if content == 'newuser':
            logger.info(f"🎉 新用户注册：UID={from_uid}")
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
            self.api.send_markdown_to_user(from_uid, welcome_msg)
            return
        
        # 构建 sender_id 和 chat_id
        is_group = 'gid' in target
        target_id = target.get('uid') or target.get('gid')
        
        # 构建唯一的 sender_id
        sender_id = str(from_uid)
        
        # 构建 chat_id（包含群组信息）
        if is_group:
            chat_id = json.dumps({'gid': target['gid'], 'from_uid': from_uid})
        else:
            chat_id = str(from_uid)
        
        logger.info(f"💬 来自 {'群组' if is_group else '用户'} {target_id}: {content[:50]}...")
        
        # 创建 InboundMessage 并发布到消息总线
        inbound_msg = InboundMessage(
            channel=self.name,
            sender_id=sender_id,
            chat_id=chat_id,
            content=content,
            metadata={
                'message_id': message.get('mid'),
                'user_id': from_uid,
                'is_group': is_group,
                'target': target,
            }
        )
        
        # 发布到消息总线
        await self.bus.publish_inbound(inbound_msg)
        logger.info(f"✅ 消息已发布到总线 (session_key: {inbound_msg.session_key})")
        logger.debug(f"   Channel: {inbound_msg.channel}, Sender: {inbound_msg.sender_id}, Chat: {inbound_msg.chat_id}")


def create_channel(config: dict, bus: MessageBus) -> VoceChatChannel:
    """创建 VoceChat Channel 实例"""
    vocechat_config = VoceChatConfig(
        server_url=config.get('server_url', 'https://vc.fn.lssv.cc:8443'),
        api_key=config.get('api_key', ''),
        bot_id=config.get('bot_id', ''),
        webhook_port=config.get('webhook_port', 8080),
        allow_from=config.get('allow_from', []),
    )
    return VoceChatChannel(vocechat_config, bus)
