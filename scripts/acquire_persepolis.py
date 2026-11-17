#!/usr/bin/env python3
"""Download Hallock's Persepolis Fortification Tablets (OIP 92) from CDLI.

Source: Cuneiform Digital Library Initiative, publication 155926 (OIP 92,
Hallock 1969), https://cdli.earth/publications/155926 — 2,087 artifacts, all
flagged is_public / is_atf_public. Per-artifact JSON includes the ATF
transliteration with Hallock-derived English translation lines (#tr.en).

Output: corpus/raw/persepolis/artifacts/{id}.json (one per tablet)
        corpus/raw/persepolis/oip92_publication.json (artifact index)
Polite: 0.25s between requests, resumable (skips existing files).
License note: CDLI data are released under CC BY (see cdli.earth terms);
attribution: CDLI + Hallock, OIP 92.
"""
import json
import pathlib
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "corpus" / "raw" / "persepolis"
ARTS = OUT / "artifacts"
UA = "discourses-on-rome research pipeline (contact: awatson1978@gmail.com)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    ARTS.mkdir(parents=True, exist_ok=True)
    pub_path = OUT / "oip92_publication.json"
    if not pub_path.exists():
        print("fetching publication index...", flush=True)
        pub = get("https://cdli.earth/publications/155926")
        pub_path.write_text(json.dumps(pub, ensure_ascii=False), encoding="utf-8")
    pub = json.loads(pub_path.read_text(encoding="utf-8"))
    artifacts = pub[0]["artifacts"]
    ids = [a["id"] for a in artifacts if a.get("is_public")]
    print(f"{len(ids)} public artifacts", flush=True)
    done = errs = 0
    for i, aid in enumerate(ids):
        fn = ARTS / f"{aid}.json"
        if fn.exists():
            done += 1
            continue
        try:
            d = get(f"https://cdli.earth/artifacts/{aid}")
            fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            done += 1
        except Exception as e:
            errs += 1
            print(f"ERR {aid}: {e}", flush=True)
            time.sleep(2.0)
        if (i + 1) % 100 == 0:
            print(f"{i+1}/{len(ids)} ({errs} errors)", flush=True)
        time.sleep(0.25)
    print(f"done: {done} fetched, {errs} errors", flush=True)
    sys.exit(1 if errs > len(ids) * 0.05 else 0)


if __name__ == "__main__":
    main()
