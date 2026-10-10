<#
Pokreće MCP poslužitelj LegalTechSuite Pro i ponovno ga diže ako padne (za Task Scheduler, zadatak LEGAL_MCP).
Javna adresa za poveznice na .docx čita se iz LEGAL_JAVNA_ADRESA (postavlja se u zadatku ili okolini korisnika).
Prestaje kad postoji datoteka .mcp_dokumenti\stop.
Ručno: powershell -NoProfile -ExecutionPolicy Bypass -File pristup\pokreni_mcp.ps1
#>
$ErrorActionPreference = "Continue"
$Repo = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Repo ".venv\Scripts\python.exe"
$Spremiste = Join-Path $Repo ".mcp_dokumenti"
New-Item -ItemType Directory -Force $Spremiste | Out-Null
$Log = Join-Path $Spremiste "posluzitelj.log"
Set-Location $Repo
while ($true) {
    if (Test-Path (Join-Path $Spremiste "stop")) { break }
    Add-Content -Path $Log -Value "[$(Get-Date -Format s)] pokrećem MCP poslužitelj"
    & $Python -m pristup.mcp_posluzitelj *>> $Log
    Add-Content -Path $Log -Value "[$(Get-Date -Format s)] poslužitelj završio s kodom $LASTEXITCODE"
    Start-Sleep -Seconds 10
}
