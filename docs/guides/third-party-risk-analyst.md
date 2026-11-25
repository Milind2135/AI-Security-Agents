# third-party-risk-analyst: how to use it

From "the business wants a new vendor" to a decision pack your approver can sign — and afterwards, reviews of existing vendors, a priority list for your whole vendor list, and exit checks.

Agent instructions: [`.github/agents/third-party-risk-analyst.agent.md`](../../.github/agents/third-party-risk-analyst.agent.md) · Forms: [`templates/tprm/`](../../templates/tprm) · Excel tool: [`tools/tprm/tprm.py`](../../tools/tprm/tprm.py)

> **Data rule:** vendor contracts, SOC reports and questionnaires are confidential (often under an NDA), and screening results contain personal data. Use them only with an AI service your organisation has approved. Keep everything under `docs/vendors/` — that folder is git-ignored, so nothing is pushed to GitHub. For practice, use the synthetic vendors in [`tests/third-party-risk-analyst/fixtures/`](../../tests/third-party-risk-analyst/fixtures).

**What the agent does and doesn't do**
- It **does:** rate the vendor, choose what to ask for, check every answer against evidence, list the gaps, draft follow-up questions, prepare the decision pack and keep track of dates.
- It **never:** approves or rejects a vendor, accepts a risk, decides whether a sanctions hit is real, contacts the vendor, or signs off QA. People do that; the agent records it.

## Part 0: One-time setup (about 10 minutes)

1. **Folders.** In the VS Code file explorer create:
   ```text
   docs/vendors/_policy/            ← your company policy file goes here
   docs/vendors/_policy/original/   ← (optional) your full policy PDF / Word file
   ```
2. **Policy file.** Copy [`templates/tprm/policy-template.md`](../../templates/tprm/policy-template.md) to `docs/vendors/_policy/policy.md` and fill it in from your company's TPRM policy (tiers, thresholds, review frequency, evidence per tier, approvers, mandatory contract clauses). Empty rows use the agent's defaults. Tip: you can put your policy PDF in `original/` and ask Claude, in a normal chat (not the agent), *"Draft docs/vendors/_policy/policy.md from the policy in docs/vendors/_policy/original/ using the template"* — then **check and approve the draft yourself**; it becomes the rulebook. You only do this once; the agent reads it automatically on every run.
3. **Excel support** (for the vendor questionnaire and the assessment workbook). You need Python with `openpyxl`. If you already ran the threat-modeler setup, you have it. Otherwise, in VS Code open **Terminal → New Terminal** and run:
   ```powershell
   python -m pip install openpyxl
   ```
   No Python? Run the threat-modeler setup script once: `powershell -ExecutionPolicy Bypass -File tools\threat-modeler-export\setup.ps1`, then close and reopen VS Code.

## Part 1: A new vendor (Claude Code chat)

Replace `<vendor>` with a short folder name, e.g. `payflow`.

### Step 1: The business owner fills the intake form
Send them [`templates/tprm/intake-form.md`](../../templates/tprm/intake-form.md) (about 35 short questions: data, access, business impact, regulation, technology). `Don't know` is allowed — the agent treats it as **High** until someone confirms. Save their answers as `docs/vendors/<vendor>/intake-<engagement>.md`.

### Step 2: Get the plan
```text
Use the third-party-risk-analyst subagent. type: new vendor: <vendor> intake: docs/vendors/<vendor>/intake-<engagement>.md
```
Add `regimes: EU-DORA, IN-RBI, IN-DPDP` if your policy file doesn't list them. The agent returns a **plan**: the tier and why, the two ratings (inherent risk and criticality), any regulatory flags, which questionnaire areas apply, **which documents to request first** and the screening checklist. Claude saves it as `docs/vendors/<vendor>/plan.md` and builds the **vendor questionnaire** `questionnaire-<vendor>-<date>.xlsx` in the same folder.

### Step 3: Confirm the tier (you)
Read the tier and the reasons. If you agree:
```text
tier: confirm — <your name>, <your role>
```
If not: `tier: 2 — <reason> — <your name, role>` (a lower tier than proposed needs the TPRM lead). Claude keeps this for the next step; nothing else happens until the vendor replies.

### Step 4: Send to the vendor and run screening (you)
- Send the **document request list** first (SOC 2 Type II report, ISO/IEC 27001:2022 certificate, pen-test summary …), then the Excel questionnaire.
- Run screening (company registry, owners, sanctions, adverse media, financials) in your company's tools and save the results as a file.
- The vendor usually takes 2–6 weeks. Put everything they send, plus the screening results and the contract draft, in `docs/vendors/<vendor>/evidence/`.

### Step 5: Review (Claude Code chat — new chat is fine)
```text
Continue the third-party-risk-analyst assessment for <vendor>: tier: confirm — <your name, role>. Evidence is in docs/vendors/<vendor>/evidence/
```
Claude converts the vendor's Excel questionnaire to text (macros are never run), then runs the agent. You get **review round 1**:
- every document checked (in date? right edition? covers the service?), SOC 2 exceptions and the controls you must run yourself;
- every answer marked **Verified · Verified with exception · Documented · Claimed · Contradicted · Expired · Missing · N/A**;
- findings so far, **follow-up questions for the vendor**, and **questions for your teams** (Privacy, Legal, Compliance, Resilience, screening).

Send the follow-up questions; when the answers come back, put them in the evidence folder and say:
```text
next: continue
```
(or `next: finalise — <reason>` to stop asking). There are at most 3 rounds.

### Step 6: The decision pack
After `finalise` (or round 3), Claude saves `result-<date>.md` and builds the **assessment workbook** `assessment-<vendor>-<date>.xlsx`: summary, tier, scoping, evidence, one tab per area with assessor and **QA** columns, findings, actions, conditions, specialist inputs, contract check, fourth parties and decision log. A **second reviewer** checks it (QA) — the agent never does.

The report lists the decision options **without recommending one**.

### Step 7: Record the decision
The named approver decides (your policy says who). Then:
```text
decision: approve with conditions — <name>, <role>, <YYYY-MM-DD>, CON-1, CON-2
```
Other options: `approve`, `reject`, `accept risk F-3 — <name, role>, <date>, expiry <date>`, `exception F-5 — …`. The agent flags anything incomplete (no conditions, no expiry, approver below the policy level). Claude saves `decision-<date>.md` — the record you use next time.

## Part 2: An existing vendor

### Scheduled review
The business owner fills the **change form** ([`templates/tprm/change-form.md`](../../templates/tprm/change-form.md)): what changed since last time. Then:
```text
Use the third-party-risk-analyst subagent. type: review vendor: <vendor> previous: docs/vendors/<vendor>/decision-<date>.md change: docs/vendors/<vendor>/change-<date>.md evidence: docs/vendors/<vendor>/evidence/
```
The agent reads the **last tier from the saved record** (not from memory), recalculates it, and shows `Previous: Tier 3 → Proposed: Tier 2 — because …`. Higher tiers apply at once; lower tiers need the TPRM lead. It refreshes only expired or affected evidence and shows old findings as **Fixed · Still open · Overdue**. Then Steps 3–7 as above.

### Something happened (trigger)
```text
type: trigger vendor: <vendor> previous: <latest record> change: <what happened, e.g. "vendor reported a data breach on 2026-12-01">
```

### Vendor leaving (exit)
```text
type: exit vendor: <vendor> previous: <latest record> evidence: docs/vendors/<vendor>/exit/
```
Checks data return, certified deletion, access removal, open findings and regulatory register updates.

## Part 3: Your whole vendor list (portfolio)
Export your vendor list (Excel or CSV) to `docs/vendors/_register/vendors.csv` (columns such as vendor, tier, last review, services, data, owner). If it's Excel, Claude converts it first. Then:
```text
Use the third-party-risk-analyst subagent. type: portfolio register: docs/vendors/_register/vendors.csv
```
You get a **priority list** (never-assessed critical vendors first, then overdue reviews and expiring evidence), concentration and gaps in your register. Suggested tiers from a list are always marked *unverified* — assess them properly with `type: new` or `type: review`.

For an Excel register of everything you've already assessed: `python tools/tprm/tprm.py register docs/vendors`.

## How the tier is decided (in short)
| Rating | Comes from | Examples |
|---|---|---|
| **Inherent risk** | What the vendor can see or touch | Customer personal data and volume, card data, access to critical systems, privileged access, regulated activity, cloud, AI on your data |
| **Criticality** | What happens to you if the vendor stops | Critical business service, time to harm, customers affected, how long to replace, concentration |
| **Tier** | Both, plus "automatic Tier 1" rules | e.g. critical service with harm within 4 hours → Tier 1 |
| **Residual risk** | After the evidence review | Open findings, missing independent assurance |

Unknown answers count as **High**. Spend never sets the tier. Your policy file can change the thresholds.

## In GitHub Copilot
Pick **third-party-risk-analyst** in the Copilot Chat agent dropdown and reply to its pauses in the same chat (not yet tested). Copilot does not save files or run tools for you, so:
- convert Excel questionnaires first: `python tools/tprm/tprm.py convert docs/vendors/<vendor>/evidence/<file>.xlsx`;
- save each message yourself (plan, result) and build Excel files with `python tools/tprm/tprm.py questionnaire <saved plan.md>` or `workbook <saved result.md>`.

## Quick reference
| Input | Purpose |
|---|---|
| `type:` | `new` · `review` · `trigger` · `portfolio` · `exit` (send nothing to get the menu) |
| `vendor:` | Vendor folder name under `docs/vendors/` |
| `intake:` / `change:` | Business-owner forms |
| `evidence:` | Folder with the vendor's documents, converted questionnaire, screening results, contract draft |
| `tier:` | `confirm — <name, role>` or `<1-4> — <reason> — <name, role>` |
| `next:` | `continue` or `finalise — <reason>` after a review round |
| `decision:` | The approver's decision, recorded exactly |
| `previous:` | The latest saved record (`decision-<date>.md`) |
| `regimes:` / `sector:` | e.g. `EU-DORA, UK-PRA, US-Interagency, IN-RBI, IN-DPDP`; `sector: general` for non-financial companies |
| `policy:` | Only to use a different policy file |
| `as_of:` | Date for expiry and overdue checks |
| `public_lookups: on` | Allow a public company-registry lookup of the legal entity |
| `?` | Usage card |

| If you see | Fix |
|---|---|
| `Not readable — convert first` | Run `python tools/tprm/tprm.py convert <file.xlsx>` (Claude does this automatically in Claude Code) |
| `openpyxl is not installed` | `python -m pip install openpyxl` |
| Old `.xls` file | Save it as `.xlsx` in Excel, or `python -m pip install xlrd` |
| `Policy: none found — built-in defaults` | Create `docs/vendors/_policy/policy.md` (Part 0) |
| `PC-1: policy says … regime requires …` | Your policy is weaker than a regulation you selected — Compliance decides |
