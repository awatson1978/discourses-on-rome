# Graph Report - /Volumes/MobileDev/Claude/discourses-on-rome  (2026-11-16)

## Corpus Check
- 172 files · ~407,290 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 366 nodes · 463 edges · 30 communities (28 shown, 2 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.89)
- Token cost: 144,889 input · 24,671 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Causal Claim Schema|Causal Claim Schema]]
- [[_COMMUNITY_Dataset Hypothesis Schema|Dataset Hypothesis Schema]]
- [[_COMMUNITY_Case Studies & Dataset Inventory|Case Studies & Dataset Inventory]]
- [[_COMMUNITY_Alignment Schema|Alignment Schema]]
- [[_COMMUNITY_Validation & Testing|Validation & Testing]]
- [[_COMMUNITY_Discourses Text & Themes|Discourses Text & Themes]]
- [[_COMMUNITY_Agrarian Law & Land Politics|Agrarian Law & Land Politics]]
- [[_COMMUNITY_Research Method & Corpus|Research Method & Corpus]]
- [[_COMMUNITY_Schema Field Fragments|Schema Field Fragments]]
- [[_COMMUNITY_Observation Field Lists|Observation Field Lists]]
- [[_COMMUNITY_Corpus Segmentation|Corpus Segmentation]]
- [[_COMMUNITY_Observation Schema|Observation Schema]]
- [[_COMMUNITY_Chapter Mapping|Chapter Mapping]]
- [[_COMMUNITY_Reference Field Schema|Reference Field Schema]]
- [[_COMMUNITY_Observation ID Schema|Observation ID Schema]]
- [[_COMMUNITY_Provenance Field Schema|Provenance Field Schema]]
- [[_COMMUNITY_Source Passage Schema|Source Passage Schema]]
- [[_COMMUNITY_Wikisource Acquisition|Wikisource Acquisition]]
- [[_COMMUNITY_GraphML Export|GraphML Export]]
- [[_COMMUNITY_Claim Testing|Claim Testing]]
- [[_COMMUNITY_Admin Actions Field|Admin Actions Field]]
- [[_COMMUNITY_Mechanism Field Schema|Mechanism Field Schema]]
- [[_COMMUNITY_Date Uncertainty Field|Date Uncertainty Field]]
- [[_COMMUNITY_Outcomes Field|Outcomes Field]]
- [[_COMMUNITY_Political Actions Field|Political Actions Field]]
- [[_COMMUNITY_Population Groups Field|Population Groups Field]]
- [[_COMMUNITY_Resources Field|Resources Field]]
- [[_COMMUNITY_Database Build|Database Build]]
- [[_COMMUNITY_Event Series Merge|Event Series Merge]]

## God Nodes (most connected - your core abstractions)
1. `Case B - Spurius Maelius and the Roman Famine` - 18 edges
2. `Case A - Coriolanus and the Grain Crisis` - 15 edges
3. `Case C - The Agrarian Laws and Class Conflict` - 13 edges
4. `Initial Research Report (Pilot Phase)` - 11 edges
5. `Full-Corpus Analysis: Livy I-X Event Series vs Machiavelli's Propositions` - 10 edges
6. `Discorsi sopra la prima Deca di Tito Livio` - 10 edges
7. `Ab Urbe Condita (Books I-X)` - 10 edges
8. `Book I` - 10 edges
9. `Discourses on Rome (Project README)` - 9 edges
10. `Research Method` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Chancery-Experience Hypothesis (Working-Hypothesis Category 2)` --semantically_similar_to--> `Florentine Fingerprint`  [INFERRED] [semantically similar]
  reports/initial_report.md → README.md
- `Discourses on Rome (Project README)` --references--> `Initial Research Report (Pilot Phase)`  [EXTRACTED]
  README.md → reports/initial_report.md
- `Research Method` --references--> `Spillan Translation of Livy (1857)`  [EXTRACTED]
  RESEARCH_METHOD.md → SOURCES.md
- `Research Method` --references--> `Thomson Translation of the Discorsi (1883)`  [EXTRACTED]
  RESEARCH_METHOD.md → SOURCES.md
- `Case A - Coriolanus and the Grain Crisis` --cites--> `Ab Urbe Condita (Books I-X)`  [EXTRACTED]
  reports/case_A_coriolanus.md → SOURCES.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Pilot Phase Case Studies and Synthesis** — reports_case_a_coriolanus, reports_case_b_maelius, reports_case_c_agrarian, reports_initial_report [EXTRACTED 1.00]
- **Grain as Political Leverage Pattern** — reports_case_a_coriolanus_coriolanus, reports_case_b_maelius_spurius_maelius, reports_case_b_maelius_praefectura_annonae, reports_case_a_coriolanus_ds_annona_price_series [INFERRED 0.85]
- **Florentine Record-Producing Instruments Behind Machiavelli's Typology** — reports_case_a_coriolanus_otto_di_guardia, reports_case_b_maelius_monte_delle_doti, reports_case_b_maelius_public_vs_private_reputation, reports_initial_report_chancery_experience_hypothesis [INFERRED 0.85]

## Communities (30 total, 2 thin omitted)

### Community 0 - "Causal Claim Schema"
Cohesion: 0.04
Nodes (47): additionalProperties, enum, items, minItems, type, pattern, type, enum (+39 more)

### Community 1 - "Dataset Hypothesis Schema"
Cohesion: 0.05
Nodes (46): additionalProperties, description, items, type, pattern, type, description, enum (+38 more)

### Community 2 - "Case Studies & Dataset Inventory"
Cohesion: 0.09
Nodes (39): Dataset Levels A/B/C, Florentine Fingerprint, Case A - Coriolanus and the Grain Crisis, Coriolanus, ds:annona-price-series (B), ds:import-procurement-log (B), ds:trial-event-log (B), ds:war-mobilization-ledger (C) (+31 more)

### Community 3 - "Alignment Schema"
Cohesion: 0.05
Nodes (36): description, enum, additionalProperties, pattern, type, description, type, enum (+28 more)

### Community 4 - "Validation & Testing"
Cohesion: 0.08
Nodes (12): load_jsonl(), load_segments(), main(), norm(), load(), Automated validation. Run: python3 -m pytest tests/ -q  (or python3 tests/test_v, Full-corpus event series (scale-up phase). Skipped until merged file exists., TestCorpus (+4 more)

### Community 5 - "Discourses Text & Themes"
Cohesion: 0.08
Nodes (28): Discourses on the First Decade of Titus Livius (Thomson translation, 1883), Accusations and Calumnies, The Agrarian Law, Artillery in Modern Warfare, Book I, Book II, Book III, Conspiracies (+20 more)

### Community 6 - "Agrarian Law & Land Politics"
Cohesion: 0.18
Nodes (20): ds:unrest-event-series (B), Case C - The Agrarian Laws and Class Conflict, Antium Colony Enrollment (467 BCE), Distance-Decay Claim, ds:colonist-enrollment-register (B), ds:land-tenure-register (C), The Gracchi, Agrarian Law (Legge Agraria) (+12 more)

### Community 7 - "Research Method & Corpus"
Cohesion: 0.22
Nodes (15): Discourses on Rome (Project README), Loss Gradient, Discorsi as Lossy Compression of Livy, Research Method, Evidence Classes (Five Strata), Transformation Taxonomy, Corpus Sources and Provenance, Ab Urbe Condita (Books I-X) (+7 more)

### Community 8 - "Schema Field Fragments"
Cohesion: 0.14
Nodes (14): enum, description, type, enum, type, type, properties, confidence (+6 more)

### Community 9 - "Observation Field Lists"
Cohesion: 0.25
Nodes (8): items, type, items, type, type, actors, institutions, items

### Community 10 - "Corpus Segmentation"
Cohesion: 0.43
Nodes (6): _clean(), _disc_en_rec(), segment_discorsi_en(), segment_discorsi_it(), segment_livy(), write_jsonl()

### Community 11 - "Observation Schema"
Cohesion: 0.29
Nodes (6): additionalProperties, $id, required, $schema, title, type

### Community 12 - "Chapter Mapping"
Cohesion: 0.70
Nodes (4): load(), main(), norm_word(), words()

### Community 13 - "Reference Field Schema"
Cohesion: 0.50
Nodes (4): description, pattern, type, discorsi_reference

### Community 14 - "Observation ID Schema"
Cohesion: 0.50
Nodes (4): description, pattern, type, observation_id

### Community 15 - "Provenance Field Schema"
Cohesion: 0.50
Nodes (4): provenance, description, minItems, type

### Community 16 - "Source Passage Schema"
Cohesion: 0.50
Nodes (4): source_passage, description, minLength, type

### Community 17 - "Wikisource Acquisition"
Cohesion: 0.83
Nodes (3): api_get(), fetch_page(), main()

### Community 18 - "GraphML Export"
Cohesion: 0.83
Nodes (3): esc(), main(), write_graphml()

### Community 19 - "Claim Testing"
Cohesion: 0.83
Nodes (3): load(), main(), pct()

### Community 20 - "Admin Actions Field"
Cohesion: 0.67
Nodes (3): items, type, administrative_actions

### Community 21 - "Mechanism Field Schema"
Cohesion: 0.67
Nodes (3): description, type, claimed_mechanism

### Community 22 - "Date Uncertainty Field"
Cohesion: 0.67
Nodes (3): description, type, date_uncertainty

### Community 23 - "Outcomes Field"
Cohesion: 0.67
Nodes (3): items, type, outcomes

### Community 24 - "Political Actions Field"
Cohesion: 0.67
Nodes (3): items, type, political_actions

### Community 25 - "Population Groups Field"
Cohesion: 0.67
Nodes (3): items, type, population_groups

### Community 26 - "Resources Field"
Cohesion: 0.67
Nodes (3): resources, items, type

## Knowledge Gaps
- **140 isolated node(s):** `$schema`, `$id`, `title`, `type`, `required` (+135 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `properties` connect `Schema Field Fragments` to `Observation Field Lists`, `Observation Schema`, `Reference Field Schema`, `Observation ID Schema`, `Provenance Field Schema`, `Source Passage Schema`, `Admin Actions Field`, `Mechanism Field Schema`, `Date Uncertainty Field`, `Outcomes Field`, `Political Actions Field`, `Population Groups Field`, `Resources Field`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **What connects `$schema`, `$id`, `title` to the rest of the system?**
  _144 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Causal Claim Schema` be split into smaller, more focused modules?**
  _Cohesion score 0.044326241134751775 - nodes in this community are weakly interconnected._
- **Should `Dataset Hypothesis Schema` be split into smaller, more focused modules?**
  _Cohesion score 0.045328399629972246 - nodes in this community are weakly interconnected._
- **Should `Case Studies & Dataset Inventory` be split into smaller, more focused modules?**
  _Cohesion score 0.08502024291497975 - nodes in this community are weakly interconnected._
- **Should `Alignment Schema` be split into smaller, more focused modules?**
  _Cohesion score 0.05405405405405406 - nodes in this community are weakly interconnected._
- **Should `Validation & Testing` be split into smaller, more focused modules?**
  _Cohesion score 0.07765151515151515 - nodes in this community are weakly interconnected._