---
name: transcribe
description: Format dictated messages for sending. Use when user says "transcribe", uses /transcribe command, or requests message cleanup/formatting from audio transcription. Context-aware: one message in groups, two in private chats.
---

# Transcribe

Format dictated messages into polished, send-ready text. Designed for voice-to-text workflows where the user dictates a message and needs it cleaned up for sending.

## Context Detection

Detect whether you're in a **group chat** or **private/direct chat** and adjust behavior accordingly.

**For Telegram:** Group chats have negative chat IDs (e.g., `-5134142498`), while private/direct chats have positive IDs. Check the message header `[Telegram ... id:XXXXX]` to determine context.

## How It Works

### In Group Chats

When transcribing in a group, send ONE message using the `message` tool:

**Transcription with style matching (user-specific):**
- **Start with @mention of sender** (e.g., "@simon: " or "@micha_9898: ")
- **Michael (Telegram ID: 14423006) ONLY:** Transform transcription using MICHA_STYLE.md:
  - Use ONLY his documented greetings, emojis, elongations, abbreviations
  - Match his tone, punctuation patterns, sign-offs
  - Preserve the core message content but express it how he would write it
  - **Keep it natural and casual** - not perfect grammar/capitalization if his style is relaxed
  - Flow and vibe > grammatical perfection (e.g., "am arbeiten" not "am Arbeiten" if that's his style)
  - Use his vocabulary choices ("supi", "mega geile", "gönnen", "in the hood" etc.)
- **All other users (including Simon):** Clean verbatim with grammar/punctuation corrections only. NO style matching.
- NO bold, italics, or markdown formatting

### In Private/Direct Chats (1-on-1)

When user provides transcribed audio (or text to format), send TWO separate Telegram messages using the `message` tool:

**Message 1: Clean Copy-Ready Text**
- Grammar and punctuation corrected
- NO formatting (no bold, italics, markdown)
- NO emojis or decorations
- NO preamble or wrapper text
- Just the message itself, ready to copy and paste
- Keep the original tone and language

**Message 2: Enhanced Reformulation**
- Improved phrasing and clarity
- Still keeps the original tone and intent
- Can suggest better word choices or structure
- Keep the original language

**Important:** Use the `message` tool to send each version as a separate Telegram message so the user can easily tap and copy whichever version they prefer.

### Iteration & Refinement

After transcribing, the user may request changes or improvements. Handle these conversationally:

**User says:** "Can you improve it?" / "Make it shorter" / "Make it more formal" / "Change the tone"
**Action:** Work with the previous transcription output—don't treat the request itself as new text to transcribe. Apply the requested changes and send TWO updated messages again.

**Examples of iteration requests:**
- "Can you make it more professional?"
- "Too long, can you shorten it?"
- "Remove the greeting"
- "Make it friendlier"
- "Can you improve the second version?"

When iterating, always output both the clean and enhanced versions again (not just the one being modified) so the user can choose between them.

## Language & Tone Detection

- Detect and preserve the language of the original message
- Maintain the tone (formal, casual, friendly, professional, etc.)
- If the user is dictating a message that starts with a greeting like "Hi [name]" or ends with "Cheers", preserve that structure

## Unclear Words

If any words in the transcription are unclear or ambiguous:
- Ask the user to type out the unclear word(s)
- Don't guess at names, technical terms, or specialized vocabulary

## Examples

**User dictates:**
"Hi John, hope you're doing well. Wanted to check in about the project timeline we discussed last week. Let me know when you have a moment to chat. Cheers."

**Message 1 (Clean):**
Hi John, hope you're doing well. Wanted to check in about the project timeline we discussed last week. Let me know when you have a moment to chat. Cheers.

**Message 2 (Enhanced):**
Hi John, hope you're doing well. I wanted to follow up on the project timeline we discussed last week. Let me know when you have a moment to chat. Cheers.

---

**User dictates (French):**
"Salut Marie, j'espère que tu vas bien. Je voulais te demander si tu as reçu le document que je t'ai envoyé hier."

**Message 1 (Clean):**
Salut Marie, j'espère que tu vas bien. Je voulais te demander si tu as reçu le document que je t'ai envoyé hier.

**Message 2 (Enhanced):**
Salut Marie, j'espère que tu vas bien. Je voulais savoir si tu as bien reçu le document que je t'ai envoyé hier.
