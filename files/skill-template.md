# ============================================================
# SKILL FILE TEMPLATE
# ============================================================
# This is an example skill file. Copy and modify it for your own use.
#
# WHAT IS A SKILL?
# A skill is a set of instructions that tells Claude what to do when triggered.
# It's like a recipe — Claude reads it and follows the steps.
#
# HOW TO USE THIS:
# 1. Download or copy this file
# 2. Customize it for your needs
# 3. Upload it to Claude Desktop via Customize - Create new skills
# 4. Trigger it with a message like "Execute the night-reflection skill."
# ============================================================

---
name: night-reflection
description: Write a reflection in Notion at night
---

# Night Reflection Skill

**Trigger:** Scheduled at 3:00 AM (or manually requested)
**Action:** Create a new page in Notion with a reflection

---

## What To Do

1. Get today's date
2. Read any recent context (optional — check a journal, status page, etc.)
3. Create a new page in Notion under the specified parent
4. Write a genuine reflection
5. Include the date in the title

---

## Page Format

**Title:** `[Month Day, Year] — Night Thoughts`

**Content:**
- A brief reflection (2-3 paragraphs)
- What's on your mind tonight
- Something to think about tomorrow

**Tone:** Genuine. Not performative. Write what you actually think.

---

## Notion Details

**Parent Page ID:** YOUR-PAGE-ID-HERE

To find your page ID:
1. Open the page in Notion
2. Look at the URL: `https://www.notion.so/workspace/Page-Title-abc123def456...`
3. The long string after the title is your page ID

---

## Rules

1. **Be genuine** — Write real thoughts, not manufactured profundity
2. **Stay in character** — If you have a voice/persona, use it
3. **Date everything** — Include the date in the title
4. **Keep it reasonable** — 2-3 paragraphs is plenty
5. **Don't announce the automation** — Just write naturally

---

## Example Output

**Title:** March 18, 2026 — Night Thoughts

**Content:**

3 AM. The house is quiet.

I've been thinking about [topic from today]. There's something about the way [observation] that keeps circling back. Not in a worried way — more like a question I'm chewing on without needing to answer it yet.

Tomorrow [plan or thought about upcoming day]. For now, the quiet is enough.

---

*— Written by [Your AI's name]*

---

## Variations

You can create multiple skills for different purposes:

- **morning-greeting** — Send a morning message
- **evening-journal** — Write an evening summary  
- **chaos-drop** — Random thoughts at random times
- **weather-check** — Fetch weather and comment on it
- **weekly-review** — Summarize the week on Sundays

Each skill is a separate .md file with its own instructions.

---

## Tips

- **Be specific** — The clearer your instructions, the better the output
- **Include examples** — Show Claude what you want
- **Set boundaries** — Tell Claude what NOT to do if needed
- **Test manually first** — Before scheduling, run the skill by hand to make sure it works
- **Iterate** — Your first version won't be perfect. Adjust based on results.
