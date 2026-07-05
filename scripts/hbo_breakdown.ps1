$txt = [System.IO.File]::ReadAllText("$PWD\output\deposits\hbo_pmovi_x_s.list")
$tests = [regex]::Matches($txt, 'TEST_RENAME=replace:(hub_hbo\S+)') | ForEach-Object { $_.Groups[1].Value }
Write-Host "Total hbo pmovi_x_s tests: $($tests.Count)"
Write-Host ""
Write-Host "--- by config-prefix (config + array_type) ---"
$tests | ForEach-Object { ($_ -replace '_pmovi.*$','') -replace '^hub_','' } |
    Group-Object | Sort-Object Name | Format-Table Name, Count -AutoSize
Write-Host "--- by variant suffix ---"
$tests | ForEach-Object {
    if ($_ -match 'pmovi_x_s(_\w+)?$') {
        if ($matches[1]) { $matches[1].TrimStart('_') } else { 'BASE' }
    }
} | Group-Object | Sort-Object Count -Descending | Format-Table Name, Count -AutoSize
