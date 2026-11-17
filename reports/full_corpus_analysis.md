# Full-Corpus Analysis: Livy I–X Event Series vs Machiavelli's Propositions

*Scale-up phase, 2026-11-16. Data: `extractions/livy_events.jsonl` (383 events,
10 books, LLM-coded from Spillan's translation with validator-enforced verbatim
quotes; 0 rejects), `extractions/chapter_map.jsonl` (142 chapters),
`reports/claim_tests.json`.*

**Standing caveat.** These are tests against *Livy's representation* of Rome,
not against Roman reality; the early books are late, moralized reconstruction.
Trigger-domain and resolution-channel codings involve analyst judgment (per-book
coders, shared codebook). Confidence-weighted sensitivity checks are future work.

## 1. The denominator Machiavelli never shows

The event series is the first deliverable that does *not* pass through
Machiavelli's selection. Shape of Livy I–X domestic politics, as coded:

- **383 events**: new-institution 74, dictator-appointed 50, electoral-conflict
  47, prominent-trial 41, colony-founded 23, agrarian-agitation 19,
  levy-obstruction 19, conspiracy 18, political-killing 15, riot-tumult 15,
  veto-deadlock 13, debt-crisis 12, regime-change 10, military-mutiny 9,
  famine-scarcity 8, external-appeal 4, secession 3, grain-dispute 3.
- **Resolution channels**: ordinary 250 (65%), extraordinary 38 (10%),
  unresolved 37, mixed 25, na 33.

Livy's first decade, taken whole, is dominated by *institutional production*
(new offices, laws, colonies) and *channeled conflict* (trials, elections,
vetoes); open violence is a one-in-ten outcome. Machiavelli's *Discorsi* I.4
thesis — that Rome's tumults were productive because they discharged through
ordini — is, at this descriptive level, a fair summary of Livy's shape, which
is itself unsurprising: it is Livy's own editorial thesis too.

## 2. T1 — the roba-vs-onori test (claim:d1c37-roba-vs-onori)

Machiavelli: men value property over honors; the nobility yielded honors
without extraordinary scandal but defended property until the plebs resorted
to extraordinary means.

Within Livy I–X, among conflict-type events:

| trigger domain | n | ≈extraordinary share |
|---|---|---|
| property (land+debt+food) | 58 | **7.8%** |
| honors-office | 60 | **7.5%** |
| legal-rights | 34 | **35.3%** |

**Result: no property-vs-honors difference within the first decade** — both
run ~8%, i.e. the nobility temporized property conflicts exactly as
successfully as honors conflicts in this period. This does not refute
Machiavelli outright, because his own claim is temporally structured: he says
the elites *successfully* temporized ("con pazienza ed industria la
temporeggiavano") until the Gracchi — who lie outside Livy I–X. The test
*does* establish two things he does not say:

1. **The early-republican data alone give no support** to the preference
   asymmetry (roba > onori): the agrarian agitations of the first decade were
   not systematically more violent than the consulship/priesthood struggles.
   His asymmetry claim rests entirely on the non-Livian, late-republican
   material (see `aln:c-gracchi-trajectory`).
2. **The actually violent domain in Livy I–X is neither roba nor onori but
   legal-rights** (35% extraordinary): the decemviral tyranny and overthrow,
   Verginia, the Manlian debt-bondage rescues, appeal/provocatio crises —
   conflicts over personal liberty and legal protection. Machiavelli has no
   dedicated variable for this domain; his roba/onori dichotomy (Disc I.37)
   partitions away the category where Livy's violence actually lives. This is
   a genuine *gap in the recovered ontology*, found only by building the
   denominator.

## 3. T2 — the accusation-channel proxy (claim:d1c7-accusation-channels)

41 prominent-citizen trials; **82.9% resolve through ordinary channels**;
15 political killings in the same corpus. Descriptively consistent with
Machiavelli's claim that Rome's accusation institutions absorbed elite-directed
anger. But this is the weak version of the test: the strong version needs
within-Rome variation in channel *availability*, which barely exists in Livy
I–X (the tribunate exists from Book 2 on). Machiavelli saw this himself — his
I.7 evidence is cross-polity (Rome vs Clusium vs Florence ×2), not
within-Rome. The claim remains untested in the strict sense; our contribution
is establishing the Roman base rates (trials common, killings rare,
trial-to-killing ratio ≈ 2.7:1).

## 4. T3 — selection bias, first quantification

Using the chapter map's candidate anchors (quote + name heuristics, 114 Livy
chapters implicated): events in Machiavelli-candidate chapters run
**16.2% extraordinary vs 12.5%** in unimplicated chapters. Direction as
expected: he samples toward the violent and dramatic. The gap is modest, and
the cited/uncited partition is noisy (name-anchor candidates over-include);
a verified chapter map will sharpen this. But even at this resolution, the
374 events in *uncited* chapters include 74 institutional creations he never
discusses — the routine constitutional production that his
exemplum-driven method systematically under-samples.

## 5. Feedback into the pilot artifacts

- **ds:colonist-enrollment-register upgraded**: Book 10 coding found a second
  enrollment shortfall (Minturnae/Sinuessa, Livy 10:21) parallel to Antium —
  the distance-decay claim (claim:d1c37-distance-decay) now has two coded data
  points and a defined test (enrollment outcome × distance) over the 23 coded
  colony foundations.
- **ds:land-tenure-register strengthened**: Livy 10:13 records aedilician
  prosecutions of holders exceeding the land cap — evidence of *enforcement
  activity* (hence records) a century and a half before the Gracchan termini.
  Reclassification from C toward B should be considered for the 4th-c. horizon.
- **claim:d3c28-private-benefits-tyranny enriched**: Book 8 adds Flavius's
  funeral meat-largesse route to office — a second private-benefaction datum
  independent of the grain mechanism.
- **Taxonomy v2 needs**: booty/movables distribution (Book 5 coder flagged),
  viritane land distribution as non-conflict event (Book 8), guild secession
  (Book 9).

## 6. Methods note

Coding was performed by 10 parallel per-book coders from the English
translation, blind to this report's hypotheses (their brief named event types
and fields only). All 383 quotes machine-validated as verbatim substrings;
rejects file empty. Known limits: single-coder-per-book (no inter-coder
reliability yet), translation-layer coding, event granularity judgment
(arcs vs incidents) varying somewhat by coder. Next methodological step:
double-code two books with a second pass and report agreement.
