#!/usr/bin/env python3
"""Tuesday, In Full - 17 November 2026 poster renderer.
Original work for news-image-20261117. Deterministic, Pillow only.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
WHITE = (255, 255, 255)
TEAL = (0, 77, 84)
TEAL2 = (0, 105, 112)
TEAL_DARK = (0, 52, 58)
ORANGE = (232, 93, 32)
ORANGE_DARK = (196, 72, 18)
DARK = (22, 30, 32)
GREY = (86, 98, 100)
LIGHT = (242, 247, 247)
CARD_BG = (255, 255, 255)
BORDER = (198, 218, 218)
SKY = (186, 222, 224)
WATER = (32, 132, 142)
SMOKE = (120, 128, 130)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANSI = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrap(draw, xy, text, font, fill, max_w, leading, align="left", max_lines=None):
    x, y = xy
    lines = wrap(draw, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        if align == "center":
            w = draw.textlength(ln, font=font)
            draw.text((x + (max_w - w) / 2, y), ln, font=font, fill=fill)
        else:
            draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

def bridge_illustration(d, x0, y0, x1, y1):
    # sky
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    # water (lower third)
    water_y = y1 - 36
    d.rectangle([x0, water_y, x1, y1], fill=WATER)
    for i in range(9):
        yy = water_y + 6 + (i % 3) * 10
        sx = x0 + 24 + (i * 97) % 760
        d.line([sx, yy, sx + 52, yy], fill=(120, 200, 208), width=2)
    deck_y = y0 + 58
    # pillars first (behind deck)
    for px in (x0 + 72, x0 + 208, x1 - 196, x1 - 84):
        d.rectangle([px, deck_y + 12, px + 20, water_y + 6], fill=(70, 90, 92))
    # low guard rails on the intact decks (posts only, deck stays flat and clear)
    for gx in range(x0 + 20, x0 + 340, 40):
        d.line([gx, deck_y - 7, gx, deck_y], fill=TEAL_DARK, width=3)
    d.line([x0 + 8, deck_y - 7, x0 + 344, deck_y - 7], fill=TEAL_DARK, width=2)
    for gx in range(x0 + 616, x1 - 10, 40):
        d.line([gx, deck_y - 7, gx, deck_y], fill=TEAL_DARK, width=3)
    d.line([x0 + 604, deck_y - 7, x1 - 4, deck_y - 7], fill=TEAL_DARK, width=2)
    # left intact deck, ending in a jagged break
    d.rectangle([x0, deck_y, x0 + 348, deck_y + 14], fill=TEAL_DARK)
    d.rectangle([x0, deck_y + 14, x0 + 348, deck_y + 18], fill=ORANGE)
    d.polygon([(x0 + 348, deck_y), (x0 + 362, deck_y + 7), (x0 + 348, deck_y + 14)], fill=TEAL_DARK)
    # right intact deck
    d.rectangle([x0 + 596, deck_y, x1, deck_y + 14], fill=TEAL_DARK)
    d.rectangle([x0 + 596, deck_y + 14, x1, deck_y + 18], fill=ORANGE)
    d.polygon([(x0 + 596, deck_y), (x0 + 582, deck_y + 7), (x0 + 596, deck_y + 14)], fill=TEAL_DARK)
    # fallen span: a slab tipping from the left break down into the water
    d.polygon([(x0 + 356, deck_y + 8), (x0 + 574, water_y + 22), (x0 + 560, water_y + 36), (x0 + 344, deck_y + 22)], fill=ORANGE_DARK)
    d.polygon([(x0 + 356, deck_y + 8), (x0 + 574, water_y + 22), (x0 + 568, water_y + 28), (x0 + 350, deck_y + 14)], fill=ORANGE)
    # splash where the slab meets the water
    for sx in (x0 + 500, x0 + 536, x0 + 566):
        d.arc([sx, water_y - 8, sx + 30, water_y + 16], start=180, end=360, fill=WHITE, width=3)
    # smoke rising from the break point (low, attached to the deck)
    for (cx, cy, r) in [(x0 + 372, deck_y - 18, 15), (x0 + 394, deck_y - 32, 20), (x0 + 422, deck_y - 40, 15)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    # flame at the break
    d.polygon([(x0 + 344, deck_y + 4), (x0 + 356, deck_y - 20), (x0 + 368, deck_y + 4)], fill=ORANGE)
    d.polygon([(x0 + 351, deck_y + 3), (x0 + 356, deck_y - 9), (x0 + 361, deck_y + 3)], fill=(255, 176, 66))

def icon(d, kind, cx, cy):
    # cx,cy centre of 48px circle already drawn; draw glyph in white
    if kind == "chip":
        d.rectangle([cx - 13, cy - 13, cx + 13, cy + 13], outline=WHITE, width=3)
        d.rectangle([cx - 5, cy - 5, cx + 5, cy + 5], fill=WHITE)
        for off in (-9, 0, 9):
            d.line([cx + off, cy - 19, cx + off, cy - 13], fill=WHITE, width=3)
            d.line([cx + off, cy + 13, cx + off, cy + 19], fill=WHITE, width=3)
            d.line([cx - 19, cy + off, cx - 13, cy + off], fill=WHITE, width=3)
            d.line([cx + 13, cy + off, cx + 19, cy + off], fill=WHITE, width=3)
    elif kind == "drone":
        for (dx, dy) in [(-14, -12), (14, -12), (-14, 12), (14, 12)]:
            d.ellipse([cx + dx - 7, cy + dy - 4, cx + dx + 7, cy + dy + 4], outline=WHITE, width=2)
            d.line([cx, cy, cx + dx, cy + dy], fill=WHITE, width=2)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=WHITE)
    elif kind == "flag":
        d.line([cx - 12, cy - 18, cx - 12, cy + 18], fill=WHITE, width=3)
        d.polygon([(cx - 12, cy - 18), (cx + 16, cy - 11), (cx - 12, cy - 4)], fill=WHITE)
        d.line([cx - 16, cy + 18, cx + 16, cy + 18], fill=WHITE, width=3)
    elif kind == "exit":
        d.rectangle([cx - 16, cy - 16, cx + 4, cy + 16], outline=WHITE, width=3)
        d.line([cx + 2, cy, cx + 18, cy], fill=WHITE, width=3)
        d.polygon([(cx + 18, cy), (cx + 10, cy - 6), (cx + 10, cy + 6)], fill=WHITE)
    elif kind == "shield":
        d.polygon([(cx, cy - 18), (cx + 15, cy - 11), (cx + 15, cy + 4), (cx, cy + 19), (cx - 15, cy + 4), (cx - 15, cy - 11)], outline=WHITE, width=3)
        d.line([cx - 8, cy, cx - 2, cy + 7], fill=WHITE, width=3)
        d.line([cx - 2, cy + 7, cx + 10, cy - 8], fill=WHITE, width=3)
    elif kind == "jet":
        # top-view fighter jet: nose up, swept wings, tail fins
        d.polygon([(cx, cy - 20), (cx + 5, cy - 6), (cx + 19, cy + 8), (cx + 19, cy + 13),
                   (cx + 6, cy + 9), (cx + 5, cy + 16), (cx + 11, cy + 20), (cx + 2, cy + 20),
                   (cx, cy + 17), (cx - 2, cy + 20), (cx - 11, cy + 20), (cx - 5, cy + 16),
                   (cx - 6, cy + 9), (cx - 19, cy + 13), (cx - 19, cy + 8), (cx - 5, cy - 6)], fill=WHITE)

def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # top rule
    d.rectangle([0, 0, W, 10], fill=TEAL)
    d.rectangle([0, 10, W, 14], fill=ORANGE)

    # Masthead
    d.text((36, 24), "EVERY  STORY  THAT  MATTERED", font=f(SANSB, 21), fill=ORANGE_DARK)
    d.text((36, 48), "TUESDAY, IN FULL", font=f(SERIFB, 66), fill=TEAL)
    # date bar
    d.rectangle([36, 126, 988, 166], fill=ORANGE)
    date_txt = "TUESDAY  \u00b7  17 NOVEMBER 2026  \u00b7  ALL STORIES DATE-CHECKED"
    df = f(SANSB, 21)
    dw = d.textlength(date_txt, font=df)
    d.text(((W - dw) / 2, 135), date_txt, font=df, fill=WHITE)

    # HERO
    d.rounded_rectangle([36, 178, 988, 416], radius=10, fill=LIGHT, outline=TEAL, width=2)
    bridge_illustration(d, 52, 190, 972, 306)
    d.text((52, 314), "KERCH BRIDGE FALLS", font=f(SANSB, 36), fill=DARK)
    # orange underline
    d.rectangle([52, 354, 300, 359], fill=ORANGE)
    hero_cap = ("Ukraine\u2019s overnight strike drops a span into the Kerch Strait; rail damaged, "
                "one lane reopens. Zelenskyy: phase seven. The Kremlin vows to rebuild.")
    draw_wrap(d, (52, 364), hero_cap, f(SANS, 20), GREY, 920, 24)

    # CARDS
    cards = [
        ("chip", TEAL, "NVIDIA: $115.8B QUARTER",
         "First report since Huang stepped down; data centres $107.6B, Q4 guide $130B."),
        ("drone", ORANGE_DARK, "DRONE AT U.S. RADAR, BAHRAIN",
         "Iran fires a drone at a U.S. radar site in Bahrain."),
        ("flag", TEAL, "TRUMP IN MANILA",
         "ASEAN summit closes in Manila with Trump attending."),
        ("exit", ORANGE_DARK, "MONGOLIA PRESIDENT QUITS",
         "Khurelsukh Ukhnaa to resign over a $25M scandal."),
        ("shield", TEAL, "UK SANCTIONS SETTLER FIRMS",
         "Britain sanctions 8 Israeli settler companies."),
        ("jet", ORANGE_DARK, "JAPAN JETS SCRAMBLE",
         "Japanese jets rise to meet Russian aircraft."),
    ]
    card_w, card_h, gap = 309, 172, 12
    top = 428
    for i, (kind, col, head, cap) in enumerate(cards):
        r, c = divmod(i, 3)
        x0 = 36 + c * (card_w + gap)
        y0 = top + r * (card_h + gap)
        x1, y1 = x0 + card_w, y0 + card_h
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD_BG, outline=BORDER, width=2)
        d.rectangle([x0, y0, x1, y0 + 6], fill=col)
        # icon circle
        cx, cy = x0 + 34, y0 + 38
        d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=col)
        icon(d, kind, cx, cy)
        # headline next to icon if short, else below? Put headline to right of icon for first lines
        # Layout: headline starts right of icon, wraps full width below if needed - simpler: headline block right of icon + below
        # We'll render headline in area x0+68 .. x1-14, up to 3 lines at 22px
        hf = f(SANSB, 22)
        lines = wrap(d, head, hf, card_w - 82)
        yy = y0 + 16
        # if headline needs >2 lines, use full-width layout instead
        if len(lines) > 2:
            # icon small top-left, headline full width below icon row
            yy = y0 + 68
            lines = wrap(d, head, hf, card_w - 28)
            for ln in lines:
                d.text((x0 + 14, yy), ln, font=hf, fill=DARK)
                yy += 26
        else:
            for ln in lines:
                d.text((x0 + 68, yy), ln, font=hf, fill=DARK)
                yy += 26
            yy = max(yy + 4, y0 + 68)
        # caption
        draw_wrap(d, (x0 + 14, yy), cap, f(SANS, 20), GREY, card_w - 28, 24)

    # NUMBERS STRIP
    ny0 = 800
    d.rectangle([36, ny0, 988, 884], fill=TEAL)
    d.text((52, ny0 + 10), "THE DAY IN NUMBERS", font=f(SANSB, 20), fill=(255, 176, 66))
    nums = ("$115.8B Nvidia revenue  \u00b7  $130B Q4 guidance  \u00b7  $250M G7 Chernobyl shield fund  \u00b7  "
            "$280M Xi\u2013Carney tariff relief  \u00b7  $25M Mongolia scandal")
    draw_wrap(d, (52, ny0 + 36), nums, f(SANSB, 20), WHITE, 920, 24)

    # BOTTOM TICKER
    by0 = 896
    d.rounded_rectangle([36, by0, 988, 1006], radius=10, fill=(255, 240, 230), outline=ORANGE, width=2)
    d.text((52, by0 + 10), "AND ALSO TUESDAY", font=f(SANSB, 21), fill=ORANGE_DARK)
    ticker = ("Cricket great Dhoni retires from the IPL  \u00b7  Xi\u2013Trump\u2013Putin summit confirmed for "
              "Shenzhen, 19 Nov  \u00b7  One road lane reopens over the Kerch Strait")
    draw_wrap(d, (52, by0 + 38), ticker, f(SANS, 20), DARK, 920, 25)

    d.rectangle([0, 1018, W, 1024], fill=TEAL)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {os.path.getsize(out)} bytes")

if __name__ == "__main__":
    main()
