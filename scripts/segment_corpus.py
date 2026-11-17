#!/usr/bin/env python3
"""Segment raw corpus files into stable-ID passage records (JSONL).

Outputs (corpus/segments/):
  discorsi_it.jsonl  ids like disc:it:1:7   (book:chapter; 0 = dedica/proemio)
  discorsi_en.jsonl  ids like disc:en:1:7   (Thomson 1883)
  livy_la.jsonl      ids like livy:la:2:34  (book:chapter, Perseus lat2)
  livy_en.jsonl      ids like livy:en:2:34  (Perseus eng2, Spillan et al.)

Each record: passage_id, work, lang, edition, book, chapter, heading, text,
sections (livy only: {n: text}), source_file.
"""
import json
import pathlib
import re
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "corpus" / "raw"
SEG = ROOT / "corpus" / "segments"
TEI = "{http://www.tei-c.org/ns/1.0}"

ROMAN = {}
def _roman(n):
    vals = [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),
            (50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]
    s = ''
    for v, r in vals:
        while n >= v:
            s += r; n -= v
    return s
for i in range(1, 70):
    ROMAN[_roman(i)] = i


def write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{path.name}: {len(records)} records")


def segment_discorsi_it():
    src = RAW / "discorsi_it"
    out = []
    for fn in sorted(src.glob("*.json")):
        if fn.name == "manifest.json":
            continue
        rec = json.loads(fn.read_text(encoding="utf-8"))
        if "error" in rec:
            continue
        key = rec["key"]
        if key == "dedica":
            book, chap = 0, 0
        elif key.endswith(".proemio"):
            book, chap = int(key.split(".")[0]), 0
        else:
            book, chap = (int(x) for x in key.split("."))
        text = rec["plain_text"]
        # drop wikisource furniture: metadata header (escaped dc: block and
        # URL/timestamp echoes) and nav lines
        text = re.sub(r"&lt;dc:.*?&lt;/dc:revisiondatestamp&gt;", "", text, flags=re.S)
        nav = re.compile(
            r"^\s*(Informazioni sulla fonte|←|→|\.\.|IncludiIntestazione|Questo testo è|100%"
            r"|//it\.wikisource|\d{14}\s*$|&#x25c4;|&#x25ba;"
            r"|Niccolò Machiavelli - Discorsi|Discorsi sopra la prima Deca"
            r"|Libro (primo|secondo|terzo)(\s*-\s*Capitolo \d+)?\s*$"
            r"|Capitolo \d+\s*$|Dedica\s*$)")
        lines = [l for l in text.split("\n") if not nav.match(l)]
        text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
        import html
        text = html.unescape(text)
        heading = ""
        m = re.match(r"^(CAPITOLO\s+\S+|Dedica|Proemio)?\s*(.*?)\n", text + "\n", re.I)
        if m:
            heading = (m.group(2) or "").strip()
        out.append({
            "passage_id": f"disc:it:{book}:{chap}",
            "work": "Discorsi sopra la prima Deca di Tito Livio",
            "lang": "it",
            "edition": "it.wikisource (from Opere, ed. 19th c.; see SOURCES.md)",
            "book": book, "chapter": chap,
            "heading": heading[:300],
            "text": text,
            "source_file": f"corpus/raw/discorsi_it/{fn.name}",
        })
    out.sort(key=lambda r: (r["book"], r["chapter"]))
    write_jsonl(SEG / "discorsi_it.jsonl", out)


def segment_discorsi_en():
    src = RAW / "discourses_thomson_pg10827.txt"
    t = src.read_text(encoding="utf-8")
    # body starts at the second "BOOK I." occurrence (first is ToC)
    body_start = [m.start() for m in re.finditer(r"^BOOK I\.", t, re.M)][-1]
    end = t.find("*** END OF THE PROJECT")
    body = t[body_start:end]
    book_spans = []
    for m in re.finditer(r"^BOOK (I{1,3})\.", body, re.M):
        book_spans.append((ROMAN[m.group(1)], m.start()))
    book_spans.append((None, len(body)))
    out = []
    for (bk, s), (_, e) in zip(book_spans, book_spans[1:]):
        bt = body[s:e]
        ch_marks = [(ROMAN[m.group(1).rstrip('.')], m.start(), m.end())
                    for m in re.finditer(r"^CHAPTER ([IVXLC]+)\.?(?=[—\-\s])", bt, re.M | re.I)]
        # preface = text between book header and first chapter
        pre = bt[:ch_marks[0][1]] if ch_marks else bt
        pre_text = re.sub(r"^BOOK I{1,3}\.\s*", "", pre).strip()
        if pre_text:
            out.append(_disc_en_rec(bk, 0, "Preface", pre_text))
        ch_marks.append((None, len(bt), len(bt)))
        for (cn, cs, _), (_, ce, _) in zip(ch_marks[:-1], ch_marks[1:]):
            ct = bt[cs:ce].strip()
            hm = re.match(r"CHAPTER [IVXLC]+\.?[—-]?\s*_?(.*?)_?\n\n", ct, re.S | re.I)
            heading = re.sub(r"\s+", " ", hm.group(1)).strip("_ ") if hm else ""
            body_text = ct[hm.end():].strip() if hm else ct
            out.append(_disc_en_rec(bk, cn, heading, body_text))
    out.sort(key=lambda r: (r["book"], r["chapter"]))
    write_jsonl(SEG / "discorsi_en.jsonl", out)


def _disc_en_rec(book, chap, heading, text):
    return {
        "passage_id": f"disc:en:{book}:{chap}",
        "work": "Discourses on the First Decade of Titus Livius",
        "lang": "en",
        "edition": "trans. Ninian Hill Thomson, 1883 (Project Gutenberg #10827)",
        "book": book, "chapter": chap,
        "heading": heading[:300],
        "text": text,
        "source_file": "corpus/raw/discourses_thomson_pg10827.txt",
    }


def segment_livy(xml_name, lang, edition, out_name, max_book=10):
    tree = ET.parse(RAW / xml_name)
    out = []
    for bdiv in tree.iter(f"{TEI}div"):
        if bdiv.get("subtype") != "book":
            continue
        try:
            book = int(bdiv.get("n"))
        except (TypeError, ValueError):
            continue
        if book > max_book:
            continue
        for cdiv in bdiv.iter(f"{TEI}div"):
            if cdiv.get("subtype") != "chapter":
                continue
            try:
                chap = int(cdiv.get("n"))
            except (TypeError, ValueError):
                continue
            sections = {}
            for sdiv in cdiv.iter(f"{TEI}div"):
                if sdiv.get("subtype") == "section":
                    sections[sdiv.get("n")] = _clean("".join(sdiv.itertext()))
            text = " ".join(sections.values()) if sections else _clean("".join(cdiv.itertext()))
            out.append({
                "passage_id": f"livy:{lang}:{book}:{chap}",
                "work": "Ab Urbe Condita",
                "lang": lang,
                "edition": edition,
                "book": book, "chapter": chap,
                "heading": "",
                "text": text,
                "sections": sections,
                "source_file": f"corpus/raw/{xml_name}",
            })
    out.sort(key=lambda r: (r["book"], r["chapter"]))
    write_jsonl(SEG / out_name, out)


def _clean(s):
    return re.sub(r"\s+", " ", s).strip()


if __name__ == "__main__":
    segment_discorsi_it()
    segment_discorsi_en()
    segment_livy("livy_lat2.xml", "la",
                 "Perseus phi0914.phi001.perseus-lat2 (W. Weissenborn, H.J. Müller)",
                 "livy_la.jsonl")
    segment_livy("livy_eng2.xml", "en",
                 "Perseus phi0914.phi001.perseus-eng2 (D. Spillan et al., 1857)",
                 "livy_en.jsonl")
