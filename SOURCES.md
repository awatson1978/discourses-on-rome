# Corpus Sources and Provenance

Retrieved 2026-11-16. Project Gutenberg's main site was down for maintenance on
the retrieval date; the PGLAF master mirror was used instead (identical files).

## 1. Discorsi — Italian original

- **Work:** Niccolò Machiavelli, *Discorsi sopra la prima Deca di Tito Livio*
  (composed c. 1513–1519; first printed Blado, Rome 1531).
- **Digital edition:** Italian Wikisource transcription,
  https://it.wikisource.org/wiki/Discorsi_sopra_la_prima_Deca_di_Tito_Livio
  (per-chapter subpages; dedication + 3 book proemi + 142 chapters:
  I.1–60, II.1–33, III.1–49).
- **Underlying print edition:** 19th-century *Opere* text as transcribed by
  Wikisource (not a modern critical edition; see RESEARCH_METHOD.md
  "Edition effects").
- **Retrieval:** `scripts/acquire_discorsi_it.py` via the MediaWiki API,
  wikitext + rendered plain text per page; revision IDs recorded per file in
  `corpus/raw/discorsi_it/*.json`.
- **License:** text public domain; Wikisource transcription layer CC BY-SA 4.0.
- **Limitations:** modernized-ish 19th-c. orthography; II.5's numbering follows
  the Wikisource/vulgate chapter division.

## 2. Discorsi — English translation

- **Edition:** *Discourses on the First Decade of Titus Livius*, trans.
  **Ninian Hill Thomson** (London: Kegan Paul, Trench & Co., 1883).
- **Digital source:** Project Gutenberg eBook #10827, plain text
  (`10827-0.txt`), retrieved from the PGLAF master mirror
  https://gutenberg.pglaf.org/1/0/8/2/10827/10827-0.txt
- **License:** public domain (US); Project Gutenberg license applies to the PG
  file packaging.
- **Limitations:** Victorian diction; occasionally paraphrases; chapter headings
  sometimes condense Machiavelli's titoli.

## 3. Livy — Latin

- **Work:** Titus Livius, *Ab Urbe Condita*. This project primarily uses
  Books I–X (the "first decade" Machiavelli discusses).
- **Digital edition:** Perseus Digital Library CTS text
  `urn:cts:latinLit:phi0914.phi001.perseus-lat2`, ed. W. Weissenborn &
  H. J. Müller (Teubner), via PerseusDL/canonical-latinLit (GitHub, master).
  https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/master/data/phi0914/phi001/phi0914.phi001.perseus-lat2.xml
- **License:** CC BY-SA 4.0 (Perseus).
- **Limitations:** not the current OCT/Ogilvie text; section numbering is the
  standard Weissenborn-Müller division used by most citations.

## 4. Livy — English

- **Edition:** *History of Rome*, trans. **D. Spillan** (Books I–VIII, 1857,
  Bohn), with Cyrus Edmonds and W. A. McDevitte for later books.
- **Digital source:** Perseus `urn:cts:latinLit:phi0914.phi001.perseus-eng2`,
  via PerseusDL/canonical-latinLit (GitHub, master).
- **License:** CC BY-SA 4.0 (Perseus layer); translation public domain.
- **Limitations:** 1857 translation; renders some institutional terms loosely
  ("commons" for plebs etc.). Where wording matters we quote the Latin.

## 5. Ancillary sources (used, not yet ingested as corpus)

- **Polybius, *Histories* VI** (anacyclosis; Machiavelli's Disc I.2 depends on
  it, probably via an intermediary — he likely could not read Greek). Candidate
  digital text: Perseus `tlg0543.tlg001`. Status: NOT ingested; cited only in
  prose analysis, marked `modern-scholarship` / `analysis-inference`.
- **Dionysius of Halicarnassus, *Roman Antiquities* VII–VIII** (fuller
  Coriolanus narrative). Status: NOT ingested; noted as comparison gap.
- **Machiavelli's chancery writings** (legations, *Ordinanza* documents,
  provisioning correspondence) — used only as published-scholarship context,
  no digital corpus ingested. Gap documented in reports/initial_report.md.

## Known gaps

- No modern critical edition of the Discorsi (Inglese 1984 / Bausi 2001) is
  openly licensed; textual variants are therefore invisible to this pipeline.
- Persepolis Fortification Archive data (Phase VIII): machine-readable tablet
  data exist (e.g. OCHRE/PFA Online, Hallock's PF editions); not yet acquired.
  The analysis referenced in the project brief is treated as unverified.
