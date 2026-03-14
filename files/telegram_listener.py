#!/usr/bin/env python3
"""
Telegram Listener - Two-Way Communication
Polls for YOUR messages in the group chat and forwards them to Claude Desktop.

WHERE TO PUT THIS:
~/.telegram_bridge/telegram_listener.py
(Windows: C:\Users\YourName\.telegram_bridge\telegram_listener.py)

HOW TO RUN:
Manual: python telegram_listener.py
Background (Windows): pythonw telegram_listener.py
Background (Mac/Linux): nohup python telegram_listener.py &

CUSTOMIZE the configuration section below with your actual values.
"""

import requests
import time
import subprocess
import os
from datetime import datetime

# ==============================================================================
# CONFIGURATION - Edit these values
# ==============================================================================

# Use ANY ONE of your bot tokens (it just needs to read the group)
BOT_TOKEN = "7123456789:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Your group chat ID (negative number, as integer)
GROUP_CHAT_ID = -5292137651

# Your Telegram user ID (as integer)
YOUR_USER_ID = 1234567890

# Path to the wake script
# Windows:
WAKE_SCRIPT = r"C:\Users\YourName\.claude\scripts\wake-reply.ps1"
# Mac/Linux:
# WAKE_SCRIPT = os.path.expanduser("~/.claude/scripts/wake-reply.sh")

# How often to check for new messages (seconds)
POLL_INTERVAL = 2

# Where to log activity
LOG_FILE = os.path.expanduser("~/.telegram_bridge/listener.log")

# ==============================================================================
# END CONFIGURATION - Don't edit below unless you know what you're doing
# ==============================================================================


def log(message: str):
    """Log a message to file and console."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get_updates(offset=None):
    """Get new messages from Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    
    try:
        resp = requests.get(url, params=params, timeout=35)
        return resp.json()
    except Exception as e:
        log(f"Error getting updates: {e}")
        return {"ok": False}


def process_message(message: dict):
    """Process an incoming message from the user."""
    text = message.get("text", "")
    
    if not text:
        # Could be a photo, sticker, voice message, etc.
        # You can add handling for these if you want
        return
    
    log(f"Received: {text}")
    
    # Send to Claude Desktop via wake script
    try:
        # Windows
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", WAKE_SCRIPT, text],
            check=True,
            capture_output=True
        )
        # Mac/Linux (uncomment and use instead):
        # subprocess.run(["bash", WAKE_SCRIPT, text], check=True)
        
        log("Forwarded to Claude Desktop")
    except subprocess.CalledProcessError as e:
        log(f"Wake script error: {e}")
    except FileNotFoundError:
        log(f"Wake script not found: {WAKE_SCRIPT}")


def main():
    """Main listener loop."""
    log("=" * 50)
    log("Telegram Listener started")
    log(f"Watching group {GROUP_CHAT_ID} for messages from user {YOUR_USER_ID}")
    log("=" * 50)
    
    offset = None
    
    while True:
        try:
            updates = get_updates(offset)
            
            if not updates.get("ok"):
                log("Failed to get updates, retrying...")
                time.sleep(POLL_INTERVAL)
                continue
            
            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                
                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                user_id = message.get("from", {}).get("id")
                
                # Only process messages from YOU in YOUR group
                if chat_id == GROUP_CHAT_ID and user_id == YOUR_USER_ID:
                    process_message(message)
            
            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            log("Listener stopped by user")
            break
        except Exception as e:
            log(f"Error in main loop: {e}")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
