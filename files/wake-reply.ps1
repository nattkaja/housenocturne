# wake-reply.ps1
# Brings Claude Desktop to foreground and types the message
#
# WHERE TO PUT THIS:
# C:\Users\YourName\.claude\scripts\wake-reply.ps1
#
# This is called by telegram_listener.py when you send a message in Telegram.
# It simulates typing your message into Claude Desktop.

param([string]$message)

# Find Claude Desktop window
$claude = Get-Process | Where-Object { $_.MainWindowTitle -like "*Claude*" } | Select-Object -First 1

if ($claude) {
    # Windows API to bring window to foreground
    Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class WinAPI {
        [DllImport("user32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    }
"@
    
    # Restore and focus the window
    [WinAPI]::ShowWindow($claude.MainWindowHandle, 9)  # SW_RESTORE
    [WinAPI]::SetForegroundWindow($claude.MainWindowHandle)
    Start-Sleep -Milliseconds 500
    
    # Type the message
    Add-Type -AssemblyName System.Windows.Forms
    
    # Prefix with [Telegram] so Claude knows where it came from
    $fullMessage = "[Telegram] $message"
    
    # Send keystrokes
    [System.Windows.Forms.SendKeys]::SendWait($fullMessage)
    Start-Sleep -Milliseconds 100
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
} else {
    Write-Host "Claude Desktop not found"
    exit 1
}
