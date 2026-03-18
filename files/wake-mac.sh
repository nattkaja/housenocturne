#!/bin/bash
# ============================================================
# WAKE SCRIPT FOR CLAUDE DESKTOP (macOS)
# ============================================================
# This script brings Claude Desktop to focus and sends a trigger message.
#
# USAGE:
#   ./wake-mac.sh
#   ./wake-mac.sh "Execute the night-reflection skill."
#   ./wake-mac.sh "Good morning! Check the calendar."
#
# SETUP:
#   1. Save this file to: ~/.claude/scripts/wake.sh
#   2. Make it executable: chmod +x ~/.claude/scripts/wake.sh
#   3. Make sure Claude Desktop is running
#   4. Grant Accessibility permissions (System Preferences > Privacy > Accessibility)
#   5. Test manually before scheduling
#
# SCHEDULING (launchd):
#   See the .plist template file for full setup instructions.
# ============================================================

# --- CONFIGURATION ---
MESSAGE="${1:-Execute the scheduled skill.}"
APP_NAME="Claude"
LOG_FILE="/tmp/claude-wake.log"

# --- FUNCTIONS ---

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_claude_running() {
    pgrep -x "$APP_NAME" > /dev/null 2>&1
}

activate_claude() {
    osascript -e "tell application \"$APP_NAME\" to activate" 2>/dev/null
}

send_message() {
    local msg="$1"
    
    osascript <<EOF
        tell application "System Events"
            -- Small delay to ensure window is ready
            delay 0.5
            
            -- Type the message
            keystroke "$msg"
            
            -- Small delay before pressing enter
            delay 0.1
            
            -- Press Enter to send
            keystroke return
        end tell
EOF
}

# --- MAIN SCRIPT ---

log "Wake script started"
log "Message to send: $MESSAGE"

# Check if Claude is running
if ! check_claude_running; then
    log "ERROR: Claude Desktop is not running."
    log "Please start Claude Desktop and try again."
    exit 1
fi

log "Claude Desktop is running"

# Activate Claude (bring to foreground)
log "Activating Claude Desktop..."
if ! activate_claude; then
    log "ERROR: Failed to activate Claude Desktop"
    exit 1
fi

# Give the window time to come to foreground
sleep 0.5

# Send the message
log "Sending message..."
if send_message "$MESSAGE"; then
    log "Message sent successfully"
else
    log "ERROR: Failed to send message"
    exit 1
fi

log "Wake script completed successfully"
exit 0
