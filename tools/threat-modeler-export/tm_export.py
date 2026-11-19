#!/usr/bin/env python3
"""Export a threat-modeler report (saved as Markdown) to shareable files.

Creates, in the output folder:
  dfd-NN.(png|jpg|svg|mmd)        data-flow diagrams (trust boundaries styled, critical ==> flows in red)
  deployment-NN.(png|jpg|svg|mmd) deployment diagrams
  threat-model.xlsx               threat register (from the csv block) + sheets from the JSON handoff
  threat-model.json               the JSON handoff, unchanged
  report.md                       copy of the report
  report.docx                     only with --docx and pandoc installed (diagrams embedded)

No AI, no network calls. Diagram rendering needs the Mermaid CLI (mmdc).
Usage:  python tm_export.py <report.md> [--out <folder>] [--formats png,jpg,svg] [--docx]
        python tm_export.py <saved model-review message.md> --diagrams-only   (DFD review images only)
"""
import argparse, csv, io, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_REPORT_BYTES = 5_000_000
FENCE = re.compile(r"^```(\w+)[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)
ARROW = re.compile(r"<?(?:={2,}|-{2,}|-\.+-)(?:>|o|x)?")
PRIORITY_FILL = {"P1": "F8D7DA", "P2": "FFE5CC", "P3": "FFF3CD", "P4": "D4EDDA"}


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def find_mmdc():
    for name in ("mmdc", "mmdc.cmd"):
        path = shutil.which(name)
        if path:
            return path
    return None


def blocks(text):
    """Yield (language, body, start_index) for each fenced block."""
    for m in FENCE.finditer(text):
        yield m.group(1).lower(), m.group(2), m.start()


def colour_critical_flows(src):
    """Append linkStyle for every '==>' edge, counting edges in definition order."""
    idx, critical = 0, []
    for line in src.splitlines():
        s = line.strip()
        if not s or s.startswith(("%%", "classDef", "class ", "style", "linkStyle", "subgraph", "end", "flowchart", "graph", "direction")):
            continue
        unquoted = re.sub(r'"[^"]*"', '""', s)
        unquoted = re.sub(r"\|[^|]*\|", "", unquoted)
        for a in ARROW.findall(unquoted):
            if a.startswith("==") and a.endswith(">"):
                critical.append(idx)
            idx += 1
    if critical:
        src = src.rstrip() + "\n  linkStyle " + ",".join(map(str, critical)) + " stroke:#c62828,stroke-width:3px\n"
    return src


def render(mmdc, src, base, formats):
    cfg = HERE / "mermaid-config.json"
    made = []
    with tempfile.TemporaryDirectory() as tmp:
        mmd = Path(tmp) / "d.mmd"
        mmd.write_text(src, encoding="utf-8")
        for fmt in [f for f in formats if f in ("png", "svg")] or ["png"]:
            out = base.with_suffix("." + fmt)
            cmd = [mmdc, "-i", str(mmd), "-o", str(out), "-c", str(cfg), "-b", "white"]
            if fmt == "png":
                cmd += ["-s", "2"]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0 or not out.exists():
                print(f"  ! could not render {out.name}: {r.stderr.strip()[:300]}")
                continue
            made.append(out)
    if "jpg" in formats:
        png = base.with_suffix(".png")
        if not png.exists():
            render(mmdc, src, base, ["png"])
        try:
            from PIL import Image
            Image.open(png).convert("RGB").save(base.with_suffix(".jpg"), quality=92)
            made.append(base.with_suffix(".jpg"))
            if "png" not in formats:
                png.unlink()
        except ImportError:
            print("  ! Pillow not installed: no .jpg (pip install Pillow)")
    return made


def write_xlsx(path, csv_text, data):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Font, PatternFill
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("  ! openpyxl not installed: no .xlsx (pip install openpyxl)")
        return False
    wb = Workbook()
    ws = wb.active
    ws.title = "Threat register"

    def fill_sheet(sheet, rows):
        for r in rows:
            sheet.append(["" if v is None else (json.dumps(v) if isinstance(v, (list, dict)) else v) for v in r])
        if not rows:
            return
        for c in sheet[1]:
            c.font = Font(bold=True)
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions
        for i, _ in enumerate(rows[0], start=1):
            sheet.column_dimensions[get_column_letter(i)].width = 22
        for row in sheet.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")

    rows = list(csv.reader(io.StringIO(csv_text))) if csv_text else []
    fill_sheet(ws, rows)
    if rows and "Priority" in rows[0]:
        p = rows[0].index("Priority")
        for row in ws.iter_rows(min_row=2):
            colour = PRIORITY_FILL.get(str(row[p].value).strip())
            if colour:
                for c in row:
                    c.fill = PatternFill("solid", fgColor=colour)
    if isinstance(data, dict):
        for key in ("attack_paths", "privilege_escalation", "standalone_findings", "recommendations",
                    "assumptions", "controls", "compensating_controls", "recommended_controls",
                    "vulnerabilities", "critical_interactions", "deployment", "decisions", "tickets"):
            items = data.get(key)
            if isinstance(items, list) and items and all(isinstance(i, dict) for i in items):
                cols = list(dict.fromkeys(k for i in items for k in i))
                fill_sheet(wb.create_sheet(key.replace("_", " ").capitalize()[:31]),
                           [cols] + [[i.get(c) for c in cols] for i in items])
    wb.save(path)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report", help="threat-modeler report saved as a .md file")
    ap.add_argument("--out", help="output folder (default: <report folder>/export)")
    ap.add_argument("--formats", default="png,jpg,svg", help="diagram formats: png, jpg, svg (comma-separated)")
    ap.add_argument("--docx", action="store_true", help="also build report.docx with pandoc")
    ap.add_argument("--diagrams-only", action="store_true",
                    help="only render the diagrams (e.g. from a DFD model-review message); no JSON, Excel, report copy or Word")
    a = ap.parse_args()

    report = Path(a.report)
    if not report.is_file():
        die(f"report not found: {report}")
    if report.stat().st_size > MAX_REPORT_BYTES:
        die("report larger than 5 MB — is this the right file?")
    text = report.read_text(encoding="utf-8", errors="replace")
    if "threat-modeler v" not in text and "cloud-security-analyst v" not in text:
        print("  ! this does not look like a threat-modeler report (no 'threat-modeler v' marker); continuing")
    out = Path(a.out) if a.out else report.parent / "export"
    out.mkdir(parents=True, exist_ok=True)
    formats = [f.strip().lower().replace("jpeg", "jpg") for f in a.formats.split(",") if f.strip()]

    mmdc = find_mmdc()
    if not mmdc:
        print("  ! Mermaid CLI (mmdc) not found: diagrams saved as .mmd only. Install: npm install -g @mermaid-js/mermaid-cli")
    counts, diagram_files, csv_text, data = {"dfd": 0, "deployment": 0}, [], None, None
    for lang, body, start in blocks(text):
        if lang == "mermaid":
            tag = re.match(r"\s*%%\s*diagram:\s*(dfd|deployment)", body, re.I)
            if tag:
                kind = tag.group(1).lower()
            else:  # fallback for reports without the tag
                before = text[max(0, start - 300):start].lower()
                kind = "deployment" if "deployment diagram" in before else "dfd"
            counts[kind] += 1
            base = out / f"{kind}-{counts[kind]:02d}"
            src = colour_critical_flows(body)
            base.with_suffix(".mmd").write_text(src, encoding="utf-8")
            made = render(mmdc, src, base, formats) if mmdc else []
            diagram_files.append((start, base))
            print(f"  diagram {base.name}: " + (", ".join(p.suffix for p in made) or ".mmd only"))
        elif lang == "csv" and csv_text is None:
            csv_text = body
        elif lang == "json":
            try:
                candidate = json.loads(body)
                if isinstance(candidate, dict) and candidate.get("agent") in ("threat-modeler", "cloud-security-analyst"):
                    data = candidate
            except json.JSONDecodeError:
                pass

    if a.diagrams_only:
        if not diagram_files:
            print("  ! no Mermaid diagrams found in this file")
        print(f"Done: {out}")
        return

    if data is not None:
        (out / "threat-model.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print("  threat-model.json")
    else:
        print("  ! no valid threat-modeler / cloud-security-analyst JSON handoff found")
    if csv_text or data:
        if write_xlsx(out / "threat-model.xlsx", csv_text, data):
            print("  threat-model.xlsx")
    shutil.copyfile(report, out / "report.md")

    if a.docx:
        pandoc = shutil.which("pandoc")
        if not pandoc:
            print("  ! pandoc not found: no .docx (install pandoc, then re-run with --docx)")
        else:
            md, n = text, 0
            def swap(m):
                nonlocal n
                if m.group(1).lower() != "mermaid":
                    return m.group(0)
                n += 1
                match = [b for s, b in diagram_files][n - 1]
                img = match.with_suffix(".png")
                return f"![{match.name}]({img.name})\n" if img.exists() else m.group(0)
            md = FENCE.sub(swap, text)
            tmp_md = out / "_report_for_docx.md"
            tmp_md.write_text(md, encoding="utf-8")
            r = subprocess.run([pandoc, tmp_md.name, "-o", "report.docx"], cwd=out, capture_output=True, text=True)
            tmp_md.unlink(missing_ok=True)
            print("  report.docx" if r.returncode == 0 else f"  ! pandoc failed: {r.stderr.strip()[:300]}")
    print(f"Done: {out}")


if __name__ == "__main__":
    main()
