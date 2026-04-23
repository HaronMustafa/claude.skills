---
name: linkedin-aiing-post
description: >
  Generate weekly LinkedIn "How to AI" posts for the AIING brand. Use this skill whenever the user
  asks to create a LinkedIn post, learning card, AI tip post, weekly AI content, or anything related
  to teaching AI tool usage on LinkedIn. The skill produces: (1) short punchy dot-point LinkedIn copy
  and (2) a branded .png learning card featuring the AIING logo and tool icons. Trigger this skill
  for any request mentioning "LinkedIn post", "AI tip", "learning card", "AIING post", "weekly post",
  "how to AI", or requests to create shareable AI education content.
---

# LinkedIn AIING Post Skill

Generates a weekly "How to AI" LinkedIn post + branded PNG learning card for the AIING brand.

## What This Skill Produces

1. **LinkedIn copy** — short, punchy dot-point post ready to paste into LinkedIn
2. **Branded PNG card** — 1080×1350px (portrait, LinkedIn-optimised) with:
   - AIING logo (top-left)
   - Post title / hook
   - Tip sections with icons for each AI tool
   - Clean brand-consistent design

---

## Step-by-Step Workflow

### Step 1 — Clarify the topic (if not provided)

Ask the user ONE question if topic is missing:
> "What AI tool or topic should this week's post cover? (e.g. Claude Projects, Gemini Deep Research, Perplexity, Cursor, Midjourney — or should I pick a trending one?)"

If the user says "pick one" or gives no preference, **choose the most trending tool right now** using web search.

### Step 2 — Research from Authoritative Sources

Use web search — **always** check official docs before drafting. Do not fabricate features. Prioritise:

**Tier 1 — Official docs (always check first):**
- Claude: `docs.anthropic.com` | ChatGPT: `platform.openai.com/docs`
- Gemini: `ai.google.dev` | Perplexity: `docs.perplexity.ai`
- Cursor: `docs.cursor.com` | ElevenLabs: `elevenlabs.io/docs`
- Midjourney: `docs.midjourney.com` | Runway: `runwayml.com/blog`

**Tier 2 — Dev docs & tooling platforms (great for meta/tooling posts):**
- Mintlify (`mintlify.com/blog`) — AI-native developer documentation
- GitBook (`gitbook.com/blog`) — technical knowledge bases & GitHub integration
- ReadMe (`readme.com/blog`) — API documentation as a product (AI audit features)
- Redocly (`redocly.com/blog`) — OpenAPI-first workflows, AI-powered search
- Swimm (`swimm.io/blog`) — code-coupled docs that auto-update with code changes
- Fern (`buildwithfern.com/blog`) — Stripe-like API docs with built-in AI chat
- Scribe (`scribehow.com/blog`) — browser extension that auto-creates step-by-step guides
- Document360, Apidog, Theneo, DocuWriter.ai — enterprise & automated doc tools

**Tier 3 — High-quality editorial:**
- `anthropic.com/research`, `openai.com/blog`, `blog.google/technology/ai`
- The Batch (deeplearning.ai), Import AI newsletter

**Research rules:**
- Always web-search — do not rely on training data for feature specifics
- Tips must be **currently available** (not beta/waitlisted unless clearly noted)
- Cross-check claims across 2+ sources when possible
- If a feature can't be verified in official docs → don't include it
- Keep each tip to max 15 words — specific and actionable, not generic

### Step 3 — Write LinkedIn Post Copy

Format:
```
🤖 HOW TO AI — [TOOL NAME]

[One-line hook that creates curiosity or a relatable pain point]

[2–4 dot-point tips, each starting with an emoji]

🔥 Tip: [One bonus power-user tip]

—
🏷️ #AIING #HowToAI #[ToolName] #AITools #ProductivityAI
```

Keep total post under 300 words. Write in a confident, friendly, slightly nerdy tone.

### Step 4 — Generate the PNG Learning Card

Read the brand assets:
- Logo: `assets/aiing_logo.png` (if present — fall back to text "AIING" if missing)
- Check `assets/brand.json` for brand colours (fall back to defaults if missing)

Run the card generation script:

```bash
python3 scripts/generate_card.py \
  --title "[TOOL NAME]" \
  --tips "[tip1]|[tip2]|[tip3]" \
  --tools "[tool_slug1],[tool_slug2]" \
  --output "[output_path].png"
```

**Arguments:**
- `--title`: The AI tool or topic name shown as the card headline
- `--tips`: Pipe-separated tip strings (without emojis — script adds them)
- `--tools`: Comma-separated tool slugs for icon fetching (see references/tool-icons.md for slugs)
- `--output`: Full path for the output PNG
- `--logo`: Path to logo PNG (optional, defaults to `assets/aiing_logo.png`)
- `--subtitle`: Optional subtitle line under the title

### Step 5 — Present to User

1. Print the LinkedIn copy in the chat (ready to copy-paste)
2. Present the PNG file using `present_files`
3. Ask: "Happy with this? Want to adjust the topic, tips, or card design?"

---

## Brand Defaults

These are used if `assets/brand.json` is missing:

```json
{
  "bg_color": "#0D0D0D",
  "accent_color": "#7C3AED",
  "accent2_color": "#06B6D4",
  "text_color": "#F8FAFC",
  "muted_color": "#94A3B8",
  "card_color": "#1E1E2E",
  "tip_bg_color": "#1A1A2E",
  "font_title_size": 58,
  "font_tip_size": 32,
  "border_radius": 24
}
```

To customise: create `assets/brand.json` with any of these keys overridden.

---

## Adding the AIING Logo

Place the AIING logo PNG at: `assets/aiing_logo.png`

The card generator will:
- Auto-detect and load it
- Resize to fit the top-left header area (max 160px tall)
- Fall back to a styled text "AIING" wordmark if missing

---

## Tool Icon Sources

See `references/tool-icons.md` for the full list of supported tool slugs and where their icons are fetched from (Clearbit, official favicons, or bundled fallbacks).

---

## Example Invocations

- "Create this week's LinkedIn post about Claude Projects"
- "Make an AIING learning card on Gemini 2.0"
- "Write a How to AI post — pick a trending tool"
- "Generate my weekly AI post about Cursor"
- "Make a LinkedIn card about Perplexity AI"
