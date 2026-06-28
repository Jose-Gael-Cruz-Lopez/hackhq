#!/usr/bin/env python3
"""
generate_title.py — render a "decrypting" matrix-style title as an SVG.

The title scrambles through random glyphs and resolves into the real text
(SMIL animation), over a faint matrix-code background. If a viewer doesn't
play SMIL, it still shows the clean decoded title (static fallback).

Usage: python generate_title.py "HACK PHOTO GALLERY" assets/gallery-title.svg
"""

import sys
import random

GLYPHS = "ABCDEF0123456789#%@&$*+=<>/\\|"
GREEN = "#39ff14"
DIM = "#0f3d1a"
BG = "#080b10"


def scramble(text, rng):
    return "".join(c if c == " " else rng.choice(GLYPHS) for c in text)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def make(text, out_path, seed=7):
    rng = random.Random(seed)
    W, H = 900, 150
    cx = W // 2
    cy = 94
    title_size = 34
    adv = 24  # approx per-char advance at this size

    # matrix-code background texture (dim, deterministic)
    bg_chars = []
    for gy in range(20, H - 8, 20):
        for gx in range(16, W - 8, 22):
            if rng.random() < 0.55:
                ch = esc(rng.choice(GLYPHS))
                op = round(rng.uniform(0.12, 0.5), 2)
                bg_chars.append(
                    f'<text x="{gx}" y="{gy}" font-family="monospace" font-size="13" '
                    f'fill="{DIM}" opacity="{op}">{ch}</text>'
                )
    bg = "\n  ".join(bg_chars)

    # Default state = clean decoded title (readable even with no animation).
    # On animation-capable viewers, it briefly "re-scrambles" each 5s loop.
    dur = 5.0
    g = [3.2, 3.6, 4.0, 4.4]  # scramble sub-windows (seconds), then resolve
    glitch = [scramble(text, rng) for _ in range(3)]
    layers = []

    # real title: visible always except hidden during the scramble window
    a0, a1 = g[0] / dur, g[3] / dur
    real_kt = f"0;{a0:.4f};{a0+0.001:.4f};{a1:.4f};{a1+0.001:.4f};1"
    layers.append(
        f'<text x="{cx}" y="{cy}" text-anchor="middle" font-family="monospace" '
        f'font-size="{title_size}" font-weight="bold" letter-spacing="4" '
        f'fill="{GREEN}" opacity="1" filter="url(#glow)">{esc(text)}'
        f'<animate attributeName="opacity" dur="{dur}s" repeatCount="indefinite" '
        f'keyTimes="{real_kt}" values="1;1;0;0;1;1"/></text>'
    )
    # scramble frames: hidden by default, flash only inside their sub-window
    for i, frame in enumerate(glitch):
        a, b = g[i] / dur, g[i + 1] / dur
        kt = f"0;{a:.4f};{a+0.001:.4f};{b:.4f};{b+0.001:.4f};1"
        layers.append(
            f'<text x="{cx}" y="{cy}" text-anchor="middle" font-family="monospace" '
            f'font-size="{title_size}" font-weight="bold" letter-spacing="4" '
            f'fill="#2ea043" opacity="0">{esc(frame)}'
            f'<animate attributeName="opacity" dur="{dur}s" repeatCount="indefinite" '
            f'keyTimes="{kt}" values="0;0;1;1;0;0"/></text>'
        )
    title_layers = "\n  ".join(layers)

    cursor_x = cx + (len(text) * adv) // 2 + 12

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(text)}">
  <defs>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{BG}" stroke="#15311d"/>
  {bg}
  <text x="22" y="30" font-family="monospace" font-size="13" fill="{GREEN}" opacity="0.7">&gt;_ decrypting<tspan>
    <animate attributeName="opacity" dur="1.2s" repeatCount="indefinite" values="0.7;0.2;0.7"/></tspan></text>
  <text x="{W-22}" y="30" text-anchor="end" font-family="monospace" font-size="12" fill="{DIM}">[ ENCRYPTED ]</text>
  {title_layers}
  <rect x="{cursor_x}" y="{cy-30}" width="16" height="36" fill="{GREEN}" opacity="0.9">
    <animate attributeName="opacity" dur="1s" repeatCount="indefinite" values="0.9;0;0.9"/>
  </rect>
</svg>
'''
    with open(out_path, "w") as f:
        f.write(svg)
    print(f"Wrote {out_path} for '{text}'")


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "HACK PHOTO GALLERY"
    out = sys.argv[2] if len(sys.argv) > 2 else "assets/gallery-title.svg"
    make(text, out)
