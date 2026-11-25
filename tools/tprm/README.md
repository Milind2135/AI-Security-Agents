# tools/tprm — helper for third-party-risk-analyst

One script, four commands. Needs Python 3.9+ and `openpyxl` (`python -m pip install -r tools/tprm/requirements.txt`). Old `.xls` files also need `xlrd`, or save them as `.xlsx`.

| Command | What it does |
|---|---|
| `python tools/tprm/tprm.py convert <file.xlsx/.xlsm/.xls/.csv>` | Writes `<file>.converted.md` that the agent can read: one table per sheet, hidden sheets and rows marked. **Macros are never run** — the file is read as data only. |
| `python tools/tprm/tprm.py questionnaire <saved plan.md>` | Vendor questionnaire (`.xlsx`) from the plan's scoping and the question bank: Instructions, Evidence, High-level, one tab per in-scope area, Glossary. Vendor columns only, with a Response drop-down. |
| `python tools/tprm/tprm.py workbook <saved result.md or decision.md>` | Internal assessment workbook: Summary, Profile and tier, Tier history, Scoping, Evidence, Documents, Screening, results per area with assessor and QA columns, Findings, Actions, Conditions and exceptions, Specialist inputs, Contract check, Regulatory checks, Fourth parties, Decision log. |
| `python tools/tprm/tprm.py register <saved portfolio.md or docs/vendors>` | Vendor register: from a portfolio message, or from the newest saved record of every vendor folder. |

Options: `--out <path>`; `--bank` / `--extra` for a different question bank (company questions: `docs/vendors/_policy/extra-questions.csv`, same columns, IDs starting `X-`).

Saved messages must contain the agent's whole message, from its first line to `Validation: NOT RUN (chat mode).` — the tool reads the JSON block in it. In Claude Code the main session runs these commands for you (see `CLAUDE.md`).
