# Case A — Coriolanus and the Grain Crisis

**Texts:** *Discorsi* I.7 (`disc:it:1:7`, `disc:en:1:7`) ↔ Livy II.34–35
(`livy:la:2:34`, `livy:la:2:35`).
**Machine-readable records:** `extractions/observations.jsonl` (obs:d1c7-\*, obs:l2c34-\*, obs:l2c35-\*), `extractions/alignments.jsonl` (aln:a-\*).
**Date:** traditionally 492–491 BCE (Varronian); the episode is semi-legendary.

## 1. What each text contains

Livy narrates an administrative crisis with political consequences; Machiavelli
narrates a political lesson with an administrative occasion. Livy's account is,
in modern terms, a supply-chain report wrapped around a constitutional
confrontation:

| Dimension | Livy II.34–35 | Machiavelli, Disc. I.7 | Transformation |
|---|---|---|---|
| Historical event | Scarcity then siege-grade famine, caused by fields untilled during the plebeian secession | "penuria grande di vettovaglie", cause unstated, "come avviene" (as happens) | Preservation of event; **omission of cause**; normalization of a specific shock into a recurring condition |
| Actors | Named consuls (T. Geganius, P. Minucius; M. Minucius, A. Sempronius), named tribune target (Sicinius), Aristodemus of Cumae | "il Senato", "i Tribuni"; only Coriolanus named | **Abstraction**: persons → offices |
| Material resources | Three procurement routes (Etruria/Ostia; Volscian coast to Cumae; Sicily); ships seized at Cumae under a dynastic claim; purchase refused in the Pomptine; Etruscan grain down the Tiber "sustained the plebs" | "mandato per grani in Sicilia" | **Compression**: a route-by-outcome procurement log reduced to one row |
| Administrative actions | Senate debates the **price** of state grain (*quanti plebi daretur*); colonies sent to Velitrae and Norba | Proposal to **withhold distribution** ("non gli distribuendo il frumento"); colonies absent | **Reinterpretation**: price-setting becomes binary starvation leverage; **omission** of the territorial response |
| Political outcome | Near-lynching → tribunician trial date → client-network counter-mobilization → condemnation in absentia → exile → Volscian war planning | Near-lynching → tribunician citation. Story ends there. | **Preservation** of the pivot, near-verbatim; **omission** of the sequel |
| Causal explanation | Micro-psychology: rage subsided because "each man saw himself made judge, master of the life and death of his enemy"; plus Livy's counterfactual that the patres could have traded grain-price relief for abolition of the tribunate | General law: republics must give legally ordained vents (*sfoghi*) to the humors (*umori*) of the collectivity; four-case comparison added (Rome, Clusium, Valori 1498, Soderini 1512) plus the faction-cascade counterfactual | **Reinterpretation** (one-off psychology → institutional design principle) + **additions** (two Florentine cases from direct experience; one counterfactual) |

## 2. The strategic boundary of the compression

Machiavelli ends the story at the moment it best serves his thesis: the trial
summons that converted rage into procedure. Livy's sequel — Coriolanus
condemned, exiled, and promptly organizing a Volscian war against Rome —
is omitted (`aln:a-trial-outcome`). Including it would show that the "ordinary
channel" did not neutralize the danger; it displaced it outside the walls.
Likewise omitted is Livy's own counterfactual (`aln:a-livy-counterfactual`)
that the senators could have *bought back the tribunate* with cheap grain — an
aristocratic reading incompatible with Machiavelli's defense of the tribunate
(Disc. I.4). The compression is not random: both cuts protect the proposition.

## 3. The Florentine additions

The chapter's evidentiary engine is a four-case comparison in which the Roman
case is the only one from Livy. Valori (1498) and Soderini (1512) come from
Machiavelli's own professional life — he entered the chancery weeks after
Valori's lynching and served Soderini until the 1512 collapse. The design is
genuinely comparative: channel present (Rome: trial; outcome contained) vs
channel absent (Clusium, Florence ×2: foreign swords invited). The precise
institutional datum "otto giudici" (the Otto di Guardia's eight) is chancery
knowledge, and his claim that eight judges cannot condemn the powerful is an
operational observation about tribunal size — one of the few places where the
implicit data model visibly runs on Florentine administrative detail
(`ds:trial-event-log`).

## 4. Administrative variables needed to understand the dispute (Phase V)

Reconstructed in `extractions/datasets.jsonl`:

- `ds:import-procurement-log` (B) — Livy preserves the narrative shape of one:
  route × agent × outcome × obstacle.
- `ds:annona-price-series` (B) — the Senate's *quanti daretur* debate implies a
  price decision; no value survives for 491.
- `ds:trial-event-log` (B) — accusations of powerful citizens: tribunal
  type/size, verdict, surrounding violence. Feasible on the Florentine side
  from surviving Otto di Guardia registers; narrative-only for early Rome.
- `ds:unrest-event-series` (B) — trigger domain × resolution channel; the
  variable coding comes from Machiavelli's own ordinario/straordinario
  distinction (circularity flagged in the dataset record).
- `ds:war-mobilization-ledger` (C) — documented as a **negative result**: Livy
  II.35 stages exactly the manpower/morale assessment a chancery secretary
  wrote for a living, and Machiavelli drops it entirely.

## 5. Verdict on the chapter as compression

Of 18 aligned units: 7 omissions, 3 abstractions, 1 reinterpretation at the
causal core, 3 preservations (the pivot scene nearly verbatim), 4 additions
(2 other-source from personal experience, 1 other-source from Livy V, 1
counterfactual). Machiavelli keeps the institutional skeleton and the causal
pivot; he discards logistics, prices, names, patronage operations, and the
inconvenient sequel; he substitutes a general mechanism for Livy's local
psychology; and he supplies his own comparative cases. **The chapter is not a
summary of Livy; it is a re-estimation of Livy's episode under a different
model, fitted jointly to Roman and Florentine data.**
