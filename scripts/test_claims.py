#!/usr/bin/env python3
"""Test Machiavellian propositions against the full Livy I-X event series.

Inputs: extractions/livy_events.jsonl (full-corpus coding, independent of
Machiavelli's citations), extractions/chapter_map.jsonl.

Tests (all descriptive, with explicit caveats — Livy is itself a literary
reconstruction; 'resolution_channel' coding has analyst judgment baked in):

T1  roba-vs-onori (claim:d1c37-roba-vs-onori): do property-domain conflicts
    (land, debt, food) end in extraordinary channels more often than
    honors-office conflicts?
T2  accusation-channel (claim:d1c7-accusation-channels): among events with a
    prominent-trial available vs absent, how often does violence occur?
    Proxy: share of extraordinary resolutions among prominent-trial events vs
    political-killing events without trial.
T3  selection bias: which Livy events does Machiavelli anchor chapters to
    (via chapter_map name/quote candidates), and how do cited events differ
    from uncited ones by type and channel?

Output: reports/claim_tests.json + printed summary.
"""
import collections
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

PROPERTY = {"land", "debt", "food"}
HONORS = {"honors-office"}


def load(p):
    return [json.loads(l) for l in p.open(encoding="utf-8")]


def pct(a, b):
    return round(100 * a / b, 1) if b else None


def main():
    ev = load(ROOT / "extractions/livy_events.jsonl")
    cmap = load(ROOT / "extractions/chapter_map.jsonl")

    # T1 — conflict-type events only (exclude routine colony-founded/dictator
    # unless conflictual trigger)
    conflict_types = {"secession", "riot-tumult", "military-mutiny", "grain-dispute",
                      "agrarian-agitation", "debt-crisis", "prominent-trial",
                      "veto-deadlock", "levy-obstruction", "electoral-conflict",
                      "political-killing", "conspiracy", "regime-change"}
    conf = [e for e in ev if e["event_type"] in conflict_types]
    def channel_dist(events):
        c = collections.Counter(e["resolution_channel"] for e in events)
        n = sum(c.values())
        extra = c["extraordinary"] + c["mixed"] * 0.5
        return {"n": n, "dist": dict(c), "extraordinary_share": pct(extra, n)}

    # Roman-only sensitivity: non-Roman polities (Syracuse, Macedon, Capua,
    # Carthage, Greek cities...) were coded with the polity noted in
    # groups/actors/notes; this text filter is the documented, reproducible
    # basis for the Roman-only figures quoted in README/reports. Taxonomy v2
    # plans a structured polity field to replace it.
    import re as _re
    NONROMAN = _re.compile(
        r"Syracus|Macedon|Carthag|Capuan?\b|Sparta|Nabis|Aetol|Boeot|Chalcis"
        r"|Perseus|Demetrius|Philip|Hieronymus|Hiero|Messene|Locri", _re.I)
    def is_roman(e):
        blob = " ".join(e.get("groups", []) + e.get("actors", [])) + " " + e.get("notes", "")
        if not NONROMAN.search(blob):
            return True
        return bool(_re.search(r"senate of Rome|Roman senate|at Rome", e.get("notes", ""), _re.I))
    conf_rom = [e for e in conf if is_roman(e)]

    t1 = {
        "property_domain": channel_dist([e for e in conf if e["trigger_domain"] in PROPERTY]),
        "honors_office_domain": channel_dist([e for e in conf if e["trigger_domain"] in HONORS]),
        "legal_rights_domain": channel_dist([e for e in conf if e["trigger_domain"] == "legal-rights"]),
        "roman_only": {
            "property_domain": channel_dist([e for e in conf_rom if e["trigger_domain"] in PROPERTY]),
            "honors_office_domain": channel_dist([e for e in conf_rom if e["trigger_domain"] in HONORS]),
            "legal_rights_domain": channel_dist([e for e in conf_rom if e["trigger_domain"] == "legal-rights"]),
            "filter_basis": "text filter over groups/actors/notes (see code); interim until taxonomy v2 adds a polity field",
        },
        "machiavelli_prediction": "property conflicts resolve extraordinarily more often than honors conflicts (claim:d1c37-roba-vs-onori)",
        "caveats": ("Descriptive shares over coded events in the surviving Livian corpus, "
                    "including books outside Machiavelli's documented access (41-45); "
                    "sensitive to coding and denominator choices; tests Livy's "
                    "representation, not Roman reality."),
    }

    # T2 — trials vs killings
    trials = [e for e in ev if e["event_type"] == "prominent-trial"]
    killings = [e for e in ev if e["event_type"] == "political-killing"]
    t2 = {
        "prominent_trials": channel_dist(trials),
        "political_killings_n": len(killings),
        "trials_ending_ordinary_pct": pct(
            sum(1 for e in trials if e["resolution_channel"] == "ordinary"), len(trials)),
        "note": ("Machiavelli's claim predicts trials (ordinary channel) substitute for "
                 "violence. A real test needs counterfactual periods without tribunician "
                 "prosecution; this is a descriptive proxy only."),
    }

    # T3 — which Livy chapters does Machiavelli anchor? (quote + name candidates)
    cited = set()
    for c in cmap:
        for q in c["latin_quotes"]:
            for p in q["livy_candidates"]:
                cited.add(p.replace(":la:", ":en:"))
        for a in c["name_anchors"]:
            for p in a["livy_chapters_topk"][:3]:
                cited.add(p.replace(":la:", ":en:"))
    ev_cited = [e for e in ev if e["passage_id"] in cited]
    ev_uncited = [e for e in ev if e["passage_id"] not in cited]
    def type_dist(events):
        c = collections.Counter(e["event_type"] for e in events)
        return dict(c.most_common())
    t3 = {
        "livy_chapters_with_candidate_citation": len(cited),
        "events_in_cited_chapters": len(ev_cited),
        "events_in_uncited_chapters": len(ev_uncited),
        "type_dist_cited": type_dist(ev_cited),
        "type_dist_uncited": type_dist(ev_uncited),
        "extraordinary_share_cited": channel_dist(ev_cited)["extraordinary_share"],
        "extraordinary_share_uncited": channel_dist(ev_uncited)["extraordinary_share"],
        "caveat": ("'cited' = chapter appears as a retrieval candidate in chapter_map "
                   "(name/quote heuristics), NOT verified citation. Direction of any "
                   "difference is still informative about selection."),
    }

    out = {"T1_roba_vs_onori": t1, "T2_accusation_channel": t2, "T3_selection_bias": t3,
           "n_events_total": len(ev),
           "_methods_caveat": ("Event coding is LLM-extracted from Spillan's 1857 "
                               "translation and quote-validated; channel/trigger codings "
                               "involve judgment; Livy's narrative is itself a late, "
                               "moralized reconstruction. These are tests against "
                               "LIVY'S REPRESENTATION, not against Roman reality.")}
    (ROOT / "reports/claim_tests.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"events: {len(ev)}")
    print("\nT1 roba-vs-onori:")
    for k in ["property_domain", "honors_office_domain", "legal_rights_domain"]:
        print(f"  {k:<22} n={t1[k]['n']:>3}  extraordinary≈{t1[k]['extraordinary_share']}%")
    print(f"\nT2 trials: n={t2['prominent_trials']['n']}, ordinary={t2['trials_ending_ordinary_pct']}%, killings n={t2['political_killings_n']}")
    print(f"\nT3 cited chapters={t3['livy_chapters_with_candidate_citation']}, "
          f"events cited/uncited = {len(ev_cited)}/{len(ev_uncited)}, "
          f"extraordinary share cited={t3['extraordinary_share_cited']}% vs uncited={t3['extraordinary_share_uncited']}%")
    print("\nwritten: reports/claim_tests.json")


if __name__ == "__main__":
    main()
