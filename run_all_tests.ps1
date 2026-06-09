# Run all assembler tests and compare outputs
# Usage: Run this script from the workspace root in PowerShell:
#   powershell -ExecutionPolicy Bypass -File .\run_all_tests.ps1

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$pythonCmd = "python" # change to "python3" if needed
$assembler = Join-Path $scriptDir 'Assembler.py'

$inputs = Get-ChildItem -Path .\simpleBin -Filter 'Ex_test_*.txt' -File | Where-Object { $_.Name -notmatch '_bin|_read' }

$results = @()
$passCount = 0
$failCount = 0

foreach ($infile in $inputs) {
    $base = $infile.BaseName
    $outFile = Join-Path $scriptDir ("simpleBin\out_${base}.txt")

    Write-Host "Running: $($infile.Name) -> $([IO.Path]::GetFileName($outFile))"
    & $pythonCmd $assembler $infile.FullName $outFile

    # Determine expected file: prefer simpleBin/<base>_bin.txt, fallback to bin_s/<base>.txt
    $expected1 = Join-Path $scriptDir ("simpleBin\${base}_bin.txt")
    $expected2 = Join-Path $scriptDir ("bin_s\${base}.txt")

    if (Test-Path $expected1) { $expected = $expected1 }
    elseif (Test-Path $expected2) { $expected = $expected2 }
    else { Write-Host "  WARNING: No expected file for $base" -ForegroundColor Yellow; $results += [pscustomobject]@{Test=$base;Status='NO_EXPECTED';Expected='-';Actual=$outFile}; continue }

    # Use Windows 'fc' via cmd.exe and check its exit code to determine equality.
    $fcOutput = & cmd /c fc "$expected" "$outFile" 2>&1
    $fcExit = $LASTEXITCODE
    if ($fcExit -eq 0) {
        Write-Host "  PASS" -ForegroundColor Green
        $results += [pscustomobject]@{Test=$base;Status='PASS';Expected=$expected;Actual=$outFile}
        $passCount++
    } elseif ($fcExit -eq 1) {
        Write-Host "  FAIL" -ForegroundColor Red
        Write-Host "    Expected: $expected"
        Write-Host "    Actual:   $outFile"
        Write-Host "    Diff (side-by-side):"
        Write-Host $fcOutput
        $results += [pscustomobject]@{Test=$base;Status='FAIL';Expected=$expected;Actual=$outFile}
        $failCount++
    } else {
        Write-Host "  ERROR running fc (exit code $fcExit)" -ForegroundColor Yellow
        Write-Host $fcOutput
        $results += [pscustomobject]@{Test=$base;Status='ERROR';Expected=$expected;Actual=$outFile}
        $failCount++
    }
}

Write-Host "\nSummary: $passCount passed, $failCount failed, $($results.Count) total." -ForegroundColor Cyan

# Save a CSV report
$report = Join-Path $scriptDir 'test_report.csv'
$results | Export-Csv -Path $report -NoTypeInformation -Force
Write-Host "Report saved to $report"
