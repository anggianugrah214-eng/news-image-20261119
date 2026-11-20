#!/usr/bin/env python3
"""Draw 'The World in One Day - 19 November 2026' as a newspaper front page.

Every picture on the page is drawn from shapes with Pillow: no photos, no
outside images, no network. The output is deterministic: same code, same
bytes, every run.

Usage: python3 draw_image.py   (writes entry.png next to this file)
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (24, 24, 22)
RED = (178, 34, 34)
BLUE = (31, 68, 120)
GOLD = (176, 132, 34)
SEA = (46, 110, 138)
GREEN = (46, 110, 62)
GREY = (105, 105, 100)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF_REG = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS_REG = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, max_w, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = fnt.size + 4
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def headline(draw, x, y, text, max_w, size=21):
    fnt = SANS(size)
    return text_block(draw, x, y, text, fnt, INK, max_w, size + 5)


def kicker(draw, x, y, text, color=RED):
    fnt = SANS(15)
    draw.text((x, y), text.upper(), font=fnt, fill=color)
    return y + 22


def rule(draw, x0, y, x1, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- pictograms

def draw_flags(draw, x, y, w=118, h=78):
    """Three small flags on poles: United States, China, Russia."""
    pole_w = w // 3
    for i, country in enumerate(("us", "cn", "ru")):
        fx = x + i * pole_w + 6
        draw.line([(fx + pole_w // 2, y), (fx + pole_w // 2, y + h + 26)],
                  fill=INK, width=3)
        fw, fh = pole_w - 12, h
        if country == "us":
            for s in range(7):
                draw.rectangle([fx, y + s * fh // 7, fx + fw, y + (s + 1) * fh // 7],
                               fill=RED if s % 2 == 0 else PAPER)
            draw.rectangle([fx, y, fx + fw * 2 // 5, y + 4 * fh // 7], fill=BLUE)
            for r in range(4):
                for c in range(3):
                    draw.ellipse([fx + 4 + c * 11, y + 5 + r * 9,
                                  fx + 9 + c * 11, y + 10 + r * 9], fill=PAPER)
        elif country == "cn":
            draw.rectangle([fx, y, fx + fw, y + fh], fill=RED)
            cx, cy = fx + 14, y + 13
            draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=GOLD)
            for sx, sy in ((fx + 34, y + 8), (fx + 40, y + 18),
                           (fx + 40, y + 30), (fx + 34, y + 38)):
                draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)
        else:
            third = fh // 3
            for j, col in enumerate(((255, 255, 255), (0, 57, 166), (213, 0, 50))):
                draw.rectangle([fx, y + j * third, fx + fw, y + (j + 1) * third],
                               fill=col)
        draw.rectangle([fx, y, fx + fw, y + fh], outline=INK, width=2)


def draw_table(draw, x, y, w, h):
    """A summit table with three chairs and three name cards."""
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 72, 40))
    draw.rectangle([x - 8, y + h - 22, x + w + 8, y + h - 12], fill=(146, 94, 52))
    for i, name in enumerate(("USA", "CHINA", "RUSSIA")):
        cx = x + (i + 0.5) * w / 3
        draw.rectangle([cx - 26, y + h - 52, cx + 26, y + h - 24],
                       fill=PAPER, outline=INK, width=2)
        fnt = SANS(12)
        tw = draw.textlength(name, font=fnt)
        draw.text((cx - tw / 2, y + h - 48), name, font=fnt, fill=INK)


def draw_scales(draw, cx, cy, s=1.0):
    """Scales of justice."""
    draw.line([(cx, cy - 62), (cx, cy + 58)], fill=INK, width=4)
    draw.line([(cx - 58, cy - 46), (cx + 58, cy - 46)], fill=INK, width=4)
    draw.ellipse([cx - 7, cy - 72, cx + 7, cy - 58], fill=GOLD, outline=INK)
    for sx in (cx - 58, cx + 58):
        draw.line([(sx, cy - 46), (sx - 26, cy + 6)], fill=INK, width=2)
        draw.line([(sx, cy - 46), (sx + 26, cy + 6)], fill=INK, width=2)
        draw.line([(sx, cy - 46), (sx, cy + 6)], fill=INK, width=2)
        draw.pieslice([sx - 28, cy - 6, sx + 28, cy + 26], 0, 180, fill=GOLD,
                      outline=INK)
    draw.rectangle([cx - 30, cy + 52, cx + 30, cy + 62], fill=INK)


def draw_chart(draw, x, y, w, h):
    """A falling market line over gridlines, with a red arrow down."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK,
                   width=2)
    for i in range(1, 4):
        gy = y + i * h // 4
        draw.line([(x + 4, gy), (x + w - 4, gy)], fill=(210, 210, 205), width=1)
    pts = [(x + 8 + i * (w - 16) // 6,
            y + 32 + (i * i * 11) // 6)
           for i in range(7)]
    draw.line(pts, fill=RED, width=4)
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    ex, ey = pts[-1]
    draw.polygon([(ex - 11, ey - 20), (ex + 11, ey - 20), (ex, ey - 2)],
                 fill=RED)
    fnt = SANS(15)
    draw.text((x + 8, y + 6), "S&P 500  -2.0%", font=fnt, fill=RED)
    draw.text((x + 8, y + h - 24), "5th straight fall", font=SANS_REG(13),
              fill=GREY)


def draw_bridge(draw, x, y, w, h):
    """A sea bridge with two towers, cables, and a burst of smoke."""
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=SEA)
    for wx in range(x, x + w, 26):
        draw.arc([wx, y + h - 22, wx + 26, y + h - 2], 0, 180, fill=(255, 255, 255))
    deck = y + h // 2
    draw.rectangle([x, deck, x + w, deck + 10], fill=INK)
    for tx in (x + w // 4, x + 3 * w // 4):
        draw.rectangle([tx - 6, y + 30, tx + 6, deck], fill=INK)
        draw.line([(tx, y + 30), (x + 8, deck)], fill=INK, width=2)
        draw.line([(tx, y + 30), (x + w - 8, deck)], fill=INK, width=2)
    bx, by = x + w // 2, y + 34
    for r, col in ((34, (255, 200, 60)), (22, (255, 120, 40)), (12, (220, 40, 30))):
        draw.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
    for dx, dy in ((-26, 22), (24, 26), (0, 40)):
        draw.ellipse([bx + dx - 10, by + dy - 8, bx + dx + 10, by + dy + 8],
                     fill=(120, 120, 115))


def draw_boat(draw, x, y, w, h):
    """A capsized boat in heavy waves."""
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=SEA)
    for i in range(3):
        wy = y + h - 26 + i * 10
        for wx in range(x, x + w, 34):
            draw.arc([wx, wy, wx + 34, wy + 14], 180, 360, fill=(255, 255, 255),
                     width=3)
    bx, by = x + w // 2, y + h // 2 - 6
    draw.polygon([(bx - 70, by - 6), (bx + 70, by - 6), (bx + 46, by + 26),
                  (bx - 46, by + 26)], fill=(120, 72, 40), outline=INK)
    draw.polygon([(bx - 70, by - 6), (bx + 70, by - 6), (bx + 58, by - 30),
                  (bx - 58, by - 30)], fill=(146, 94, 52), outline=INK)
    draw.line([(bx - 58, by - 30), (bx - 58, by - 64)], fill=INK, width=3)
    draw.polygon([(bx - 58, by - 64), (bx - 58, by - 30), (bx - 22, by - 30)],
                 fill=(255, 255, 255), outline=INK)
    draw.ellipse([bx + 78, by - 2, bx + 94, by + 14], fill=(240, 200, 140),
                 outline=INK)
    draw.ellipse([bx - 92, by + 8, bx - 78, by + 22], fill=(240, 200, 140),
                 outline=INK)


def draw_badge(draw, cx, cy, r=26):
    """A police shield."""
    draw.polygon([(cx, cy - r), (cx + r, cy - r + 10), (cx + r, cy + 6),
                  (cx, cy + r + 6), (cx - r, cy + 6), (cx - r, cy - r + 10)],
                 fill=BLUE, outline=GOLD, width=3)
    draw.ellipse([cx - 7, cy - 12, cx + 7, cy + 2], fill=GOLD)
    draw.rectangle([cx - 2, cy, cx + 2, cy + 16], fill=GOLD)


# ------------------------------------------------------------------- layout

def panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK,
                   width=2)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tf = SERIF(58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 18), title, font=tf, fill=INK)
    rule(d, 24, 96, W - 24, 3)
    sub = "THURSDAY  •  19 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE IMAGE"
    sf = SANS(17)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 106), sub, font=sf, fill=INK)
    rule(d, 24, 136, W - 24, 1)

    # ---- Lead story: Shenzhen summit (full width)
    lx, ly, lw, lh = 24, 150, W - 48, 236
    panel(d, lx, ly, lw, lh)
    draw_flags(d, lx + 22, ly + 78)
    draw_table(d, lx + 22, ly + 176, 400, 44)
    tx = lx + 452
    y = kicker(d, tx, ly + 16, "Lead — Shenzhen, China")
    y = headline(d, tx, y, "TRUMP, XI AND PUTIN ISSUE PEACE PLEDGE", lw - 478, 24)
    y = text_block(d, tx, y + 4,
                   "The first three-way summit of the world's biggest nuclear "
                   "powers ends with a joint declaration to keep the peace — "
                   "silent on the wars in Ukraine and Iran.",
                   SERIF_REG(17), INK, lw - 478, 23)
    d.text((tx, ly + lh - 30), "A first: no US, Chinese and Russian leaders "
           "had met three-way before.", font=SANS_REG(14), fill=GREY)

    # ---- Row 1: ICJ ruling | Wall Street
    ry, rh = 402, 252
    col_w = (W - 48 - 16) // 2
    # ICJ panel
    px, py = 24, ry
    panel(d, px, py, col_w, rh)
    draw_scales(d, px + 92, py + 128)
    tx = px + 180
    y = kicker(d, tx, py + 14, "Justice — The Hague")
    y = headline(d, tx, y, "WORLD COURT: MYANMAR COMMITTED GENOCIDE", col_w - 196, 20)
    text_block(d, tx, y + 4,
               "The International Court of Justice rules 9–6 that Myanmar's "
               "military acted with genocidal intent against the Rohingya in "
               "2017. Refugees in Bangladesh cheer the verdict.",
               SERIF_REG(15), INK, col_w - 196, 20)
    # Markets panel
    px = 24 + col_w + 16
    panel(d, px, py, col_w, rh)
    draw_chart(d, px + 18, py + 96, 210, 128)
    tx = px + 244
    y = kicker(d, tx, py + 14, "Markets — New York")
    y = headline(d, tx, y, "WALL STREET SLIDES FOR A FIFTH DAY", col_w - 260, 20)
    text_block(d, tx, y + 4,
               "The S&P 500 falls 2.0% and Tokyo's Nikkei drops 4.7% as "
               "investors fret over AI valuations. Anthropic's record stock "
               "debut fails to calm nerves.",
               SERIF_REG(15), INK, col_w - 260, 20)

    # ---- Row 2: Crimea bridge | Senegal boat
    ry2 = 670
    px, py = 24, ry2
    panel(d, px, py, col_w, rh)
    draw_bridge(d, px + 18, py + 96, 210, 128)
    tx = px + 244
    y = kicker(d, tx, py + 14, "War — Ukraine")
    y = headline(d, tx, y, "UKRAINE HITS CRIMEA BRIDGE AGAIN", col_w - 260, 20)
    text_block(d, tx, y + 4,
               "A third strike in four days halts road traffic across the "
               "Kerch Bridge to Crimea. Putin vows a harsher response.",
               SERIF_REG(15), INK, col_w - 260, 20)
    px = 24 + col_w + 16
    panel(d, px, py, col_w, rh)
    draw_boat(d, px + 18, py + 96, 210, 128)
    tx = px + 244
    y = kicker(d, tx, py + 14, "Migration — Senegal")
    y = headline(d, tx, y, "DOZENS MISSING AS MIGRANT BOAT SINKS", col_w - 260, 20)
    text_block(d, tx, y + 4,
               "A wooden boat carrying about 100 people strikes rocks and "
               "capsizes off Senegal's coast overnight. Rescue teams search "
               "for survivors.",
               SERIF_REG(15), INK, col_w - 260, 20)

    # ---- Footer strip: Haiti + also
    fy = 938
    rule(d, 24, fy, W - 24, 2)
    draw_badge(d, 62, fy + 36)
    y = kicker(d, 100, fy + 10, "Americas — Haiti", color=BLUE)
    headline(d, 100, y, "HAITI RAID KILLS 34 GANG SUSPECTS",
             430, 16)
    d.text((100, fy + 60), "Police operation in Port-au-Prince.",
           font=SERIF_REG(14), fill=INK)
    d.line([(540, fy + 8), (540, fy + 72)], fill=GREY, width=1)
    d.text((556, fy + 10), "ALSO ON 19 NOVEMBER:", font=SANS(14), fill=RED)
    text_block(d, 556, fy + 32,
               "Van Gogh sells for a record $190.4m · Denmark ratifies the "
               "Greenland defence deal · Aid groups score the Gaza plan 4 of 26",
               SERIF_REG(13), INK, W - 24 - 556, 17)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    print("wrote", path)
