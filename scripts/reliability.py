#!/usr/bin/env python3
"""Inter-coder reliability for the Livy event series (books 2 and 6).

Coder A = original per-book coding (extractions/livy_events.jsonl).
Coder B = blind re-coding (extractions/reliability/book_N_coderB.jsonl).

Unit of analysis: the EVENT. Matching is at (passage_id chapter) granularity:
two events match if same chapter AND same event_type (greedy 1:1). On matched
pairs we report percent agreement and Cohen's kappa for trigger_domain and
resolution_channel. Event-detection agreement is reported as precision/recall/F1
of B against A (A as reference is a convention, not a claim that A is truth).

Output: reports/reliability.json + printed summary.
"""
import collections
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load(p):
    return [json.loads(l) for l in p.open(encoding="utf-8") if l.strip()]


def kappa(pairs):
    """Cohen's kappa over a list of (a, b) category pairs."""
    n = len(pairs)
    if n == 0:
        return None
    po = sum(1 for a, b in pairs if a == b) / n
    ca = collections.Counter(a for a, _ in pairs)
    cb = collections.Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    if pe == 1:
        return 1.0
    return round((po - pe) / (1 - pe), 3)


def match_events(a_events, b_events):
    """Greedy 1:1 matching on (chapter, event_type)."""
    b_pool = collections.defaultdict(list)
    for e in b_events:
        b_pool[(e["passage_id"], e["event_type"])].append(e)
    matched = []
    unmatched_a = []
    for e in a_events:
        key = (e["passage_id"], e["event_type"])
        if b_pool[key]:
            matched.append((e, b_pool[key].pop(0)))
        else:
            unmatched_a.append(e)
    unmatched_b = [e for lst in b_pool.values() for e in lst]
    return matched, unmatched_a, unmatched_b


def chapter_level(a_events, b_events):
    """Looser agreement: does each chapter contain >=1 coded event?"""
    ca = {e["passage_id"] for e in a_events}
    cb = {e["passage_id"] for e in b_events}
    return {
        "chapters_A": len(ca), "chapters_B": len(cb),
        "chapters_both": len(ca & cb),
        "jaccard": round(len(ca & cb) / len(ca | cb), 3) if ca | cb else None,
    }


def analyze(book):
    a = [e for e in load(ROOT / "extractions/livy_events.jsonl") if e["book"] == book]
    bp = ROOT / f"extractions/reliability/book_{book}_coderB.jsonl"
    if not bp.exists():
        return None
    b = load(bp)
    matched, ua, ub = match_events(a, b)
    nm = len(matched)
    prec = nm / (nm + len(ub)) if nm + len(ub) else None
    rec = nm / (nm + len(ua)) if nm + len(ua) else None
    f1 = round(2 * prec * rec / (prec + rec), 3) if prec and rec else None
    trig_pairs = [(x["trigger_domain"], y["trigger_domain"]) for x, y in matched]
    chan_pairs = [(x["resolution_channel"], y["resolution_channel"]) for x, y in matched]
    return {
        "book": book, "n_A": len(a), "n_B": len(b), "n_matched": nm,
        "event_detection": {"precision_B_vs_A": round(prec, 3), "recall_B_vs_A": round(rec, 3), "f1": f1},
        "chapter_level": chapter_level(a, b),
        "trigger_domain": {
            "pct_agreement": round(100 * sum(1 for p in trig_pairs if p[0] == p[1]) / nm, 1) if nm else None,
            "cohens_kappa": kappa(trig_pairs)},
        "resolution_channel": {
            "pct_agreement": round(100 * sum(1 for p in chan_pairs if p[0] == p[1]) / nm, 1) if nm else None,
            "cohens_kappa": kappa(chan_pairs)},
        "disagreement_examples": [
            {"chapter": x["passage_id"], "event_type": x["event_type"],
             "A": {"trigger": x["trigger_domain"], "channel": x["resolution_channel"]},
             "B": {"trigger": y["trigger_domain"], "channel": y["resolution_channel"]}}
            for x, y in matched
            if x["trigger_domain"] != y["trigger_domain"]
            or x["resolution_channel"] != y["resolution_channel"]][:10],
    }


def main():
    results = [r for r in (analyze(2), analyze(6)) if r]
    if not results:
        print("no coder-B files found yet")
        return
    out = {
        "_method": ("Unit = event; 1:1 greedy match on (chapter, event_type); "
                    "kappa on matched pairs only, so field-agreement stats are "
                    "conditional on detection agreement. A-as-reference is a "
                    "convention: neither coder is ground truth."),
        "books": results,
    }
    (ROOT / "reports/reliability.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    for r in results:
        print(f"Book {r['book']}: A={r['n_A']} B={r['n_B']} matched={r['n_matched']} "
              f"F1={r['event_detection']['f1']}")
        print(f"  trigger: {r['trigger_domain']['pct_agreement']}% κ={r['trigger_domain']['cohens_kappa']}"
              f" | channel: {r['resolution_channel']['pct_agreement']}% κ={r['resolution_channel']['cohens_kappa']}")
    print("written: reports/reliability.json")


if __name__ == "__main__":
    main()
