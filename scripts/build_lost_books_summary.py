#!/usr/bin/env python3
"""The gold-dots dossier: reports/lost_books_summary.html (print to PDF via Chrome).

Book-by-book through all 107 lost books: era, the periocha-derived skeleton
events (the gold dots of the attestation chart), witness pointers (Obsequens
year-entries, Plutarch/Dio crosswalk), fragment markers. Everything rendered
from the structured files — no content composed here.
"""
import collections
import html as H
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reports" / "lost_books_summary.html"

CAT_BADGE = {"war": "#7a4f2a", "domestic-politics": "#8b2500", "institution": "#1f4e5f",
             "prominent-death": "#55503f", "trial": "#6b3fa0", "prodigy-religion": "#9a7b2f",
             "foreign-diplomacy": "#2f6b5f", "other": "#8a7a63"}


def jl(p):
    f = ROOT / p
    return [json.loads(l) for l in f.open(encoding="utf-8")] if f.exists() else []


def main():
    skeleton = {r["book"]: r for r in jl("lost_books/skeleton.jsonl")}
    events = collections.defaultdict(list)
    for e in jl("lost_books/periocha_events.jsonl"):
        events[e["book"]].append(e)
    frags = collections.defaultdict(list)
    for f in jl("lost_books/fragments.jsonl"):
        if f.get("book"):
            frags[f["book"]].append(f)
    obs_by_book = collections.Counter()
    for o in jl("lost_books/obsequens_map.jsonl"):
        if o.get("livy_book_estimate"):
            obs_by_book[o["livy_book_estimate"]] += 1
    para = collections.Counter()
    for f in ["lost_books/parallels_florus_eutropius.jsonl", "lost_books/parallels_orosius.jsonl"]:
        for r in jl(f):
            para[r["livy_book"]] += 1
    nwm_path = ROOT / "lost_books/narrative_witness_map.json"
    nwm = json.loads(nwm_path.read_text(encoding="utf-8"))["by_book"] if nwm_path.exists() else {}

    css = """
    @page { size: letter; margin: 22mm 20mm; }
    body { font-family: Georgia, serif; color: #1f1a14; line-height: 1.5;
           max-width: 50em; margin: 0 auto; padding: 24px; font-size: 13.5px; }
    h1 { font-variant: small-caps; letter-spacing: 1px; font-size: 25px;
         color: #8b2500; margin-bottom: 2px; }
    .sub { color: #7a7265; font-style: italic; margin-top: 0; }
    h2 { font-variant: small-caps; color: #1f4e5f; font-size: 17px;
         border-bottom: 2px solid #e3ddd0; margin-top: 30px; page-break-after: avoid; }
    h3 { color: #8b2500; font-size: 14.5px; margin: 18px 0 4px 0; page-break-after: avoid; }
    .wit { font-size: 11.5px; color: #7a7265; margin: 2px 0 6px 0; }
    ul { margin: 4px 0 4px 18px; padding: 0; }
    li { margin: 2.5px 0; }
    .cat { font-size: 9.5px; padding: 1px 6px; border-radius: 8px; color: #fff;
           letter-spacing: .3px; }
    .frag { background: #fdf3f1; border-left: 3px solid #a03020; padding: 6px 10px;
            font-size: 12px; margin: 6px 0; }
    .lost2 { color: #9a9183; font-style: italic; }
    .intro { background: #faf8f3; border: 1px solid #e3ddd0; border-radius: 5px;
             padding: 10px 14px; font-size: 12.5px; }
    """
    parts = [f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>The Lost Books of Livy — a summary from the derivative tradition</title>
<style>{css}</style></head><body>
<h1>The Lost Books of Livy</h1>
<p class="sub">What the derivative tradition preserves of Ab Urbe Condita's
107 lost books — the gold dots of the attestation chart ·
github.com/awatson1978/discourses-on-rome · 2026-11-17</p>
<div class="intro"><b>What this is.</b> One section per lost book. The bullet
lists are <b>periocha-derived skeleton events</b> (710 total): each is what the
ancient summary attests, extracted with a machine-validated verbatim Latin
quote on file (lost_books/periocha_events.jsonl), evidence class
<i>hypothetical-skeleton</i>. Witness lines give the attested entry counts and
the DRAFT Plutarch/Dio crosswalk (era-anchored, non-evidentiary). Red boxes
mark the only books whose actual words survive. Calibration from the
simulated-loss experiments: expect this skeleton to capture roughly 20–47%
of a book's original domestic-political record, biased toward the
spectacular and against institutional process.</div>"""]

    current_era = None
    for book in sorted(skeleton):
        r = skeleton[book]
        if r["era_block"] != current_era:
            current_era = r["era_block"]
            parts.append(f"<h2>{H.escape(current_era)} — {H.escape(r['era_description'])}</h2>")
        parts.append(f"<h3>Book {book}</h3>")
        wit_bits = []
        if obs_by_book.get(book):
            wit_bits.append(f"Obsequens: {obs_by_book[book]} year-entries")
        if para.get(book):
            wit_bits.append(f"epitome parallels: {para[book]} (Florus/Eutropius/Orosius)")
        m = nwm.get(str(book), {})
        if m.get("plutarch"):
            wit_bits.append("Plutarch: " + ", ".join(m["plutarch"][:3]))
        if m.get("dio"):
            wit_bits.append(f"Dio: {m['dio']}")
        if wit_bits:
            parts.append(f"<div class='wit'>{H.escape(' · '.join(wit_bits))}</div>")
        for f in frags.get(book, []):
            status = "words survive — see the fragments dossier" \
                if f.get("text_la") else "fragment attested; text pending acquisition"
            parts.append(f"<div class='frag'><b>◆ Verbatim fragment:</b> "
                         f"{H.escape(f['witness'])} — {H.escape(status)}</div>")
        evs = events.get(book, [])
        if evs:
            parts.append("<ul>")
            for e in evs:
                color = CAT_BADGE.get(e["category"], "#8a7a63")
                parts.append(f"<li>{H.escape(e['summary_en'])} "
                             f"<span class='cat' style='background:{color}'>"
                             f"{H.escape(e['category'])}</span></li>")
            parts.append("</ul>")
        elif book in (136, 137):
            parts.append("<p class='lost2'>Doubly lost: even the ancient summary "
                         "of this book perished. Era context is all that remains.</p>")
    parts.append("</body></html>")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    n_ev = sum(len(v) for v in events.values())
    print(f"lost_books_summary.html: {len(skeleton)} books, {n_ev} skeleton events, "
          f"{OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
