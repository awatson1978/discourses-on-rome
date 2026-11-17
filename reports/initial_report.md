# Initial Research Report
## Reverse-Engineering Machiavelli's *Discorsi* as a Historical Dataset

*Pilot phase: corpus, pipeline, and three case studies. 2026-11-16.*

All quantitative statements below carry **pilot denominators**: 44 alignment
units, 26 observations, 14 claims, 12 dataset hypotheses drawn from three
administratively rich, deliberately selected chapters (I.7, III.28, I.37) and
their Livian sources. Nothing here extrapolates to the full 142-chapter corpus.

---

## 1. The reconstructed Machiavellian ontology (Phase IV, provisional)

25 variables, `schema/ontology.json`; causal graph in
`graphs/causal_claims.graphml` (25 nodes, 49 edges, every edge marked
"historically situated claim, not established causal fact").

The pilot's central structural finding: Machiavelli's explanatory engine is a
**pressure-and-channel model**, not an actor-psychology model.

- **Master explanatory variables (his own vocabulary, not imposed):**
  *umori* (standing class-specific pressures), *ordini* (institutional
  channels), the *ordinario/straordinario* mode classifier, public vs private
  *reputazione*, *necessità vs ambizione* as motive regimes, *roba vs onori*
  as contested-good types.
- **Interventions:** accusation channels, dictatorship, land law,
  distribution control, colony foundation, timing of reform.
- **Conditions:** grain supply, public-rich/citizens-poor, distance decay.
- **Outcomes:** unrest, faction cascade, external-force invitation, tyranny
  risk, institutional survival.

Variables are overwhelmingly **institutional and distributional**; individual
character enters only as reputation-seeking strategy. Resource variables
(grain, land) appear exclusively as *political instruments* — supply and
distribution as leverage — never as quantities. The implicit schema is thus a
political *control-system* model: flows matter because they open or close
channels, not because of their magnitudes.

## 2. Three worked case studies (Phase VII)

See `reports/case_A_coriolanus.md`, `case_B_maelius.md`, `case_C_agrarian.md`,
with full machine-readable backing. One-line verdicts:

- **A (Coriolanus):** compression strategically bounded — the story stops at
  the trial summons; the sequel (exile → Volscian war) and Livy's aristocratic
  counterfactual are cut because they complicate the thesis. The chapter's
  real evidence is a 4-case comparison in which half the cases are
  Machiavelli's own Florentine professional experience.
- **B (Maelius):** extreme operational loss — a new magistracy, a grain-stock
  census, rationing rules, an intelligence channel, a price (1 as/modius),
  and Livy's documentary criticism all vanish; what remains is preserved
  near-verbatim; two reinterpretations convert a police action into a doctrine
  of preventive repression of private reputation.
- **C (Agrarian):** the deepest abstraction — ~350 years of discrete statutes
  fused into one longitudinal "law" whose value fields are left blank ("tanti
  iugeri"); the founder episode (plebs killing the first proposer) suppressed;
  the destruction-of-the-Republic thesis built on non-Livian material; one
  clean mechanism-swap on a preserved administrative datum (Antium enrollment).

## 3. Livy's narrative vs Machiavelli's compression (Phase III/VI, pilot)

From `reports/selection_analysis.json` (n = 44 units):

| Transformation | n | share |
|---|---|---|
| omission | 14 | 32% |
| addition | 9 | 20% |
| preservation | 8 | 18% |
| abstraction | 8 | 18% |
| reinterpretation | 5 | 11% |

**Loss rate (omission + abstraction) by information dimension:**

| Dimension | loss rate |
|---|---|
| material resources | 1.00 |
| actors (named persons) | 0.75 |
| administrative actions | 0.71 |
| political outcomes | 0.57 |
| causal explanations | 0.31 |
| historical events | 0.22 |

The gradient is the finding: **Machiavelli's compression preserves events and
causal structure while discarding quantities, names, and administrative
operations** — the exact inverse of an administrative record, which preserves
quantities and names while leaving causation implicit. Additions (20% of
units) are never decorative: 4 import other sources (2 of them his own
Florentine experience), 3 are theoretical inferences, 2 are explicit
counterfactuals. He adds *model*, deletes *measurement*.

Answers to the Phase VI questions, pilot-scoped: he preferentially preserves
institutional events and confrontation pivots (sometimes near-verbatim:
aln:a-near-lynching, aln:b-maelius-wealth, aln:c-perpetual-turmoil); he omits
all quantitative information (even the one price Livy records); he retains
institutional relationships while discarding demographic/economic detail
(yes — loss gradient above); elite decision-making over ordinary
administration (yes — Senate deliberations kept, rationing mechanics cut); he
introduced a causal explanation absent from or different than the source in
7/44 units (5 reinterpretations + 2 inference-additions ≈ 16%); and in all
three chapters he uses an episode to support a proposition formally testable
against other episodes — I.7 even *runs* a 4-case test.

## 4. Inventory of identifiable administrative variables (attested + reconstructed)

From `extractions/datasets.jsonl` (levels A and B):

| Dataset | Level | Producing institution (attested basis) |
|---|---|---|
| ds:magistrate-fasti | **A** | annalistic/pontifical records; *libri lintei* cited by Livy IV.13 inside a pilot passage |
| ds:grain-stock-census | B | praefectura annonae 440 BCE: declaration, monthly threshold, forced sale, ration cuts (Livy IV.12) |
| ds:annona-price-series | B | Senate price deliberation (II.34); 1 as/modius distribution (IV.16) |
| ds:import-procurement-log | B | consular purchasing missions, route × outcome (II.34); legationes (IV.12) |
| ds:colonist-enrollment-register | B | triumviri agro dando; *nomina dare* with quota (III.1) |
| ds:trial-event-log | B | tribunician diem dicere (II.35); quaestorian perduellio (II.41); Florentine side: surviving Otto di Guardia registers |
| ds:unrest-event-series | B | constructed from narrative; coding variables derive from Machiavelli (circularity flagged) |
| ds:confiscation-liquidation-records | B | quaestors selling into the treasury (IV.15); inscription + toponym read by Livy as evidence |

## 5. Inventory of hypothetical missing datasets (level C)

| Dataset | Why needed | Why hypothetical |
|---|---|---|
| ds:distribution-recipient-rolls | test largesse→partisans (III.28) | no 5th-c. BCE registration plausible; real analogues only from 123 BCE — and in Renaissance Florence |
| ds:land-tenure-register | test holding-cap enforcement and elite accumulation (I.37) | no early cadastre attested; first hard instruments are the Gracchan termini |
| ds:patronage-network-roster | test private-reputation mechanism | Roman clientela customary, unregistered; Florentine analogues (ricordanze, Monte delle doti) DID produce records |
| ds:war-mobilization-ledger | the mobilization variables Livy stages in II.35 | no Volscian records; kept as a documented negative result (Machiavelli ignores the most chancery-like material in his source) |

A recurring pattern across both inventories: **where a Machiavellian mechanism
needs a dataset Rome could not have produced, Renaissance Florence produced
it.** His private-benefits typology decomposes into Florentine record-producing
instruments; his tribunal-size claim cites a Florentine magistracy by its
numerical composition. The pilot thus supports a precise version of the
working hypothesis: chancery experience shaped the *variables* of his model
(category 2), while giving no evidence he consulted unpublished collections
(category 3 remains unestablished, and nothing in the pilot requires it).

## 6. Testability assessment

- **Testable against surviving Roman evidence now:** the roba-vs-onori
  intensity claim and the accusation-channel claim, via a full Livy I–X
  unrest/trial event coding (the denominators exist in the corpus we already
  ingested); the distance-decay claim, weakly, via colony enrollment anecdotes
  and known colony distances.
- **Testable against Florentine archives:** the tribunal-size claim (Otto
  registers), the private-benefaction claim (ricordanze, dowry funds) —
  outside this project's current corpus but archivally real.
- **Untestable as stated:** the faction-cascade counterfactual and the
  300-year retardation counterfactual (explicitly so; recorded as claim_type
  = counterfactual).
- **Persian evidence:** see §8.

## 7. Scaling plan (to 142 chapters)

1. **Alignment table first**: for each chapter, detect explicit Livy citations
   (regexes over "Tito Livio", book/chapter mentions, proper-name matching
   against a Livy I–X named-entity index built from `livy_la.jsonl`) →
   candidate passage links, human-verified. Output: `extractions/chapter_map.jsonl`.
2. **LLM-assisted extraction** with the existing schemas, under two hard
   rules proven in the pilot: every record carries a verbatim
   `source_passage` (validator-enforced), and Livy-side extraction runs
   without the Machiavelli text in context (bias control, run as separate
   passes).
3. **Unit-level alignment** only for chapters with a secure Livy anchor
   (est. 90–100 of 142); purely theoretical chapters enter the claims table
   only.
4. **Full unrest/trial event coding of Livy I–X** independent of Machiavelli's
   citations — the anti-selection-bias denominator (ds:unrest-event-series at
   scale).
5. Re-estimate the Phase VI statistics with real denominators; the pilot's
   loss gradient is the hypothesis to test.
6. Validation gates stay as-is (`scripts/validate.py`, `tests/`): no record
   without a resolvable citation enters `data/`.

## 8. Phase VIII sketch: the Persepolis Fortification Archive (bounded)

Not started; recorded here as hypothesis generation only. No claim is made
that Machiavelli knew Achaemenid material (he knew Xenophon's *Cyropaedia* —
a literary, not documentary, channel). The reported finding of ration-dispersion
changes around the Ionian Revolt is treated as **unverified** pending access to
the underlying tablet data (PFA editions: Hallock's PF texts; OCHRE/PFA
Online).

What the recovered ontology would predict, if his model travels:

- **ont:reputation-private / largesse→partisans:** officials with
  discretionary allocation power building followings should appear as
  *within-category ration dispersion* and favoritism patterns in commodity
  transfers — the PFA records allocator, recipient category, commodity,
  quantity: precisely `ds:distribution-recipient-rolls`, which Rome lacks and
  Persepolis HAS.
- **ont:grain-distribution-control as leverage:** wartime provisioning
  (499–494 BCE window) should show reallocation toward mobilization-relevant
  groups; Machiavelli's model predicts distribution shifts *precede* or
  *accompany* political stress rather than merely tracking harvests.
- **ont:ordini / administrative discretion:** his ordinary/extraordinary
  distinction maps onto authorization regularity — sealed standard
  authorizations vs ad-hoc orders; the model predicts crisis periods shift
  volume toward the extraordinary channel.
- **Classification of parallels:** all of the above are *functional analogies*
  (same data structures, different institutions), not historical parallels;
  any "rebellion → distribution change" claim would need the tablets' own
  chronology, not the model's expectation. The Achaemenid state is a monarchy
  with a palace economy — Machiavelli's republic-specific variables
  (tribunate, accusation channels) do not transfer; only the
  distribution-discretion-stability triad does.

Concrete next step if pursued: acquire Hallock's PF transliterations/OCHRE
exports, build a transfers table (date, place, commodity, quantity, recipient
category, official, seal), and test the dispersion claim before any
Machiavellian interpretation is layered on.

---

## Repository state

All pilot deliverables are built, validated (0 errors), and tested (14/14):
corpus 1,348 passages (Discorsi IT 145 / EN 144; Livy I–X LA+EN 530+530);
extractions 26 observations / 14 claims / 44 alignments / 12 dataset
hypotheses; SQLite db; 2 GraphML graphs; 3 case reports; selection analysis.
Known gaps are recorded in SOURCES.md (no modern critical editions; Polybius
and Dionysius not ingested; Machiavelli's chancery writings not ingested;
Persepolis data not acquired).
