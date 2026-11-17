# The Lost Books Program

*Reconstructing what can be reconstructed of Ab Urbe Condita's 107 lost books
— as structured data under provenance discipline. Reconstruction is never
presented as prose; the one prose artifact (the apocrypha codex) is a
labeled modern imitation whose CONTENT is firewalled to attested events —
style invented, substance never (see `apocrypha/`, enforced by TestApocrypha).*

## The inverse problem

This repository's core finding is that Machiavelli's *Discorsi* is a lossy
compression of Livy. The lost books pose the exact inverse problem: Livy's
books 11–20 and 46–142 survive only as *compressions* — the Periochae,
Obsequens's prodigy excerpts, Florus, Orosius, Eutropius, and the Livian
layers inside Plutarch and Cassius Dio. Reconstruction means reversing that
compression as far as the evidence allows, and no further.

## The three rules

1. **The evidence model is senior to the linguistic model.** Structural
   priors (see the linguistic atlas: ~15,000 words/book, narrative-density
   estimates) may reject implausible reconstructions; they never generate
   content.
2. **Fragments are quotations, not compositions.** `fragments.jsonl` holds
   only verbatim Livy transmitted by palimpsest or attributed quotation, each
   with its witness and locus; `text_la` stays `null` until the words come
   from a cited edition. No remembered text, no stylistic pastiche. Ever.
3. **Event skeletons are hypotheses.** Each lost book's event table (in
   `skeleton.jsonl` / `books/book_NNN.md`) carries evidence class
   `hypothetical`, and every row must cite at least one witness passage.

## Layout

```
skeleton.jsonl      one structured record per lost book (107): periocha spine,
                    witness slots, empty fragments/events, per-book TODOs
books/book_NNN.md   contributor-facing placeholder, one per lost book
fragments.jsonl     registry of attested verbatim fragments (seeded: the Book 91
                    Vatican palimpsest; Seneca's quotation of Book 120 on
                    Cicero's death; the grammarian-mining category)
witnesses.json      registry of the derivative-tradition sources and status
genealogy.json      witness dependence graph + the lineage counting rule
periocha_events.jsonl   710 skeleton events (the gold dots), verbatim-anchored
obsequens_map.jsonl     82 year-entries mapped by consular pair
parallels_florus_eutropius.jsonl / parallels_orosius.jsonl   419 parallels
narrative_witness_map.json   Plutarch/Dio crosswalk (DRAFT, non-evidentiary)
experiments/        simulated-loss reconstructions + scores (books 22, 39)
lost_books_summary.{html,pdf}   THE GOLD-DOTS DOSSIER — book-by-book summary
apocrypha_codex.{html,pdf}      THE APOCRYPHA CODEX — all 107 books rendered
```

## The two volumes kept here

- **`lost_books_summary.pdf` — the gold-dots dossier.** One section per lost
  book: its periocha-derived skeleton events with category badges, witness
  lines (Obsequens entry counts, epitome-parallel counts, the Plutarch/Dio
  crosswalk), fragment markers, and the honest blanks for 136–137. The
  simulated-loss calibration (20–47% recall, spectacular-biased) is stated in
  the header. Regenerate: `python3 scripts/build_lost_books_summary.py`, then
  Chrome headless `--print-to-pdf`.
- **`apocrypha_codex.pdf` — the rendering.** The 107 apocrypha of
  `apocrypha/` bound into one era-sectioned volume. English-only by design;
  content firewalled to the attested events with per-sentence citations;
  "None of this is Livy" on the title page; enforced mechanically by
  `TestApocrypha`. Regenerate: `python3 scripts/build_apocrypha_codex.py` +
  Chrome. (The third volume, the verbatim-fragments dossier, stays in
  `reports/lost_fragments.pdf` with the project's other analytical reports —
  fragments are *evidence*, and evidence reporting lives in `reports/`.)

Witness texts live in the main corpus: `corpus/raw/witnesses/` and
`corpus/segments/witnesses_la.jsonl` (Periochae 11–20, Obsequens, Florus 1–2,
Orosius 1–7, Eutropius 1–10 — acquired by `scripts/acquire_witnesses.py`).
The Periochae of 46–142 were already in `corpus/segments/livy_periochae_la.jsonl`
(Perseus). **The periochae of Books 136–137 are themselves lost** and so
marked in the skeleton.

## Current status (scaffold)

- [x] 107 placeholder records + contributor pages
- [x] Periocha spine attached for 105 books (Latin)
- [x] Five witness corpora acquired in Latin (≈936k chars)
- [x] Fragment registry seeded (2 certain items + mining category), texts
      pending acquisition from cited editions
- [x] Obsequens entries mapped to books (82 year-entries by consular pair;
      `obsequens_map.jsonl`; gaps 174-168, 82-78, 72-64, 41-18 BCE flagged)
- [x] Florus/Orosius/Eutropius parallel passages located per book: 419
      verbatim-anchored parallels (`parallels_florus_eutropius.jsonl` 201,
      covering 102/107; `parallels_orosius.jsonl` 218, covering 100/107);
      uncovered books (46-48, 70, 84, 121) are themselves attestation data;
      intra-lineage divergences flagged (e.g. Orosius vs periocha on who
      defeated Crixus)
- [x] Plutarch/Dio mapping upgraded to book level with verbatim periocha
      anchors (`narrative_witness_map.json`, DRAFT non-evidentiary; 81/107
      books have Plutarch coverage)
- [~] Quotation mining: Seneca Suasoriae acquired and BOTH Book 120
      fragments extracted verbatim (`fragments.jsonl`); grammarian corpora
      (Priscian, Nonius) still to mine
- [x] Event skeletons extracted from periochae: **710 events across all 105
      books with surviving periochae, 0 validation rejects**
      (`periocha_events.jsonl`)
- [x] Simulated-loss experiments run and scored (`experiments/`):
      Book 22 recall 46.6% / precision 83.3%; Book 39 recall 19.7% /
      precision 55.6%, zero hallucinations. Shared law: epitomes preserve
      the spectacular (dictatorships, scandals, famous deaths) and destroy
      institutional process (the Bacchanalia's 8 coded phases → 1 sentence).
      These are the calibration numbers for every gold dot in the
      attestation chart — and the recall ceiling for the 107 lost books.
- [x] Fragments dossier: `reports/lost_fragments.pdf` (Latin + working
      translations, provenance, honesty labels)
- [ ] External review pass for missed witnesses (planned: ChatGPT session)

## Evidence genealogy — agreement is not independence

`genealogy.json` encodes the dependence structure of the witness set, with
relationship statuses (direct-quotation / direct-transmission /
probable-dependence / possible-dependence / shared-intermediary-suspected /
substantially-independent / conjecture) and the **counting rule**: attestation
count = number of independent *lineages*, not witnesses. The Periochae,
Oxyrhynchus epitome, Obsequens, Florus, Eutropius, and Orosius are
(by default) ONE Livy-derivative lineage; Plutarch and Dio are partially
independent lineages; the palimpsest and the Seneca quotations are direct
transmission. Divergence *within* a lineage is recorded as data, never
averaged away. Review passes may downgrade, merge, or reject connections —
the scaffold must be able to lose confidence, not only gain material.

## Architecture: unified cross-book graph, not per-book silos

Witness corpora, the Obsequens year-map, the parallels files, and the
genealogy are all **corpus-level, cross-book artifacts**; the per-book
records in `skeleton.jsonl` and `books/` are *views* into them keyed by book
number. This means a witness passage re-dated to a different year migrates
between books without re-extraction, and duplicate-evidence merging happens
once, globally. (The eventual evidence-dependency graph will live in
`graphs/` alongside the project's other GraphML artifacts.)

## Simulated-loss experiments (`experiments/`)

The decisive calibration: pretend a *surviving* book is lost, reconstruct its
event skeleton from the derivative tradition alone (blinded agents, forbidden
the full text and its codings), then score against the independently coded
ground truth (891-event series). This measures how much domestic-political
information the derivative tradition actually preserves — i.e., the expected
recall ceiling for the genuinely lost books — and where epitome agreement
manufactures false confidence. First subjects: Book 22 (a dramatic, dense
year) and Book 39 (the Bacchanalia and Cato's censorship).

## How to contribute a witness or fragment

Add to the relevant `books/book_NNN.md` checklist AND the structured file:
witnesses with source + passage ref + what they preserve; fragments only with
quoting author, locus, and the exact quoted words from a named edition. The
validator will check that fragment texts, once present, are substrings of an
acquired witness text.
