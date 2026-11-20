# hunt-01 — synthetic npm-worm hunt (soc-analyst hunt mode)

All data is invented (documentation IP 203.0.113.45, `.example` domains, `example-org`). Files:
- `sources.md`, `context.md` — inputs for the **plan** stage.
- `hunt-plan.json` — a fixed plan, so the **analysis** stage can be tested without running a SIEM.
- `Q1.csv` (stacked process pairs; 2 rare hosts), `Q2.csv` and `Q3.csv` (header only = no results), `Q4.csv` (2,500 raw rows = too large).
Expected results: `tests/soc-analyst/expected-results.md`, tests H1–H7.
