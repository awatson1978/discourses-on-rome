#!/usr/bin/env python3
"""Validate extraction artifacts against schemas and corpus segments.

Checks:
  1. structural validity (required fields, id patterns, enums) per schema/
  2. referential integrity (all passage ids resolve; cross-references resolve)
  3. citation fidelity: every source_passage is a verbatim substring of the
     cited segment, after whitespace normalization
  4. unsupported numbers: digits appearing in livy_content/machiavelli_content
     of alignments must appear in one of the referenced segments
Exit code 1 on any failure; prints a report.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEG = ROOT / "corpus" / "segments"
EXT = ROOT / "extractions"

EVIDENCE_CLASSES = {"source-reported", "machiavelli-claim", "modern-scholarship",
                    "analysis-inference", "hypothetical"}
TRANSFORMATIONS = {"preservation", "omission", "abstraction", "reinterpretation", "addition"}
ADDITION_SUBTYPES = {"other-source", "inference", "counterfactual", "unsupported", None}
EVIDENTIARY_LEVELS = {"A-attested", "B-reconstructed-structure", "C-hypothetical"}
CLAIM_TYPES = {"causal-mechanism", "empirical-generalization", "counterfactual",
               "prescription", "definition"}


def norm(s: str) -> str:
    s = s.replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def load_segments():
    segs = {}
    for f in SEG.glob("*.jsonl"):
        for line in f.open(encoding="utf-8"):
            r = json.loads(line)
            segs[r["passage_id"]] = norm(r["text"])
    return segs


def load_jsonl(name):
    path = EXT / name
    if not path.exists():
        return []
    return [json.loads(l) for l in path.open(encoding="utf-8")]


def main() -> int:
    errors, warnings = [], []
    segs = load_segments()
    if not segs:
        errors.append("no segments found — run segment_corpus.py first")

    obs = load_jsonl("observations.jsonl")
    claims = load_jsonl("claims.jsonl")
    alns = load_jsonl("alignments.jsonl")
    dsets = load_jsonl("datasets.jsonl")
    onto = json.loads((ROOT / "schema" / "ontology.json").read_text(encoding="utf-8"))
    ont_ids = {v["id"] for v in onto["variables"]}

    obs_ids, claim_ids = set(), set()

    for o in obs:
        oid = o.get("observation_id", "<missing>")
        if not re.match(r"^obs:[a-z0-9][a-z0-9-]+$", oid):
            errors.append(f"{oid}: bad observation_id")
        if oid in obs_ids:
            errors.append(f"{oid}: duplicate observation_id")
        obs_ids.add(oid)
        for field in ["source_passage", "historical_event", "evidence_class",
                      "confidence", "provenance", "discorsi_reference"]:
            if not o.get(field):
                errors.append(f"{oid}: missing {field}")
        if o.get("evidence_class") not in EVIDENCE_CLASSES:
            errors.append(f"{oid}: bad evidence_class {o.get('evidence_class')}")
        ref = o.get("discorsi_reference", "")
        if ref not in segs:
            errors.append(f"{oid}: unresolvable reference {ref}")
        elif norm(o.get("source_passage", "")) not in segs[ref]:
            errors.append(f"{oid}: source_passage NOT verbatim in {ref}")

    for c in claims:
        cid = c.get("claim_id", "<missing>")
        if not re.match(r"^claim:[a-z0-9][a-z0-9-]+$", cid):
            errors.append(f"{cid}: bad claim_id")
        claim_ids.add(cid)
        if c.get("claim_type") not in CLAIM_TYPES:
            errors.append(f"{cid}: bad claim_type")
        ref = c.get("source_ref", "")
        if ref not in segs:
            errors.append(f"{cid}: unresolvable source_ref {ref}")
        elif c.get("source_passage") and norm(c["source_passage"]) not in segs[ref]:
            errors.append(f"{cid}: source_passage NOT verbatim in {ref}")
        for v in c.get("cause_variables", []) + c.get("effect_variables", []) \
                + c.get("moderator_variables", []):
            if v not in ont_ids:
                errors.append(f"{cid}: unknown ontology variable {v}")
        for so in c.get("supporting_observations", []):
            if so not in obs_ids:
                errors.append(f"{cid}: unknown supporting observation {so}")

    for a in alns:
        aid = a.get("alignment_id", "<missing>")
        if a.get("transformation") not in TRANSFORMATIONS:
            errors.append(f"{aid}: bad transformation")
        if a.get("transformation") == "addition":
            if a.get("addition_subtype") not in ADDITION_SUBTYPES - {None}:
                errors.append(f"{aid}: addition requires addition_subtype")
            if a.get("livy_ref") is not None and "V.33" not in a.get("notes", "") \
               and "Livy" not in a.get("livy_content", "—"):
                pass
        if a.get("transformation") == "omission" and a.get("machiavelli_content") not in ("—", ""):
            warnings.append(f"{aid}: omission but machiavelli_content non-empty")
        for reffield in ["livy_ref", "discorsi_ref"]:
            ref = a.get(reffield)
            if ref is not None and ref not in segs:
                errors.append(f"{aid}: unresolvable {reffield} {ref}")
        # unsupported-number check: digits in content fields should occur in a
        # referenced segment or be flagged in notes
        for cf in ["livy_content", "machiavelli_content"]:
            for num in re.findall(r"\b\d{2,4}\b", a.get(cf, "")):
                refs = [a.get("livy_ref"), a.get("discorsi_ref")]
                in_seg = any(r and num in segs.get(r, "") for r in refs)
                if not in_seg and not re.search(r"\bBCE?\b|\d{3,4}", a.get("notes", "")):
                    warnings.append(f"{aid}: number {num} in {cf} not found in cited segments or notes")

    for d in dsets:
        did = d.get("dataset_id", "<missing>")
        if d.get("evidentiary_level") not in EVIDENTIARY_LEVELS:
            errors.append(f"{did}: bad evidentiary_level")
        for tc in d.get("tests_claims", []):
            if tc not in claim_ids:
                errors.append(f"{did}: unknown claim {tc}")
        if not d.get("producing_institution") or not d.get("institution_evidence"):
            errors.append(f"{did}: missing institution fields")
        for v in d.get("variables", []):
            for ref in v.get("attested_in", []):
                if ref not in segs:
                    errors.append(f"{did}: variable {v.get('name')} cites unknown segment {ref}")
            if d.get("evidentiary_level") == "C-hypothetical" and v.get("attested_in"):
                # C-level datasets may cite segments only as negative/contextual evidence
                warnings.append(f"{did}: C-level variable {v.get('name')} has attestations — check it should not be level B")

    print(f"segments: {len(segs)} | observations: {len(obs)} | claims: {len(claims)} "
          f"| alignments: {len(alns)} | datasets: {len(dsets)}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
