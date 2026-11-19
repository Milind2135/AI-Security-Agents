# Using threat-modeler on a real project

A step-by-step guide for a first-time user: what to collect, which prompts to send, and what comes back at each stage.
The agent instructions are in [`.github/agents/threat-modeler.agent.md`](../.github/agents/threat-modeler.agent.md);
the questionnaire the application team fills in is [`docs/threat-model-intake.md`](threat-model-intake.md).

> **Data rule.** Real designs, code and diagrams describe your organisation's weaknesses. Use them only with an AI service your organisation has approved, keep them in a git-ignored folder (`docs/threat-models/` is ignored in this repository), and never paste them into online diagram or AI tools. For practice, use the synthetic systems in [`tests/threat-modeler/fixtures/`](../tests/threat-modeler/fixtures).

## How a run works

```text
Collect material ─▶ Run 1: questionnaire ─▶ Team answers (one go) ─▶ Run 2: model + DFD review ─▶ You approve ─▶ Run 3: full report ─▶ Export files
```

The agent pauses at only two points: **once** for the intake questionnaire and for the **data-flow diagram (DFD) review** (at most 3 rounds). It never asks anything else; whatever is still missing is recorded as a gap.

In **Claude Code**, a subagent cannot wait for a reply, so each pause ends the run and you start the next run with the extra input. In **GitHub Copilot** you can simply reply in the same chat.

## Step 1 — Collect the material from the application team

Ask the team for what they already have and put it in one folder, e.g. `docs/threat-models/<system>/input/`:

| Material | Formats the agent can read |
|---|---|
| Design / architecture documents | PDF, Markdown, text (save Word files as PDF first) |
| Diagrams | PNG or JPG (export Visio / draw.io diagrams to PNG first) |
| Source code | The repository folder or the relevant paths (entry points, auth, data access) |
| Infrastructure as code | Terraform, CloudFormation, Bicep/ARM, Kubernetes, Helm |
| API specifications | OpenAPI / GraphQL / gRPC files |
| Pipeline files | CI/CD definitions |

Code and IaC matter most: without them, controls can only be marked `Claimed` and overall confidence is `Low`.

## Step 2 — Get the questions to the team

Choose one:

- **A. Send the blank form.** Give the team [`docs/threat-model-intake.md`](threat-model-intake.md) (25 questions in 4 tiers). It explains itself and says what not to include.
- **B. Let the agent ask.** Run the agent once without `intake:` and send the team the questionnaire it prints:
  ```text
  Use the threat-modeler subagent. system: docs/threat-models/<system>/input/ Show me the complete output verbatim.
  ```
  At this point the agent has not read your documents yet. It only marks questions where a matching file is present (e.g. `Received: architecture-diagram.png` for the diagram question).

## Step 3 — Collect the answers in one go

- Ask the team to answer **everything they can in one reply**, and to write **`not available`** for anything they do not have. That is a valid answer.
- Save their answers as a file next to the input folder (not inside it), e.g. `docs/threat-models/<system>/intake-answers.md`.
- Do not chase every gap before running the agent: each unanswered item is recorded in the report with its effect, so the team can close it later.

## Step 4 — Run 2: build the model and review the diagram

```text
Use the threat-modeler subagent. system: docs/threat-models/<system>/input/ intake: docs/threat-models/<system>/intake-answers.md Show me the complete output verbatim.
```

You get a **model for review**:
- **Mismatches (`MM-#`)** listed first, where the documents and the code or IaC disagree. These are often the most valuable findings.
- The DFD with labelled elements, trust boundaries and critical interactions (★), plus a deployment view.
- The readiness result and a **JSON block** at the end. Keep it for the next step.

Check the diagram with the application team. If something is wrong, re-run with a correction:
```text
Use the threat-modeler subagent. system: docs/threat-models/<system>/input/ intake: docs/threat-models/<system>/intake-answers.md model: <paste the JSON block> review: <what is wrong, in plain words> Show me the complete output verbatim.
```

## Step 5 — Run 3: approve and get the full report

```text
Use the threat-modeler subagent. system: docs/threat-models/<system>/input/ intake: docs/threat-models/<system>/intake-answers.md model: <paste the latest JSON block> review: approve — <your name>, <your role> Show me the complete report verbatim.
```

The report has 14 sections: threats, vulnerabilities, existing-control validation, risks ranked P1–P4, treatment and residual risk, recommended controls with owners and ticket drafts, plus CSV and JSON blocks.

## How gaps appear in the report

Every one of the 25 questions appears in the **intake checklist** with one status:

| Status | Meaning |
|---|---|
| `Provided` | The team answered it, or a matching file was supplied |
| `Derived` | Not answered, but found in the documents, with `file:line` |
| `Not provided` | Not answered and not found, with one line on how the gap weakens the model |
| `Not applicable` | The material shows it does not exist (e.g. no AI features) |

- `Not provided` never means "does not exist". Missing logging details do not mean there is no logging.
- **Readiness:** `Not ready` (stops and lists the most useful missing items) if nothing says what the system does or no component and data flow are described; `Proceed with limits` if no code or IaC was read.
- **Confidence:** `High` only when Q1–Q6 are answered or derived, code or IaC was read, and the DFD was approved.
- Anything the agent had to assume goes into the **assumptions register** for the team to confirm.

The result: each gap is a **named weakness the team can fix later, not a silent guess**.

## Step 6 — Save and export

1. Save the complete report (from `threat-modeler vX.Y | result` to `Validation: NOT RUN (chat mode).`) to `docs/threat-models/<system>/<date>/report.md`.
2. Optional: turn it into diagram images, an Excel threat register and a Word report with the [exporter](../tools/threat-modeler-export/README.md):
   ```powershell
   python tools\threat-modeler-export\tm_export.py docs\threat-models\<system>\<date>\report.md --docx
   ```

## Step 7 — After the review

| Situation | Add to the prompt |
|---|---|
| The risk owner decides on a threat | `decisions: T-03 accept — Head of Payments, 2027-03-31` (or treat / transfer / avoid) |
| The team has a temporary fix | `compensating: T-05 compensating — <control> — <evidence> — <owner> — until <date>` |
| Later recheck after fixes | `previous: <the earlier report JSON>` with the current material; the report shows what is fixed, still open, changed or new |

The agent records decisions; it never accepts a risk itself.

## Quick reference

| Input | Purpose |
|---|---|
| `system:` | Folder or paths with the material (required) |
| `intake:` | Answers file or pasted answers; `skip` for no questions; leave out to get the questionnaire |
| `checkpoint: skip` | No DFD review pause (quick runs and tests only) |
| `model:` + `review:` | Continue after the DFD review (correction or `approve — <name, role>`) |
| `previous:`, `decisions:`, `compensating:` | Recheck and follow-up |
| `focus:` / `depth:` | Model only some components / more research budget |
| `?` | Print the usage card |
