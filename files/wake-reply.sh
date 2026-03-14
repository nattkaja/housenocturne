#!/bin/bash
# wake-reply.sh
# Brings Claude Desktop to foreground and types the message (Mac version)
#
# WHERE TO PUT THIS:
# ~/.claude/scripts/wake-reply.sh
#
# MAKE EXECUTABLE:
# chmod +x ~/.claude/scripts/wake-reply.sh
#
# This is called by telegram_listener.py when you send a message in Telegram.

MESSAGE="$1"

# Bring Claude to front (Mac)
osascript -e 'tell application "Claude" to activate'
sleep 0.5

# Type the message with [Telegram] prefix
osascript -e "tell application \"System Events\" to keystroke \"[Telegram] $MESSAGE\""
osascript -e 'tell application "System Events" to keystroke return'

# NOTE FOR LINUX USERS:
# Replace the osascript lines with xdotool:
# xdotool search --name "Claude" windowactivate
# sleep 0.5
# xdotool type "[Telegram] $MESSAGE"
# xdotool key Return
