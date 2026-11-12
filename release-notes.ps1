<#
  Print CHANGELOG.md entries, newest first. Used by publish.ps1 (one version) and by the Monday release-message
  task (everything released in the last 7 days). Not published to SCs.

  Usage:  powershell -ExecutionPolicy Bypass -File release-notes.ps1 -Version 0.15.1
          powershell -ExecutionPolicy Bypass -File release-notes.ps1 -Since 2026-11-05   (default: last 7 days)

  Headings must look like "## 0.15.1 (12 Nov 2026): title". Exit code 1 if nothing matches.
#>
param([string]$Version, [string]$Since)
$ErrorActionPreference = 'Stop'
$lines = Get-Content (Join-Path $PSScriptRoot 'CHANGELOG.md') -Encoding UTF8
$culture = [Globalization.CultureInfo]::InvariantCulture
$from = if ($Since) { [datetime]::ParseExact($Since, 'yyyy-MM-dd', $culture) } else { (Get-Date).Date.AddDays(-7) }

$out = New-Object System.Collections.Generic.List[string]
$keep = $false
foreach ($line in $lines) {
  if ($line -match '^## (\S+).*?\((\d{1,2} \w{3} \d{4})') {
    $keep = if ($Version) { $Matches[1] -eq $Version }
            else { [datetime]::ParseExact($Matches[2], 'd MMM yyyy', $culture) -ge $from }
  } elseif ($line -match '^# ') { $keep = $false }
  if ($keep) { $out.Add($line) }
}
if ($out.Count -eq 0) { exit 1 }
$out
