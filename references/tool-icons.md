# Tool Icons Reference

This file lists supported AI tool slugs and how their icons are sourced.

The card generator (`generate_card.py`) fetches icons in this priority order:
1. Bundled PNG in `assets/tool-icons/[slug].png`
2. Official favicon via `https://www.google.com/s2/favicons?domain=[domain]&sz=128`
3. Fallback: coloured circle with tool initials

---

## Supported Tool Slugs

| Slug | Display Name | Icon Domain |
|------|-------------|-------------|
| `claude` | Claude | anthropic.com |
| `chatgpt` | ChatGPT | openai.com |
| `gemini` | Gemini | gemini.google.com |
| `perplexity` | Perplexity | perplexity.ai |
| `cursor` | Cursor | cursor.so |
| `midjourney` | Midjourney | midjourney.com |
| `suno` | Suno | suno.com |
| `runway` | Runway | runwayml.com |
| `kling` | Kling AI | klingai.com |
| `elevenlabs` | ElevenLabs | elevenlabs.io |
| `grok` | Grok | x.ai |
| `copilot` | GitHub Copilot | github.com |
| `v0` | v0 by Vercel | v0.dev |
| `replit` | Replit | replit.com |
| `notion-ai` | Notion AI | notion.so |
| `gamma` | Gamma | gamma.app |
| `descript` | Descript | descript.com |
| `heygen` | HeyGen | heygen.com |
| `synthesia` | Synthesia | synthesia.io |
| `luma` | Luma AI | lumalabs.ai |
| `ideogram` | Ideogram | ideogram.ai |
| `leonardo` | Leonardo AI | leonardo.ai |
| `pika` | Pika | pika.art |
| `adobe-firefly` | Adobe Firefly | adobe.com |
| `canva-ai` | Canva AI | canva.com |
| `zapier-ai` | Zapier AI | zapier.com |
| `make` | Make (Integromat) | make.com |
| `n8n` | n8n | n8n.io |
| `windsurf` | Windsurf | codeium.com |
| `bolt` | Bolt | bolt.new |

---

## Adding a New Tool

1. Add a row to the table above
2. Optionally drop a `[slug].png` (128×128px, transparent bg) into `assets/tool-icons/`
3. Use the slug in `--tools` argument when calling `generate_card.py`

---

## Fallback Initials Colors

When no icon is available, the generator creates a coloured circle using these brand colors per tool category:

- **Chat/LLM**: #7C3AED (purple)
- **Image/Video**: #EC4899 (pink)
- **Code/Dev**: #06B6D4 (cyan)
- **Audio**: #F59E0B (amber)
- **Productivity**: #10B981 (emerald)
