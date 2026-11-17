#!/usr/bin/env python3
"""Build data/discorsi.db (SQLite) from segments + extractions."""
import json
import pathlib
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "discorsi.db"


def rows(path):
    if not path.exists():
        return
    for line in path.open(encoding="utf-8"):
        yield json.loads(line)


def main():
    DB.parent.mkdir(exist_ok=True)
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript("""
    PRAGMA foreign_keys = ON;
    CREATE TABLE passages (
      passage_id TEXT PRIMARY KEY, work TEXT, lang TEXT, edition TEXT,
      book INTEGER, chapter INTEGER, heading TEXT, text TEXT, source_file TEXT);
    CREATE TABLE observations (
      observation_id TEXT PRIMARY KEY,
      passage_ref TEXT REFERENCES passages(passage_id),
      source_passage TEXT, source_language TEXT, historical_event TEXT,
      estimated_date TEXT, date_uncertainty TEXT, location TEXT,
      claimed_mechanism TEXT, evidence_class TEXT, confidence TEXT,
      record_json TEXT);
    CREATE TABLE claims (
      claim_id TEXT PRIMARY KEY, author TEXT,
      source_ref TEXT REFERENCES passages(passage_id),
      statement TEXT, claim_type TEXT, polarity TEXT, scope_claimed TEXT,
      record_json TEXT);
    CREATE TABLE claim_variables (
      claim_id TEXT REFERENCES claims(claim_id),
      variable_id TEXT, role TEXT);
    CREATE TABLE alignments (
      alignment_id TEXT PRIMARY KEY, case_key TEXT, dimension TEXT,
      livy_ref TEXT, discorsi_ref TEXT, livy_content TEXT,
      machiavelli_content TEXT, transformation TEXT, addition_subtype TEXT,
      notes TEXT);
    CREATE TABLE datasets (
      dataset_id TEXT PRIMARY KEY, name TEXT, evidentiary_level TEXT,
      producing_institution TEXT, institution_evidence TEXT, period TEXT,
      survival_status TEXT, notes TEXT, record_json TEXT);
    CREATE TABLE dataset_claims (
      dataset_id TEXT REFERENCES datasets(dataset_id),
      claim_id TEXT REFERENCES claims(claim_id));
    CREATE TABLE ontology (
      variable_id TEXT PRIMARY KEY, label TEXT, domain TEXT, role TEXT,
      discovered INTEGER, notes TEXT);
    CREATE TABLE livy_events (
      event_id TEXT PRIMARY KEY,
      passage_id TEXT REFERENCES passages(passage_id),
      book INTEGER, event_type TEXT, trigger_domain TEXT,
      resolution_channel TEXT, quote TEXT, notes TEXT, confidence TEXT,
      record_json TEXT);
    """)
    seg_dir = ROOT / "corpus" / "segments"
    for f in seg_dir.glob("*.jsonl"):
        for r in rows(f):
            con.execute("INSERT INTO passages VALUES (?,?,?,?,?,?,?,?,?)",
                        (r["passage_id"], r["work"], r["lang"], r["edition"],
                         r["book"], r["chapter"], r.get("heading", ""),
                         r["text"], r["source_file"]))
    ext = ROOT / "extractions"
    for r in rows(ext / "observations.jsonl"):
        con.execute("INSERT INTO observations VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (r["observation_id"], r["discorsi_reference"], r["source_passage"],
                     r["source_language"], r["historical_event"], r.get("estimated_date"),
                     r.get("date_uncertainty", ""), r.get("location", ""),
                     r.get("claimed_mechanism", ""), r["evidence_class"],
                     r["confidence"], json.dumps(r, ensure_ascii=False)))
    for r in rows(ext / "claims.jsonl"):
        con.execute("INSERT INTO claims VALUES (?,?,?,?,?,?,?,?)",
                    (r["claim_id"], r["author"], r["source_ref"], r["statement"],
                     r["claim_type"], r.get("polarity", ""), r.get("scope_claimed", ""),
                     json.dumps(r, ensure_ascii=False)))
        for role, key in [("cause", "cause_variables"), ("effect", "effect_variables"),
                          ("moderator", "moderator_variables")]:
            for v in r.get(key, []):
                con.execute("INSERT INTO claim_variables VALUES (?,?,?)",
                            (r["claim_id"], v, role))
    for r in rows(ext / "alignments.jsonl"):
        con.execute("INSERT INTO alignments VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (r["alignment_id"], r["case"], r["dimension"], r.get("livy_ref"),
                     r.get("discorsi_ref"), r["livy_content"], r["machiavelli_content"],
                     r["transformation"], r.get("addition_subtype"), r.get("notes", "")))
    for r in rows(ext / "datasets.jsonl"):
        con.execute("INSERT INTO datasets VALUES (?,?,?,?,?,?,?,?,?)",
                    (r["dataset_id"], r["name"], r["evidentiary_level"],
                     r["producing_institution"], r["institution_evidence"],
                     r.get("period", ""), r.get("survival_status", ""),
                     r.get("notes", ""), json.dumps(r, ensure_ascii=False)))
        for c in r["tests_claims"]:
            con.execute("INSERT INTO dataset_claims VALUES (?,?)", (r["dataset_id"], c))
    for r in rows(ext / "livy_events.jsonl"):
        con.execute("INSERT INTO livy_events VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (r["event_id"], r["passage_id"], r["book"], r["event_type"],
                     r["trigger_domain"], r["resolution_channel"], r["quote"],
                     r.get("notes", ""), r["confidence"],
                     json.dumps(r, ensure_ascii=False)))
    onto = json.loads((ROOT / "schema" / "ontology.json").read_text(encoding="utf-8"))
    for v in onto["variables"]:
        con.execute("INSERT INTO ontology VALUES (?,?,?,?,?,?)",
                    (v["id"], v["label"], v["domain"], v["role"],
                     1 if v.get("discovered") else 0, v.get("notes", "")))
    con.commit()
    n = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
         for t in ["passages", "observations", "claims", "claim_variables",
                   "alignments", "datasets", "dataset_claims", "ontology"]}
    print("built", DB.name, n)
    con.close()


if __name__ == "__main__":
    main()
