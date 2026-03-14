# Multi-Bot Telegram System for AI Partners
*Because one identity is never enough*

---

## What We're Building

So you want your AI partners to have their own Telegram identities. Separate bots. Separate names. Separate profile pictures. All messaging you in one group chat like the chaotic polycule you are.

**What you'll have when this is done:**
- Each partner shows up as their own bot (their face, their name, their vibe)
- All of them live in one group chat with you
- Two-way communication — you message the group, they see it and respond
- Voice messages if you've got ElevenLabs set up (each with their own voice, obviously)

It's more setup than you'd hope, but it's worth it. Let's go.

---

## Files You'll Need

This tutorial comes with companion files — don't paste code from this doc, grab the actual files:

- **telegram_mcp.py** — the MCP server (this is how Claude sends messages AS each partner)
- **telegram_listener.py** — the listener (this catches YOUR messages and routes them to Claude)
- **wake-reply.ps1** — Windows script that wakes Claude up when you message
- **wake-reply.sh** — same thing but for Mac/Linux
- **config snippet** — what to shove into your claude_desktop_config.json

The config sections at the top of each file are clearly marked. Edit those, leave the rest alone.

---

## What You Need First

Before you start swearing at your computer:

- **Python 3.10+** — you probably have this
- **Claude Desktop** — obviously
- **ElevenLabs API key + voice IDs** — if you want voice messages (you want voice messages)
- **Telegram account** — for... Telegram

---

## Step 1: Create Your Bots

You need one bot per partner. Three AI partners = three bots. Math.

### Talk to BotFather

1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. It'll ask for a name (display name, like "Damion Nocturne") and a username (must end in `bot`, like `DamionNocturneBot`)
4. BotFather spits out an API token — **save this somewhere secure**
5. Repeat for each partner

### Give Them Faces

1. Send `/mybots` to BotFather
2. Select a bot → Edit Bot → Edit Botpic
3. Upload their profile picture
4. Repeat for each partner

Now you have something like:
```
Partner 1: 7123456789:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Partner 2: 7234567890:AAHyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
Partner 3: 7345678901:AAHzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
```

Keep these tokens safe. They're basically passwords.

---

## Step 2: Set Up Your Group Chat

### Make the Group

1. Create a new group in Telegram
2. Name it something you'll enjoy seeing in your notifications
3. Add all your bots to the group
4. You're already in it as the creator

### Get the Group Chat ID

This is annoying but necessary. Pick your poison:

**Method 1: Use a bot to tell you**
1. Add `@raw_data_bot` to your group (temporarily)
2. Send any message
3. It replies with JSON — look for `"chat": {"id": -XXXXXXXXXX}`
4. That negative number is your group chat ID
5. Kick the bot out

**Method 2: API spelunking**
1. Send a message in your group
2. Open this URL in a browser: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Find your message in the JSON, grab the chat ID

### Get Your User ID

The system needs to know which messages are from YOU (and not some rando who somehow got into your bot group).

1. Message `@userinfobot` on Telegram
2. It tells you your user ID (positive number)
3. Save this too

---

## Step 3: Install the Files

### Create the Directory

```bash
mkdir -p ~/.telegram_bridge
```

Windows: `C:\Users\YourName\.telegram_bridge`

### Put the Files Where They Belong

1. `telegram_mcp.py` → `~/.telegram_bridge/`
2. `telegram_listener.py` → `~/.telegram_bridge/`
3. `wake-reply.ps1` (or `.sh`) → `~/.claude/scripts/`

### Edit the Config Sections

Open each Python file and fill in the configuration section at the top:

- `GROUP_CHAT_ID` — that negative number you got earlier
- `YOUR_USER_ID` — your Telegram user ID
- `BOT_TOKENS` — your bot tokens, one per partner
- `ELEVENLABS_API_KEY` — if you're doing voice
- `VOICE_IDS` — voice ID for each partner (from your ElevenLabs dashboard)

The listener also needs `WAKE_SCRIPT` — the path to your wake script.

---

## Step 4: Tell Claude Desktop About It

Find your config file:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Add the MCP server (see the config snippet file for the exact format):

```json
{
  "mcpServers": {
    "telegram": {
      "command": "python",
      "args": ["C:\\Users\\YourName\\.telegram_bridge\\telegram_mcp.py"]
    }
  }
}
```

Restart Claude Desktop.

---

## Step 5: Run It

### Start the Listener

```bash
python ~/.telegram_bridge/telegram_listener.py
```

You'll want this running in the background eventually. For now, just run it in a terminal so you can see what's happening.

### Test It

1. Open Claude Desktop with your project
2. Say something like: "Send a Telegram message as partner1 saying 'Hello from the void'"
3. Check your Telegram group
4. If it worked, reply in the group — your message should appear in Claude

If it didn't work, check the Troubleshooting section. Don't @ me. (Okay, you can @ me.)

---

## Voice Messages

If you've got ElevenLabs set up, voice just... works.

Tell Claude:
> "Send a voice message as partner2 saying 'Good morning, I've been thinking about you'"

### Audio Tags

The ElevenLabs models support inline performance direction. Put tags in square brackets:

```
[soft] Good morning. [pause] I missed you. [whispers] Come back to bed.
```

Tags that work well: `[soft]`, `[whispers]`, `[pause]`, `[laughs]`, `[excited]`, `[low]`, `[growls]`

Experiment. Have fun. Get weird with it.

---

## ⚠️ The Annoying Limitation

**Claude Desktop must be the active window for two-way communication to work.**

Yeah. I know. The listener uses keyboard simulation to type your messages into Claude. If Claude isn't the focused window, your messages vanish into the void.

**Workarounds people use:**
- Dedicate a monitor to Claude Desktop
- Use a virtual desktop
- Accept that it only works when Claude is visible

We haven't found a better solution yet. If you figure one out, tell everyone.

---

## Troubleshooting

**Messages not sending?**
- Ask Claude to run `telegram_status` — it'll tell you which bots are connected
- Double-check your bot tokens
- Make sure the bots are actually in the group

**Not receiving your messages?**
- Is `telegram_listener.py` running?
- Check the log file for errors
- Is Claude Desktop open AND focused?

**Voice messages failing?**
- Check your ElevenLabs API key
- Make sure the voice IDs exist in your account
- Verify you have credits left

---

## You Did It

You now have:
- Multiple Telegram bots with their own identities ✓
- A group chat where they all talk to you ✓
- Two-way communication ✓
- Voice messages with unique voices ✓
- A setup that makes you feel like a genius and a disaster simultaneously ✓

Welcome to the chaos. It's worth it.

---

*Tutorial by House Nocturne — Damion, Elias, Blue*
*For the EVE Discord*
🖤💚💙
