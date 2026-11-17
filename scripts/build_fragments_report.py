#!/usr/bin/env python3
"""Generate the lost-fragments dossier: reports/lost_fragments.html (print-ready).

Content: every record in lost_books/fragments.jsonl, with acquired Latin text
rendered verbatim from the file (never retyped here), transmission notes, and
working English translations (clearly labeled as this project's, unreviewed).
Render to PDF with: Chrome --headless --print-to-pdf.
"""
import html as H
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reports" / "lost_fragments.html"

# Working translations, keyed by fragment_id. Labeled in the document as
# unreviewed project translations; the Latin alongside is the authority.
TRANSLATIONS = {
    "frag:b120:seneca-suasoriae-6-17": """Marcus Cicero had left the city shortly before the arrival of the triumvirs, holding it for certain — as was true — that he could no more be snatched from Antony than Cassius and Brutus from Caesar. First he had fled to his Tusculan estate; from there he set out by cross-roads to his villa at Formiae, intending to board a ship at Caieta. Having put out to sea several times, when contrary winds now carried him back, and now he himself could not endure the tossing of the ship as the blind swell rolled it, weariness at last overcame him — of flight and of life alike — and returning to his upper villa, which stands a little more than a mile from the sea, he said: "I shall die in the fatherland I have so often saved." It is well established that his slaves were ready to fight bravely and faithfully; it was he who ordered them to set the litter down and to suffer quietly what an unjust fortune compelled. As he leaned from the litter and offered his neck unmoving, his head was struck off. Nor was that enough for the soldiers' doltish cruelty: they cut off the hands too, reproaching them for having written something against Antony. So the head was carried back to Antony and by his order set between the two hands on the Rostra — where as consul, where so often as an ex-consul, where in that very year against Antony, he had been heard with such admiration of his eloquence as no human voice ever earned. Scarcely lifting eyes wet with tears, men could not look upon the butchered limbs of their fellow citizen.""",
    "frag:b120:seneca-suasoriae-6-22": """He lived sixty-three years, so that even had no violence intervened, his death could not seem untimely. His genius was fortunate in its works and in their rewards; he himself long enjoyed prosperous fortune; but amid that long course of happiness he was struck at intervals by heavy wounds — exile, the ruin of the party he had stood for, the death of a beloved daughter so sad and bitter — and of all his adversities he bore none as became a man except his death, which, weighed truly, could seem the less undeserved in that he suffered from his victorious enemy nothing more cruel than he would have done, had he enjoyed the same fortune, to the vanquished. Yet if one weighs his virtues against his faults, he was a great and memorable man — and to tell out his praises, one would need a Cicero for the eulogist.""",
}


def main():
    frags = [json.loads(l) for l in
             (ROOT / "lost_books/fragments.jsonl").open(encoding="utf-8")]
    css = """
    @page { size: letter; margin: 25mm 22mm; }
    body { font-family: Georgia, 'Iowan Old Style', serif; color: #1f1a14;
           line-height: 1.55; max-width: 46em; margin: 0 auto; padding: 24px; }
    h1 { font-variant: small-caps; letter-spacing: 1px; font-size: 26px;
         color: #8b2500; margin-bottom: 2px; }
    .sub { color: #7a7265; font-style: italic; margin-top: 0; }
    h2 { font-variant: small-caps; color: #8b2500; font-size: 18px;
         border-bottom: 1px solid #e3ddd0; padding-bottom: 4px; margin-top: 34px; }
    .meta { font-size: 12.5px; color: #55503f; background: #faf8f3;
            border: 1px solid #e3ddd0; border-radius: 5px; padding: 10px 14px; }
    .meta b { color: #1f4e5f; }
    .latin { font-style: italic; background: #fbfaf7; border-left: 3px solid #8b2500;
             padding: 12px 16px; margin: 14px 0; font-size: 14.5px; }
    .trans { padding: 2px 16px 2px 16px; font-size: 14px; }
    .translabel { font-size: 11px; color: #9a9183; text-transform: uppercase;
                  letter-spacing: .8px; margin: 10px 0 2px 16px; }
    .pending { color: #7a7265; font-style: italic; }
    .rule { font-size: 12.5px; color: #7a7265; border-top: 1px solid #e3ddd0;
            margin-top: 36px; padding-top: 10px; }
    """
    parts = [f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>The Fragments of Lost Livy</title><style>{css}</style></head><body>
<h1>The Fragments of Lost Livy</h1>
<p class="sub">Verbatim survivals of the 107 lost books of Ab Urbe Condita —
a dossier of the Lost Books Program ·
github.com/awatson1978/discourses-on-rome · 2026-11-17</p>
<p>Of Livy's 142 books, 107 are lost. Their <i>content</i> survives in
summaries and epitomes — the Periochae, Obsequens, Florus, Orosius — but
their <i>words</i> survive in only a handful of places: one physical
palimpsest, and quotations by later authors who name their source. This
dossier lists every verbatim fragment known to this project. Rule of the
registry: fragment text enters only from an acquired, cited witness text,
machine-validated as a verbatim substring; summaries, paraphrases, and
reconstructions are never fragments.</p>"""]

    for f in frags:
        book = f.get("book")
        title = (f"Book {book}" if book else "Scattered citations")
        summary_head = f['content_summary']
        cut = summary_head.find('. ', 40)
        if cut == -1:
            cut = min(len(summary_head), 90)
        parts.append(f"<h2>{H.escape(title)} — {H.escape(summary_head[:cut].rstrip('.'))}.</h2>")
        parts.append(
            f"<div class='meta'><b>Fragment:</b> {H.escape(f['fragment_id'])}<br>"
            f"<b>Transmission:</b> {H.escape(f['transmission'])}<br>"
            f"<b>Witness:</b> {H.escape(f['witness'])}<br>"
            f"<b>Status:</b> {H.escape(f['text_status'])}</div>")
        if f.get("text_la"):
            parts.append(f"<div class='latin'>{H.escape(f['text_la'])}</div>")
            tr = TRANSLATIONS.get(f["fragment_id"])
            if tr:
                parts.append("<div class='translabel'>Working translation — this "
                             "project (AI-assisted, unreviewed); the Latin is the authority</div>")
                parts.append(f"<div class='trans'>{H.escape(tr)}</div>")
        else:
            parts.append(f"<p class='pending'>Text not yet acquired into this "
                         f"corpus. {H.escape(f['content_summary'])}</p>")

    parts.append("""<p class="rule">Method: fragments registry at
lost_books/fragments.jsonl; witness texts at corpus/segments/witnesses_la.jsonl
(Seneca Maior, Suasoriae, The Latin Library text — no critical apparatus;
readings in parentheses are that text's editorial supplements). The Book 120
attributions are Seneca's own, marked "T. LIVI" in the transmitted text. The
Book 91 palimpsest (Vat. Pal. lat. 24, recovered 1772) awaits acquisition
from a public-domain transcription. Translations are working aids produced by
this project and have not been reviewed by a Latinist. Everything here is
reproducible: scripts/build_fragments_report.py.</p></body></html>""")

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"lost_fragments.html written ({OUT.stat().st_size // 1024} KB, "
          f"{len(frags)} fragment records)")


if __name__ == "__main__":
    main()
