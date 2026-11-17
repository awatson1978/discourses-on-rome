"""Automated validation. Run: python3 -m pytest tests/ -q  (or python3 tests/test_validation.py)"""
import json
import pathlib
import re
import sqlite3
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate  # noqa: E402


def load(name):
    return [json.loads(l) for l in (ROOT / "extractions" / name).open(encoding="utf-8")]


class TestCorpus(unittest.TestCase):
    def test_discorsi_complete(self):
        recs = [json.loads(l) for l in
                (ROOT / "corpus/segments/discorsi_it.jsonl").open(encoding="utf-8")]
        chapters = {(r["book"], r["chapter"]) for r in recs}
        for b, n in [(1, 60), (2, 33), (3, 49)]:
            for c in range(1, n + 1):
                self.assertIn((b, c), chapters, f"missing Discorsi IT {b}.{c}")
        self.assertIn((0, 0), chapters)  # dedica
        self.assertIn((1, 0), chapters)  # proemio I
        self.assertIn((2, 0), chapters)  # proemio II

    def test_discorsi_en_complete(self):
        recs = [json.loads(l) for l in
                (ROOT / "corpus/segments/discorsi_en.jsonl").open(encoding="utf-8")]
        chapters = {(r["book"], r["chapter"]) for r in recs}
        for b, n in [(1, 60), (2, 33), (3, 49)]:
            for c in range(1, n + 1):
                self.assertIn((b, c), chapters, f"missing Discorsi EN {b}.{c}")

    def test_livy_first_decade(self):
        for fn in ["livy_la.jsonl", "livy_en.jsonl"]:
            recs = [json.loads(l) for l in
                    (ROOT / f"corpus/segments/{fn}").open(encoding="utf-8")]
            books = {r["book"] for r in recs}
            self.assertEqual(books, set(range(1, 11)), fn)
            self.assertGreater(len(recs), 500, fn)

    def test_no_empty_texts(self):
        for fn in ROOT.glob("corpus/segments/*.jsonl"):
            for l in fn.open(encoding="utf-8"):
                r = json.loads(l)
                self.assertGreater(len(r["text"]), 50,
                                   f"suspiciously short: {r['passage_id']}")


class TestExtractions(unittest.TestCase):
    def test_validator_passes(self):
        self.assertEqual(validate.main(), 0, "validate.py reported errors")

    def test_citation_fidelity_direct(self):
        segs = validate.load_segments()
        for o in load("observations.jsonl"):
            self.assertIn(validate.norm(o["source_passage"]),
                          segs[o["discorsi_reference"]],
                          f"{o['observation_id']}: quote not verbatim")

    def test_no_evidence_class_violations(self):
        # Livy-side extractions must be source-reported; Discorsi-side retellings
        # of history must be machiavelli-claim
        for o in load("observations.jsonl"):
            ref = o["discorsi_reference"]
            if ref.startswith("livy:"):
                self.assertEqual(o["evidence_class"], "source-reported", o["observation_id"])
            if ref.startswith("disc:"):
                self.assertEqual(o["evidence_class"], "machiavelli-claim", o["observation_id"])

    def test_addition_alignments_have_subtype_and_no_livy_claim(self):
        for a in load("alignments.jsonl"):
            if a["transformation"] == "addition":
                self.assertIn(a.get("addition_subtype"),
                              {"other-source", "inference", "counterfactual", "unsupported"},
                              a["alignment_id"])
            if a["transformation"] == "omission":
                self.assertEqual(a["machiavelli_content"], "—", a["alignment_id"])

    def test_hypothetical_datasets_have_no_fabricated_values(self):
        # level-C variables must not claim attestation as values
        for d in load("datasets.jsonl"):
            for v in d["variables"]:
                if d["evidentiary_level"] == "C-hypothetical":
                    # attestations allowed only as contextual/negative evidence,
                    # and the dataset notes must explain the C classification
                    if v.get("attested_in"):
                        self.assertTrue(d.get("institution_evidence"),
                                        d["dataset_id"])

    def test_claims_cite_known_ontology(self):
        onto = json.loads((ROOT / "schema/ontology.json").read_text(encoding="utf-8"))
        ids = {v["id"] for v in onto["variables"]}
        for c in load("claims.jsonl"):
            for v in (c["cause_variables"] + c["effect_variables"]
                      + c.get("moderator_variables", [])):
                self.assertIn(v, ids, c["claim_id"])


class TestLivyEvents(unittest.TestCase):
    """Full-corpus event series (scale-up phase). Skipped until merged file exists."""

    def setUp(self):
        self.path = ROOT / "extractions/livy_events.jsonl"
        if not self.path.exists():
            self.skipTest("livy_events.jsonl not yet built")

    def test_quotes_verbatim(self):
        segs = {}
        for l in (ROOT / "corpus/segments/livy_en.jsonl").open(encoding="utf-8"):
            r = json.loads(l)
            segs[r["passage_id"]] = re.sub(r"\s+", " ", r["text"]).strip().lower()
        for l in self.path.open(encoding="utf-8"):
            e = json.loads(l)
            q = re.sub(r"\s+", " ", e["quote"]).strip().lower()
            self.assertIn(q, segs[e["passage_id"]], e["event_id"])

    def test_all_books_covered(self):
        books = {json.loads(l)["book"] for l in self.path.open(encoding="utf-8")}
        self.assertEqual(books, set(range(1, 11)))

    def test_rejects_documented(self):
        # rejected records must be preserved, not silently dropped
        self.assertTrue((ROOT / "extractions/livy_events_rejected.jsonl").exists())


class TestChapterObservations(unittest.TestCase):
    """Full 142-chapter observation extraction. Skipped until merged file exists."""

    def setUp(self):
        self.path = ROOT / "extractions/chapter_observations.jsonl"
        if not self.path.exists():
            self.skipTest("chapter_observations.jsonl not yet built")
        self.recs = [json.loads(l) for l in self.path.open(encoding="utf-8")]

    def test_all_142_chapters(self):
        ids = {r["chapter_id"] for r in self.recs}
        for b, n in [(1, 60), (2, 33), (3, 49)]:
            for c in range(1, n + 1):
                self.assertIn(f"disc:it:{b}:{c}", ids)

    def test_quotes_verbatim(self):
        segs = {}
        for l in (ROOT / "corpus/segments/discorsi_it.jsonl").open(encoding="utf-8"):
            r = json.loads(l)
            segs[r["passage_id"]] = re.sub(r"\s+", " ", r["text"]).strip()
        def norm(s):
            return re.sub(r"\s+", " ", s).strip()
        for r in self.recs:
            text = segs[r["chapter_id"]]
            self.assertIn(norm(r["thesis_quote"]), text, r["chapter_id"])
            for p in r["propositions"]:
                self.assertIn(norm(p["quote"]), text, r["chapter_id"])
            for e in r["episodes"]:
                self.assertIn(norm(e["quote"]), text, r["chapter_id"])

    def test_livy_refs_resolve_in_decade(self):
        livy = {json.loads(l)["passage_id"] for l in
                (ROOT / "corpus/segments/livy_la.jsonl").open(encoding="utf-8")}
        for r in self.recs:
            for e in r["episodes"]:
                if e.get("livy_ref_candidate"):
                    self.assertIn(e["livy_ref_candidate"], livy, r["chapter_id"])


class TestPersepolis(unittest.TestCase):
    """PF transfer parsing. Skipped until parsed file exists."""

    def setUp(self):
        self.path = ROOT / "extractions/persepolis_transfers.jsonl"
        if not self.path.exists():
            self.skipTest("persepolis_transfers.jsonl not yet built")
        self.recs = [json.loads(l) for l in self.path.open(encoding="utf-8")]

    def test_no_invented_values(self):
        # every quantity/year must be recoverable from the stored translation
        for r in self.recs:
            if r["parse_confidence"] == "none":
                continue
            t = r["translation"].lower()
            for q in r["quantities"]:
                v = q["value"]
                sv = str(int(v)) if v == int(v) else str(v)
                self.assertIn(sv, t.replace(",", "."), r["designation"])
            if r["regnal_year"] is not None:
                self.assertIn(str(r["regnal_year"]), t, r["designation"])

    def test_translation_only_records_flagged(self):
        for r in self.recs:
            if not r["has_translation"]:
                self.assertEqual(r["parse_confidence"], "none", r["designation"])


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts/build_db.py")],
                       check=True, capture_output=True)
        cls.con = sqlite3.connect(ROOT / "data/discorsi.db")

    def test_referential_integrity(self):
        orphans = self.con.execute("""
            SELECT o.observation_id FROM observations o
            LEFT JOIN passages p ON o.passage_ref = p.passage_id
            WHERE p.passage_id IS NULL""").fetchall()
        self.assertEqual(orphans, [])
        orphans = self.con.execute("""
            SELECT dc.dataset_id FROM dataset_claims dc
            LEFT JOIN claims c ON dc.claim_id = c.claim_id
            WHERE c.claim_id IS NULL""").fetchall()
        self.assertEqual(orphans, [])

    def test_counts(self):
        n = self.con.execute("SELECT COUNT(*) FROM passages").fetchone()[0]
        self.assertGreater(n, 1300)


class TestGraph(unittest.TestCase):
    def test_graphml_wellformed(self):
        import xml.etree.ElementTree as ET
        subprocess.run([sys.executable, str(ROOT / "scripts/build_graph.py")],
                       check=True, capture_output=True)
        for g in ["causal_claims.graphml", "case_entities.graphml"]:
            tree = ET.parse(ROOT / "graphs" / g)
            ns = "{http://graphml.graphdrawing.org/xmlns}"
            nodes = tree.findall(f".//{ns}node")
            edges = tree.findall(f".//{ns}edge")
            self.assertGreater(len(nodes), 10, g)
            self.assertGreater(len(edges), 10, g)
            ids = {n.get("id") for n in nodes}
            for e in edges:
                self.assertIn(e.get("source"), ids, f"{g}: dangling edge source")
                self.assertIn(e.get("target"), ids, f"{g}: dangling edge target")

    def test_causal_edges_marked_as_claims(self):
        text = (ROOT / "graphs/causal_claims.graphml").read_text(encoding="utf-8")
        self.assertIn("historically situated claim", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
