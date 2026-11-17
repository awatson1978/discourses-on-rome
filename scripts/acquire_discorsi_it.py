#!/usr/bin/env python3
"""Download the Italian Discorsi sopra la prima Deca di Tito Livio from it.wikisource.

Source: https://it.wikisource.org/wiki/Discorsi_sopra_la_prima_Deca_di_Tito_Livio
Edition: Wikisource transcription (based on Opere complete, Firenze 1843 per page
metadata; see SOURCES.md). License: public domain text, CC BY-SA for the
transcription layer.

Output: corpus/raw/discorsi_it/ one JSON file per page, with wikitext and
plain-text rendering, plus a manifest.
"""
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

API = "https://it.wikisource.org/w/api.php"
BASE = "Discorsi sopra la prima Deca di Tito Livio"
BOOKS = {1: ("Libro primo", 60), 2: ("Libro secondo", 33), 3: ("Libro terzo", 49)}
OUT = pathlib.Path(__file__).resolve().parent.parent / "corpus" / "raw" / "discorsi_it"
UA = "discourses-on-rome research pipeline (contact: awatson1978@gmail.com)"


def api_get(params: dict) -> dict:
    params = dict(params, format="json")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch_page(title: str) -> dict:
    d = api_get({"action": "parse", "page": title, "prop": "wikitext|text|revid"})
    if "error" in d:
        return {"title": title, "error": d["error"].get("code", "unknown")}
    p = d["parse"]
    html = p["text"]["*"]
    # strip html to plain text
    text = re.sub(r"<style.*?</style>|<script.*?</script>", "", html, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"</p>|</div>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return {
        "title": title,
        "revid": p.get("revid"),
        "wikitext": p["wikitext"]["*"],
        "plain_text": text,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pages = [("dedica", f"{BASE}/Dedica")]
    for n, (name, nch) in BOOKS.items():
        # Machiavelli wrote proemi for Books I and II only; Wikisource holds
        # them at .../Introduzione. The bare book pages are just indexes.
        if n in (1, 2):
            pages.append((f"{n}.proemio", f"{BASE}/{name}/Introduzione"))
        for c in range(1, nch + 1):
            pages.append((f"{n}.{c}", f"{BASE}/{name}/Capitolo {c}"))
    manifest = []
    for key, title in pages:
        fn = OUT / (key.replace(".", "_") + ".json")
        if fn.exists():
            manifest.append({"key": key, "title": title, "file": fn.name, "cached": True})
            continue
        rec = fetch_page(title)
        rec["key"] = key
        rec["retrieved"] = "2026-11-16"
        fn.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        ok = "error" not in rec
        manifest.append({"key": key, "title": title, "file": fn.name, "ok": ok})
        print(("OK  " if ok else "ERR ") + key, flush=True)
        time.sleep(0.4)
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    errs = [m for m in manifest if m.get("ok") is False]
    print(f"done: {len(manifest)} pages, {len(errs)} errors")
    if errs:
        print("errors:", [m["key"] for m in errs])
        sys.exit(1)


if __name__ == "__main__":
    main()
