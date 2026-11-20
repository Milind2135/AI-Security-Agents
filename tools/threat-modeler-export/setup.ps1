# threat-modeler exporter - one-time setup for Windows (PowerShell)
#
# Installs only what is missing, so it is safe to run again:
#   Python packages  -> Excel threat register (openpyxl) and JPG images (Pillow)
#   pandoc           -> Word report (.docx)
#   Node.js + Mermaid CLI -> diagram images (PNG / JPG / SVG)
# It never deletes or changes anything else.
#
# Run from the repository folder:
#   powershell -ExecutionPolicy Bypass -File tools\threat-modeler-export\setup.ps1
# Options: -NoWord (skip pandoc)  -NoImages (skip Node.js and Mermaid CLI)
#
# On a managed work laptop, installing software may need IT approval.

param([switch]$NoWord, [switch]$NoImages)

$ErrorActionPreference = 'Continue'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$installedSomething = $false
$results = [ordered]@{}

function Have($name) { return [bool](Get-Command $name -ErrorAction SilentlyContinue) }

function Install-WithWinget($id, $label) {
    if (-not (Have 'winget')) {
        Write-Host "  ! winget is not available - install $label manually (see tools\threat-modeler-export\README.md)" -ForegroundColor Yellow
        return $false
    }
    Write-Host "  Installing $label with winget ..."
    winget install --id $id -e --accept-source-agreements --accept-package-agreements
    if ($LASTEXITCODE -eq 0) { $script:installedSomething = $true; return $true }
    Write-Host "  ! winget could not install $label (exit code $LASTEXITCODE)" -ForegroundColor Yellow
    return $false
}

Write-Host "threat-modeler exporter setup" -ForegroundColor Cyan

# 1. Python + packages (Excel, JPG)
Write-Host "`n[1/3] Python and packages (Excel)"
$py = $null
foreach ($cand in @('python', 'py')) { if (Have $cand) { $py = $cand; break } }
if (-not $py) {
    if (Install-WithWinget 'Python.Python.3.12' 'Python 3.12') {
        $results['Excel (Python)'] = 'INSTALLED - restart VS Code, then run this script again for the packages'
    } else {
        $results['Excel (Python)'] = 'MISSING - install Python 3.10+ from python.org'
    }
} else {
    & $py -m pip install --disable-pip-version-check -r (Join-Path $here 'requirements.txt')
    if ($LASTEXITCODE -eq 0) { $results['Excel (Python)'] = 'OK' }
    else { $results['Excel (Python)'] = 'FAILED - pip could not install the packages (proxy or permissions?)' }
}

# 2. pandoc (Word)
Write-Host "`n[2/3] pandoc (Word report)"
if ($NoWord) { $results['Word (pandoc)'] = 'SKIPPED (-NoWord)' }
elseif (Have 'pandoc') { $results['Word (pandoc)'] = 'OK' }
elseif (Install-WithWinget 'JohnMacFarlane.Pandoc' 'pandoc') { $results['Word (pandoc)'] = 'INSTALLED - restart VS Code' }
else { $results['Word (pandoc)'] = 'MISSING - no Word report until pandoc is installed' }

# 3. Node.js + Mermaid CLI (images)
Write-Host "`n[3/3] Node.js and Mermaid CLI (diagram images)"
if ($NoImages) { $results['Images (Mermaid CLI)'] = 'SKIPPED (-NoImages)' }
elseif (Have 'mmdc') { $results['Images (Mermaid CLI)'] = 'OK' }
elseif (-not (Have 'npm')) {
    if (Install-WithWinget 'OpenJS.NodeJS.LTS' 'Node.js LTS') {
        $results['Images (Mermaid CLI)'] = 'Node.js INSTALLED - restart VS Code, then run this script again to add Mermaid CLI'
    } else {
        $results['Images (Mermaid CLI)'] = 'MISSING - no diagram images until Node.js and Mermaid CLI are installed'
    }
} else {
    Write-Host "  Installing Mermaid CLI with npm (first run downloads a small headless browser) ..."
    npm install -g @mermaid-js/mermaid-cli
    if ($LASTEXITCODE -eq 0) { $installedSomething = $true; $results['Images (Mermaid CLI)'] = 'INSTALLED - restart VS Code' }
    else { $results['Images (Mermaid CLI)'] = 'FAILED - npm could not install Mermaid CLI (a company proxy may block it)' }
}

# Summary
Write-Host "`nSummary" -ForegroundColor Cyan
foreach ($k in $results.Keys) {
    $v = $results[$k]
    $colour = if ($v -eq 'OK') { 'Green' } elseif ($v -like 'SKIPPED*') { 'Gray' } elseif ($v -like 'INSTALLED*' -or $v -like 'Node.js INSTALLED*') { 'Cyan' } else { 'Yellow' }
    Write-Host ("  {0,-22} {1}" -f $k, $v) -ForegroundColor $colour
}
if ($installedSomething) {
    Write-Host "`nSomething was installed: CLOSE VS CODE COMPLETELY AND REOPEN IT, then run this script once more to check." -ForegroundColor Cyan
} else {
    Write-Host "`nNothing new was installed." -ForegroundColor Green
}
