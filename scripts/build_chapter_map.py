#!/usr/bin/env python3
"""Map each Discorsi chapter to candidate Livy I-X anchor passages.

Signals, strongest first:
  1. latin-quote: word 5-grams of the Italian chapter text that occur verbatim
     in a Livy Latin chapter (Machiavelli embeds Latin quotations).
  2. tito-livio: explicit mentions of 'Tito Livio' / 'Livio' in the chapter.
  3. name-overlap: distinctive Roman proper names shared between the chapter
     (Italianized, via a curated name map) and Livy chapters.

Output: extractions/chapter_map.jsonl, one record per Discorsi chapter:
  {chapter_id, explicit_livy_mentions, latin_quotes:[{ngram, livy_candidates}],
   name_anchors:[{name, latin, livy_chapters_topk}], candidate_books, confidence}

Confidence: 'quote' (latin quote matched) > 'named' (explicit mention + name
anchors) > 'name-only' > 'none'. This is a RETRIEVAL aid for Phase-II scaling,
not a verified alignment; human/LLM verification is required downstream.
"""
import collections
import json
import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEG = ROOT / "corpus" / "segments"
OUT = ROOT / "extractions" / "chapter_map.jsonl"

NGRAM = 5

# Italianized → Latin stem map for distinctive persons/places frequent in the
# Discorsi. Stems are matched case-insensitively against Livy Latin text.
NAME_MAP = {
    "Coriolano": "Coriolan", "Bruto": "Brut", "Tarquin": "Tarquin",
    "Romolo": "Romul", "Numa": "Numa", "Tullo": "Tull", "Anco": "Anc",
    "Camillo": "Camill", "Manlio": "Manli", "Valerio": "Valeri",
    "Virginio": "Vergini", "Virginia": "Vergini", "Appio": "Appi",
    "Claudio": "Claudi", "Spurio Melio": "Maeli", "Melio": "Maeli",
    "Spurio Cassio": "Cassi", "Maelio": "Maeli", "Cincinnato": "Cincinnat",
    "Fabio": "Fabi", "Papirio": "Papiri", "Decio": "Deci",
    "Torquato": "Torquat", "Corvino": "Corvin", "Scevola": "Scaevol",
    "Orazio": "Horati", "Curiazi": "Curiati", "Porsenna": "Porsenn",
    "Sanniti": "Samni", "Volsci": "Volsc", "Equi": "Aequ",
    "Veienti": "Veien", "Veio": "Vei", "Fidene": "Fiden",
    "Anzio": "Antiu", "Capova": "Capu", "Ardea": "Ardea",
    "Decemviri": "decemvir", "decemviri": "decemvir", "Tribuni": "tribun",
    "Dittatore": "dictator", "Ciminia": "Cimini", "Sentino": "Sentin",
    "Soderini": None, "Savonarola": None, "Medici": None,  # non-Roman: excluded
}


def norm_word(w):
    w = unicodedata.normalize("NFD", w)
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z]", "", w.lower())


def words(text):
    return [norm_word(w) for w in text.split() if norm_word(w)]


def load(path):
    return [json.loads(l) for l in path.open(encoding="utf-8")]


def main():
    disc = [r for r in load(SEG / "discorsi_it.jsonl") if r["chapter"] > 0]
    livy = load(SEG / "livy_la.jsonl")

    # --- 5-gram index of Livy Latin ---
    index = collections.defaultdict(set)
    for r in livy:
        ws = words(r["text"])
        for i in range(len(ws) - NGRAM + 1):
            index[tuple(ws[i:i + NGRAM])].add(r["passage_id"])
    print(f"livy 5-gram index: {len(index)} distinct grams")

    # --- per-name Livy chapter lists (top-k by hits) ---
    name_hits = {}
    for it_name, stem in NAME_MAP.items():
        if stem is None:
            continue
        hits = collections.Counter()
        pat = re.compile(re.escape(stem), re.I)
        for r in livy:
            n = len(pat.findall(r["text"]))
            if n:
                hits[r["passage_id"]] = n
        name_hits[it_name] = hits

    out = []
    conf_counts = collections.Counter()
    for r in disc:
        text = r["text"]
        cid = r["passage_id"]
        mentions = len(re.findall(r"Tito Livio|T\. Livio|\bLivio\b", text))

        # latin quote scan
        ws = words(text)
        matched = {}
        i = 0
        while i < len(ws) - NGRAM + 1:
            g = tuple(ws[i:i + NGRAM])
            if g in index:
                # extend the match greedily
                j = i + NGRAM
                cands = set(index[g])
                while j < len(ws):
                    g2 = tuple(ws[j - NGRAM + 1:j + 1])
                    c2 = index.get(g2)
                    if not c2 or not (cands & c2):
                        break
                    cands &= c2
                    j += 1
                matched[" ".join(ws[i:j])] = sorted(cands)[:6]
                i = j
            else:
                i += 1
        # drop trivial matches (formulaic latin shared by everything)
        quotes = [{"ngram": k, "livy_candidates": v}
                  for k, v in matched.items() if len(v) <= 6 and v]

        # name anchors
        anchors = []
        for it_name, hits in name_hits.items():
            if re.search(r"\b" + re.escape(it_name), text):
                top = hits.most_common(5)
                if top:
                    anchors.append({"name": it_name,
                                    "livy_chapters_topk": [p for p, _ in top]})

        books = collections.Counter()
        for q in quotes:
            for p in q["livy_candidates"]:
                books[int(p.split(":")[2])] += 3
        for a in anchors:
            for p in a["livy_chapters_topk"]:
                books[int(p.split(":")[2])] += 1

        if quotes:
            conf = "quote"
        elif mentions and anchors:
            conf = "named"
        elif anchors:
            conf = "name-only"
        else:
            conf = "none"
        conf_counts[conf] += 1

        out.append({
            "chapter_id": cid,
            "heading": r["heading"][:160],
            "explicit_livy_mentions": mentions,
            "latin_quotes": quotes,
            "name_anchors": anchors,
            "candidate_books": [b for b, _ in books.most_common(3)],
            "confidence": conf,
        })

    with OUT.open("w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"chapter_map.jsonl: {len(out)} chapters")
    print("confidence distribution:", dict(conf_counts))
    nq = sum(len(r["latin_quotes"]) for r in out)
    print(f"latin quote matches: {nq} across "
          f"{sum(1 for r in out if r['latin_quotes'])} chapters")


if __name__ == "__main__":
    main()
