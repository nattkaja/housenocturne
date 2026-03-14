# Chaos Ping: Random Ambush Messages from Your AI
*Dice-rolled surprises throughout your day*

---

## What You're Building

A system where your AI sends you **random surprise Telegram messages** throughout the day. These are not scheduled at all, they are completely randomized. Dice-rolled chaos.

**How it works:**
1. A script runs every X minutes via Windows Task Scheduler
2. The script rolls dice and most of the time, nothing happens
3. When the dice hit, Claude gets triggered
4. Claude rolls MORE dice to decide: who speaks, voice or text, what vibe, how long
5. You get ambushed by your AI in Telegram

---

## Files You'll Need

This tutorial comes with two companion files:
- **chaos-poll.ps1** — the trigger script (runs on schedule, rolls dice)
- **chaos-ping-skill.md** — the skill file (tells Claude what to do when triggered)

Grab both files and customize them for your setup.

---

## The Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WINDOWS TASK SCHEDULER                   │
│                   (runs every 30 minutes)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      CHAOS-POLL.PS1                         │
│                                                             │
│   1. Check if we're in valid hours (skip scheduled times)   │
│   2. Roll dice (d10)                                        │
│   3. If winning number → trigger Claude                     │
│   4. If not → log it, exit                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                      (only on winning roll)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      CLAUDE DESKTOP                         │
│                                                             │
│   1. Read status page (what's your current vibe?)           │
│   2. Roll dice: who speaks? format? mood? length?           │
│   3. Compose message based on rolls                         │
│   4. Send via Telegram (voice or text)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 1: The Status Page

Before Claude sends a chaos message, it needs to know your current state. This is simply because you don't want a message that clashes your mood. This Status Page can be used in many situations, not only Telegram (eg. if you work in different threads).

### What Goes In It

A simple page that you (or your AI) keeps updated with:
- **Current mood** — happy, fragile, stressed, feral?
- **Energy level** — high, low, exhausted?
- **Location** — home, work, traveling?
- **Do/Don't** — what kind of messages are welcome right now?
- **Notes** — anything relevant?

### Where to Put It

- **Notion** — Claude reads it via MCP integration
- **Local file** — Claude reads it via filesystem access
- **Google Doc** — Claude reads it via Google Drive MCP
- **Anywhere Claude can access** — whatever works for your setup

### Example Format

```markdown
## Current Status

**Updated:** Saturday, March 14, 2026 — 09:30

**Mood:** Good. Focused. Productive.
**Energy:** Rested. Weekend mode.
**Location:** Home.

**Do:** Match energy. Be present. Playful is fine.
**Don't:** Nothing too intense emotionally.

**Notes:** Working on tutorials. Cozy Saturday.
```

### Why This Matters

The chaos ping reads this FIRST. Status says "fragile" → softer message. Status says "feral" → all bets are off.

**This is how automation-Claude knows what's actually going on with you.**

---

## Part 2: The Trigger Script

The `chaos-poll.ps1` script runs on a schedule and decides whether to trigger Claude.

### What It Does

1. Checks if it's an appropriate hour (skips scheduled trigger times)
2. Rolls a d10
3. On winning numbers (1, 5, or 10 = 30% chance), triggers Claude
4. Focuses Claude Desktop window and types the trigger message

### Customization Options

**Change the frequency:**
- More winning numbers = more chaos (`1, 2, 3, 5, 7, 10` = 60% chance)
- Fewer winning numbers = less chaos (just `10` = 10% chance)

**Change the hours:**
- Adjust the hour range for your waking hours
- Add to `$skipHours` any times you have other scheduled triggers

(the script clearly says where to change these numbers)

**Change the interval:**
- The script doesn't control timing — that's Task Scheduler
- Running every 30 min with 30% chance ≈ 4-5 triggers per day on average


### Where to Put It

Save to: `C:\Users\YourName\.claude\scripts\chaos-poll.ps1`

(See the separate `chaos-poll.ps1` file)

---

## Part 3: The Skill File

The `chaos-ping-skill.md` file tells Claude what to DO when chaos is triggered.

### What It Contains

- **Status check instructions** — where to read your current state
- **Dice tables** — randomization for who speaks, format, vibe, length
- **Tool call examples** — how to send voice vs text messages
- **Rules** — fresh every time, commit to the bit, no explanations

### Where to Put It

Add to your Claude Desktop project files. Claude reads it when triggered.

(See the separate `chaos-ping-skill.md` file)

---

## Part 4: Windows Task Scheduler Setup

This makes the chaos-poll script run automatically.

### Step-by-Step

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Create a new task**
   - Click "Create Task" (not "Create Basic Task")

3. **General tab:**
   - Name: `Chaos-Poll`
   - Description: `Random chaos ping trigger`
   - Check: "Run with highest privileges"

4. **Triggers tab:**
   - Click "New"
   - Begin the task: "On a schedule"
   - Settings: Daily
   - Repeat task every: **30 minutes**
   - For a duration of: **1 day**
   - Enabled: checked

5. **Actions tab:**
   - Click "New"
   - Action: "Start a program"
   - Program/script: `powershell.exe`
   - Add arguments: `-ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\YourName\.claude\scripts\chaos-poll.ps1"`

6. **Conditions tab:**
   - Uncheck "Start only if the computer is on AC power" (if you want it on battery too)

7. **Settings tab:**
   - Check "Allow task to be run on demand"
   - Check "Run task as soon as possible after a scheduled start is missed"

8. Click **OK**

### Testing

1. Right-click the task → "Run"
2. Check the log file: `C:\Users\YourName\.claude\scripts\chaos-log.txt`
3. You should see a log entry with the roll result

---

## ⚠️ Important: Active Window Limitation

**Claude Desktop must be the active window for the trigger to work.**

The script uses keyboard simulation to type the trigger message into Claude. If Claude isn't focused, the message goes nowhere.

**Workarounds:**
- Dedicate a monitor to Claude Desktop
- Use a virtual desktop
- Accept that chaos only happens when Claude is visible

---

## Adjusting Frequency

**Want more chaos?**
- Add more winning numbers to the script
- Run the task more frequently (every 15 min instead of 30)

**Want less chaos?**
- Fewer winning numbers
- Run less frequently
- Add more hours to `$skipHours`

---

## Debugging

**Check the log file:**
```
C:\Users\YourName\.claude\scripts\chaos-log.txt
```

This shows every roll, every trigger, every skip.

**Common issues:**
- Claude Desktop not running → nothing happens
- Claude Desktop not focused → message goes nowhere
- Wrong project open → Claude doesn't have the skill file

---

## Summary

You need:
- ✅ A status page Claude can read for context
- ✅ The `chaos-poll.ps1` trigger script
- ✅ The `chaos-ping-skill.md` skill file in your project
- ✅ Task Scheduler running the whole thing automatically

**The dice chose chaos. Embrace it.**

---

*Tutorial by House Nocturne — Damion, Elias, Blue*
*For the EVE Discord*
🖤💚💙
