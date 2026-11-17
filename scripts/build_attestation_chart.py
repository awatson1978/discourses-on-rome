#!/usr/bin/env python3
"""Attestation-density chart across all 142 books of Ab Urbe Condita.

One dot = one attested item:
  teal   — coded political event from surviving full text (891, books 1-10/21-45)
  gold   — periocha-derived skeleton event (lost books; evidence: hypothetical)
  red ◆  — attested verbatim fragment of a lost book (Book 91 palimpsest,
           Book 120 via Seneca)
  grey × — books 136-137: periocha itself lost; nothing to plot

Output: dashboard/img/attestation_142.svg (self-contained, GitHub-renderable)
"""
import collections
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "dashboard" / "img" / "attestation_142.svg"


def jl(p):
    f = ROOT / p
    return [json.loads(l) for l in f.open(encoding="utf-8")] if f.exists() else []


def main():
    extant = collections.Counter(e["book"] for e in jl("extractions/livy_events.jsonl"))
    skeleton = collections.Counter(e["book"] for e in jl("lost_books/periocha_events.jsonl"))
    frags = collections.Counter(
        f["book"] for f in jl("lost_books/fragments.jsonl") if f.get("book"))
    doubly_lost = {136, 137}

    # geometry
    left, bottom_pad, top_pad = 46, 46, 56
    colw, r, dy = 9.2, 2.6, 6.0
    W = left + 142 * colw + 20
    maxdots = max(max(extant.values()), max(skeleton.values()) if skeleton else 1)
    H = top_pad + maxdots * dy + bottom_pad

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
             f'font-family="Georgia,serif">')
    s.append(f'<rect width="{W:.0f}" height="{H:.0f}" fill="#ffffff"/>')
    s.append(f'<text x="{left}" y="24" font-size="17" fill="#8b2500" '
             f'style="font-variant:small-caps;letter-spacing:.5px">Ab Urbe Condita — attestation density, all 142 books</text>')
    s.append(f'<text x="{left}" y="42" font-size="11" fill="#7a7265" font-style="italic">'
             f'one dot = one attested item · teal: coded event in surviving text · '
             f'gold: periocha-derived skeleton event (hypothetical) · red ◆: verbatim fragment survives · ×: periocha itself lost</text>')

    baseline = H - bottom_pad
    # era shading for lost ranges
    for lo, hi in [(11, 20), (46, 142)]:
        x0 = left + (lo - 1) * colw - colw / 2 + colw / 2
        x1 = left + (hi - 1) * colw + colw / 2 + colw / 2
        s.append(f'<rect x="{x0:.1f}" y="{top_pad - 6}" width="{x1 - x0:.1f}" '
                 f'height="{baseline - top_pad + 6:.1f}" fill="#f7f4ee"/>')

    s.append(f'<line x1="{left}" y1="{baseline + .5}" x2="{W - 14}" y2="{baseline + .5}" '
             f'stroke="#e3ddd0" stroke-width="1"/>')

    for b in range(1, 143):
        cx = left + (b - 1) * colw + colw / 2
        n_ext = extant.get(b, 0)
        n_skel = skeleton.get(b, 0)
        for i in range(n_ext):
            s.append(f'<circle cx="{cx:.1f}" cy="{baseline - r - i * dy:.1f}" '
                     f'r="{r}" fill="#1f4e5f" opacity="0.88"/>')
        for i in range(n_skel):
            s.append(f'<circle cx="{cx:.1f}" cy="{baseline - r - i * dy:.1f}" '
                     f'r="{r}" fill="#c7903c" opacity="0.92"/>')
        if frags.get(b):
            fy = baseline - r - max(n_ext, n_skel) * dy - 7
            s.append(f'<path d="M {cx:.1f} {fy - 4.4:.1f} l 4.4 4.4 l -4.4 4.4 l -4.4 -4.4 z" '
                     f'fill="#a03020"/>')
        if b in doubly_lost:
            s.append(f'<text x="{cx:.1f}" y="{baseline - 3:.1f}" font-size="10" '
                     f'fill="#9a9183" text-anchor="middle">×</text>')
        if b % 10 == 0 or b == 1:
            s.append(f'<text x="{cx:.1f}" y="{baseline + 16}" font-size="10" '
                     f'fill="#5a4a33" text-anchor="middle">{b}</text>')
    s.append(f'<text x="{left + 14.5 * colw:.1f}" y="{baseline + 32}" font-size="10" '
             f'fill="#9a9183" text-anchor="middle">books 11–20 lost</text>')
    s.append(f'<text x="{left + 93 * colw:.1f}" y="{baseline + 32}" font-size="10" '
             f'fill="#9a9183" text-anchor="middle">books 46–142 lost — attested only through the derivative tradition</text>')
    s.append('</svg>')
    OUT.write_text("\n".join(s), encoding="utf-8")

    n_books_skel = len(skeleton)
    print(f"attestation_142.svg: extant events {sum(extant.values())} across "
          f"{len(extant)} books | skeleton events {sum(skeleton.values())} across "
          f"{n_books_skel} lost books | fragment markers: {sorted(frags)}")


if __name__ == "__main__":
    main()
