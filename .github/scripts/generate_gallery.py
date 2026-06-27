#!/usr/bin/env python3
"""
generate_gallery.py — render the community photo gallery into README.md.

Reads .github/scripts/gallery.json (a list of submitted photos) and writes a
responsive 3-column grid between the <!-- GALLERY_START --> / <!-- GALLERY_END -->
markers. Photos are committed under assets/gallery/.

Each gallery.json entry:
{
  "image": "assets/gallery/hackmit-2026-jose.jpg",
  "hackathon": "HackMIT 2026",
  "caption": "Demoing our project at 3am",
  "credit": "Jose Cruz",
  "credit_url": "https://www.linkedin.com/in/josegaelcruz"
}
Only "image" and "hackathon" are required.
"""

import os
import json
import util

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GALLERY_FILE = os.path.join(SCRIPT_DIR, "gallery.json")
README = os.path.join(SCRIPT_DIR, "..", "..", "README.md")
START = "<!-- GALLERY_START -->"
END = "<!-- GALLERY_END -->"
COLS = 3


def load_gallery():
    if not os.path.exists(GALLERY_FILE):
        return []
    with open(GALLERY_FILE, "r") as f:
        return json.load(f)


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def cell(photo):
    image = esc(photo["image"])
    hackathon = esc(photo.get("hackathon", ""))

    img = (
        f'<a href="{image}">'
        f'<img src="{image}" width="260" alt="{hackathon}"></a>'
    )

    return f'    <td align="center" valign="top">\n      {img}\n    </td>'


def build_grid(photos):
    if not photos:
        return (
            "<p align=\"center\"><i>No photos yet. Be the first — "
            "share a shot from a hackathon you found here!</i></p>"
        )
    rows = []
    for i in range(0, len(photos), COLS):
        chunk = photos[i:i + COLS]
        cells = "\n".join(cell(p) for p in chunk)
        rows.append(f"  <tr>\n{cells}\n  </tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def main():
    photos = load_gallery()
    grid = build_grid(photos)
    util.embed_table(README, grid, START, END)
    print(f"Gallery updated: {len(photos)} photo(s).")


if __name__ == "__main__":
    main()
