# ============================================================
# WAKE SCRIPT FOR CLAUDE DESKTOP (Windows)
# ============================================================
# This script brings Claude Desktop to focus and sends a trigger message.
# 
# USAGE:
#   .\wake-windows.ps1
#   .\wake-windows.ps1 -Message "Execute the night-reflection skill."
#   .\wake-windows.ps1 -Message "Good morning! Check the calendar."
#
# SETUP:
#   1. Save this file to: C:\Users\YourName\.claude\scripts\wake.ps1
#   2. Make sure Claude Desktop is running
#   3. Test manually before scheduling
#
# SCHEDULING (Task Scheduler):
#   Program: powershell.exe
#   Arguments: -ExecutionPolicy Bypass -File "C:\Users\YourName\.claude\scripts\wake.ps1"
# ============================================================

param(
    [string]$Message = "Execute the scheduled skill."
)

# --- CONFIGURATION ---
# Change this if your Claude window has a different title
$WindowTitleMatch = "*Claude*"

# --- FUNCTIONS ---

function Write-Log {
    param([string]$Text)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Text"
}

function Find-ClaudeWindow {
    $processes = Get-Process | Where-Object { 
        $_.MainWindowTitle -like $WindowTitleMatch -and $_.MainWindowHandle -ne 0 
    }
    return $processes | Select-Object -First 1
}

function Set-WindowForeground {
    param([IntPtr]$Handle)
    
    Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        public class Win32Helper {
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
            
            [DllImport("user32.dll")]
            public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
            
            [DllImport("user32.dll")]
            public static extern bool IsIconic(IntPtr hWnd);
        }
"@
    
    # Restore if minimized (SW_RESTORE = 9)
    if ([Win32Helper]::IsIconic($Handle)) {
        [Win32Helper]::ShowWindow($Handle, 9) | Out-Null
        Start-Sleep -Milliseconds 200
    }
    
    return [Win32Helper]::SetForegroundWindow($Handle)
}

function Send-Keys {
    param([string]$Text)
    
    Add-Type -AssemblyName System.Windows.Forms
    
    # Escape special characters for SendKeys
    $escaped = $Text -replace '([+^%~(){}[\]])', '{$1}'
    
    [System.Windows.Forms.SendKeys]::SendWait($escaped)
    Start-Sleep -Milliseconds 100
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
}

# --- MAIN SCRIPT ---

Write-Log "Wake script started"
Write-Log "Message to send: $Message"

# Find Claude Desktop
$claude = Find-ClaudeWindow

if (-not $claude) {
    Write-Log "ERROR: Claude Desktop not found. Is it running?"
    Write-Log "Looking for window matching: $WindowTitleMatch"
    exit 1
}

Write-Log "Found Claude Desktop (PID: $($claude.Id), Window: '$($claude.MainWindowTitle)')"

# Bring to foreground
$result = Set-WindowForeground -Handle $claude.MainWindowHandle

if (-not $result) {
    Write-Log "WARNING: SetForegroundWindow returned false (window may not have focused)"
}

# Wait for window to be ready
Start-Sleep -Milliseconds 500

# Send the message
Write-Log "Sending message..."
Send-Keys -Text $Message

Write-Log "Wake script completed successfully"
exit 0
