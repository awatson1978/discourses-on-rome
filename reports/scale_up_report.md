# Scale-Up Report: Full-Corpus Extraction, Reliability, Taxonomy v2

*2026-11-16/17. Companion to `reports/initial_report.md` (pilot) and
`reports/full_corpus_analysis.md` (event series).*

## 1. Per-chapter observation extraction — all 142 chapters

`extractions/chapter_observations.jsonl`: one record per chapter, produced by
nine parallel extractors working from the Italian text (English translation as
comprehension aid only), merged under the standard validation gate.

**Validation: 142/142 chapters accepted, 0 rejections; every one of the
~1,000 Italian quotations machine-verified as a verbatim substring of its
chapter.** Out-of-decade Livy references (Books 21+) were sanitized to null
with an audit note rather than guessed into the first decade.

Totals: **407 propositions, 520 historical episodes, 186 episodes anchored to
a specific Livy I–X chapter** (49 by explicit citation, 114 by verified name
match, 23 by chapter-map hint).

### The headline number: the Discorsi's evidence base is only half Livian Rome

| Episode period | n | share |
|---|---|---|
| Roman Republic | 265 | 51% |
| **Contemporary Italy/Europe (1400s–1500s)** | **122** | **23%** |
| Other antiquity (Greece, Persia, Carthage...) | 74 | 14% |
| Roman Kingdom | 22 | 4% |
| Roman Empire | 14 | 3% |
| Medieval | 13 | 2% |
| Biblical/legendary | 10 | 2% |

A "commentary on the first decade of Livy" draws nearly a quarter of its
evidence from Machiavelli's own political lifetime, and a further seventh from
non-Roman antiquity. Every chapter contains at least one historical episode —
there is no purely abstract chapter in the whole work. The pilot's
"Florentine fingerprint" finding is thus not an artifact of case selection:
contemporary evidence is structural to the method.

Also notable: **Hannibal is the most-cited individual** (17 episodes) — much
of the Discorsi's Roman evidence comes from Livy's *third* decade (the
Hannibalic war, Books 21–30), which is outside both "la prima Deca" of the
title and our ingested corpus. Corpus expansion to Books 21–45 is the single
highest-value next acquisition.

### Proposition types (n=407)

causal-mechanism 35% · empirical-generalization 33% · prescription 26% ·
counterfactual 4% · definition 2%. Two-thirds of the work's propositions are
empirical in form (mechanisms + generalizations) — supporting the project's
premise that the Discorsi encode a testable implicit model, not just counsel.

### Extraction quality notes

Extractors flagged genuine source discrepancies in passing (e.g. III.18's
Tempanius episode: Machiavelli says Aequi, Livy IV.38–41 has Volsci), a
garbled Wikisource heading at I.11, and a textual lacuna in II.7 — all
recorded in the notes fields, none silently fixed.

## 2. Inter-coder reliability (Livy event series)

Two blind re-coders (Books 2 and 6, identical codebook, explicitly forbidden
from reading coder A's output). Full numbers in `reports/reliability.json`.

| Metric | Book 2 | Book 6 |
|---|---|---|
| Events A / B | 50 / 54 | 33 / 44 |
| Event-detection F1 (B vs A) | 0.83 | 0.75 |
| Trigger-domain agreement (matched pairs) | 90.7% (κ=0.89) | 89.7% (κ=0.87) |
| Resolution-channel agreement | 88.4% (κ=0.78) | 82.8% (κ=0.75) |

Reading: the two **analysis variables** (trigger domain, resolution channel)
sit in the substantial-to-almost-perfect κ range, so the claim-test results in
`full_corpus_analysis.md` rest on codings two independent coders largely
reproduce. Event *detection* diverges more (F1 0.75–0.83), driven by
granularity — coder B splits multi-year arcs (notably the Licinian-Sextian
struggle) into more events. Detection counts (event frequencies) should
therefore be treated as ±~20%; channel/trigger *shares* are robust.
Convention note: A-as-reference is arbitrary; neither coder is ground truth.

## 3. Taxonomy v2

Specified in `schema/event_taxonomy_v2.md` from coder feedback: new types
`resource-distribution`, `corporate-secession`, `honorific-award`; a
`dictator_purpose` subfield (12 of 50 v1 dictatorships were
electoral/ceremonial, not emergency); an optional validator-checked
`quantities` field. v2 is a specification — the 383-event series remains v1,
and mixed-version analysis is forbidden by design.

## 4. What this changes in the research picture

1. The compression thesis gains a corpus-scale complement: Machiavelli not
   only deletes measurement from Livy (pilot), he *dilutes* Livy — half the
   evidence base is non-first-decade material, with contemporary Italy the
   largest single supplement.
2. The 186 chapter→Livy anchors are the verified skeleton for scaling the
   pilot's unit-level alignment method (Phase III) beyond the three cases.
3. Reliability numbers convert the event-series findings from "one coder
   says" to "reproducible under blind re-coding, with quantified error bars."
