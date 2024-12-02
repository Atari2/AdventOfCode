# Advent of Code

This repository contains my solutions to the [Advent of Code](https://adventofcode.com/) challenges.

The solutions are written in a mix of Python, C and C++, and their correctness is verified by the provided test cases.

The solutions are not meant to be the fastest, most elegant, most efficient or anything of the sort. They are just my solutions to the challenges, and their main goal is to be correct and (expecially with the C++ solutions) to experiment with new features of the language. So keep this in mind while reading the code. Sometimes solutions are golfed, sometimes they are silly, verbose or weird, because the primary goal is to have fun while writing them.

The repo is organized in folders, one for each year, and each year folder contains a folder for each day of the challenge. Each day folder contains the solutions to the two parts of the challenge, and the input file used to test them.

2021 was the first year I partecipated in the challenge and I didn't have a specified workflow so that specific folder doesn't follow the same structure as the others, it's just there to preserve the solutions I wrote.

The years are not complete, when I give up depends on how busy I am, how much I enjoy the challenges, how much I feel like writing code in my free time and how complex they are. I don't have a specific goal in mind, I just do it for fun until I don't feel like doing it anymore.

## Running the solutions

### Requirements (running the provided powershell script)
> If you want to run the solutions manually you don't need any of this, instead you need the requirements listed [here](#requirements-running-the-solutions-manually)
- Windows operating system (10 or above)
- Python 3.11 or above
- Visual Studio 2022 Preview with the C++ workload installed, a version new enough to support C++23 features (e.g. 17.13.0 Preview 1.0)
- Powershell 7

### Steps
- Clone the repository
- Open a Powershell terminal
- Run `.\run_all.ps1 -year <year>` to run all the solutions for a specific year, if omitted the script will run the solutions for the current year, if the year is not present in the repository the script will exit with an error, 2021 is not supported because it doesn't follow the same structure as the other years as mentioned above.

### Requirements (running the solutions manually)
- Python 3.11 or above (for the python solutions)
- A C compiler that supports C99 (for the C solutions)
- A C++ compiler + standard library that support most C++23 features (specifically, [__cpp_lib_ranges](https://en.cppreference.com/w/cpp/feature_test#cpp_lib_ranges) needs to be `202207L`) (for the C++ solutions), for example:
    - Visual Studio 2022 Preview (17.13.0 Preview 1.0 or above)
    - GCC 14.1 or above
    - Clang 19.1.0 or above

