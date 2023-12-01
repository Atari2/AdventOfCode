param(
    [Int32]$year = (Get-Date).Year
)

if (Get-Command cl -errorAction SilentlyContinue) {
    Write-Host "MSVC compiler already available"
}
else {
    $vsPath = &"${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationpath
    Import-Module (Get-ChildItem $vsPath -Recurse -File -Filter Microsoft.VisualStudio.DevShell.dll).FullName
    Enter-VsDevShell -VsInstallPath $vsPath -SkipAutomaticLocation -DevCmdArguments '-arch=x64'
}

Push-Location $year
Get-Content EXPECTED.lst | ForEach-Object {
    $dir, $exp_part1, $exp_part2 = $_.Split(" ")
    
    Push-Location $dir
    $part1, $part2 = (py main.py).Split(" ")
    if ($part1 -eq $exp_part1 -and $part2 -eq $exp_part2) {
        Write-Host "Python OK: $dir"
    }
    else {
        Write-Host "Python FAIL: $dir"
        Write-Host "Expected: $exp_part1 $exp_part2 but got $part1 $part2"
    }
    if (Test-Path main.c -PathType Leaf) {
        # only test the C version if it exists
        cl /nologo /O2 main.c | Out-Null
        $part1, $part2 = (.\main.exe).Split(" ")
        if ($part1 -eq $exp_part1 -and $part2 -eq $exp_part2) {
            Write-Host "C OK: $dir"
        }
        else {
            Write-Host "C FAIL: $dir"
            Write-Host "Expected: $exp_part1 $exp_part2 but got $part1 $part2"
        }
    }
    if (Test-Path main.cpp -PathType Leaf) {
        cl /nologo /O2 /EHsc main.cpp | Out-Null
        $part1, $part2 = (.\main.exe).Split(" ")
        if ($part1 -eq $exp_part1 -and $part2 -eq $exp_part2) {
            Write-Host "CPP OK: $dir"
        }
        else {
            Write-Host "CPP FAIL: $dir"
            Write-Host "Expected: $exp_part1 $exp_part2 but got $part1 $part2"
        }
    }
    Pop-Location
}

Pop-Location