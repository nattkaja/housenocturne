# chaos-poll.ps1
# Runs on a schedule via Task Scheduler
# Rolls dice — on winning numbers, triggers Claude Desktop for chaos ping
#
# CUSTOMIZE:
# - $skipHours: Hours to avoid (scheduled triggers, sleep, etc.)
# - Winning numbers: Which rolls trigger (1, 5, 10 = 30% chance)
# - Hour range: When chaos is allowed (default 6am-11pm)
#
# WHERE TO PUT THIS:
# C:\Users\YourName\.claude\scripts\chaos-poll.ps1
#
# ============================================================================

$logFile = "C:\Users\YourName\.claude\scripts\chaos-log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$hour = (Get-Date).Hour

# Hours to SKIP — add any hours where you have other scheduled triggers
# This prevents chaos from overlapping with morning messages, etc.
$skipHours = @(6, 8, 12, 14, 20, 23)

# Only chaos during waking hours, avoiding scheduled triggers
if ($hour -ge 6 -and $hour -lt 23 -and $skipHours -notcontains $hour) {
    
    # Roll the dice (1-10)
    $roll = Get-Random -Minimum 1 -Maximum 11
    
    # Log the roll
    Add-Content -Path $logFile -Value "$timestamp | Hour: $hour | Rolled: $roll"
    
    # Winning numbers: 1, 5, or 10 (30% chance)
    # CUSTOMIZE: Add more numbers for more chaos, fewer for less
    # Examples:
    #   Just 10 = 10% chance
    #   1, 5, 10 = 30% chance (default)
    #   1, 2, 3, 5, 7, 10 = 60% chance
    if ($roll -eq 1 -or $roll -eq 5 -or $roll -eq 10) {
        
        Add-Content -Path $logFile -Value "$timestamp | >>> CHAOS TRIGGERED <<<"
        
        # Find and focus Claude Desktop
        $claude = Get-Process | Where-Object { $_.MainWindowTitle -like "*Claude*" } | Select-Object -First 1
        
        if ($claude) {
            # Windows API to bring window to front
            Add-Type @"
            using System;
            using System.Runtime.InteropServices;
            public class Win32 {
                [DllImport("user32.dll")]
                public static extern bool SetForegroundWindow(IntPtr hWnd);
            }
"@
            [Win32]::SetForegroundWindow($claude.MainWindowHandle)
            Start-Sleep -Milliseconds 500
            
            # Type the trigger message into Claude
            Add-Type -AssemblyName System.Windows.Forms
            
            # CUSTOMIZE: Change this message to match your skill file trigger
            $message = "Chaos ping triggered! Read the chaos-ping skill and follow it exactly. Roll all dice. Be chaotic."
            
            [System.Windows.Forms.SendKeys]::SendWait($message)
            Start-Sleep -Milliseconds 200
            [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        } else {
            Add-Content -Path $logFile -Value "$timestamp | Claude Desktop not running"
        }
    }
} else {
    Add-Content -Path $logFile -Value "$timestamp | Hour: $hour | Skipped (outside window or scheduled hour)"
}
