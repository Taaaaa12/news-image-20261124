#!/usr/bin/env python3
"""Compose the 24 November 2026 front-page image (1024x1024 PNG).

Written fresh in this session. Layout: dark navy front page, gold globe
motif, masthead, date line, five stories with coloured kickers, footer.
Output: entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (13, 27, 46)
NAVY_LIGHT = (19, 38, 62)
GOLD = (212, 164, 55)
WHITE = (245, 242, 235)
MUTED = (168, 182, 196)
RULE = (90, 110, 130)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

STORIES = [
    ("KOREA · ULLEUNG", (231, 76, 60),
     "Russian jet enters South Korean airspace",
     "Ulleung island evacuation warning briefly issued"),
    ("THE GULF · HORMUZ", (243, 156, 18),
     "UN counts 25 seafarers killed near Hormuz",
     "Death toll rises from tanker attacks in the strait"),
    ("BALTIC · ESTONIA", (93, 173, 226),
     "Russia warns Estonia of 'open war'",
     "Moscow fumes over planned border closure"),
    ("NEPAL · NEW DELHI", (39, 174, 96),
     "India pledges $1.6bn to rebuild Nepal",
     "Flood recovery package agreed in Modi\u2013Shah talks"),
    ("GAZA", (142, 68, 173),
     "Israeli strikes kill three, including UN worker",
     "UN staffer among the dead in Gaza City"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to lines that fit max_w (measured with getlength)."""
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


def draw_globe(draw, cx, cy, r):
    """Simple gold wireframe globe: outline, meridians, parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    draw.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
                 outline=GOLD, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=GOLD, width=2)
    draw.line([cx - int(r * 0.87), cy - int(r * 0.5),
               cx + int(r * 0.87), cy - int(r * 0.5)], fill=GOLD, width=2)
    draw.line([cx - int(r * 0.87), cy + int(r * 0.5),
               cx + int(r * 0.87), cy + int(r * 0.5)], fill=GOLD, width=2)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    mx = 64                      # side margin
    content_w = W - 2 * mx

    # Globe motif, centred near the top.
    draw_globe(d, W // 2, 78, 42)

    # Masthead.
    f_mast = font(SERIF_B, 58)
    mast = "THE WORLD TODAY"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 132), mast,
           font=f_mast, fill=WHITE)

    # Gold rule under the masthead.
    d.line([mx, 212, W - mx, 212], fill=GOLD, width=3)
    d.line([mx, 218, W - mx, 218], fill=GOLD, width=1)

    # Date line + subtitle.
    f_date = font(SANS_B, 26)
    date = "TUESDAY, 24 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 232), date,
           font=f_date, fill=GOLD)
    f_sub = font(SANS, 22)
    sub = "Five stories that defined the day"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 266), sub,
           font=f_sub, fill=MUTED)

    # Story blocks.
    f_kick = font(SANS_B, 20)
    f_head = font(SANS_B, 33)
    f_deck = font(SANS, 21)
    y = 310
    block_h = 128
    for i, (kicker, colour, headline, deck) in enumerate(STORIES):
        d.text((mx, y), kicker, font=f_kick, fill=colour)
        lines = wrap(d, headline, f_head, content_w)
        assert len(lines) <= 2, f"headline too long: {headline!r} -> {lines}"
        hy = y + 28
        for ln in lines:
            d.text((mx, hy), ln, font=f_head, fill=WHITE)
            hy += 38
        dy = y + 28 + 38 * len(lines) + 4
        assert d.textlength(deck, font=f_deck) <= content_w, \
            f"deck too long: {deck!r}"
        d.text((mx, dy), deck, font=f_deck, fill=MUTED)
        if i < len(STORIES) - 1:
            d.line([mx, y + block_h - 6, W - mx, y + block_h - 6],
                   fill=RULE, width=1)
        y += block_h

    # Footer.
    f_foot = font(SANS, 18)
    foot = "Compiled from wire and UN reports \u00b7 24 November 2026"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 968), foot,
           font=f_foot, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
