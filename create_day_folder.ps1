param(
    [Int32]$year = (Get-Date).Year,
    [Int32]$day = (Get-Date).Day,
    [Switch]$cpp = $false
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
if ($cpp) {
    New-Item -Path . -Name "main.cpp" -ItemType "file"
}

$prelude_py = @"
SAMPLE_DATA: bool = True
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()
"@

$prelude_cpp = @"
#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>
#include <cstdio>
#include <unordered_map>
#include <numeric>
#include <print>

namespace r = std::ranges;
namespace v = std::ranges::views;
using namespace std::string_view_literals;

constexpr bool SAMPLE_DATA = true;

std::vector<std::string> read_file(std::string_view filename) {
    std::ifstream file(filename.data());
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);

}
"@

Set-Content -Path ".\main.py" -Value $prelude_py
if ($cpp) {
    Set-Content -Path ".\main.cpp" -Value $prelude_cpp
}