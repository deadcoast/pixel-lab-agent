$ErrorActionPreference = 'Stop'
$evidenceRoot = [System.IO.Path]::GetFullPath($PSScriptRoot)
$receiptPath = Join-Path $evidenceRoot 'old-profile-cleanup.json'
if (Test-Path -LiteralPath $receiptPath) { throw 'Do not overwrite a cleanup receipt.' }
$temporaryRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath()).TrimEnd('\')
$rows = @()
foreach ($consumerName in @('codex-01', 'claude-01')) {
    foreach ($domain in @('terrain', 'animation')) {
        $capture = Join-Path $evidenceRoot "$consumerName/old-kit/$domain/output/capture"
        $launch = Get-Content -LiteralPath (Join-Path $capture 'launch.json') -Raw | ConvertFrom-Json
        $execution = Get-Content -LiteralPath (Join-Path $capture 'execution.json') -Raw | ConvertFrom-Json
        $argument = @($launch.args | Where-Object { $_.StartsWith('--user-data-dir=') })
        if ($argument.Count -ne 1) { throw 'Expected one exact retained browser profile argument.' }
        $profile = [System.IO.Path]::GetFullPath($argument[0].Substring('--user-data-dir='.Length))
        $expectedPrefix = if ($domain -eq 'terrain') { 'pixl-tiles-' } else { 'pixl-animation-' }
        if ([System.IO.Path]::GetDirectoryName($profile) -ne $temporaryRoot -or
            -not [System.IO.Path]::GetFileName($profile).StartsWith($expectedPrefix)) {
            throw "Refuse cleanup outside the exact generated temporary profile: $profile"
        }
        $owners = @(Get-CimInstance Win32_Process | Where-Object {
            $_.CommandLine -and $_.CommandLine.Contains("--user-data-dir=$profile")
        })
        if ($owners.Count -ne 0) { throw "Retained profile still has a live owner: $profile" }
        $existed = Test-Path -LiteralPath $profile
        if ($existed) {
            $item = Get-Item -LiteralPath $profile -Force
            if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) { throw 'Refuse redirected profile.' }
            if ([System.IO.Path]::GetFullPath($item.FullName) -ne $profile) { throw 'Resolved profile identity changed.' }
            Remove-Item -LiteralPath $profile -Recurse -Force
        }
        $rows += [ordered]@{consumer=$consumerName; domain=$domain; browser_pid=$execution.browser_pid;
            profile=$profile; live_exact_profile_owners=0; existed=$existed;
            removed_or_already_absent=(-not (Test-Path -LiteralPath $profile))}
    }
}
[ordered]@{version=1; scope='Follow-up cleanup of exact profiles from retained failed old-kit attempts';
    recorded_at=[DateTime]::UtcNow.ToString('o'); old_failure_receipts_unchanged=$true;
    process_kills=0; profiles=$rows} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $receiptPath -Encoding utf8
Get-Content -LiteralPath $receiptPath -Raw
