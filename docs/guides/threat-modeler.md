# threat-modeler: how to use it on a real project

From "the application team sent us their design" to a full threat model. **Part 1** needs no installation and gives you the complete report. **Part 2** is optional and adds an Excel threat register, a Word report and diagram images.

Agent instructions: [`.github/agents/threat-modeler.agent.md`](../../.github/agents/threat-modeler.agent.md) · Intake form for the application team: [`docs/threat-model-intake.md`](../threat-model-intake.md)

> **Data rule:** real designs and code describe your organisation's weaknesses. Use them only with an AI service your organisation has approved. Everything stays under `docs/threat-models/`, which is git-ignored so nothing is pushed. Never paste diagrams into online Mermaid or diagram sites. For practice, use the synthetic systems in [`tests/threat-modeler/fixtures/`](../../tests/threat-modeler/fixtures).

## Part 1: Get the threat model (no installation needed)

You need VS Code with the **Claude Code extension**, and this repository open in VS Code (see [Claude Code setup](../../README.md#claude-code-tested-runtime)). Everything below happens in the VS Code **file explorer** and the **Claude Code chat**. Replace `<system>` with a short name for the application (e.g. `careslot`).

### Step 1: Ask the application team for their material

Send them the intake form [`docs/threat-model-intake.md`](../threat-model-intake.md) (25 questions in 4 tiers). Ask them to:
- answer what they can **in one go**, writing `not available` for anything they don't have; that is a valid answer;
- send any **diagrams, design documents, code, infrastructure-as-code (IaC) and API specs** they have. Code and IaC matter most: without them, controls can only be marked `Claimed` and confidence is `Low`.

### Step 2: Put the files in the project folder

In the VS Code file explorer, create these folders and drag the files in:

| Put | Where |
|---|---|
| Their documents, diagrams, code, IaC, API specs | `docs/threat-models/<system>/input/` |
| Their filled intake form | `docs/threat-models/<system>/intake-answers.md` (next to `input/`, **not** inside it) |

> **Keep the answers file next to `input/`, not inside it.** Everything inside `input/` is read as the system's own material, so answers placed there are mixed in with the team's documents. Always give the answers with `intake:`.

- Don't drop files into the chat box: the agent only reads files saved in the project folder.
- Save Word, Visio and draw.io files as **PDF or PNG** first. The agent reads text files, code, PDF and PNG/JPG.

### Step 3: Start the threat model (Claude Code chat)

```text
Use the threat-modeler subagent. system: docs/threat-models/<system>/input/ intake: docs/threat-models/<system>/intake-answers.md
```

No filled form yet? Leave out the `intake:` part. The agent then asks its 25 questions first; answer in the chat (or give a file path) and Claude passes your answers on.

### Step 4: Review the data-flow diagram

The agent stops and asks you to check its picture of the system. Claude saves this review as `docs/threat-models/<system>/review-round-1.md`.

To see the diagram, **open that file and press `Ctrl+Shift+V`** (Markdown preview). The Claude Code chat itself shows the diagram only as text. If you have done the optional setup (Part 2), Claude also gives you the diagram as **PNG** files.

Check it with the application team:
- Are all components, data stores, users and third parties there?
- Are the flows between them right?
- Read the **mismatches** listed first: places where their documents and their code disagree.

### Step 5: Approve or correct (Claude Code chat)

If the diagram is right:

```text
approve — <your name>, <your role>
```

If something is wrong, say so in plain words, for example:

```text
the notification worker also reads the PostgreSQL database
```

Claude passes your reply to the agent. A correction gives you a new review (`review-round-2.md`, up to 3 rounds); approval starts the full analysis. Take your time on the review: each round re-runs the whole agent.

**Continuing in a new chat?** A new Claude Code session does not remember the old chat, but the saved review does. Use:

```text
Continue the threat-modeler run for <system>: approve — <your name>, <your role>. Use the model JSON from docs/threat-models/<system>/review-round-1.md
```

### Step 6: Read the report

Claude saves the full report as `docs/threat-models/<system>/report-<date>.md`. Open it and press **Ctrl+Shift+V** for a readable view. It contains:
- a summary, readiness and confidence;
- the **intake checklist**: what was provided, what was missing and why it matters;
- the data-flow and deployment diagrams;
- threats (STRIDE), vulnerabilities and validation of the existing controls;
- risks ranked **P1–P4**, with treatment options and residual risk;
- recommended controls with owners, plus ticket drafts;
- assumptions to confirm, and CSV and JSON blocks for further use.

**How gaps appear:** every intake question is marked `Provided`, `Derived` (found in the documents, with `file:line`), `Not provided` (with how the gap weakens the model) or `Not applicable`. Each gap is a **named weakness the team can fix later, not a silent guess**; readiness and confidence are lowered accordingly.

## Part 2 (optional): Excel, Word and diagram images

Want the threat register in **Excel**, the report in **Word**, or the diagrams as **PNG**? Do this setup once. After that, Claude creates these files automatically after every review and report.

### One-time setup

1. In VS Code, open **Terminal → New Terminal**. It opens in your project folder.
2. Run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File tools\threat-modeler-export\setup.ps1
   ```
   It installs only what is missing and prints a summary:

   | Tool | Gives you |
   |---|---|
   | Python packages (openpyxl, Pillow) | Excel threat register, JPG images |
   | pandoc | Word report |
   | Node.js + Mermaid CLI | Diagram images (PNG/JPG/SVG), also embedded in the Word report |

3. **Close VS Code completely and reopen it.** VS Code does not see newly installed programs until it restarts. If the summary asks you to, run the script once more.

Notes:
- Each tool is optional: without pandoc there is no Word file, and without Mermaid CLI there are no images. Excel only needs Python.
- On a managed work laptop, installing software may need IT approval.
- Prefer to install by hand? See the [exporter README](../../tools/threat-modeler-export/README.md).

### What you get

After the report (Step 6), Claude asks permission to run the export, then lists the files in `docs/threat-models/<system>/export-<date>/`:

| File | What it is |
|---|---|
| `threat-model.xlsx` | **Excel threat register**: threats with STRIDE category, risk rating and P1–P4 priority (coloured, with filters), plus sheets for assumptions, controls, recommended and compensating controls, vulnerabilities, critical interactions, deployment, decisions and ticket drafts |
| `report.docx` | **Word report** in Calibri, with the diagrams embedded |
| `dfd-01.png`, `deployment-01.png` (and `.jpg`, `.svg`) | **Diagram images**: trust boundaries as red dashed boxes, critical flows in thick red |
| `threat-model.json` | Give it to the agent next time as `previous:` to see what has been fixed |
| `report.md`, `*.mmd` | A copy of the report and the diagram source text, used to build the files above; the report you keep is `report-<date>.md` one folder up |

To run the export yourself (e.g. after copying a report from Copilot):

```powershell
python tools\threat-modeler-export\tm_export.py docs\threat-models\<system>\report.md --docx
```

| If you see | Fix |
|---|---|
| `pandoc not found` (no Word file) | Run the setup script, restart VS Code, run the export again |
| `Mermaid CLI (mmdc) not found` (no images) | Same as above |
| `no valid threat-modeler ... JSON handoff found` | The saved report is incomplete: save it again from the first line to `Validation: NOT RUN (chat mode).` |
| `cd : Cannot find path ...` | You are in a separate PowerShell window; use **Terminal → New Terminal** in VS Code instead |

## After the review: decisions, temporary fixes, rechecks

Add these to the Step 3 prompt when needed:

| Situation | Add |
|---|---|
| The risk owner decides on a threat | `decisions: T-03 accept — Head of Payments, 2027-03-31` (or treat / transfer / avoid) |
| The team has a temporary fix | `compensating: T-05 compensating — <control> — <evidence> — <owner> — until <date>` |
| Recheck after fixes | `previous: <path to the earlier threat-model.json>` with the current material; the report shows what is fixed, still open, changed or new |

The agent records decisions; it never accepts a risk itself.

## In GitHub Copilot

Steps 1–2 are the same. Pick **threat-modeler** in the Copilot Chat agent dropdown and send the Step 3 prompt; to approve, reply `approve — <your name, role>` in the same chat. Copilot does not save files or run the export for you: copy the report into `docs/threat-models/<system>/report.md` and run the export command above. Copilot Chat in VS Code 1.109+ may draw the diagram directly in the chat (not yet tested).

## Quick reference

| Input | Purpose |
|---|---|
| `system:` | Folder with the material (required) |
| `intake:` | Answers file or pasted answers; leave out to get the questionnaire; `skip` for no questions |
| `checkpoint: skip` | No diagram review pause (quick runs and tests only) |
| `focus:` | Model only some components in depth (also uses less of your usage quota) |
| `depth: thorough` | More research budget |
| `previous:`, `decisions:`, `compensating:` | Recheck and follow-up |
| `?` | Print the agent's usage card |
