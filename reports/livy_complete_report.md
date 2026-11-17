# The Complete Extant Livy: 891 Events Across All 35 Surviving Books

*2026-11-17. The corpus now holds every surviving full-text book of Ab Urbe
Condita (I–X, XXI–XLV, Latin + English, 3,528 chapters) plus the Periochae of
lost books 46–142. The political event series covers all of it: **891 events,
every quotation machine-validated verbatim, zero rejections.** We have not
located a prior machine-readable, quote-validated political-event dataset
over the complete extant Livy; no systematic literature review has been
performed, so no priority claim is made.*

## 1. What the corpus expansion is

- Segmentation extended to Books 21–45 (`livy:la/en:21:1` … `45:44`):
  1,234 new chapters per language. Periochae of lost books segmented
  separately (`livy:per:46:0` … `142:0`, 95 summaries).
- 25 per-book coders, same v1 codebook as Books 1–10 (reliability measured on
  that codebook: trigger κ≈.88, channel κ≈.76). Books with ancient lacunae
  (33, 41, 43) handled honestly: coders flagged Crevier editorial supplements
  and asterisk gaps, downgrading confidence rather than inventing content.
- **The access asymmetry is now structural:** Machiavelli never saw Books
  41–45 (Lorsch 1527 / printed 1531). Event-series analyses describe *Livy's
  world*; Machiavelli-source analyses must restrict to I–X + XXI–XL. The
  source-access screening (`reports/falsification_41_45.json`) found no
  identified dependencies on 41–45-unique content — a negative result within
  the extraction's coverage and matching rules, consistent with the recovery
  chronology.

## 2. The claim tests at full scale (`reports/claim_tests.json` regenerated)

### T1 — roba vs onori: the observed direction is opposite to the claim

| conflict domain | all polities (n / ≈extraordinary) | Roman-only (n / ≈extraordinary) |
|---|---|---|
| property (land+debt+food) | 81 / 11.1% | 76 / **7.2%** |
| honors-office | 150 / 16.7% | 135 / **11.9%** |
| legal-rights | 67 / 37.3% | 58 / **34.5%** |
| dynastic | 36 / 62.5% | 16 / 68.8% (regal-period successions) |

Across the coded corpus, **honors-office conflicts show a higher
extraordinary-resolution share than property conflicts** — contrary to the
direction anticipated by our reading of Disc I.37 (nobles yield honors
peacefully, fight for roba). The middle republic supplies the difference: triumph disputes, the Trials of the Scipios,
censorial wars, command-assignment battles. And the earlier finding deepens:
**legal-rights conflict remains the most violent domain by a factor of ~3**,
and it still has no variable in Machiavelli's ontology. (Sensitivity: the directional result survives exclusion of non-Roman
polities; the Roman-only figures are reproducible via the documented text
filter in `scripts/test_claims.py` — output key `T1_roba_vs_onori.roman_only`
in `reports/claim_tests.json`. All shares are descriptive, over coded events
in a corpus that includes books outside Machiavelli's documented access, and
are subject to coding and denominator choices.)

### T2 — trials: the ordinary-channel share FALLS with scale

108 prominent trials (was 41); ordinary-resolution share drops from 82.9% to
**64.8%**, with 39 political killings. The early-republican trials were
institutional set-pieces; the middle-republican record adds contested,
obstructed, and evaded proceedings (Scipio tearing up the account books,
Popillius defying the senate, censors prosecuted by tribunes). Machiavelli's
I.7 picture of the accusation channel as a clean pressure valve fits Livy's
first decade much better than Livy's whole.

### T3 — selection bias: the direction FLIPS

Events in Machiavelli-candidate-cited chapters: 20.9% extraordinary vs 23.5%
in uncited chapters (was 16.2% vs 12.5% on Books I–X alone). With the full
corpus mapped, he no longer looks like he samples toward violence — the
later books are full of violent episodes (court murders, mutinies,
suppression campaigns) that he *ignores*, because his persuasive targets are
institutional lessons, not atrocities. The pilot's selection-bias reading was
itself an artifact of the truncated denominator — a finding about our own
method worth preserving.

## 3. The shape of Livy's domestic politics, complete

891 events; the first decade contributes 383 (densest: Book 4 with 52), the
Hannibalic decade 235 (densest: Book 23 — Capua's defection politics), the
fourth/fifth decades 273 (densest: Book 39 — the Bacchanalian suppression and
Cato's censorship). New-institution remains the modal event type corpus-wide;
the middle republic adds the accountability machinery the early books lack:
extortion recuperatores (43), commission inquiries (29's Locri affair),
informer-reward instruments (32, 39).

## 4. What this buys the Machiavelli project

1. **A complete source-side denominator.** Every proposition anchored to any
   surviving Livian narrative can now be tested against everything Livy says,
   not a tenth of it.
2. **The Hannibal anchor-mass.** The Discorsi's most-cited individual now has
   his decade in the corpus; the chapter map's full-corpus rebuild lifted
   quote-anchored chapters to 24 and cut anchorless chapters from 23 to 12.
3. **A dated upper bound on his sources.** With 41–45 ingested and the
   screening negative, the corpus encodes what Machiavelli could and could
   not have read as a machine-checkable constraint on downstream analyses.

## 5. Caveats (standing)

Single coder per book for 21–45 (reliability measured only on 2 and 6);
translation-layer coding (1857); the polity filter for non-Roman events runs
on notes/groups text, not a schema field (taxonomy v2 adds one); Livy's
middle-republican books are themselves better-sourced than his legendary
early decade, so cross-decade comparisons mix evidentiary regimes — tests
remain tests against *Livy's representation*.
