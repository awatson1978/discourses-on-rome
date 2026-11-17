# External contribution: Livy Linguistic & Structural Atlas

**Provenance:** contributed 2026-11-16 by the project's human researcher from a
session with **ChatGPT (OpenAI)**, which ran an independent linguistic analysis
of the same Perseus Weissenborn–Müller Latin text this repository uses.
Files received as-is: `livy_linguistic_atlas.html` (self-contained report,
vector charts), `livy_35_books_linguistic_metrics.csv` (per-book structural
metrics), `livy_most_frequent_word_forms.csv` (corpus frequency table).

**Independent verification (ours):** `scripts/verify_linguistic_atlas.py`
recomputed per-book token counts and word-form frequencies from this
repository's own segmentation. Result: **CONFIRMED within tokenizer
tolerance** — mean per-book word-count delta 0.87% (max 1.84%), top word
forms within 0.4%; the single chapter-count mismatch (Book 1: 61 vs 60) is
the praefatio counting convention. Full comparison:
`reports/linguistic_atlas_verification.json`.

**Known definitional differences:** the atlas excludes interleaved Periochae
from book boundaries (our segmentation separates them already); sentence
counts are punctuation-heuristic and editorial, flagged as such in the atlas
itself; Books 41–45 lengths reflect lacunose survival, not original size.

These statistics serve the lost-books program as **probabilistic constraints,
not templates** — see the README's "Linguistic fingerprint" section and the
Discussion section's reconstruction principles.
