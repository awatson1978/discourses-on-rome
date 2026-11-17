# Case C — The Agrarian Laws and Class Conflict

**Texts:** *Discorsi* I.37 (`disc:it:1:37`, `disc:en:1:37`) ↔ Livy II.41
(Spurius Cassius, 486 BCE) and III.1 (Antium colony, 467 BCE), with the
Licinian-Sextian rogations (Livy VI.35–42) and the Gracchan laws (outside
Livy I–X) as the fused later layers.
**Machine-readable records:** obs:d1c37-\*, obs:l2c41-cassius, obs:l3c1-antium; aln:c-\*.

## 1. The master transformation: synthesis into a single "law"

Machiavelli writes of **one** *legge agraria* with two fixed clauses — a
holding cap "più che tanti iugeri" and division of conquered land — that
periodically "awakens" across 350+ years until the Gracchi reactivate it and
the Republic dies of it (`aln:c-single-law-fusion`). Livy's record is a
*series* of distinct measures: Cassius's bill of 486 (specific Hernican land,
Latin allies included, restitution of occupied *ager publicus* — **no holding
cap**), decades of tribunician bills, the Licinian cap of 367, the Gracchan
laws of 133–121. The fusion is what makes the disease metaphor (*morbo*)
possible: one pathogen, long latency, fatal relapse. It is also what a modern
analyst would call constructing a **longitudinal variable** out of discrete
statutes — an act of data modeling, not of narration.

Notably, Machiavelli does not reproduce the 500-iugera figure available in the
tradition; his "tanti iugeri" (so-many iugera) is a schema with the value left
unfilled — the clearest instance in the pilot of his retaining a variable while
discarding its measurement.

## 2. The suppressed founder episode

Livy's Cassius narrative (II.41) is omitted wholesale (`aln:c-cassius-omitted`),
and it contains the datum most awkward for I.37's frame: **the plebs
themselves** rejected Cassius's largesse as "nothing less than payment for
kingship" (*mercedem regni*) and acquiesced in his execution. Early-republican
agrarian politics was not a clean nobles-vs-plebs property fight; suspicion of
the *proposer* could trump appetite for the *proposal*. The omission
streamlines the class-conflict model. (Livy also preserves two variant trial
traditions and argues for one — "idque propius fidem est" — another instance
of his documentary layer, invisible in the Discorsi.)

## 3. What is preserved and what is honestly flagged

- Livy's programmatic sentence — first promulgation, "never afterwards
  agitated without the greatest upheavals" — survives nearly intact as "mai
  non si parlò di questa legge in Roma, che quella città non andasse
  sottosopra" (`aln:c-perpetual-turmoil`).
- The **Antium enrollment datum** is the pilot's unique case of Machiavelli
  explicitly citing an administrative record as evidence: he calls Livy's
  remark that few gave their names a "termine notabile" (`aln:c-antium-enrollment`).
  He drops the commission's names and the Volscian back-fill, and — decisively —
  replaces Livy's mechanism (*fastidium copia*, satiety from abundance) with
  his own distance-preference reading (`aln:c-antium-explanation`), which feeds
  his distance-decay explanation of the law's dormancy (claim:d1c37-distance-decay).
  Same observation, substituted cause: the cleanest mechanism-swap in the pilot.
- The elite's delaying repertoire (army out, tribune vs tribune, partial
  concession, colony) is a genuine analytic contribution: Machiavelli compiles
  scattered Livian incidents into an explicit tactical menu
  (`aln:c-elite-tactics`) — abstraction in the productive direction.

## 4. The non-Livian half of the argument

Everything after "infino ai Gracchi" — Gracchi, Marius's seven consulships,
Sulla, Caesar vs Pompey, "primo tiranno in Roma" — lies outside Livy I–X
(`aln:c-gracchi-trajectory`; Livy's own books for the period survive only as
periochae). Sources plausibly Plutarch, Sallust, the Appian tradition, Florus.
The chapter's headline causal claim — the agrarian contention **caused** the
destruction of the Republic — is therefore an inference bridging Livian early
material to non-Livian late material (`aln:c-destruction-thesis`), buttressed
by an explicit counterfactual (the law also *delayed* servitude by braking
noble ambition, `aln:c-retardation-counterfactual`). Machiavelli is here
closest to a modern comparative-historical analyst: event-series construction,
mechanism attribution, counterfactual control — and furthest from his cited
source.

## 5. Phase V datasets anchored here

- `ds:land-tenure-register` (C) — enforcement of any iugera cap presupposes a
  possessor-by-area register; none attested until the Gracchan commission's
  *termini* (3 surviving boundary stones). Machiavelli's implicit data model
  exceeds the period's attested administrative capacity.
- `ds:colonist-enrollment-register` (B) — *nomina dare* before named triumvirs
  with a monitorable quota: a register by definition, engaged by both authors.
  His distance-decay claim is testable in principle against enrollment rate ×
  colony distance — one of the few immediately operationalizable Machiavellian
  propositions.
- `ds:unrest-event-series` (B) — the roba-vs-onori claim
  (claim:d1c37-roba-vs-onori) predicts higher conflict intensity for property
  disputes than honor-access disputes; a full Livy I–X event coding could test
  it without Machiavelli's case selection.
