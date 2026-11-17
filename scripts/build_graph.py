#!/usr/bin/env python3
"""Build GraphML graphs from extractions.

graphs/causal_claims.graphml  — ontology variables as nodes; claims as edges
                                (cause→effect, one edge per pair, attributed)
graphs/case_entities.graphml  — observations, actors, institutions, passages
"""
import json
import pathlib
import xml.sax.saxutils as sx

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "graphs"


def esc(s):
    return sx.escape(str(s))


def write_graphml(path, nodes, edges, node_keys, edge_keys):
    with open(path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">\n')
        for i, k in enumerate(node_keys):
            f.write(f'  <key id="nk{i}" for="node" attr.name="{k}" attr.type="string"/>\n')
        for i, k in enumerate(edge_keys):
            f.write(f'  <key id="ek{i}" for="edge" attr.name="{k}" attr.type="string"/>\n')
        f.write('  <graph edgedefault="directed">\n')
        for nid, attrs in nodes.items():
            f.write(f'    <node id="{esc(nid)}">\n')
            for i, k in enumerate(node_keys):
                if attrs.get(k):
                    f.write(f'      <data key="nk{i}">{esc(attrs[k])}</data>\n')
            f.write('    </node>\n')
        for j, (src, tgt, attrs) in enumerate(edges):
            f.write(f'    <edge id="e{j}" source="{esc(src)}" target="{esc(tgt)}">\n')
            for i, k in enumerate(edge_keys):
                if attrs.get(k):
                    f.write(f'      <data key="ek{i}">{esc(attrs[k])}</data>\n')
            f.write('    </edge>\n')
        f.write('  </graph>\n</graphml>\n')
    print(f"{path.name}: {len(nodes)} nodes, {len(edges)} edges")


def main():
    OUT.mkdir(exist_ok=True)
    onto = json.loads((ROOT / "schema" / "ontology.json").read_text(encoding="utf-8"))
    claims = [json.loads(l) for l in (ROOT / "extractions" / "claims.jsonl").open(encoding="utf-8")]
    obs = [json.loads(l) for l in (ROOT / "extractions" / "observations.jsonl").open(encoding="utf-8")]

    # --- causal claims graph ---
    nodes = {v["id"]: {"label": v["label"], "domain": v["domain"], "role": v["role"],
                       "discovered": str(bool(v.get("discovered")))}
             for v in onto["variables"]}
    edges = []
    for c in claims:
        for cv in c["cause_variables"]:
            for ev in c["effect_variables"]:
                edges.append((cv, ev, {
                    "claim_id": c["claim_id"], "author": c["author"],
                    "statement": c["statement"], "polarity": c.get("polarity", ""),
                    "claim_type": c["claim_type"], "source_ref": c["source_ref"],
                    "epistemic_status": "historically situated claim, not established causal fact",
                }))
        for mv in c.get("moderator_variables", []):
            for ev in c["effect_variables"]:
                edges.append((mv, ev, {
                    "claim_id": c["claim_id"], "author": c["author"],
                    "statement": "(moderator) " + c["statement"],
                    "polarity": "moderates", "claim_type": c["claim_type"],
                    "source_ref": c["source_ref"],
                    "epistemic_status": "historically situated claim, not established causal fact",
                }))
    write_graphml(OUT / "causal_claims.graphml", nodes, edges,
                  ["label", "domain", "role", "discovered"],
                  ["claim_id", "author", "statement", "polarity", "claim_type",
                   "source_ref", "epistemic_status"])

    # --- entity graph ---
    enodes, eedges = {}, []
    for o in obs:
        oid = o["observation_id"]
        enodes[oid] = {"label": o["historical_event"][:120], "kind": "observation",
                       "evidence_class": o["evidence_class"]}
        ref = o["discorsi_reference"]
        enodes.setdefault(ref, {"label": ref, "kind": "passage", "evidence_class": ""})
        eedges.append((oid, ref, {"relation": "extracted_from"}))
        for kind, key in [("actor", "actors"), ("institution", "institutions"),
                          ("group", "population_groups"), ("resource", "resources")]:
            for name in o.get(key, []):
                nid = f"{kind}:{name}"
                enodes.setdefault(nid, {"label": name, "kind": kind, "evidence_class": ""})
                eedges.append((oid, nid, {"relation": f"mentions_{kind}"}))
    write_graphml(OUT / "case_entities.graphml", enodes, eedges,
                  ["label", "kind", "evidence_class"], ["relation"])


if __name__ == "__main__":
    main()
