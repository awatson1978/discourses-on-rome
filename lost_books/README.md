# The Lost Books Program

*Reconstructing what can be reconstructed of Ab Urbe Condita's 107 lost books
— as structured data under provenance discipline, never as prose.*

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
```

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
- [ ] Obsequens entries mapped to books (consular-year keying)
- [ ] Florus/Orosius/Eutropius parallel passages located per book
- [ ] Plutarch/Dio section-level mapping (currently era-level, APPROXIMATE)
- [ ] Grammarian quotation mining
- [ ] Event skeletons extracted from periochae
- [ ] External review pass for missed witnesses (planned: ChatGPT session)

## How to contribute a witness or fragment

Add to the relevant `books/book_NNN.md` checklist AND the structured file:
witnesses with source + passage ref + what they preserve; fragments only with
quoting author, locus, and the exact quoted words from a named edition. The
validator will check that fragment texts, once present, are substrings of an
acquired witness text.
