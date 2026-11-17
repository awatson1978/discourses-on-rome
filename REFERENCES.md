# References & Related Work

*Convention, in keeping with this repository's evidence discipline: every
entry carries a status flag. `consulted` means the text informed the work
directly; `cited-not-yet-read` means the reference was identified (by the
researcher or an external review pass) as relevant positioning literature but
has not yet been read against this project's claims. Nothing here is cited as
support for a finding unless consulted.*

## Computational analysis of political theory and classics

- DeCanio, Stephen J. (2020). "Can an AI learn political theory?"
  *AI Perspectives* 2, art. 3. doi:10.1186/s42467-020-00007-2.
  **Status: cited-not-yet-read.** Reported relevance: LDA topic modeling over
  six classical political works including Machiavelli's *Prince* and
  *Discourses*; demonstrates computational treatment of political theory but
  does not attempt source-to-claim reconstruction — the gap this project
  works in.

- Dexter, Joseph P.; Katz, Theodore; Tripuraneni, Nilesh; Dasgupta, Tathagata;
  Kannan, Ajay; Brofos, James A.; Bonilla Lopez, Jorge A.; Schroeder, Lea A.;
  Casarez, Adriana; Rabinovich, Maxim; Haimson Lushkov, Ayelet; Chaudhuri,
  Pramit (2017). "Quantitative criticism of literary relationships."
  *PNAS* 114(16): E3195–E3204. doi:10.1073/pnas.1611910114.
  **Status: cited-not-yet-read.** Reported relevance: machine-learning
  stylometry with a Livy case study (citational vs non-citational content;
  Caesarian influence on Livian prose) — establishes the computational-classics
  tradition this project's linguistic-fingerprint work (see
  `external/linguistic_atlas/`) sits inside.

## Machiavelli and Livy

- Internet Encyclopedia of Philosophy, s.v. "Niccolò Machiavelli."
  https://iep.utm.edu/machiave/
  **Status: cited-not-yet-read.** Reported relevance: explicitly identifies
  the extent of Machiavelli's transformation of Livy's thought as an open
  question — the question this repository operationalizes (the transformation
  taxonomy, the loss gradient, the 44 unit-level alignments).

## Source-based historical event coding

- "Historical archives from the Roman monarchic and republican periods show
  human perceptions of environment and climate change in Italy, 753–29 BCE"
  (2025). *The Holocene*. doi:10.1177/09596836241307302.
  **Status: cited-not-yet-read.** Reported relevance: a structured dataset of
  319 environmental observations coded from Livy, Obsequens, Dionysius, and
  Dio — direct methodological kin to our 891-event political series and the
  Obsequens witness corpus in `lost_books/`. Notable overlap: they code the
  same prodigy tradition we hold as a lost-books witness; a
  cross-walk of their event table against `corpus/segments/witnesses_la.jsonl`
  (Obsequens) would be a natural validation exercise.

## Primary-source editions and data used directly (consulted)

See `SOURCES.md` for the full corpus provenance (Perseus Weissenborn–Müller
Livy; it.wikisource Discorsi; Thomson 1883; Spillan 1857; The Latin Library
witness texts; CDLI Persepolis tablets per Hallock OIP 92), and
`external/linguistic_atlas/README.md` for the externally contributed,
independently verified linguistic atlas.

## How to add a reference

Add the entry under the right section with a status flag and one sentence of
claimed relevance. When a cited-not-yet-read item gets read, upgrade its
status and note what it changed (or didn't) in the relevant report. The
researcher's planned external review passes (ChatGPT source-hunting for
`lost_books/witnesses.json`) should deposit candidates here as
cited-not-yet-read, never directly into findings.
