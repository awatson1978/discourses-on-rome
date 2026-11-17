# Dashboard

`index.html` is a **fully self-contained** visualization of the project's
datasets: no CDN, no build step, no network requests. All data is embedded at
generation time. Open it in any browser, or serve it with GitHub Pages
(Settings → Pages → deploy from `main`, then visit
`/discourses-on-rome/dashboard/`).

Regenerate after any data change:

```bash
python3 scripts/build_dashboard.py
```

## Panels and their data sources

| Panel | Source | What it shows |
|---|---|---|
| Headline stats | all extraction files | corpus and dataset sizes |
| The Loss Gradient | `reports/selection_analysis.json` | % of Livy information units omitted/abstracted per dimension (pilot, n=44) |
| Transformation Distribution | same | omission / addition / preservation / abstraction / reinterpretation shares |
| Event Series strip | `extractions/livy_events.jsonl` | all 383 domestic-political events in Livy I–X, by book and chapter, colored by resolution channel |
| Event Types | same | frequency of the 18 event types |
| Trigger × Channel | same | how conflicts over food/land/debt/honors/rights resolved |
| Claim Test T1 | `reports/claim_tests.json` | roba-vs-onori: extraordinary-resolution share by conflict domain |
| Selection Bias T3 + Anchors | `reports/claim_tests.json`, `extractions/chapter_map.jsonl` | cited-vs-uncited violence share; chapter→Livy anchor quality |
| Causal Model | `extractions/claims.jsonl`, `schema/ontology.json` | Machiavelli's propositions as a directed graph over the recovered ontology; hover any edge for the claim text |
| Persepolis transfers | `extractions/persepolis_transfers.jsonl` | every parsed PF commodity transfer by Darius I regnal year (log quantity, commodity color, marris ring); Ionian Revolt marked at year 23 ≈ 499 BCE |
| Persepolis coverage | same + `reports/persepolis_analysis.json` | the honesty panel: 68 of 2,087 tablets transliterated (3.3%), commodity mix of that subset |
| Persepolis dispersion (H5) | `reports/persepolis_analysis.json` | CV of grain quantities per regnal year; Ionian window in red; explicitly inconclusive |

## Honesty notes

Everything rendered here inherits the dataset's caveats (see
`RESEARCH_METHOD.md` and `reports/full_corpus_analysis.md` §Methods): pilot
denominators are small and non-random; the event series is single-coded from an
1857 translation; causal edges are **historically situated claims, never
established facts** — the graph legend says so and means it.
