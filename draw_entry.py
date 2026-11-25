#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261125.

A newspaper front page summing up Wednesday 25 November 2026:
six verified stories, each with a hand-drawn geometric illustration.
Everything is drawn with PIL primitives; no external images.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (20, 36, 62)
RED = (179, 39, 30)
GOLD = (201, 162, 39)
GREY = (90, 90, 90)
PANEL = (255, 255, 255)
LINE = (180, 172, 158)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(d, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, fnt):
    d.text((x, y), text, font=fnt, fill=RED)


# ---------------------------------------------------------------- icons
def icon_tower(d, x, y, s):
    # PIF-style skyscraper with lattice facade, smoke and a small drone
    bx, by = x + s * 0.28, y + s * 0.10
    bw, bh = s * 0.44, s * 0.78
    d.rectangle([bx, by, bx + bw, by + bh], fill=(58, 82, 120), outline=NAVY, width=3)
    for i in range(1, 6):
        yy = by + bh * i / 6
        d.line([(bx, yy), (bx + bw, yy)], fill=(140, 165, 200), width=2)
    for i in range(1, 4):
        xx = bx + bw * i / 4
        d.line([(xx, by), (xx, by + bh)], fill=(140, 165, 200), width=2)
    # damage + smoke near the top
    d.ellipse([bx + bw * 0.55, by + bh * 0.18, bx + bw * 0.95, by + bh * 0.38],
              fill=(60, 60, 60))
    d.ellipse([bx + bw * 0.62, by - s * 0.02, bx + bw * 0.82, by + s * 0.14],
              fill=(150, 150, 150))
    d.ellipse([bx + bw * 0.70, by - s * 0.10, bx + bw * 0.86, by + s * 0.02],
              fill=(185, 185, 185))
    # drone
    dx, dy = x + s * 0.78, y + s * 0.22
    d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=INK)
    d.line([(dx - 16, dy), (dx + 16, dy)], fill=INK, width=3)
    d.line([(dx, dy - 12), (dx, dy + 12)], fill=INK, width=3)
    # ground
    d.line([(x, y + s * 0.92), (x + s, y + s * 0.92)], fill=NAVY, width=3)


def icon_ship(d, x, y, s):
    # warship on waves + radar sweep above
    d.polygon([(x + s * 0.08, y + s * 0.55), (x + s * 0.92, y + s * 0.55),
               (x + s * 0.80, y + s * 0.72), (x + s * 0.20, y + s * 0.72)],
              fill=(58, 82, 120), outline=NAVY)
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.58, y + s * 0.55],
                fill=(90, 110, 140), outline=NAVY, width=2)
    d.line([(x + s * 0.48, y + s * 0.22), (x + s * 0.48, y + s * 0.38)],
           fill=NAVY, width=3)
    d.ellipse([x + s * 0.44, y + s * 0.16, x + s * 0.52, y + s * 0.24], fill=RED)
    for i, yy in enumerate((0.80, 0.86)):
        d.arc([x + s * 0.05, y + s * yy, x + s * 0.95, y + s * (yy + 0.12)],
              0, 180, fill=(60, 120, 180), width=3)
    # radar arcs top right
    cx, cy = x + s * 0.82, y + s * 0.18
    for r in (10, 20, 30):
        d.arc([cx - r, cy - r, cx + r, cy + r], -60, 30, fill=GOLD, width=3)


def icon_shield(d, x, y, s):
    # shield with a padlock, circuit traces around it
    cx, cy = x + s * 0.5, y + s * 0.46
    d.polygon([(cx - s * 0.32, cy - s * 0.30), (cx + s * 0.32, cy - s * 0.30),
               (cx + s * 0.32, cy + s * 0.05), (cx, cy + s * 0.38),
               (cx - s * 0.32, cy + s * 0.05)],
              fill=(58, 82, 120), outline=NAVY, width=3)
    lx, ly = cx - s * 0.11, cy - s * 0.06
    d.rectangle([lx, ly, lx + s * 0.22, ly + s * 0.20], fill=GOLD, outline=NAVY, width=2)
    d.arc([lx + s * 0.03, ly - s * 0.10, lx + s * 0.19, ly + s * 0.06],
          180, 360, fill=NAVY, width=4)
    d.ellipse([cx - 3, ly + s * 0.07, cx + 3, ly + s * 0.13], fill=NAVY)
    # circuit traces
    for (x1, y1, x2, y2) in [(0.05, 0.15, 0.22, 0.15), (0.05, 0.80, 0.22, 0.80),
                             (0.78, 0.15, 0.95, 0.15), (0.78, 0.80, 0.95, 0.80)]:
        d.line([(x + s * x1, y + s * y1), (x + s * x2, y + s * y2)],
               fill=(60, 120, 180), width=3)
        d.ellipse([x + s * x1 - 4, y + s * y1 - 4, x + s * x1 + 4, y + s * y1 + 4],
                  fill=(60, 120, 180))


def icon_flask(d, x, y, s):
    # Erlenmeyer flask with liquid + warning triangle
    d.polygon([(x + s * 0.38, y + s * 0.12), (x + s * 0.62, y + s * 0.12),
               (x + s * 0.62, y + s * 0.34), (x + s * 0.85, y + s * 0.80),
               (x + s * 0.15, y + s * 0.80), (x + s * 0.38, y + s * 0.34)],
              fill=(220, 235, 245), outline=NAVY, width=3)
    d.polygon([(x + s * 0.24, y + s * 0.58), (x + s * 0.76, y + s * 0.58),
               (x + s * 0.85, y + s * 0.80), (x + s * 0.15, y + s * 0.80)],
              fill=(120, 190, 90))
    d.ellipse([x + s * 0.42, y + s * 0.42, x + s * 0.52, y + s * 0.52], fill=(255, 255, 255))
    d.ellipse([x + s * 0.58, y + s * 0.48, x + s * 0.66, y + s * 0.56], fill=(255, 255, 255))
    # bubbles
    d.ellipse([x + s * 0.30, y + s * 0.30, x + s * 0.36, y + s * 0.36], fill=GREY)
    d.ellipse([x + s * 0.66, y + s * 0.26, x + s * 0.72, y + s * 0.32], fill=GREY)
    # small warning triangle
    tx, ty = x + s * 0.72, y + s * 0.05
    d.polygon([(tx, ty), (tx + 26, ty + 22), (tx - 26, ty + 22)], fill=(240, 200, 40),
              outline=NAVY)
    d.text((tx - 3, ty + 4), "!", font=font(SANS_B, 16), fill=INK)


def icon_court(d, x, y, s):
    # courthouse: pediment + columns + gavel
    d.polygon([(x + s * 0.10, y + s * 0.30), (x + s * 0.50, y + s * 0.08),
               (x + s * 0.90, y + s * 0.30)], fill=(58, 82, 120), outline=NAVY, width=3)
    d.rectangle([x + s * 0.10, y + s * 0.30, x + s * 0.90, y + s * 0.38],
                fill=NAVY)
    for i in range(4):
        cx = x + s * (0.20 + i * 0.20)
        d.rectangle([cx - 7, y + s * 0.40, cx + 7, y + s * 0.78], fill=(200, 205, 215),
                    outline=NAVY, width=2)
    d.rectangle([x + s * 0.08, y + s * 0.78, x + s * 0.92, y + s * 0.86], fill=NAVY)
    # gavel
    d.line([(x + s * 0.62, y + s * 0.55), (x + s * 0.92, y + s * 0.88)],
           fill=(120, 80, 40), width=6)
    d.rectangle([x + s * 0.55, y + s * 0.48, x + s * 0.75, y + s * 0.62],
                fill=(120, 80, 40), outline=NAVY, width=2)


def icon_blast(d, x, y, s):
    # explosion starburst over a crate
    cx, cy = x + s * 0.5, y + s * 0.42
    pts = []
    import math
    for i in range(16):
        r = s * 0.34 if i % 2 == 0 else s * 0.16
        a = math.pi * i / 8 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(240, 180, 40), outline=RED)
    d.ellipse([cx - s * 0.10, cy - s * 0.10, cx + s * 0.10, cy + s * 0.10],
              fill=RED)
    d.rectangle([x + s * 0.30, y + s * 0.72, x + s * 0.70, y + s * 0.90],
                fill=(150, 110, 60), outline=NAVY, width=3)
    d.line([(x + s * 0.30, y + s * 0.81), (x + s * 0.70, y + s * 0.81)],
           fill=NAVY, width=2)


# ---------------------------------------------------------------- page
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# Masthead
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((512, 14), "THE WORLD TODAY", font=font(SERIF_B, 74),
       fill=(255, 255, 255), anchor="ma")
d.text((512, 96), "ONE DAY  ·  SIX STORIES  ·  THE NEWS THAT MATTERED",
       font=font(SANS_B, 15), fill=GOLD, anchor="ma")

# Date strip
d.rectangle([0, 118, W, 164], fill=RED)
d.text((24, 126), "WEDNESDAY  ·  25 NOVEMBER 2026", font=font(SANS_B, 32),
       fill=(255, 255, 255))
d.text((1000, 130), "25 NOV 2026", font=font(SANS_B, 24), fill=(255, 255, 255),
       anchor="ra")

# ---- lead story: Riyadh tower
LX, LY, LW, LH = 24, 176, 976, 252
d.rectangle([LX, LY, LX + LW, LY + LH], fill=PANEL, outline=LINE, width=2)
d.rectangle([LX, LY, LX + LW, LY + 8], fill=NAVY)
kicker(d, LX + 20, LY + 20, "MIDDLE EAST  ·  LEAD STORY", font(SANS_B, 17))
draw_text_block(d, LX + 20, LY + 44,
                wrap(d, "HOUTHIS STRIKE RIYADH'S TALLEST TOWER", font(SERIF_B, 36), 620),
                font(SERIF_B, 36), INK, leading=42)
sub = ("A drone hits the PIF skyscraper in Riyadh's financial district — "
       "11 injured, second strike in a week.")
y = draw_text_block(d, LX + 20, LY + 146,
                    wrap(d, sub, font(SANS, 22), 600), font(SANS, 22), INK)
d.text((LX + 20, LY + 214), "REUTERS  ·  FIRST REPORTED 24 NOV",
       font=font(SANS_B, 16), fill=GREY)
icon_tower(d, LX + 660, LY + 28, 200)

# ---- 2x2 grid of four stories
stories = [
    ("UKRAINE  ·  NATO", "UKRAINE HITS RUSSIAN SHIPS",
     "Zelenskyy confirms the strikes; NATO radar jets to watch Poland's skies.",
     "REUTERS  ·  23–24 NOV", icon_ship),
    ("UNITED STATES  ·  SECURITY", "CIA AND ODNI HIT BY CYBER BREACH",
     "Hackers expose unclassified data on the spy agencies' open-source network.",
     "NYT / REUTERS  ·  24 NOV", icon_shield),
    ("IRAN  ·  ISRAEL", "ISRAEL: IRAN MAKING CHEMICAL WEAPONS",
     "Katz: Tehran is developing chemical arms; strike plans drawn up.",
     "CBS / FOX  ·  24 NOV", icon_flask),
    ("TECH  ·  TRADE", "HUAWEI CONVICTED IN US TRIAL",
     "A New York jury finds the tech giant guilty of stealing trade secrets.",
     "AP  ·  24 NOV", icon_court),
]
GX, GY = 24, 442
CW, CH, GAP = 480, 172, 14
for i, (kick, head, sub, src, icon) in enumerate(stories):
    px = GX + (i % 2) * (CW + GAP)
    py = GY + (i // 2) * (CH + GAP)
    d.rectangle([px, py, px + CW, py + CH], fill=PANEL, outline=LINE, width=2)
    icon(d, px + 14, py + 26, 116)
    tx = px + 146
    kicker(d, tx, py + 12, kick, font(SANS_B, 13))
    y = draw_text_block(d, tx, py + 34,
                        wrap(d, head, font(SERIF_B, 24), CW - 160),
                        font(SERIF_B, 24), INK, leading=28)
    y = draw_text_block(d, tx, y + 4,
                        wrap(d, sub, font(SANS, 16), CW - 160),
                        font(SANS, 16), (60, 60, 60), leading=20)
    d.text((tx, py + CH - 26), src, font=font(SANS_B, 13), fill=GREY)

# ---- bottom strip: Iowa detonation (a 25 Nov event) + markets ticker
BX, BY, BW, BH = 24, 814, 976, 104
d.rectangle([BX, BY, BX + BW, BY + BH], fill=PANEL, outline=LINE, width=2)
d.rectangle([BX, BY, BX + BW, BY + 6], fill=RED)
icon_blast(d, BX + 16, BY + 12, 84)
kicker(d, BX + 116, BY + 14, "UNITED STATES  ·  TODAY, 25 NOV", font(SANS_B, 14))
d.text((BX + 116, BY + 36), "US ARMY TO DETONATE BOMB STOCKPILE IN IOWA",
       font=font(SERIF_B, 27), fill=INK)
d.text((BX + 116, BY + 72),
       "The Army will blow up its lead-azide store on Wednesday morning, after a court gave the go-ahead.  ·  AP",
       font=font(SANS, 16), fill=(60, 60, 60))

# ---- markets ticker
d.rectangle([0, 932, W, 962], fill=NAVY)
d.text((512, 938),
       "MARKETS: Nvidia rally fades, shares −6%  ·  Australia inflation hotter than forecast  ·  US inflation & GDP due today",
       font=font(SANS_B, 14), fill=(255, 255, 255), anchor="ma")

# ---- footer
d.text((512, 972),
       "First reported 24 Nov, still leading on 25 Nov — except Iowa & Australia CPI, 25 Nov.  Sources: Reuters · AP · NYT · CBS",
       font=font(SANS, 12), fill=GREY, anchor="ma")

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
