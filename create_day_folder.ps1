param(
    [Int32]$year = (Get-Date).Year,
    [Int32]$day = (Get-Date).Day
)
$dir_name = $year.ToString() + "\\Day" + $day.ToString()
if (Test-Path $dir_name) {
    Write-Host "Directory already exists"
    exit 1
}
mkdir $dir_name
Set-Location $dir_name
New-Item -Path . -Name "sample_data.txt" -ItemType "file"
New-Item -Path . -Name "data.txt" -ItemType "file"
New-Item -Path . -Name "main.py" -ItemType "file"

$prelude = @"
SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()
"@

Set-Content -Path ".\main.py" -Value $prelude