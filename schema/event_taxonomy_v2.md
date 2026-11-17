# Livy Event Taxonomy v2 (specification)

Status: **specified, not yet applied**. The 383-event series
(`extractions/livy_events.jsonl`) was coded under v1. v2 incorporates the gaps
the per-book coders flagged during the v1 pass. Re-coding to v2 is a planned
batch job; until then, analyses must use v1 categories.

## Changes from v1

### New event types

| Type | Why | Flagged by |
|---|---|---|
| `resource-distribution` | Non-conflictual distributions of movables or land: war booty divisions, viritane land grants, confiscated-goods distributions. v1 forced these into `grain-dispute` (Veii booty, 5:20, coder note) or left them uncoded (viritane grants at 8:11, coder note). Distributions are precisely the administrative events this project cares about; they need their own type. | Book 5, Book 8 coders |
| `corporate-secession` | Collective withdrawal by a non-plebeian corporate group (the flute-players' guild walkout, 9:30, coded `secession` at low confidence in v1). Distinct from constitutional plebeian secession. | Book 9 coder |
| `honorific-award` | Public honors as a governance instrument (Minucius's gilded ox, triumph disputes). v1 captured these only inside `notes`. Relevant to the ont:reputation-public variable. | pilot Case B |

### Amended definitions

- `dictator-appointed`: v2 adds a required subfield `dictator_purpose`
  (military | repression | elections | ceremonial-nail | other) — the Book 6/7
  coders found purpose heterogeneity that the bare type hides (12 of the 50
  v1 dictatorships were electoral/ceremonial, not emergency).
- `secession`: restricted to plebeian constitutional secession; corporate
  walkouts go to `corporate-secession`.
- `grain-dispute`: restricted to grain; other movables go to
  `resource-distribution` with a `contested: true/false` flag.

### New optional fields (all types)

- `contested` (bool): was the event itself a site of conflict?
- `quantities` (array): any numerical values the source gives (price, ration,
  acreage, headcount), each as `{"value": "...", "unit": "...", "quote": "..."}`
  with the quote validator-checked. Motivated by the pilot finding that hard
  numbers are the rarest and most valuable preserved data.

## Migration plan

1. Apply v2 automatically where deterministic (dictator_purpose derivable from
   notes in ~80% of cases; script pass).
2. Re-code flagged borderline events only (the ~15 events coder notes marked
   as approximations), not the full series.
3. Version field `taxonomy: "v1"|"v2"` on every event record; mixed-version
   analysis forbidden by validator rule.
