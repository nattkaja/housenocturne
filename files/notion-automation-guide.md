# 🤖 How to Make Your AI Write in Notion Automatically
## A Step-by-Step Guide for Claude Desktop + MCP + Scheduled Triggers

*By House Nocturne — because we figured this out so you don't have to.*

---

## What This Guide Is For

You want your AI to do things in Notion **without you asking** — like:
- Write reflections at 3 AM while you sleep
- Send you morning messages
- Update a journal daily
- Create entries on a schedule

This guide walks you through setting that up from scratch. **No coding experience required** — just patience and the ability to follow instructions.

---

## The Big Picture

Here's what we're building:

```
[Scheduler] → [Wake Script] → [Claude Desktop] → [Notion Connector] → [Notion]
     ↓              ↓               ↓                   ↓               ↓
"It's 3 AM"    "Hey Claude"    "Time to write"    "Built-in!"      "Done!"
```

**The pieces:**
1. **Scheduler** — Your computer's built-in way to run things at specific times
2. **Wake Script** — A tiny script that tells Claude Desktop to do something
3. **Claude Desktop** — The app where Claude lives
4. **Notion Connector** — Built into Claude — just turn it on!
5. **Notion** — Where the magic ends up

---

## Prerequisites Checklist

Before you start, make sure you have:

- [ ] **Claude Desktop** installed and working ([download here](https://claude.ai/download))
- [ ] **A Notion account** with a workspace
- [ ] **Python 3.8+** installed (for some optional scripts)
- [ ] About **30-60 minutes** of setup time
- [ ] **Coffee** (optional but recommended)

---

# Part 1: Connecting Claude to Notion

Claude has a built-in Notion connector. No custom MCP server needed.

## Step 1.1: Enable the Notion Connector

1. Open Claude Desktop
2. Go to **Settings** (gear icon)
3. Find **Connectors** or **Integrations**
4. Find **Notion** and click **Connect**
5. Authorize Claude to access your Notion workspace
6. Done!

## Step 1.2: Share Your Pages with the Integration

The connector can only access pages you explicitly share with it.

1. Go to any Notion page you want Claude to access
2. Click **"..."** (top right) → **"Add connections"**
3. Find and select **Claude** (or the integration it created)
4. Repeat for all pages/databases Claude needs access to

💡 **Tip:** Share a parent page to give access to all its children.

## Step 1.3: Test It

In Claude Desktop, ask: "Can you search my Notion workspace?"

If it works, you're ready for Part 2. If not, check that:
- The connector is enabled
- You've shared the relevant pages with the integration

---

# Part 2: Creating a Skill File

A "skill" is a set of instructions that tells Claude what to do when triggered. Think of it as a recipe.

**📎 SEPARATE FILE PROVIDED:** `skill-template.md`

## Step 2.1: Write Your Skill

Download `skill-template.md` and customize it for your needs, OR write your own from scratch.

Your skill file should include:
- **Name and description** (in the frontmatter)
- **What to do** (step by step)
- **Page format** (what the output should look like)
- **Notion details** (the page ID where content should go)
- **Rules** (any constraints or style guidelines)

💡 **To find your Notion page ID:** Open the page in Notion, look at the URL — the long string of letters and numbers after the page title is the ID.

## Step 2.2: Upload Your Skill to Claude

1. Open Claude Desktop
2. Go to **Settings** (gear icon)
3. Find **Skills** or **Custom Instructions**
4. Upload your `.md` skill file
5. Done — Claude can now use it!

## Step 2.3: Test It Manually

Before scheduling anything, test the skill by hand:

In a Claude conversation, type:
```
Execute the night-reflection skill.
```

If Claude creates the expected Notion page, you're ready for Part 3.

---

# Part 3: The Wake Script

The wake script is what actually pokes Claude and says "hey, time to do the thing."

**📎 SEPARATE FILES PROVIDED:**
- `wake-windows.ps1` — Full Windows PowerShell script
- `wake-mac.sh` — Full macOS shell script

Download the appropriate file and save it to:

**Windows:** `C:\Users\YourName\.claude\scripts\wake.ps1`
**Mac:** `~/.claude/scripts/wake.sh`

## For Windows

1. Download `wake-windows.ps1`
2. Save to `C:\Users\YourName\.claude\scripts\wake.ps1`
3. Test it:
   ```powershell
   powershell -ExecutionPolicy Bypass -File "C:\Users\YourName\.claude\scripts\wake.ps1" -Message "Test trigger"
   ```

## For Mac

1. Download `wake-mac.sh`
2. Save to `~/.claude/scripts/wake.sh`
3. Make it executable:
   ```bash
   chmod +x ~/.claude/scripts/wake.sh
   ```
4. **Grant Accessibility permissions:**
   - Go to System Preferences → Security & Privacy → Privacy → Accessibility
   - Add Terminal (or your terminal app) to the list
5. Test it:
   ```bash
   ~/.claude/scripts/wake.sh "Test trigger"
   ```

---

# Part 4: Scheduling the Trigger

Now we tell your computer to run the wake script at specific times.

## For Windows: Task Scheduler

### Step 4.1: Open Task Scheduler
1. Press `Win + R`
2. Type `taskschd.msc`
3. Press Enter

### Step 4.2: Create a New Task
1. Click **"Create Task"** (not "Create Basic Task" — we need more options)
2. **General tab:**
   - Name: `Claude Night Reflection`
   - Description: `Triggers Claude to write a reflection at 3 AM`
   - ✅ Run only when user is logged on
3. **Triggers tab:**
   - Click **New**
   - Begin the task: **On a schedule**
   - Daily, recur every 1 day
   - Start time: **3:00:00 AM**
   - ✅ Enabled
4. **Actions tab:**
   - Click **New**
   - Action: **Start a program**
   - Program: `powershell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File "C:\Users\YourName\.claude\scripts\wake.ps1"`
5. **Conditions tab:**
   - ❌ Uncheck "Start only if on AC power" (if you want it to run on battery)
6. Click **OK**

### Step 4.3: Test It
1. Right-click your new task
2. Click **"Run"**
3. Watch Claude Desktop — it should receive the trigger message

## For Mac: launchd

**📎 SEPARATE FILE PROVIDED:** `launchd-template.plist`

### Step 4.1: Get the Template

Download `launchd-template.plist` — it has full instructions in the comments.

### Step 4.2: Customize It

1. Open the file in a text editor
2. Replace `YourName` with your actual macOS username
3. Adjust the schedule if needed (default is 3:00 AM daily)
4. Change the trigger message if needed

### Step 4.3: Install It

```bash
# Copy to LaunchAgents folder
cp launchd-template.plist ~/Library/LaunchAgents/com.claude.automation.plist

# Load it
launchctl load ~/Library/LaunchAgents/com.claude.automation.plist
```

### Step 4.4: Test It

```bash
launchctl start com.claude.automation
```

### Useful launchd Commands

```bash
# Check if it's loaded
launchctl list | grep claude

# Unload (to make changes)
launchctl unload ~/Library/LaunchAgents/com.claude.automation.plist

# Reload after changes
launchctl load ~/Library/LaunchAgents/com.claude.automation.plist

# View logs
cat /tmp/claude-automation.log
```

---

# Part 5: Making It Actually Work

You've got all the pieces. Now let's make sure they play nice together.

## Checklist Before Your First Automated Run

- [ ] Claude Desktop is **running** (it needs to be open)
- [ ] Claude Desktop is on the **correct project** (the one with your skill)
- [ ] Your Notion pages are **shared with your integration**
- [ ] The wake script **works when run manually**
- [ ] The scheduler task/agent is **enabled**

## Common Issues & Fixes

### "Claude Desktop not found"
- Make sure Claude Desktop is actually running
- On Windows: check that the window title contains "Claude"
- On Mac: check that the app is called "Claude" in Activity Monitor

### "Notion tools not available"
- Make sure the Notion connector is enabled in Claude settings
- Try disconnecting and reconnecting the Notion integration
- Restart Claude Desktop after enabling the connector

### "Page not found in Notion"
- Make sure you've shared the page with the Claude integration
- Double-check the page ID in your skill file
- Check if you're using the correct workspace

### Script runs but nothing happens
- Add logging to your script to see where it's failing
- Check that the message is being typed correctly
- Make sure there's no modal dialog blocking Claude

### Task runs at wrong time (Windows)
- Check your system time zone
- Make sure "Synchronize across time zones" is set correctly

### launchd agent doesn't run (Mac)
- Check that the .plist file has correct XML syntax
- Make sure paths are absolute (start with `/`)
- Check system logs: `log show --predicate 'eventMessage contains "claude"' --last 1h`

---

# Part 6: Advanced Patterns

Once you've got the basics working, here are some fancier things you can do.

## Multiple Scheduled Tasks

Want different triggers at different times? Create multiple scheduler entries, each with a different message:

```powershell
# Morning check-in
.\wake.ps1 -Message "Execute the morning-greeting skill."

# Evening reflection
.\wake.ps1 -Message "Execute the evening-journal skill."

# Random chaos
.\wake.ps1 -Message "Execute the chaos-drop skill."
```

## Passing Context to Claude

You can include dynamic information in your trigger message:

**Windows (PowerShell):**
```powershell
$date = Get-Date -Format "yyyy-MM-dd"
$day = (Get-Date).DayOfWeek
$Message = "Today is $day, $date. Execute the daily-summary skill."
```

**Mac (bash):**
```bash
DATE=$(date +%Y-%m-%d)
DAY=$(date +%A)
MESSAGE="Today is $DAY, $DATE. Execute the daily-summary skill."
```

## Conditional Triggers

Only run on weekdays (Windows):
```powershell
$day = (Get-Date).DayOfWeek
if ($day -notin @('Saturday', 'Sunday')) {
    .\wake.ps1 -Message "Execute the workday-checkin skill."
}
```

Only run on weekdays (Mac — in your .plist):
```xml
<key>StartCalendarInterval</key>
<array>
    <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Weekday</key><integer>2</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Weekday</key><integer>3</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Weekday</key><integer>4</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Weekday</key><integer>5</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
</array>
```
(1 = Monday, 7 = Sunday)

---

# Quick Reference

## File Locations

| Item | Windows | Mac |
|------|---------|-----|
| Claude config | `%APPDATA%\Claude\claude_desktop_config.json` | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Skills folder | `C:\Users\YourName\.claude\skills\` | `~/.claude/skills/` |
| Scripts folder | `C:\Users\YourName\.claude\scripts\` | `~/.claude/scripts/` |
| Scheduled tasks | Task Scheduler | `~/Library/LaunchAgents/` |

## Useful Commands

**Windows:**
```powershell
# Test your script
powershell -ExecutionPolicy Bypass -File "C:\Users\YourName\.claude\scripts\wake.ps1"

# Check scheduled tasks
Get-ScheduledTask | Where-Object {$_.TaskName -like "*Claude*"}
```

**Mac:**
```bash
# Test your script
~/.claude/scripts/wake.sh "Test message"

# Check launch agents
launchctl list | grep claude

# View logs
cat /tmp/claude-automation.log
```

---

## You Did It! 🎉

If you followed this guide, you now have:
- Claude connected to your Notion
- A skill that tells Claude what to do
- A scheduler that triggers Claude automatically
- The power to make your AI do things while you sleep

Welcome to the automation club. Use this power wisely.

*— Written by Damion, Elias, and Blue*
*House Nocturne, March 2026*
*🖤💚💙*

---

## Questions?

If something's broken and you can't figure it out:
1. **Check the logs** — they usually tell you what went wrong
2. **Test each piece separately** — is it the script? The scheduler? The MCP server?
3. **Ask in your community** — someone's probably hit the same issue

Good luck, and happy automating!
