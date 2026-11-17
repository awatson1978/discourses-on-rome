#!/usr/bin/env python3
"""Bind the 107 apocrypha into one print-ready codex:
lost_books/apocrypha_codex.html (→ PDF via Chrome headless).
Pure assembly — no content composed here."""
import html as H
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "lost_books" / "apocrypha_codex.html"

ERAS = [(11, "292–219 BCE"), (46, "167–91 BCE"), (71, "91–78 BCE"),
        (91, "78–49 BCE"), (109, "49–44 BCE"), (117, "44–30 BCE"),
        (134, "29–9 BCE")]

css = """
@page { size: letter; margin: 24mm 24mm; }
body { font-family: Georgia, serif; color: #1f1a14; line-height: 1.6;
       max-width: 44em; margin: 0 auto; padding: 24px; font-size: 13.5px; }
h1 { font-variant: small-caps; letter-spacing: 1.5px; font-size: 30px;
     color: #8b2500; text-align: center; margin: 120px 0 6px 0; }
.tsub { text-align: center; color: #7a7265; font-style: italic; }
.warn { background: #fdf3f1; border: 1.5px solid #a03020; border-radius: 6px;
        padding: 14px 18px; font-size: 12.5px; margin: 40px 0; }
h2.era { font-variant: small-caps; color: #1f4e5f; font-size: 19px;
         page-break-before: always; border-bottom: 2px solid #e3ddd0;
         padding-top: 60px; }
h3 { font-variant: small-caps; color: #8b2500; font-size: 16px;
     margin-top: 28px; page-break-after: avoid; }
blockquote { font-size: 10.5px; color: #9a5a50; border-left: 2px solid #d8a79f;
             margin: 6px 0 12px 0; padding: 2px 10px; line-height: 1.4; }
.ev { font-size: 10px; color: #8a8273; border-top: 1px dotted #d8cdb4;
      margin-top: 10px; padding-top: 4px; line-height: 1.45; }
p { margin: 8px 0; }
.cite { color: #1f4e5f; font-size: 10.5px; }
"""


def render(md_text):
    body = re.sub(r"^---.*?---\s*", "", md_text, flags=re.S)
    body = re.sub(r"^# .*$", "", body, count=1, flags=re.M)
    # pull the blockquote disclaimer
    disc_lines = [l[1:].strip().replace("**", "") for l in body.splitlines() if l.startswith(">")]
    prose_lines, ev_line = [], ""
    in_ev = False
    for l in body.splitlines():
        if l.startswith(">"):
            continue
        if l.strip().startswith("*Events:"):
            in_ev = True
        if in_ev:
            ev_line += " " + l.strip()
        elif l.strip() and not l.strip().startswith("---"):
            line = l.strip().replace("**", "")
            if line.startswith("*") and line.endswith("*") and len(line) > 2:
                line = line[1:-1]
            prose_lines.append(line)
    prose = "\n".join(f"<p>{H.escape(p)}</p>" for p in prose_lines)
    prose = re.sub(r"\[(\d+\.\d+(?:[-–]\d+)?)\]",
                   r"<span class='cite'>[\1]</span>", prose)
    ev = H.escape(ev_line.replace("*Events:", "Events:").strip(" *"))
    return (f"<blockquote>{H.escape(' '.join(disc_lines))}</blockquote>"
            f"{prose}<div class='ev'>{ev}</div>")


def main():
    files = sorted((ROOT / "apocrypha").glob("book_*.md"))
    parts = [f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>The Apocrypha of Livy</title><style>{css}</style></head><body>
<h1>The Apocrypha of Livy</h1>
<p class="tsub">The Lost Books of Ab Urbe Condita<br>
rendered as modern English compositions in Livy's manner, from the attested
skeleton of the derivative tradition<br>the Lost Books Program ·
github.com/awatson1978/discourses-on-rome</p>
<p class="tsub" style="margin-top:28px">© 2026 Abigail Watson.<br>
All rights reserved.</p>
<div class="warn"><b>None of this is Livy.</b> Every page below is a modern,
AI-composed English imitation whose content is restricted to events attested
in the ancient summaries (bracketed citations resolve to
lost_books/periocha_events.jsonl, where each event carries a machine-validated
verbatim Latin quote from its periocha). Style is the only invented layer; no
Latin is composed anywhere; nothing here is evidence for anything. Calibration
from simulated-loss experiments on surviving books: skeletons like these
capture roughly 20–47% of a book's original domestic record, biased toward
the spectacular and against institutional process. The real books remain
lost. For the places where Livy's actual words survive, see
reports/lost_fragments.pdf.</div>"""]
    era_iter = iter(ERAS)
    next_era = next(era_iter, None)
    for fn in files:
        book = int(fn.stem.split("_")[1])
        if next_era and book >= next_era[0]:
            parts.append(f"<h2 class='era'>{H.escape(next_era[1])}</h2>")
            next_era = next(era_iter, None)
        parts.append(f"<h3>Book {book}</h3>")
        parts.append(render(fn.read_text(encoding="utf-8")))
    parts.append("</body></html>")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"apocrypha_codex.html: {len(files)} books, {OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
