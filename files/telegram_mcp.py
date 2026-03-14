#!/usr/bin/env python3
"""
Telegram MCP Server - Multi-Bot System
Allows Claude to send messages as different personas via their own bots.

WHERE TO PUT THIS:
~/.telegram_bridge/telegram_mcp.py
(Windows: C:\Users\YourName\.telegram_bridge\telegram_mcp.py)

CUSTOMIZE the configuration section below with your actual values.
"""

import sys
import json
import asyncio
import aiohttp
import tempfile
import os

# ==============================================================================
# CONFIGURATION - Edit these values
# ==============================================================================

# Your group chat ID (negative number, as string)
GROUP_CHAT_ID = "-5292137651"

# Your Telegram user ID
YOUR_USER_ID = "1234567890"

# Bot tokens - one per persona
# Get these from @BotFather on Telegram
BOT_TOKENS = {
    "partner1": "7123456789:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "partner2": "7234567890:AAHyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
    "partner3": "7345678901:AAHzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",
}

# ElevenLabs configuration (for voice messages)
ELEVENLABS_API_KEY = "your_elevenlabs_api_key_here"

# Voice IDs - one per persona
# Get these from your ElevenLabs dashboard
VOICE_IDS = {
    "partner1": "voice_id_for_partner1",
    "partner2": "voice_id_for_partner2",
    "partner3": "voice_id_for_partner3",
}

# ==============================================================================
# END CONFIGURATION - Don't edit below unless you know what you're doing
# ==============================================================================


async def send_telegram_message(message: str, sender: str) -> dict:
    """Send a text message via the specified sender's bot."""
    token = BOT_TOKENS.get(sender.lower())
    if not token:
        return {"error": f"Unknown sender: {sender}. Valid: {list(BOT_TOKENS.keys())}"}
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": GROUP_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            result = await resp.json()
            if result.get("ok"):
                return {"success": True, "sender": sender}
            return {"error": result.get("description", "Unknown error")}


async def send_voice_message(text: str, voice: str, also_text: bool = False) -> dict:
    """Generate voice via ElevenLabs and send as Telegram voice message."""
    voice_id = VOICE_IDS.get(voice.lower())
    token = BOT_TOKENS.get(voice.lower())
    
    if not voice_id:
        return {"error": f"Unknown voice: {voice}. Valid: {list(VOICE_IDS.keys())}"}
    if not token:
        return {"error": f"Unknown sender: {voice}. Valid: {list(BOT_TOKENS.keys())}"}
    
    # Generate audio via ElevenLabs
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    async with aiohttp.ClientSession() as session:
        # Get audio from ElevenLabs
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                return {"error": f"ElevenLabs error: {error_text}"}
            audio_data = await resp.read()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(audio_data)
            temp_path = f.name
        
        try:
            # Send to Telegram
            tg_url = f"https://api.telegram.org/bot{token}/sendVoice"
            form = aiohttp.FormData()
            form.add_field("chat_id", GROUP_CHAT_ID)
            form.add_field("voice", open(temp_path, "rb"), filename="voice.ogg")
            
            async with session.post(tg_url, data=form) as resp:
                result = await resp.json()
                
            # Optionally send text transcript too
            if also_text and result.get("ok"):
                await send_telegram_message(text, voice)
                
            if result.get("ok"):
                return {"success": True, "voice": voice, "also_text": also_text}
            return {"error": result.get("description", "Unknown error")}
            
        finally:
            os.unlink(temp_path)


async def check_status() -> dict:
    """Check if all bots are working."""
    results = {}
    async with aiohttp.ClientSession() as session:
        for name, token in BOT_TOKENS.items():
            url = f"https://api.telegram.org/bot{token}/getMe"
            try:
                async with session.get(url) as resp:
                    data = await resp.json()
                    if data.get("ok"):
                        results[name] = "✓ Connected"
                    else:
                        results[name] = f"✗ Error: {data.get('description')}"
            except Exception as e:
                results[name] = f"✗ Error: {str(e)}"
    return results


# ==============================================================================
# MCP PROTOCOL HANDLING
# ==============================================================================

def read_message():
    """Read a JSON-RPC message from stdin."""
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line)


def write_message(msg):
    """Write a JSON-RPC message to stdout."""
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def handle_initialize(msg):
    """Handle the initialize request."""
    return {
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {
                "name": "telegram-multi-bot",
                "version": "1.0.0"
            }
        }
    }


def handle_tools_list(msg):
    """Return the list of available tools."""
    tools = [
        {
            "name": "telegram_send",
            "description": "Send a text message on Telegram. Use 'sender' to specify which persona sends it.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to send"
                    },
                    "sender": {
                        "type": "string",
                        "description": f"Who sends: {', '.join(BOT_TOKENS.keys())}",
                        "default": list(BOT_TOKENS.keys())[0]
                    }
                },
                "required": ["message"]
            }
        },
        {
            "name": "voice_send",
            "description": "Send a voice message using ElevenLabs text-to-speech.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to convert to speech"
                    },
                    "voice": {
                        "type": "string",
                        "description": f"Which voice: {', '.join(VOICE_IDS.keys())}"
                    },
                    "also_text": {
                        "type": "boolean",
                        "description": "Also send text transcript (default: false)",
                        "default": False
                    }
                },
                "required": ["text", "voice"]
            }
        },
        {
            "name": "telegram_status",
            "description": "Check if all Telegram bots are connected and working.",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
    ]
    
    return {
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": {"tools": tools}
    }


def handle_tool_call(msg):
    """Handle a tool call request."""
    params = msg.get("params", {})
    tool_name = params.get("name")
    args = params.get("arguments", {})
    
    if tool_name == "telegram_send":
        result = asyncio.run(send_telegram_message(
            args.get("message", ""),
            args.get("sender", list(BOT_TOKENS.keys())[0])
        ))
    elif tool_name == "voice_send":
        result = asyncio.run(send_voice_message(
            args.get("text", ""),
            args.get("voice", ""),
            args.get("also_text", False)
        ))
    elif tool_name == "telegram_status":
        result = asyncio.run(check_status())
    else:
        result = {"error": f"Unknown tool: {tool_name}"}
    
    return {
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": {
            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
        }
    }


def main():
    """Main MCP server loop."""
    while True:
        msg = read_message()
        if msg is None:
            break
        
        method = msg.get("method", "")
        
        if method == "initialize":
            write_message(handle_initialize(msg))
        elif method == "notifications/initialized":
            pass  # Acknowledgment, no response needed
        elif method == "tools/list":
            write_message(handle_tools_list(msg))
        elif method == "tools/call":
            write_message(handle_tool_call(msg))
        else:
            # Unknown method
            if "id" in msg:
                write_message({
                    "jsonrpc": "2.0",
                    "id": msg["id"],
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                })


if __name__ == "__main__":
    main()
