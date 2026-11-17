# threat-modeler exporter

Turns a saved **threat-modeler** report into shareable files. Plain Python, no AI, no network calls.

| Output | What it is |
|---|---|
| `dfd-NN.png` / `.jpg` / `.svg` | Data-flow diagrams: trust boundaries as red dashed boxes, colour per element type, critical (`★`, `==>`) flows in thick red |
| `deployment-NN.png` / `.jpg` / `.svg` | Deployment diagrams |
| `*.mmd` | Diagram source (editable; GitHub renders it; can be imported into draw.io) |
| `threat-model.xlsx` | Threat register (colour by priority, filters) + sheets for assumptions, controls, recommended controls, compensating controls, vulnerabilities, critical interactions, deployment, decisions, tickets |
| `threat-model.json` | The agent's JSON handoff — pass it as `previous:` next time |
| `report.docx` | Full report with diagrams embedded (only with `--docx` and pandoc installed) |

## One-time setup (Windows, VS Code terminal — PowerShell)
1. **Python packages** (Python 3.10+):
   ```powershell
   pip install -r tools\threat-modeler-export\requirements.txt
   ```
2. **Mermaid CLI** for the images — needs Node.js LTS:
   ```powershell
   winget install OpenJS.NodeJS.LTS
   npm install -g @mermaid-js/mermaid-cli
   mmdc -V
   ```
   Close and reopen the terminal after installing Node.js. The Mermaid CLI downloads a headless Chromium browser the first time; a corporate proxy may block that — ask IT if `npm install` fails.
3. **pandoc** (optional, for `.docx`):
   ```powershell
   winget install --id JohnMacFarlane.Pandoc
   ```
At the office, installing Node.js, npm packages or pandoc may need IT approval.

## Use
1. Copy the agent's **complete report** (from `threat-modeler v1.3 | result` to `Validation: NOT RUN (chat mode).`) into a file, e.g. `docs\threat-models\orders-api\2026-11-17\report.md`.
2. Run:
   ```powershell
   python tools\threat-modeler-export\tm_export.py docs\threat-models\orders-api\2026-11-17\report.md --docx
   ```
3. Files appear in `...\2026-11-17\export\`. Options: `--formats png,jpg,svg` (default all three), `--out <folder>`.

If a tool is missing, the script says so and still produces everything else (e.g. `.mmd` diagram sources and the Excel file without Mermaid CLI).

## Security notes
- Diagrams are rendered locally (Mermaid `securityLevel: strict`). **Never paste internal architecture into online Mermaid or diagram websites.**
- The outputs describe your architecture and its weaknesses: keep them in an access-controlled location. `docs/threat-models/` is git-ignored in this repository because the repository is public — commit only synthetic test outputs.
