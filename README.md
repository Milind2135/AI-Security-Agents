# VM Triage Agent — Stabilization Kit

Phase 1 of the AI Security Agents roadmap: make the VM Triage Agent produce a complete, evidence-backed, machine-checkable 26-section report for one CVE.

## Why the previous version was unreliable, and what this kit changes

| Observed failure | Root cause | Fix in this kit |
|---|---|---|
| Sections missing or renamed | Contract enforced only by prose instructions; the model self-audits poorly on long outputs | `validate_report.py` checks all 26 headings, order, titles and per-section status lines; the agent must run it and repair before replying |
| Generic summaries, no IOC values | Agent wrote from search snippets; "hashes are in the advisory" was accepted | Every source carries a retrieval status. IOCs and PUBLISHED rule text must cite a source marked `API`, `FETCHED_FULL` or `FETCHED_PARTIAL`; snippet-sourced IOCs fail validation |
| Scores/EPSS/KEV possibly recalled from memory | LLM fetching and re-typing JSON | `enrich.py` pulls CVE.org, NVD, EPSS and the full KEV feed deterministically; the validator cross-checks the report against it |
| Conflicts not reported | Nothing forced comparison | `enrich.py` computes conflicts (CVSS across CNA/ADP/NVD, KEV feed vs NVD, CWE, record state); validator fails if Section 24 ignores them |
| Agent-written queries looked like published rules | No labeling requirement | `Origin: PUBLISHED | ANALYST-GENERATED`; analyst content requires assumptions, false positives and validation notes |
| Scope creep into priority/exposure | Instruction only | Validator rejects P0–P4 labels and statements about a specific organization's environment |
| Tools silently missing | VS Code ignores unavailable tools listed in `tools:` | Phase 0 preflight: the agent must confirm a page-retrieval tool exists or stop |

## Contents

```
.github/agents/vm-triage.agent.md     Agent definition (VS Code custom agent)
templates/report-template.md          26-section report contract
tools/vm_triage/enrich.py             Deterministic core facts → core.json / core.md
tools/vm_triage/validate_report.py    Contract + fact validator (exit 1 on ERROR)
tests/test_vm_triage.py               32 regression tests (offline)
tests/fixtures/CVE-2099-10001/        SYNTHETIC fixtures + passing sample report
tests/golden-cves.md                  Golden CVE set and acceptance rubric
```
Python 3.9+, standard library only. No `pip install` needed.

## Install into your repo (Windows / PowerShell)

1. Copy the kit contents into `F:\GitHub\ai-security-team` so the folders above sit at the repo root (merge `.github\agents`).
2. Move or rename the old `vm-triage-agent*.agent.md` files out of `.github\agents` so only one triage agent is discovered (VS Code treats any `.md` there as an agent).
3. Check the MCP server name. The agent's `tools:` line uses `tavily/*`. That prefix must equal the server key in your `.vscode/mcp.json` (or user MCP config). If your key is different, edit the line. Remove DuckDuckGo from this agent's workflow; it was rate-limiting.
4. Optional: set an NVD API key for higher rate limits:
   ```powershell
   [Environment]::SetEnvironmentVariable("NVD_API_KEY", "<your key>", "User")
   ```
5. Run the offline tests:
   ```powershell
   python -m unittest discover -s tests -v
   ```
   Expected: `Ran 32 tests ... OK`.
6. Run a live enrichment once, outside the agent, to prove your network/proxy allows the four APIs:
   ```powershell
   python tools/vm_triage/enrich.py CVE-2021-44228 --out reports/CVE-2021-44228
   ```
   Expected: `sources_ok=4/4`. If any source shows FAILED, fix proxy/firewall access before testing the agent; the agent will otherwise report those facts as gaps.
7. In VS Code: right-click in the Chat view → **Diagnostics**, confirm `vm-triage` loads without errors. Select it in the agent picker and type `#` to confirm `web/fetch` and the Tavily tools appear.

## Running the agent

Select **vm-triage** and enter a CVE ID. The agent will:

0. Preflight its tools → 1. run `enrich.py` → 2. discover and **open** sources, logging each in `reports/<CVE>/evidence.md` → 3. extract IOCs/rules into the ledger → 4. write `reports/<CVE>/<CVE>-triage.md` from the template → 5. run `validate_report.py` and repair (max 3 cycles) → 6. reply with a short status.

Approve terminal commands only for `tools/vm_triage/enrich.py` and `tools/vm_triage/validate_report.py`.

Validate several reports at once:
```powershell
python tools/vm_triage/validate_report.py (Get-ChildItem reports\*\CVE-*-triage.md) --summary
```

## Acceptance

Work through `tests/golden-cves.md`. The validator proves structure and provenance labeling; it cannot prove that a cited page actually contains a value. The rubric's manual spot-checks (10 IOCs, every PUBLISHED rule, 5 claims) cover that. Treat the agent as stable when all eight golden CVEs pass twice in a row.

## Known limitations

- **Not live-tested.** The scripts were tested offline with synthetic fixtures shaped like the CVE JSON 5.x, NVD 2.0, EPSS and KEV formats. The build environment could not reach those APIs, so run step 6 before relying on them.
- **Tool names vary.** The npm `tavily-mcp` server exposes `tavily-search` / `tavily-extract`; some builds (for example the Docker image) use underscores. The agent refers to both generically; check the names shown under `#` in chat.
- **Page fetching limits.** `web/fetch` may truncate long pages or miss JavaScript-rendered content. Those sources must be marked `FETCHED_PARTIAL`. Prefer `raw.githubusercontent.com` for rule files.
- **Validator scope.** It checks format, provenance labels, consistency with `core.json` and scope language. It does not open URLs to confirm content.
- **Large KEV feed.** `enrich.py` caches the KEV feed in `tools/vm_triage/.cache/` for 6 hours. Add `.cache/` to `.gitignore`.

## Next (after the golden set passes)

1. Optionally split IOC extraction and detection research into VS Code Agent Skills (check the current VS Code docs for the skills folder location) if the single agent's context gets crowded on large CVEs like Log4Shell.
2. Freeze the report format as the input contract for the Vulnerability Hunt Agent (Section 3, 13, 14, 15, 21 are its primary inputs).
