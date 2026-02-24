#!/usr/bin/env python3
"""
VoceChat Bot - nanobot 集成
发送消息到 VoceChat
"""

import requests

# ==================== 配置 ====================
SERVER_URL = "https://vc.fn.lssv.cc:8443"
API_KEY = "8e131792069c84653df7115ce06c8e66d2515852cd4b757effc99ec7ac5eaff37b22756964223a342c226e6f6e6365223a2243367649413756346e476b41414141414d323232474d4e3138594a5345626963227d"
# =============================================

class VoceChatBot:
    """VoceChat Bot 客户端"""
    
    def __init__(self, server_url: str, api_key: str):
        self.server_url = server_url
        self.api_key = api_key
    
    def send_text(self, uid: int, text: str) -> int:
        """发送文本消息给用户，返回消息 ID"""
        url = f"{self.server_url}/api/bot/send_to_user/{uid}"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "text/plain"
        }
        
        response = requests.post(url, headers=headers, data=text, verify=False)
        
        if response.status_code == 200:
            msg_id = int(response.text)
            print(f"✅ 消息发送成功！消息 ID: {msg_id}")
            return msg_id
        else:
            print(f"❌ 发送失败：HTTP {response.status_code}")
            print(f"响应：{response.text}")
            return -1
    
    def send_markdown(self, uid: int, markdown: str) -> int:
        """发送 Markdown 消息给用户"""
        url = f"{self.server_url}/api/bot/send_to_user/{uid}"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "text/markdown"
        }
        
        response = requests.post(url, headers=headers, data=markdown, verify=False)
        
        if response.status_code == 200:
            msg_id = int(response.text)
            print(f"✅ Markdown 消息发送成功！消息 ID: {msg_id}")
            return msg_id
        else:
            print(f"❌ 发送失败：HTTP {response.status_code}")
            return -1
    
    def send_to_group(self, gid: int, content: str, content_type: str = "text/plain") -> int:
        """发送消息到频道"""
        url = f"{self.server_url}/api/bot/send_to_group/{gid}"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": content_type
        }
        
        response = requests.post(url, headers=headers, data=content, verify=False)
        
        if response.status_code == 200:
            msg_id = int(response.text)
            print(f"✅ 频道消息发送成功！消息 ID: {msg_id}")
            return msg_id
        else:
            print(f"❌ 发送失败：HTTP {response.status_code}")
            return -1
    
    def get_channels(self) -> list:
        """获取 Bot 所在的频道"""
        url = f"{self.server_url}/api/bot"
        headers = {"x-api-key": self.api_key}
        
        response = requests.get(url, headers=headers, verify=False)
        
        if response.status_code == 200:
            try:
                channels = response.json()
                print(f"✅ Bot 在 {len(channels)} 个频道中")
                return channels
            except:
                print("⚠️ 响应不是 JSON 格式")
                return []
        else:
            print(f"❌ 获取失败：HTTP {response.status_code}")
            return []


# ==================== 测试 ====================
if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    
    bot = VoceChatBot(SERVER_URL, API_KEY)
    
    print("="*60)
    print("VoceChat Bot 测试")
    print("="*60)
    
    # 测试 1: 发送文本消息
    print("\n[测试 1] 发送文本消息给用户 #1")
    bot.send_text(1, "🐱 你好！我是 nanobot，这是测试消息～")
    
    # 测试 2: 发送 Markdown 消息
    print("\n[测试 2] 发送 Markdown 消息给用户 #1")
    markdown_content = """# 🐱 nanobot

这是一条 **Markdown** 格式的消息。

## 功能
- ✅ 文本消息
- ✅ Markdown 消息
- ✅ 频道消息

> 如果你看到格式化的消息，说明一切正常！
"""
    bot.send_markdown(1, markdown_content)
    
    # 测试 3: 获取频道
    print("\n[测试 3] 获取 Bot 所在的频道")
    channels = bot.get_channels()
    for ch in channels:
        print(f"  - 频道 ID: {ch.get('gid')}, 名称：{ch.get('name')}")
    
    print("\n" + "="*60)
    print("测试完成")
    print("="*60)
