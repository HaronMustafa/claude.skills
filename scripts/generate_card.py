#!/usr/bin/env python3
"""
generate_card.py — AIING LinkedIn Learning Card Generator v2
Produces a 1080×1350px multi-section infographic card for LinkedIn posts.
Style: warm coral/terracotta sections on dark background.
"""

import argparse, json, math, os, sys, urllib.request
from io import BytesIO
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow not installed.")
    sys.exit(1)

CARD_W, CARD_H = 1080, 1350
SKILL_DIR = Path(__file__).parent.parent
ASSETS_DIR = SKILL_DIR / "assets"
TOOL_ICONS_DIR = ASSETS_DIR / "tool-icons"

TOOL_DOMAINS = {
    "claude":"anthropic.com","chatgpt":"openai.com","gemini":"gemini.google.com",
    "perplexity":"perplexity.ai","cursor":"cursor.so","midjourney":"midjourney.com",
    "suno":"suno.com","runway":"runwayml.com","kling":"klingai.com",
    "elevenlabs":"elevenlabs.io","grok":"x.ai","copilot":"github.com",
    "v0":"v0.dev","replit":"replit.com","notion-ai":"notion.so","gamma":"gamma.app",
    "descript":"descript.com","heygen":"heygen.com","synthesia":"synthesia.io",
    "luma":"lumalabs.ai","ideogram":"ideogram.ai","leonardo":"leonardo.ai",
    "pika":"pika.art","adobe-firefly":"adobe.com","canva-ai":"canva.com",
    "zapier-ai":"zapier.com","make":"make.com","n8n":"n8n.io",
    "windsurf":"codeium.com","bolt":"bolt.new",
}

DEFAULT_BRAND = {
    "bg":           "#1C1714",
    "bg2":          "#251D19",
    "coral_dark":   "#A84832",
    "coral_mid":    "#C4614A",
    "coral_light":  "#D4795F",
    "coral_pale":   "#E09078",
    "text_on_dark": "#F5EDE8",
    "text_on_coral":"#FFFFFF",
    "muted":        "#A89A94",
    "border":       "#3A2E28",
    "takeaway_bg":  "#2A1F1A",
}

def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def load_brand():
    b = dict(DEFAULT_BRAND)
    bp = ASSETS_DIR / "brand.json"
    if bp.exists():
        try:
            data = json.load(open(bp))
            for k in DEFAULT_BRAND:
                if k in data: b[k] = data[k]
        except: pass
    return b

def load_font(size, bold=False):
    bold_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    reg_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for p in (bold_paths if bold else reg_paths):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: continue
    return ImageFont.load_default()

def tw(draw, text, font):
    b = draw.textbbox((0,0), text, font=font); return b[2]-b[0]
def th(draw, text, font):
    b = draw.textbbox((0,0), text, font=font); return b[3]-b[1]

def wrap(draw, text, font, max_w):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = f"{cur} {w}".strip()
        if tw(draw, t, font) <= max_w: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines or [""]

def rr(draw, xy, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def fetch_favicon(domain, size=96):
    url = f"https://www.google.com/s2/favicons?domain={domain}&sz={size}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r: data = r.read()
        img = Image.open(BytesIO(data)).convert("RGBA")
        return img.resize((size,size), Image.LANCZOS)
    except: return None

def initials_icon(slug, size=64):
    img = Image.new("RGBA", (size,size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([0,0,size-1,size-1], fill=(196,97,74,220))
    f = load_font(size//3, bold=True)
    s = slug[:2].upper()
    b = d.textbbox((0,0),s,font=f)
    sw,sh = b[2]-b[0], b[3]-b[1]
    d.text(((size-sw)//2,(size-sh)//2-1), s, font=f, fill=(255,255,255,255))
    return img

def tool_icon(slug, size=60):
    p = TOOL_ICONS_DIR/f"{slug}.png"
    if p.exists(): return Image.open(p).convert("RGBA").resize((size,size),Image.LANCZOS)
    fav = fetch_favicon(TOOL_DOMAINS.get(slug,f"{slug}.com"), 128)
    if fav: return fav.resize((size,size),Image.LANCZOS)
    return initials_icon(slug, size)

def load_logo(logo_path=None, max_h=52):
    cands = []
    if logo_path: cands.append(logo_path)
    cands += [str(ASSETS_DIR/"aiing_logo.png"), str(ASSETS_DIR/"logo.png")]
    for p in cands:
        if p and os.path.exists(p):
            img = Image.open(p).convert("RGBA")
            ratio = max_h/img.height
            return img.resize((int(img.width*ratio), max_h), Image.LANCZOS)
    return None

def draw_star(draw, cx, cy, r, color):
    for i in range(8):
        a = math.radians(i*45)
        x1,y1 = cx+math.cos(a)*r*0.28, cy+math.sin(a)*r*0.28
        x2,y2 = cx+math.cos(a)*r, cy+math.sin(a)*r
        draw.line([(x1,y1),(x2,y2)], fill=(*color,255), width=max(4,r//6))

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def generate_card(title, subtitle, hook, sections, tips, takeaway, tools, output, logo_path=None):
    B = load_brand()
    PAD = 44
    IW = CARD_W - PAD*2

    img = Image.new("RGB", (CARD_W, CARD_H), hex_rgb(B["bg"]))
    draw = ImageDraw.Draw(img)

    # ── HEADER ────────────────────────────────────────────────────────────────
    HDR_H = 152
    draw.rectangle([0, 0, CARD_W, HDR_H], fill=hex_rgb(B["bg2"]))
    draw.line([(0,HDR_H),(CARD_W,HDR_H)], fill=hex_rgb(B["coral_dark"]), width=3)

    logo = load_logo(logo_path)
    logo_end = PAD
    if logo:
        ly = (HDR_H - logo.height)//2
        img.paste(logo, (PAD, ly), logo)
        logo_end = PAD + logo.width + 18
    else:
        draw_star(draw, PAD+26, HDR_H//2, 26, hex_rgb(B["coral_mid"]))
        logo_end = PAD + 66

    # HOW TO AI pill
    pf = load_font(20, bold=True)
    pt = "HOW TO AI"
    pw, ph = tw(draw, pt, pf)+28, 34
    px = CARD_W - PAD - pw
    rr(draw, [px, 18, px+pw, 18+ph], r=17, fill=hex_rgb(B["coral_mid"]))
    draw.text((px+14, 25), pt, font=pf, fill=hex_rgb(B["text_on_coral"]))

    # Title
    tf = load_font(54, bold=True)
    tlines = wrap(draw, title, tf, CARD_W - logo_end - PAD - 20)
    line_h = 62
    ty = (HDR_H - len(tlines)*line_h - (30 if subtitle else 0))//2
    for i, line in enumerate(tlines[:2]):
        if i == len(tlines)-1 and ' ' in line:
            parts = line.rsplit(' ',1)
            draw.text((logo_end, ty), parts[0]+' ', font=tf, fill=hex_rgb(B["text_on_dark"]))
            draw.text((logo_end + tw(draw, parts[0]+' ', tf), ty), parts[1],
                      font=tf, fill=hex_rgb(B["coral_light"]))
        else:
            draw.text((logo_end, ty), line, font=tf, fill=hex_rgb(B["text_on_dark"]))
        ty += line_h
    if subtitle:
        sf = load_font(24)
        draw.text((logo_end, ty+2), subtitle, font=sf, fill=hex_rgb(B["muted"]))

    y = HDR_H + 20

    # ── HOOK BAND ─────────────────────────────────────────────────────────────
    hf = load_font(29)
    hlines = wrap(draw, hook, hf, IW - 30)
    hook_h = len(hlines)*38 + 24
    draw.rectangle([0, y, CARD_W, y+hook_h], fill=hex_rgb(B["coral_dark"]))
    hy = y+12
    for line in hlines:
        draw.text((PAD+12, hy), line, font=hf, fill=hex_rgb(B["text_on_coral"]))
        hy += 38
    y += hook_h + 18

    # ── SECTION CARDS ─────────────────────────────────────────────────────────
    if sections:
        n = min(len(sections), 3)
        gap = 12
        cw = (IW - gap*(n-1))//n
        slabf = load_font(22, bold=True)
        sbodyf = load_font(24)

        # Pill headers
        sx = PAD
        for label, _ in sections[:n]:
            lw2 = tw(draw, label, slabf)+28
            rr(draw, [sx, y, sx+lw2, y+34], r=17, fill=hex_rgb(B["coral_mid"]))
            draw.text((sx+14, y+7), label, font=slabf, fill=hex_rgb(B["text_on_coral"]))
            sx += cw+gap
        y += 40

        # Body cells — uniform height
        max_bh = 0
        for _, desc in sections[:n]:
            ls = wrap(draw, desc, sbodyf, cw-28)
            max_bh = max(max_bh, len(ls)*32+24)

        colors = [hex_rgb(B["coral_pale"]), hex_rgb(B["coral_light"]), hex_rgb(B["coral_pale"])]
        sx = PAD
        for i, (_, desc) in enumerate(sections[:n]):
            rr(draw, [sx, y, sx+cw, y+max_bh], r=10, fill=colors[i%3])
            dy = y+14
            for line in wrap(draw, desc, sbodyf, cw-28):
                draw.text((sx+14, dy), line, font=sbodyf, fill=hex_rgb(B["bg"]))
                dy += 32
            sx += cw+gap
        y += max_bh+20

    # ── STEP-BY-STEP TABLE ────────────────────────────────────────────────────
    draw.rectangle([0, y, CARD_W, y+40], fill=hex_rgb(B["coral_dark"]))
    draw.text((PAD+10, y+10), "★  STEP-BY-STEP", font=load_font(23, bold=True),
              fill=hex_rgb(B["text_on_coral"]))
    y += 40

    tipf = load_font(26)
    for i, tip in enumerate(tips[:5]):
        alt = i%2==0
        bg = hex_rgb(B["bg2"]) if alt else hex_rgb(B["bg"])
        tlines = wrap(draw, tip, tipf, IW-75)
        rh = len(tlines)*36 + 28
        draw.rectangle([0, y, CARD_W, y+rh], fill=bg)
        draw.rectangle([0, y, 5, y+rh], fill=hex_rgb(B["coral_mid"]))  # left bar
        # Number circle
        nr, ncx, ncy = 18, PAD+18, y+rh//2
        draw.ellipse([ncx-nr,ncy-nr,ncx+nr,ncy+nr], fill=hex_rgb(B["coral_mid"]))
        nf2 = load_font(17, bold=True)
        ns = str(i+1)
        draw.text((ncx-tw(draw,ns,nf2)//2, ncy-th(draw,ns,nf2)//2-1), ns, font=nf2, fill=(255,255,255))
        # Text
        tx, ty2 = PAD+44, y+14
        for line in tlines:
            draw.text((tx, ty2), line, font=tipf, fill=hex_rgb(B["text_on_dark"]))
            ty2 += 36
        draw.line([(PAD,y+rh-1),(CARD_W-PAD,y+rh-1)], fill=hex_rgb(B["border"]))
        y += rh

    y += 16

    # ── TAKEAWAY BOX ──────────────────────────────────────────────────────────
    if takeaway:
        tkf = load_font(26)
        tklf = load_font(20, bold=True)
        tklines = wrap(draw, takeaway, tkf, IW-80)
        tkh = len(tklines)*36 + 52
        rr(draw, [PAD, y, PAD+IW, y+tkh], r=12,
           fill=hex_rgb(B["takeaway_bg"]), outline=hex_rgb(B["coral_mid"]), width=2)
        draw.text((PAD+20, y+12), "💡  KEY TAKEAWAY", font=tklf, fill=hex_rgb(B["coral_light"]))
        ty2 = y+38
        for line in tklines:
            draw.text((PAD+20, ty2), line, font=tkf, fill=hex_rgb(B["text_on_dark"]))
            ty2 += 36
        y += tkh+16

    # ── TOOL ICONS ────────────────────────────────────────────────────────────
    ICON_SZ = 54
    icon_gap = 28
    icons = [(tool_icon(s.strip(), ICON_SZ), s.replace("-"," ").title()) for s in tools[:6]]
    if icons:
        row_h = ICON_SZ + 32
        draw.rectangle([0, y, CARD_W, y+row_h], fill=hex_rgb(B["bg2"]))
        draw.line([(0,y),(CARD_W,y)], fill=hex_rgb(B["coral_dark"]), width=2)
        total_w = len(icons)*(ICON_SZ+icon_gap)-icon_gap
        ix = (CARD_W-total_w)//2
        ilf = load_font(19)
        for ico, name in icons:
            if ico.mode=="RGBA":
                tmp = Image.new("RGB", ico.size, hex_rgb(B["bg2"]))
                tmp.paste(ico, mask=ico.split()[3])
                img.paste(tmp, (ix, y+6))
            else:
                img.paste(ico, (ix, y+6))
            lw3 = tw(draw, name, ilf)
            draw.text((ix+(ICON_SZ-lw3)//2, y+ICON_SZ+10), name, font=ilf, fill=hex_rgb(B["muted"]))
            ix += ICON_SZ+icon_gap
        y += row_h

    # ── FOOTER (fixed slim height) ────────────────────────────────────────────
    FOOTER_H = 48
    fy = CARD_H - FOOTER_H
    # Fill any gap between content and footer with bg color
    if y < fy:
        draw.rectangle([0, y, CARD_W, fy], fill=hex_rgb(B["bg"]))
    draw.rectangle([0, fy, CARD_W, CARD_H], fill=hex_rgb(B["coral_dark"]))
    # Thin top border line on footer
    draw.line([(0, fy), (CARD_W, fy)], fill=hex_rgb(B["coral_mid"]), width=2)
    ff = load_font(19, bold=True)
    fm = load_font(17)
    mid_y = fy + (FOOTER_H - 20) // 2
    draw.text((PAD+8, mid_y), "AIING", font=ff, fill=hex_rgb(B["text_on_coral"]))
    tags = "#AIING  #HowToAI  #AITools"
    draw.text((CARD_W-PAD-tw(draw,tags,fm), mid_y+2), tags, font=fm, fill=hex_rgb(B["bg2"]))

    # ── SAVE ──────────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(output) if os.path.dirname(output) else ".", exist_ok=True)
    img.save(output, "PNG", quality=95)
    print(f"✅ Card saved: {output}  ({CARD_W}×{CARD_H}px)")


# ─── CLI ──────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--hook", required=True)
    p.add_argument("--sections", default="")
    p.add_argument("--tips", required=True)
    p.add_argument("--takeaway", default="")
    p.add_argument("--tools", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--logo", default=None)
    args = p.parse_args()

    sections = []
    if args.sections:
        for item in args.sections.split("|"):
            if ":" in item:
                a,b2 = item.split(":",1)
                sections.append((a.strip(), b2.strip()))

    generate_card(
        title=args.title,
        subtitle=args.subtitle,
        hook=args.hook,
        sections=sections,
        tips=[t.strip() for t in args.tips.split("|") if t.strip()],
        takeaway=args.takeaway,
        tools=[t.strip() for t in args.tools.split(",") if t.strip()],
        output=args.output,
        logo_path=args.logo,
    )

if __name__ == "__main__":
    main()
