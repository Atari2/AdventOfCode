param(
    [Int32]$year = (Get-Date).Year
)

if (-not ($IsWindows)) {
    Write-Host "This script is only supported on Windows"
    exit 1
}

if (-not (Test-Path $year)) {
    Write-Host "Directory $year does not exist"
    exit 1
}

if (Get-Command py -ErrorAction SilentlyContinue) {
    $version = [System.Version](py --version).Split(" ")[1]
    if ($version -le [System.Version]"3.11") {
        Write-Host "Python version $version is not supported, please install Python 3.11 or above"
        exit 1
    }
    py -c "import numpy" | Out-Null     # check for numpy
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Numpy found"
    }
    else {
        Write-Host "Numpy not found, please install numpy"
        exit 1
    }
    Write-Host "Python version $version found"
}
else {
    Write-Host "Python not found, please install Python 3.11 or above"
    exit 1
}

if (Get-Command cl -ErrorAction SilentlyContinue) {
    Write-Host "MSVC compiler already available"
}
else {
    if (-not (Test-Path "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe")) {
        Write-Host "Visual Studio not found, please install Visual Studio 2022 Preview with the C++ workload"
        exit 1
    }
    $vsPath = &"${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" -prerelease -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationpath
    $commonLocation = "$vsPath\Common7\Tools\Microsoft.VisualStudio.DevShell.dll"
    if (Test-Path $commonLocation) {
        $dllPath = $commonLocation
    } else {
        $dllPath = (Get-ChildItem $vsPath -Recurse -File -Filter Microsoft.VisualStudio.DevShell.dll).FullName
    }
    Import-Module -Force $dllPath
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
        Remove-Item -ErrorAction SilentlyContinue .\main.exe
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
        Remove-Item -ErrorAction SilentlyContinue .\main.exe
        cl /nologo /O2 /EHsc /std:c++latest main.cpp | Out-Null
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