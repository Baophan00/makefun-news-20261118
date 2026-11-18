#!/usr/bin/env python3
"""Deterministic 1024x1024 editorial poster. Standard library + Pillow only."""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

S = 2048
OUT = 1024
ROOT = Path(__file__).resolve().parent

NAVY = (8, 15, 32)
CARD = (16, 27, 51)
LINE = (40, 56, 86)
WHITE = (244, 247, 252)
MUTED = (152, 170, 198)
AMBER = (255, 186, 46)
RED = (255, 84, 84)
CYAN = (62, 220, 236)
TEAL = (58, 212, 162)

BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, max_w, start):
    """Largest font at or below start whose rendered text fits max_w."""
    size = start
    while size > 12:
        f = font(path, size)
        box = draw.textbbox((0, 0), text, font=f)
        if box[2] - box[0] <= max_w:
            return f
        size -= 2
    return font(path, size)


def thick_line(d, p0, p1, w, fill):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    length = math.hypot(dx, dy)
    nx, ny = -dy / length * w / 2, dx / length * w / 2
    d.polygon(
        [
            (p0[0] + nx, p0[1] + ny),
            (p1[0] + nx, p1[1] + ny),
            (p1[0] - nx, p1[1] - ny),
            (p0[0] - nx, p0[1] - ny),
        ],
        fill=fill,
    )


def icon_faces(d, cx, cy, c):
    """Two facing profile circles."""
    r = 54
    for off, a0, a1, eye in (
        (-62, -50, 50, (28, -12)),
        (62, 130, 230, (-28, -12)),
    ):
        x = cx + off
        d.ellipse([x - r, cy - r, x + r, cy + r], fill=c)
        d.pieslice([x - r, cy - r, x + r, cy + r], a0, a1, fill=WHITE)
        d.ellipse(
            [x + eye[0] - 8, cy + eye[1] - 8, x + eye[0] + 8, cy + eye[1] + 8],
            fill=NAVY,
        )


def icon_missile_ship(d, cx, cy, c):
    """Missile over a ship."""
    d.polygon(
        [(cx - 100, cy + 38), (cx + 100, cy + 38), (cx + 72, cy + 76), (cx - 72, cy + 76)],
        fill=c,
    )
    d.rectangle([cx - 62, cy + 16, cx + 62, cy + 36], fill=WHITE)
    d.rectangle([cx - 6, cy - 18, cx + 6, cy + 16], fill=WHITE)

    p0 = (cx - 74, cy - 26)
    p1 = (cx + 22, cy - 92)
    thick_line(d, p0, p1, 20, WHITE)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux
    nose = (p1[0] + ux * 34, p1[1] + uy * 34)
    d.polygon(
        [
            (p1[0] + nx * 10, p1[1] + ny * 10),
            nose,
            (p1[0] - nx * 10, p1[1] - ny * 10),
        ],
        fill=c,
    )
    for k in (1, 2, 3):
        qx, qy = p0[0] - ux * k * 22, p0[1] - uy * k * 22
        d.ellipse([qx - 6, qy - 6, qx + 6, qy + 6], fill=WHITE)


def icon_bridge(d, cx, cy, c):
    """Broken bridge."""
    d.polygon(
        [
            (cx - 110, cy - 10), (cx - 20, cy - 10), (cx - 34, cy + 6),
            (cx - 14, cy + 22), (cx - 110, cy + 22),
        ],
        fill=c,
    )
    d.polygon(
        [
            (cx + 110, cy - 10), (cx + 20, cy - 10), (cx + 34, cy + 6),
            (cx + 14, cy + 22), (cx + 110, cy + 22),
        ],
        fill=c,
    )
    for tx in (cx - 82, cx + 82):
        d.rectangle([tx - 8, cy - 78, tx + 8, cy - 10], fill=WHITE)
        d.line([(tx, cy - 76), (tx - 66 if tx < cx else tx + 66, cy - 10)], fill=WHITE, width=6)
        d.line([(tx, cy - 76), (tx + 54 if tx < cx else tx - 54, cy - 10)], fill=WHITE, width=6)
    d.line([(cx - 110, cy + 56), (cx - 40, cy + 56)], fill=WHITE, width=5)
    d.line([(cx + 40, cy + 56), (cx + 110, cy + 56)], fill=WHITE, width=5)
    d.rectangle([cx - 10, cy + 40, cx + 2, cy + 52], fill=WHITE)
    d.rectangle([cx + 12, cy + 62, cx + 24, cy + 74], fill=WHITE)


def icon_quad(d, cx, cy, c):
    """Four linked dots."""
    pts = [(cx, cy - 62), (cx + 62, cy), (cx, cy + 62), (cx - 62, cy)]
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        d.line([a, b], fill=WHITE, width=10)
    for x, y in pts:
        d.ellipse([x - 24, y - 24, x + 24, y + 24], fill=c, outline=WHITE, width=6)


def icon_ballot(d, cx, cy, c):
    """Ballot checkbox."""
    d.rounded_rectangle([cx - 72, cy - 72, cx + 72, cy + 72], radius=16, outline=WHITE, width=10)
    d.line(
        [(cx - 42, cy + 4), (cx - 12, cy + 36), (cx + 48, cy - 34)],
        fill=c,
        width=18,
        joint="curve",
    )


def icon_chip(d, cx, cy, c):
    """Microchip."""
    x0, y0, x1, y1 = cx - 58, cy - 58, cx + 58, cy + 58
    for i in (-2, -1, 0, 1, 2):
        p = cx + i * 26
        d.rectangle([p - 6, y0 - 22, p + 6, y0], fill=WHITE)
        d.rectangle([p - 6, y1, p + 6, y1 + 22], fill=WHITE)
        d.rectangle([x0 - 22, p - 6, x0, p + 6], fill=WHITE)
        d.rectangle([x1, p - 6, x1 + 22, p + 6], fill=WHITE)
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=c)
    d.rounded_rectangle([cx - 28, cy - 28, cx + 28, cy + 28], radius=6, outline=WHITE, width=8)


CARDS = [
    ("SHENZHEN", "XI + PUTIN", "APEC BEFORE TRUMP", AMBER, icon_faces),
    ("GULF", "IRAN - US BASES", "QESHM STRUCK, HORMUZ", RED, icon_missile_ship),
    ("UKRAINE", "KERCH BRIDGE", "DESTROYED", CYAN, icon_bridge),
    ("MANILA", "QUAD SUMMIT", "FIRST IN 2 YEARS", TEAL, icon_quad),
    ("ALASKA", "PELTOLA WINS", "SENATE FLIPS", AMBER, icon_ballot),
    ("TECH + MARKETS", "NVIDIA 115.8B", "OUTAGES, GOLD BELOW 3.8K", CYAN, icon_chip),
]


def draw_card(d, x, y, w, h, card):
    top, head, sub, color, icon = card
    d.rounded_rectangle([x, y, x + w, y + h], radius=24, fill=CARD, outline=LINE, width=4)
    d.rounded_rectangle([x, y, x + 14, y + h], radius=7, fill=color)
    icon(d, x + 150, y + h // 2, color)

    tx = x + 280
    max_w = w - 280 - 36
    f_top = fit_font(d, top, BOLD, max_w, 50)
    f_head = fit_font(d, head, BOLD, max_w, 66)
    f_sub = fit_font(d, sub, REG, max_w, 42)
    d.text((tx, y + 82), top, font=f_top, fill=color)
    d.text((tx, y + 166), head, font=f_head, fill=WHITE)
    d.text((tx, y + 282), sub, font=f_sub, fill=MUTED)


def main():
    img = Image.new("RGB", (S, S), NAVY)
    d = ImageDraw.Draw(img)

    m = 92
    d.rectangle([m, 70, m + 120, 82], fill=AMBER)
    d.text((m, 118), "WORLD NEWS", font=font(BOLD, 196), fill=WHITE)
    d.text((m + 4, 348), "18 NOVEMBER 2026", font=font(BOLD, 76), fill=AMBER)
    d.text((m + 4, 452), "ONE DAY / SIX STORIES", font=font(REG, 56), fill=MUTED)
    d.rectangle([m, 548, S - m, 552], fill=LINE)

    gap = 40
    cw = (S - 2 * m - gap) // 2
    ch, vgap, top = 420, 40, 610
    for i, card in enumerate(CARDS):
        x = m + (i % 2) * (cw + gap)
        y = top + (i // 2) * (ch + vgap)
        draw_card(d, x, y, cw, ch, card)

    resample = getattr(getattr(Image, "Resampling", None), "LANCZOS", getattr(Image, "LANCZOS", 3))
    img = img.resize((OUT, OUT), resample)
    out = ROOT / "entry.png"
    img.save(out)
    with Image.open(out) as check:
        print(f"{out} | {check.size[0]}x{check.size[1]} px | {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
