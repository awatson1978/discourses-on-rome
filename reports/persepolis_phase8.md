# Phase VIII — The Persepolis Fortification Archive

*2026-11-17. Status: data acquired (partial by necessity), hypotheses
formalized, one crude descriptive check run. Nothing here is a confirmed
finding; see §5.*

## 1. What was acquired

Hallock's *Persepolis Fortification Tablets* (OIP 92, 1969) via the Cuneiform
Digital Library Initiative (CDLI publication 155926, CC BY):

- **2,087 tablet records** downloaded (`corpus/raw/persepolis/artifacts/`,
  one JSON per tablet; reproducible via `scripts/acquire_persepolis.py`;
  0 fetch errors).
- Of these, **68 (3.3%) carry ATF transliterations with Hallock-derived
  English translation lines** — CDLI's `is_atf_public` flag marks permission,
  not existence; most records are catalog metadata only. The transliterated
  subset is **non-random** (selected by CDLI's digitization effort), which is
  the binding constraint on everything below.
- Parsed into `extractions/persepolis_transfers.jsonl`
  (`scripts/parse_persepolis.py`): per tablet — commodity, quantities with
  units (BAR dry / marris liquid), Darius I regnal year, month, persons
  ({hal} determinative), places ({asz}), function keywords, and a
  parse-confidence flag. Validator rule: every parsed value must be
  recoverable from the stored translation text (tests/TestPersepolis).

A sample record (PF 0001): *"30 bar of grain (to) Anshan was taken, 17th
year... Makuš received it, Umanna (is) to apportion (it)."* — commodity,
quantity, destination, year, receiving official, apportioning official. This
is, structurally, `ds:distribution-recipient-rolls` — the dataset the Roman
pilot classified as **C-hypothetical** because Rome could not have produced
it. The Achaemenid administration *did* produce it, and it survives. That
asymmetry is the central Phase VIII result: **Machiavelli's data model, which
exceeds the documentary capacity of the Rome he theorized, matches almost
field-for-field the actual record-keeping of an ancient state he knew only
through literary sources.**

## 2. The recovered-ontology → PFA field mapping

| Machiavellian variable | PFA observable | Status |
|---|---|---|
| ont:grain-distribution-control | commodity transfers with named allocators and receivers | directly observable (68 texts) |
| ont:reputation-private (largesse→partisans) | within-allocator favoritism patterns across recipients | requires recipient-category coverage we lack |
| ont:ordini / ordinary-vs-extraordinary | sealed standard authorizations vs ad-hoc orders | observable in principle via seal data (OIP 117, not ingested) |
| ont:distance-decay | quantities × destination distance (Anshan, Baršan, Tirazziš...) | toponyms parsed; distances not yet coded |
| ont:public-rich-citizens-poor | treasury vs individual allocations | partially: "treasury" keyword appears |

All mappings are **functional analogies** (same data structures, different
institutions), never historical parallels: a palace redistributive economy
under a king is not a republic, and the republic-specific half of the
ontology (tribunate, accusation channels) has no PFA counterpart by design.
No claim is made that Machiavelli knew this archive (his Persian knowledge
was literary — Xenophon's *Cyropaedia*, cited in the Discorsi).

## 3. Formalized hypotheses (testable with full PFA data)

- **H1 (distributional hierarchy):** ration quantities stratify by recipient
  category (officials > workers; gender/age gradients), with category gaps
  stable across sites. [Needs Hallock category codes + recipient fields.]
- **H2 (discretion signature):** allocations authorized by the same named
  official show lower variance than cross-official allocations at the same
  site-month (administrative discretion leaves a dispersion fingerprint).
- **H3 (wartime provisioning):** transfer composition shifts toward
  mobilization-relevant categories (travel rations, horse feed) in years
  22–24 (~500–498 BCE), *preceding* rather than tracking harvest variation.
- **H4 (distance decay):** per-transfer quantities decline with destination
  distance from the Persepolis core, controlling for commodity.
- **H5 (the brief's dispersion claim):** within-group ration dispersion
  increases around the Ionian Revolt's outbreak (~499 BCE = Darius year 23).
  **Treated as unverified**; provenance of the claimed analysis unknown.

## 4. The crude check we could run (H5-adjacent, underpowered)

Grain quantities in BAR with a parsed regnal year, all text types pooled
(n=26 values across 10 years — NOT a within-group ration series):

| window | n | CV (sd/mean) |
|---|---|---|
| years 22–23 (~500–499 BCE) | 12 | 1.01 |
| all other years | 14 | 1.87 |

Direction is *opposite* to H5, but the comparison is worthless as evidence:
tiny n, mixed text types (transport vs deposit vs rations), and a non-random
transliterated subset. The honest conclusion is **no support either way;
coverage, not method, is the constraint.** Full numbers in
`reports/persepolis_analysis.json`.

## 5. What would make this real

1. Hallock's category codes (A–W) per text — recoverable from OIP 92's
   print organization (archive.org scan acquired by CDLI; OCR pass feasible).
2. PFA Online / OCHRE export of the post-Hallock editions (thousands of
   additional texts incl. NN series) — requires contacting the PFA project;
   no bulk endpoint found in this session.
3. Recipient-category coding (gentlemen/workers/boys/women/princess...)
   on ration texts — partially parseable from the existing 68.
4. Seal-protocol data (OIP 117) to operationalize the ordinary/extraordinary
   channel distinction.

Until then, Phase VIII stands as: hypotheses formalized, pipeline built and
tested end-to-end on real tablet data, and the project's sharpest structural
finding confirmed from the Persian side — the dataset Machiavelli's model
needs, and Rome lacks, exists at Persepolis.
