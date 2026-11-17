# Moving the agents to GitHub Copilot (VS Code) in the office

Goal: the agents that pass their tests in **Claude Code** produce equivalent, checklist-passing output in **GitHub Copilot in VS Code**. Identical wording is not expected — the model, tools and network differ. Judge the office run against the same golden-test checklist and the saved Claude Code baseline.

## 1. Before moving (in this repo)
- [ ] Each agent passes its golden tests in Claude Code (`tests/<agent>/README.md`).
- [ ] The best Claude Code report per agent is saved as a baseline in `tests/<agent>/results.md` (date, model, depth, tools used).
- [ ] Each agent file in `.github/agents/` is self-contained (core rules, tool-role mapping, runtime notes) — it must not depend on Claude Code files.
- [ ] Confirm with your organisation that custom agents may be added to work repositories, and that these files may be moved from a personal repository. Remove anything personal or test-only you do not want to carry over.

## 2. What to copy to the office repository
| Copy | Purpose |
|---|---|
| `.github/agents/*.agent.md` | **Required.** Copilot loads these directly. |
| `AGENTS.md` | Optional shared rules (agents are self-contained). |
| `docs/` (template, changelogs, this guide) and `tests/` (golden tests, baselines) | Process, history and acceptance tests. |

| Do **not** copy | Why |
|---|---|
| `.claude/agents/`, `CLAUDE.md` | Claude Code only. Copying `.claude/agents/` may make VS Code show a second entry with the same agent name. |
| `.cline/`, `archive/` | Legacy runtime and old versions. |

## 3. Office setup checklist
| # | Check | How |
|---|---|---|
| 1 | VS Code and the GitHub Copilot Chat extension are up to date (custom-agent features need recent versions; e.g. handoffs need VS Code 1.106+). | Help → Check for Updates; Extensions view. |
| 2 | Your Copilot plan and organisation policy allow agent mode and custom agents. | Ask your Copilot / IT administrator. |
| 3 | A strong model is available in Copilot's model picker and is the one you will use for testing. Optionally pin it with `model:` in the agent frontmatter. | Results vary by model; test with the production model. |
| 4 | **Page fetch works through the corporate network.** The agents need `nvd.nist.gov`, `services.nvd.nist.gov`, `cveawg.mitre.org`, `api.first.org`, `www.cve.org`, `cisa.gov`, `osv.dev`, `github.com`, `raw.githubusercontent.com` and vendor advisory sites. | In Copilot Chat ask it to fetch `https://nvd.nist.gov/vuln/detail/CVE-2021-44228` and confirm the page content is returned. If blocked, ask IT to allow these domains. |
| 5 | **Web search (optional).** A built-in Copilot web-search tool was not confirmed. Options: (a) a Tavily MCP server, **only if security approves external MCP servers and APIs**, configured in `.vscode/mcp.json` with the server named `tavily` and the API key supplied through an `${input:…}` prompt or secret — never written into the file; (b) no search — the agents switch to their no-search mode (fewer sources). | Ask your security team about MCP servers and external APIs. |
| 6 | **The agent loads.** | Agent dropdown lists the agent; right-click in Chat → **Diagnostics** shows no errors for it; the first reply line is the preflight marker (e.g. `vm-triage v5.0 \| preflight`) and names the page-fetch and web-search tools. |
| 7 | **Tool approvals.** | Approve page fetches. Reject anything that edits files or runs commands. Change auto-approve settings only if policy allows. |
| 8 | **Re-run the golden tests** with the office model and compare with the baseline. | Record runtime, model, depth, tools and pass/fail in `tests/<agent>/results.md`. |
| 9 | **Data handling.** Agents that see internal data (soc-analyst, vulnerability-hunt) may only receive what your organisation's data policy allows for its enterprise Copilot. Golden tests stay synthetic. | Check your data classification policy. |

## 4. Differences you may see, and what to do
| You see | Likely cause | Action |
|---|---|---|
| Fewer sources, IOCs or detections | No web search in the office | Get a search tool approved, or accept no-search mode (it is reported in Section 25). |
| Core sources `FAILED` | Proxy / firewall, or JSON endpoints unreadable | Ask IT to allow the domains; the agent's fallbacks (NVD page, secondary EPSS) still run. |
| Report stops before the JSON block | Model output limit | Use `standard` depth, or ask "continue from Section N". |
| Different wording, same facts | Different model | Expected. Pass/fail is decided by the checklist. |
| Two entries with the same agent name | `.claude/agents/` was copied | Delete `.claude/agents/` from the office repo. |
| Agent missing from the dropdown | File location, frontmatter error or policy | Check the file is in `.github/agents/` of the opened workspace folder, and see **Diagnostics**. |

## 5. Per-agent notes
| Agent | Needs in the office |
|---|---|
| `vm-triage` | Page fetch (required); web search (optional). Public data only. |
| `soc-analyst` | Read access to supplied alerts/logs; optional read-only SIEM/EDR MCP tools added to `tools:`. Internal data → data policy applies. |
| `vulnerability-hunt` | Inventory/SBOM/scanner exports or read-only inventory tools; ticket creation only if a ticketing MCP tool is approved and `ticketing: create` is requested. |
| `threat-intel-analyst` | Page fetch; web search recommended. |
