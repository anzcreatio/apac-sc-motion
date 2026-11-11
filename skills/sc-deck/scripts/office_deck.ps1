<#
  PowerPoint steps python-pptx can't do. Quits PowerPoint afterwards, even on error, unless the SC already had it
  open (an orphaned Office process once locked a deal folder for a day: 11 Nov 2026).

  (Library slides are copied by build_deck.py in Python: PowerPoint automation is blocked on decks with a
   sensitivity label such as Creatio 'Confidential'.)
  -Action render : export every slide to PNG (1600x900) in -OutDir.
  -Action extract: save slides -Slides "4,5,6" of -Deck as a new file -Out (for the slide library).
#>
param(
  [Parameter(Mandatory)][ValidateSet('render', 'extract')][string]$Action,
  [Parameter(Mandatory)][string]$Deck,
  [string]$Spec, [string]$OutDir, [string]$Slides, [string]$Out
)
$ErrorActionPreference = 'Stop'
$Deck = (Resolve-Path $Deck).Path
# PowerPoint runs one instance per user: if the SC already has it open, use it but never quit it.
$alreadyRunning = @(Get-Process POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$pp = New-Object -ComObject PowerPoint.Application
$opened = @()
try {
  # Open(FileName, ReadOnly, Untitled, WithWindow): read-only, no window, never changes the source
  $pres = $pp.Presentations.Open($Deck, -1, 0, 0); $opened += $pres
  switch ($Action) {
    'render' {
      New-Item -ItemType Directory -Force $OutDir | Out-Null
      $OutDir = (Resolve-Path $OutDir).Path   # PowerPoint needs absolute paths
      Get-ChildItem $OutDir -Filter 'slide-*.png' | Remove-Item
      $i = 1
      foreach ($s in $pres.Slides) { $s.Export((Join-Path $OutDir ('slide-{0:D2}.png' -f $i)), 'PNG', 1600, 900); $i++ }
      Write-Output "rendered $($i - 1) slides to $OutDir"
    }
    'extract' {
      $keep = $Slides.Split(',') | ForEach-Object { [int]$_.Trim() }
      for ($i = $pres.Slides.Count; $i -ge 1; $i--) { if ($keep -notcontains $i) { $pres.Slides.Item($i).Delete() } }
      $pres.SaveCopyAs([System.IO.Path]::GetFullPath($Out))
      Write-Output "saved $($keep.Count) slides to $Out"
    }
  }
}
finally {
  foreach ($p in $opened) { try { $p.Close() } catch {} }
  if (-not $alreadyRunning) { $pp.Quit() }
  [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($pp)
  [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}
