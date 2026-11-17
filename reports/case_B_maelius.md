# Case B — Spurius Maelius and the Roman Famine

**Texts:** *Discorsi* III.28 (`disc:it:3:28`, `disc:en:3:28`) ↔ Livy IV.12–16
(`livy:la:4:12` … `livy:la:4:16`).
**Machine-readable records:** obs:d3c28-\*, obs:l4c12-\* … obs:l4c16-\*; aln:b-\*.
**Date:** traditionally 440–439 BCE; historicity debated in modern scholarship.

## 1. The asymmetry

This is the pilot's extreme case of operational information loss. Livy IV.12–16
is the densest administrative narrative in the early decades; Machiavelli's
III.28 opens with a 60-word summary and then leaves the episode entirely for
theory. What Livy records and Machiavelli deletes:

| Livy's operational record | Fate in Disc. III.28 |
|---|---|
| Famine with **two transmitted causes**, left unresolved ("nam utrumque traditur") | "aggravata dalla fame" — cause and source-criticism gone |
| Creation of a **new magistracy**: L. Minucius *praefectus annonae*, corroborated by the *libri lintei* | absent |
| **Scarcity administration**: compulsory declaration of private grain stocks; forced sale of surplus above one month's need; cuts to slaves' daily rations; prosecution of dealers; the audit "revealed rather than relieved" the shortage; plebeians drown themselves in the Tiber | "non bastando le provisioni publiche" — five words |
| Maelius's **procurement network**: Etruscan grain, private money, agency of *hospites* and *clientes*; Livy's conjecture ("credo") that private buying crowded out public procurement | "fare provisione privatamente di frumento" |
| **Intelligence channel**: the same personnel worked both grain operations; Minucius reports weapons stockpiles, house assemblies, bribed tribunes | absent |
| **Legal machinery**: consuls bound by the *provocatio* laws; dictator needed as a man "freed from the chains of the laws"; named chain of command (Quinctius → Cincinnatus → Ahala) | "gli creò uno Dittatore addosso" — rationale replaced (see §3) |
| Summons, refusal, killing; dictator's legal theory: *iure caesum* **even if innocent**, for refusing the summons | "fecelo morire" |
| **Fiscal liquidation**: goods sold by quaestors into the treasury; house razed (Aequimelium); confiscated grain resold to the plebs at **1 as per modius** — the pilot corpus's one hard price | absent |
| **Constitutional aftershock**: tribunician agitation; military tribunes with consular power elected instead of consuls | absent |
| **Documentary criticism**: *libri lintei* cited; the "11th tribune" tradition refuted against a false statue inscription | absent |

22 aligned units: 8 omissions, 4 abstractions, 2 reinterpretations,
4 preservations, 1 addition. Material-resource and administrative-action
dimensions lose essentially everything.

## 2. What is preserved is preserved verbatim

"uno Spurio Melio, essendo assai ricco, **secondo quegli tempi**" tracks Livy's
"Sp. Maelius... **ut illis temporibus** praedives" down to the relativizing
aside (`aln:b-maelius-wealth`). Machiavelli worked close to the text; the
deletions are editorial choices, not distance from the source.

## 3. The two reinterpretations

1. **The threat** (`aln:b-threat-reframing`). In Livy the Senate reacts to
   intelligence of an armed conspiracy ("non dubia regni consilia"). In
   Machiavelli the Senate acts *before* any plot matures — against the
   potential inherent in liberality itself ("per opprimerla avanti che la
   pigliasse più forze"). Livy's police action becomes a doctrine of
   preventive repression of private reputation.
2. **The dictator's rationale** (`aln:b-provocatio-constraint`). Livy grounds
   the dictatorship in a legal constraint (ordinary magistrates bound by
   appeal protections). Machiavelli grounds it in an epistemic one (the people
   "accecato da una spezie di falso bene" cannot judge). Same institution,
   different theory of why republics need it.

Both moves serve the chapter's thesis: *sotto una opera pia si nasconde uno
principio di tirannide* — the pious work itself, not the weapons cache, is the
danger.

## 4. The addition: a Florentine patronage inventory

The chapter's theoretical core — reputation through public vs private ways —
has no Livian basis (`aln:b-reputation-theory`). Its typology of private
favors is concrete: lending money, dowering daughters, defending men from the
magistrates. Each item corresponds to a documented Florentine instrument
(loans, the Monte delle doti, influence with the Otto), i.e. to record-producing
institutions of Machiavelli's own world. Where his Roman source offered him an
administrative apparatus (Minucius's grain census) he cut it; what he added
runs on Florentine administrative categories. This is the pilot's strongest
evidence for working-hypothesis category 2 (chancery experience shaping the
data model) — and simultaneously evidence **against** the naive version of the
hypothesis, since administrative experience did not make him *retain*
administrative detail (see `ds:war-mobilization-ledger` for the Case A
parallel).

## 5. Phase V datasets anchored here

- `ds:grain-stock-census` (B) — the Minucian declarations: declarant, stock,
  monthly-need threshold, forced sale. Structure is Livy's own; values lost;
  fifth-century historicity doubted (possible retrojection of late-republican
  annona practice — flagged in the record).
- `ds:distribution-recipient-rolls` (C) — who received Maelian grain; needed to
  test largesse→partisans; could not have existed in 440 BCE, did exist in
  Renaissance Florence (Abbondanza records).
- `ds:confiscation-liquidation-records` (B) — quaestorian sale, proceeds to the
  treasury, memorial sanctions; Livy here *reads physical records* (toponym,
  inscription) and says so.
- `ds:annona-price-series` (B) — anchored by the 1 as/modius datum.
- `ds:magistrate-fasti` (A) — the *libri lintei* citation inside this very
  episode is the pilot's only directly attested ancient dataset.
