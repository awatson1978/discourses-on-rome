# Research Method

## Object of study

Machiavelli's *Discorsi* is treated as the output of an information-processing
system: historical narratives (mostly Livy) + professional administrative
experience (Florentine chancery, 1498–1512) → general political propositions.
We reverse the pipeline: from propositions back to the observations, variables,
and (hypothetically) the administrative records that would ground them.

## Evidentiary discipline

Every statement in this repository belongs to exactly one of five strata, and
records carry an explicit `evidence_class`:

| Stratum | Label | Example |
|---|---|---|
| What ancient sources report | `source-reported` | Livy II.34: grain was bought up from Etruria |
| What Machiavelli claims | `machiavelli-claim` | Disc I.7: accusations channel humors that otherwise burst out illegally |
| What modern scholarship establishes | `modern-scholarship` | the Coriolanus narrative is heavily legendary (see limitations) |
| What our analysis infers | `analysis-inference` | Machiavelli's compression drops Livy's supply-side detail |
| What remains hypothetical | `hypothetical` | annona-style distribution registers for the 490s BCE |

Rules:

1. **No fabricated passages.** Every quotation carries a `passage_id` resolvable
   against `corpus/segments/`. Gaps are reported, not filled.
2. **Independent extraction before comparison** (Phase III): Livy records are
   extracted from Livy's text on its own terms, then aligned with Machiavelli.
   Extraction worksheets for Livy are drafted without the Machiavelli record open.
3. **Claims, not facts.** Causal edges in `graphs/` are historically situated
   claims attributed to an author, never validated mechanisms.
4. **No circularity.** A mechanism derived from Machiavelli may organize questions
   put to Livy, but Livy's narrative is never counted as *independent* validation
   of a mechanism that was read off Machiavelli in the first place. The
   `provenance` array on every record makes the derivation path auditable.
5. **Hypothetical datasets stay hypothetical** (Phase V class C). They are data
   *structures* (schemas), never populated with invented values.
6. **Roman ≠ Renaissance recordkeeping.** Dataset hypotheses name the institution
   that could have produced the records and the period-appropriate documentary
   form (e.g. tabulae publicae in the aerarium vs. Florentine ricordanze or the
   Dieci di Balìa's registri); we do not project quattrocento bureaucracy onto
   the early Republic.

## Known limitations

- **Livy's own sources.** For the early Republic Livy writes 500 years after the
  events, from annalistic predecessors; "Livy's dataset" is itself a compressed,
  moralized reconstruction. Our comparison measures *Machiavelli's* transformation
  of *Livy*, not either author's fidelity to events. Dates use Varronian
  chronology and are flagged `traditional` where the underlying episode is
  legendary or semi-legendary (virtually everything before ~300 BCE).
- **Translation layers.** Quantitative selection measures are computed on the
  original languages wherever possible; translations (Thomson 1883, Spillan 1857)
  are aids, and both are 19th-century texts with period biases.
- **Edition effects.** The Wikisource Italian text and Perseus Latin text are
  19th-century editions, not modern critical editions (Inglese, Ogilvie). Chapter
  numbering is stable across editions; wording may differ in places.
- **Machiavelli's memory and secondary channels.** Machiavelli sometimes cites
  Livy loosely or from memory, and knew intermediary traditions (Polybius via
  friends' translations — he probably could not read Greek; Flavio Biondo;
  Florentine civic humanism). An "Addition" classification therefore does not
  imply invention; each addition is investigated for a plausible channel.
- **Case selection bias (ours).** The three pilot cases were chosen because they
  are administratively rich (grain, land). Selection statistics from the pilot
  (Phase VI) must not be extrapolated to the full corpus; they are reported with
  pilot-only denominators.
- **Documentary-exposure hypothesis.** The claim that Machiavelli drew on
  unpublished administrative collections (category 3 of the working hypothesis)
  is NOT assumed anywhere in the pipeline. What is used: his attested chancery
  practice (legations, the 1506 Ordinanza, provisioning correspondence), which
  is cited from his official writings where relevant and marked as such.

## Transformation taxonomy (Phase III/VI)

For each aligned information unit: `preservation`, `omission`, `abstraction`,
`reinterpretation`, `addition`. An addition is sub-classified:
`other-source | inference | counterfactual | unsupported`. Units are
clause-level items from the Livy-side extraction (actors, resources, actions,
outcomes, explanations), so denominators are explicit and auditable.

## Pipeline

1. `acquire_*` — download sources with recorded provenance.
2. `segment_corpus.py` — stable-ID passages.
3. Case-study extraction (pilot: expert manual extraction recorded as JSONL
   against `schema/`; scale-up: LLM-assisted extraction with the same schema and
   mandatory `source_passage` verification — see initial report §7).
4. `build_db.py` — SQLite with referential integrity.
5. `validate.py` + `tests/` — malformed records, dangling references, citation
   checks (every quoted `source_passage` must be a substring of the cited
   segment, modulo whitespace), unsupported-number detection.
6. Analysis + graphs + reports.
