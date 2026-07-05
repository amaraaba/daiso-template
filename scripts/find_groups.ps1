$files = @(
    "output\deposits\muf_pmovi_x_s.list",
    "output\deposits\hbo_pmovi_x_s.list",
    "output\deposits\disp_pmovi_x_s.list",
    "output\deposits\memss0_pmovi_x_s.list"
)
$txt = ""
foreach ($f in $files) { $txt += [System.IO.File]::ReadAllText("$PWD\$f") }

Write-Host "--- group= values across all 173 tests ---"
[regex]::Matches($txt, 'group=(\S+)') | ForEach-Object { $_.Groups[1].Value } |
    Group-Object | Sort-Object Count -Descending | Format-Table Name, Count -AutoSize

Write-Host "--- tests with group=main ---"
$blocks = $txt -split '(?=^\[)' -split "`r?`n`r?`n"  # naive split
$mainBlocks = $blocks | Where-Object { $_ -match 'group=main' -and $_ -match 'pmovi_x_s' }
Write-Host "Count: $($mainBlocks.Count)"
$mainBlocks | ForEach-Object {
    if ($_ -match 'TEST_RENAME=replace:(\S+)') { $matches[1] }
} | Select-Object -First 30
