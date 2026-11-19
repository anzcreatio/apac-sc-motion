<#
  Publish the plugin to the team's SharePoint folder, where every SC installs and updates it from.

  Usage (Renzo only):  powershell -ExecutionPolicy Bypass -File publish.ps1 [-Title "<title>"] [-Bump minor] [-DryRun]
  Then tell the SCs:   claude plugin update apac-sc-motion@apac-sc

  How versions work (19 Nov 2026): chats never edit the version. Any chat commits its change and adds a bullet under
  "## Unreleased" in CHANGELOG.md. This script is the only thing that picks a version: it turns Unreleased into
  "## <next> (<d Mon yyyy>): <title>" (patch bump by default, -Bump minor for a bigger release), sets
  .claude-plugin/plugin.json, commits "Release <next>", publishes and tags v<next>.

  Rules: only committed work is published (so the git history matches what the team has); plugin.json must still
  equal the last v* tag (a hand-edited version stops the publish); Unreleased must not be empty. The weekly release
  message for the SCs is built from CHANGELOG.md by release-notes.ps1.
#>
param([string]$Target, [string]$Title, [ValidateSet('patch', 'minor')][string]$Bump = 'patch', [switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = $PSScriptRoot

if (-not $Target) {
  $cfg = Join-Path $env:USERPROFILE '.apac-sc-motion.json'
  $root = (Get-Content $cfg -Raw | ConvertFrom-Json).sharepoint_root
  $Target = Join-Path $root 'Plugin\apac-sc-motion'
}

$dirty = git -C $repo status --porcelain
if ($dirty) { throw "Uncommitted changes in the repo. Commit first:`n$dirty" }

# --- Pick the version: only this script does it -------------------------------------------------------------------
$pluginJson = Join-Path $repo '.claude-plugin\plugin.json'
$changelogPath = Join-Path $repo 'CHANGELOG.md'
$utf8 = New-Object System.Text.UTF8Encoding($false)
$current = (Get-Content $pluginJson -Raw | ConvertFrom-Json).version
$tags = @(git -C $repo tag --list 'v*' | ForEach-Object { $_.Substring(1) } | Where-Object { $_ -match '^\d+(\.\d+)+$' } |
  Sort-Object { [version]$_ })
$lastTag = if ($tags.Count) { $tags[-1] } else { $current }
$headSubject = git -C $repo log -1 --format='%s'

if ($current -ne $lastTag) {
  if ($headSubject -like "Release $current*") {
    # A previous run committed the release but stopped before publishing: carry on with that version.
    $version = $current
    Write-Output "Resuming release $version (committed earlier, not yet published)."
  } else {
    throw "plugin.json says $current but the last release is v$lastTag. Versions are picked only by publish.ps1: set plugin.json back to $lastTag, put the change under '## Unreleased' in CHANGELOG.md, commit, and publish again."
  }
} else {
  $text = [IO.File]::ReadAllText($changelogPath, $utf8)
  $m = [regex]::Match($text, '(?ms)^## Unreleased[ \t]*\r?\n(.*?)(?=^## |\z)')
  if (-not $m.Success -or -not $m.Groups[1].Value.Trim()) {
    throw "Nothing under '## Unreleased' in CHANGELOG.md. Add what changed for SCs (and any '**Each SC:**' action), commit, then publish."
  }
  $body = $m.Groups[1].Value.TrimEnd()
  $p = [version]$lastTag
  $version = if ($Bump -eq 'minor') { "$($p.Major).$($p.Minor + 1).0" } else { "$($p.Major).$($p.Minor).$($p.Build + 1)" }
  if (-not $Title) {
    $first = ($body -split "`n" | Where-Object { $_ -match '^\s*-\s' } | Select-Object -First 1)
    $Title = if ($first) { (($first -replace '^\s*-\s*', '') -replace '\*\*', '' -split '[:.]')[0].Trim() } else { 'Maintenance release' }
    if ($Title.Length -gt 80) { $Title = $Title.Substring(0, 80).Trim() }
  }
  $date = (Get-Date).ToString('d MMM yyyy', [Globalization.CultureInfo]::InvariantCulture)
  $heading = "## $version ($date): $Title"
  if ($DryRun) {
    Write-Output "Dry run: would release $version (last v$lastTag, bump $Bump)"
    Write-Output $heading
    Write-Output $body
    exit 0
  }
  $newText = $text.Substring(0, $m.Index) + "## Unreleased`n`n$heading`n`n$body`n`n" + $text.Substring($m.Index + $m.Length)
  [IO.File]::WriteAllText($changelogPath, $newText, $utf8)
  $json = [IO.File]::ReadAllText($pluginJson, $utf8) -replace '"version":\s*"[^"]+"', "`"version`": `"$version`""
  [IO.File]::WriteAllText($pluginJson, $json, $utf8)
  git -C $repo add CHANGELOG.md .claude-plugin/plugin.json | Out-Null
  git -C $repo commit -q -m "Release ${version}: $Title" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
  if ($LASTEXITCODE -ne 0) { throw "Committing the release failed." }
}
if ($DryRun) { Write-Output "Dry run: release $version is committed but not published; run again without -DryRun."; exit 0 }
$publishedFile = Join-Path $Target '.claude-plugin\plugin.json'
if (Test-Path $publishedFile) {
  $published = (Get-Content $publishedFile -Raw | ConvertFrom-Json).version
  if ([version]$version -le [version]$published) { throw "Version $version is not higher than the published $published. Bump .claude-plugin/plugin.json." }
}

$notes = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo 'release-notes.ps1') -Version $version
if ($LASTEXITCODE -ne 0 -or -not $notes) {
  throw "CHANGELOG.md has no entry for $version. Add '## $version (<d Mon yyyy>): <title>' with what changed and what SCs must do, commit, then publish."
}
if (git -C $repo tag --list "v$version") { throw "Tag v$version already exists. Bump .claude-plugin/plugin.json." }

New-Item -ItemType Directory -Force $Target | Out-Null
# Mirror the repo, leaving out git internals, test outputs (they hold customer content) and caches.
robocopy $repo $Target /MIR /XD .git out blind __pycache__ '*-png' /XF '~$*' publish.ps1 release-notes.ps1 RELEASE-QUEUE.md /R:1 /W:1 /NFL /NDL /NP /NJH | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed with exit code $LASTEXITCODE" }
# The self-serve entry points sit one level up, in Plugin/, where SCs look first.
$pluginDir = Split-Path $Target -Parent
Copy-Item (Join-Path $repo 'rollout\START-HERE.md') (Join-Path $pluginDir 'START-HERE.md') -Force
Copy-Item (Join-Path $repo 'rollout\HOW-TO-RUN-A-DEAL.md') (Join-Path $pluginDir 'HOW-TO-RUN-A-DEAL.md') -Force
$deck = Join-Path $repo 'rollout\overview\APAC-SC-Motion-Overview.pptx'
if (Test-Path $deck) {
  try { Copy-Item $deck (Join-Path $pluginDir 'APAC-SC-Motion-Overview.pptx') -Force -ErrorAction Stop }
  catch { Write-Warning "Overview deck not copied (open in PowerPoint?). Close it and copy rollout\overview\APAC-SC-Motion-Overview.pptx to Plugin\ by hand." }
}
$commit = git -C $repo log -1 --format='%h %s'
Set-Content -Path (Join-Path $Target 'PUBLISHED.txt') -Value "Version $version, published $(Get-Date -Format 'yyyy-MM-dd HH:mm') from commit $commit" -Encoding UTF8
git -C $repo tag -a "v$version" -m "apac-sc-motion $version" | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Warning "Published, but tagging v$version failed. Tag it by hand: git tag -a v$version" }
Write-Output "Published apac-sc-motion $version to $Target (tagged v$version)"
Write-Output "SCs update with: claude plugin update apac-sc-motion@apac-sc"
Write-Output ""
Write-Output "Changelog entry (goes into Monday's release message):"
$notes
