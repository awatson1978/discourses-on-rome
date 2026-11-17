#!/usr/bin/env python3
"""Build the lost-books reconstruction scaffold.

One record per lost book of Ab Urbe Condita (11-20, 46-142; the periochae of
136-137 are themselves lost and marked so). The spine of each record is its
Periocha; witness slots point at the derivative tradition; fragments and
events start EMPTY — this scaffold never fabricates content.

Outputs:
  lost_books/skeleton.jsonl       one structured record per lost book
  lost_books/books/book_NNN.md    contributor-facing placeholder per book
Run after scripts/acquire_witnesses.py.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
LB = ROOT / "lost_books"

ERA_BLOCKS = [
    (11, 20, "292-219 BCE", "Third Samnite aftermath, Pyrrhic War, First Punic War, interwar years"),
    (46, 70, "167-91 BCE", "post-Pydna Mediterranean hegemony, Carthage and Corinth destroyed, the Gracchi, Jugurtha, Cimbri, the road to the Social War"),
    (71, 90, "91-78 BCE", "Social War, civil wars of Marius and Sulla, Sullan dictatorship and death"),
    (91, 108, "78-49 BCE", "Sertorius, Lucullus and Mithridates, Pompey's commands, Catiline, the triumvirate, Gaul"),
    (109, 116, "49-44 BCE", "civil war of Caesar and Pompey, Caesar's dictatorship, the Ides"),
    (117, 133, "44-30 BCE", "post-Ides struggle, triumviral proscriptions, Philippi, Actium, Alexandria"),
    (134, 142, "29-9 BCE", "Augustan settlement, Spanish and German campaigns, death of Drusus"),
]

# Approximate era-level crosswalk to the narrative witnesses. APPROXIMATE —
# verification per book is exactly the contribution this scaffold invites.
PLUTARCH = {
    (11, 20): ["Pyrrhus", "Fabius Maximus (ancestor material)"],
    (46, 70): ["Aemilius Paullus (end)", "Cato Major", "Tiberius Gracchus", "Gaius Gracchus", "Marius (early)"],
    (71, 90): ["Marius", "Sulla", "Sertorius (start)", "Lucullus (start)"],
    (91, 108): ["Sertorius", "Lucullus", "Pompey", "Crassus", "Caesar", "Cicero", "Cato Minor"],
    (109, 116): ["Caesar", "Pompey (end)", "Cato Minor", "Cicero", "Brutus", "Antony"],
    (117, 133): ["Cicero (end)", "Brutus", "Antony"],
    (134, 142): [],
}
DIO = {
    (11, 20): "Cassius Dio frr. (epitomes of Zonaras, books 8-9 of Zonaras)",
    (46, 70): "Cassius Dio frr. books ~21-27 (via excerpts/Zonaras)",
    (71, 90): "Cassius Dio frr. books ~28-33",
    (91, 108): "Cassius Dio books 36-41 (fully extant from 69 BCE)",
    (109, 116): "Cassius Dio books 41-44",
    (117, 133): "Cassius Dio books 45-51",
    (134, 142): "Cassius Dio books 52-55",
}

LOST = list(range(11, 21)) + list(range(46, 143))


def era_of(book):
    for lo, hi, dates, desc in ERA_BLOCKS:
        if lo <= book <= hi:
            return (lo, hi), dates, desc
    return None, None, None


def load_periochae():
    per = {}
    # Perseus periochae (46-142, minus 136-137)
    p = ROOT / "corpus/segments/livy_periochae_la.jsonl"
    if p.exists():
        for l in p.open(encoding="utf-8"):
            r = json.loads(l)
            per[r["book"]] = {"text": r["text"], "source": r["passage_id"],
                              "edition": "Perseus phi0914.phi001.perseus-lat2"}
    # Latin Library periochae (11-20)
    w = ROOT / "corpus/segments/witnesses_la.jsonl"
    if w.exists():
        for l in w.open(encoding="utf-8"):
            r = json.loads(l)
            m = re.match(r"wit:periocha:(\d+)", r["passage_id"])
            if m:
                n = int(m.group(1))
                text = re.sub(r"^.*?PERIOCHA\s*", "", r["text"], flags=re.S)
                per[n] = {"text": text.strip(), "source": r["passage_id"],
                          "edition": "The Latin Library"}
    return per


def main():
    (LB / "books").mkdir(parents=True, exist_ok=True)
    per = load_periochae()
    records = []
    for book in LOST:
        blk, dates, desc = era_of(book)
        pe = per.get(book)
        periocha = ({"status": "present", **pe} if pe else
                    {"status": "lost", "text": None, "source": None,
                     "note": "The periochae of books 136-137 are themselves lost in the tradition."})
        rec = {
            "book": book,
            "status": "scaffold",
            "era_block": dates,
            "era_description": desc,
            "period_covered": None,
            "periocha": periocha,
            "witnesses": [
                {"source": "obsequens", "ref": "wit:obsequens",
                 "coverage": "prodigy entries by consular year, 190-11 BCE (Livy ~37-142)",
                 "mapped": False},
                {"source": "florus", "ref": "wit:florus:1 / wit:florus:2",
                 "coverage": "thematic epitome drawn largely from Livy", "mapped": False},
                {"source": "orosius", "ref": "wit:orosius:1-7",
                 "coverage": "Livian layers esp. books 3-6", "mapped": False},
                {"source": "eutropius", "ref": "wit:eutropius:1-10",
                 "coverage": "breviarium, Livian tradition", "mapped": False},
                {"source": "plutarch", "lives": PLUTARCH.get(blk, []),
                 "coverage": "APPROXIMATE era-level mapping; verify per book",
                 "mapped": False, "text_in_corpus": False},
                {"source": "cassius-dio", "ref": DIO.get(blk),
                 "coverage": "APPROXIMATE era-level mapping; verify per book",
                 "mapped": False, "text_in_corpus": False},
            ],
            "fragments": [],
            "events": [],
            "todo": [
                "map Obsequens prodigy entries to this book's consular years",
                "locate Florus/Orosius/Eutropius parallel passages",
                "verify Plutarch/Dio coverage; add section refs",
                "mine grammarians (Priscian, Nonius, Servius) for book-numbered citations",
                "extract event skeleton from periocha (evidence class: hypothetical)",
            ],
        }
        records.append(rec)

        md = LB / "books" / f"book_{book:03d}.md"
        pe_txt = (periocha["text"] if periocha["status"] == "present"
                  else "*The periocha of this book is itself lost.*")
        md.write_text(f"""---
book: {book}
status: scaffold
era: {dates}
periocha: {periocha['status']}
---

# Livy, Book {book} (lost)

**Era:** {dates} — {desc}

## Periocha ({periocha.get('edition', '—')})

> {pe_txt}

## Witnesses located
<!-- add: source, passage ref, what it preserves -->
- [ ] Obsequens entries for these years
- [ ] Florus parallels
- [ ] Orosius parallels
- [ ] Eutropius parallels
- [ ] Plutarch: {', '.join(PLUTARCH.get(blk, [])) or '—'}
- [ ] Cassius Dio: {DIO.get(blk)}

## Attested fragments (verbatim Livy only — never reconstructed prose)
<!-- cite: quoting author, locus, the quoted words, edition -->

## Event skeleton (evidence class: hypothetical; every row needs a witness ref)
| date | event | witnesses |
|---|---|---|

## Notes
""", encoding="utf-8")

    with (LB / "skeleton.jsonl").open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    n_per = sum(1 for r in records if r["periocha"]["status"] == "present")
    print(f"skeleton.jsonl: {len(records)} lost books | periochae present: {n_per} "
          f"| periochae lost: {len(records) - n_per} (books 136-137)")
    print(f"books/: {len(records)} placeholder files")


if __name__ == "__main__":
    main()
