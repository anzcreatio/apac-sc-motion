<#
  Publish the plugin to the team's SharePoint folder, where every SC installs and updates it from.

  Usage (Renzo only):  powershell -ExecutionPolicy Bypass -File publish.ps1
  Then tell the SCs:   claude plugin update apac-sc-motion@apac-sc

  Rules: only committed work is published (so the git history matches what the team has), the version in
  .claude-plugin/plugin.json must be higher than the published one (or SCs won't receive the update), and
  CHANGELOG.md must have a "## <version> (<d Mon yyyy>): ..." entry for it. Each publish tags the commit v<version>.
  The weekly release message for the SCs is built from CHANGELOG.md by release-notes.ps1.
#>
param([string]$Target)
$ErrorActionPreference = 'Stop'
$repo = $PSScriptRoot

if (-not $Target) {
  $cfg = Join-Path $env:USERPROFILE '.apac-sc-motion.json'
  $root = (Get-Content $cfg -Raw | ConvertFrom-Json).sharepoint_root
  $Target = Join-Path $root 'Plugin\apac-sc-motion'
}

$dirty = git -C $repo status --porcelain
if ($dirty) { throw "Uncommitted changes in the repo. Commit first:`n$dirty" }

$version = (Get-Content (Join-Path $repo '.claude-plugin\plugin.json') -Raw | ConvertFrom-Json).version
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
robocopy $repo $Target /MIR /XD .git out blind __pycache__ '*-png' /XF '~$*' publish.ps1 release-notes.ps1/R:1 /W:1 /NFL /NDL /NP /NJH | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed with exit code $LASTEXITCODE" }
# The self-serve entry points sit one level up, in Plugin/, where SCs look first.
$pluginDir = Split-Path $Target -Parent
Copy-Item (Join-Path $repo 'rollout\START-HERE.md') (Join-Path $pluginDir 'START-HERE.md') -Force
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
