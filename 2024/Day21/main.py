from functools import cache

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, "r") as f:
    codes = f.read().split()

numpad: dict[str, complex] = {
    "7": 0 + 0j,
    "8": 1 + 0j,
    "9": 2 + 0j,
    "4": 0 + 1j,
    "5": 1 + 1j,
    "6": 2 + 1j,
    "1": 0 + 2j,
    "2": 1 + 2j,
    "3": 2 + 2j,
    " ": 0 + 3j,
    "0": 1 + 3j,
    "A": 2 + 3j,
}

robot: dict[str, complex] = {
    " ": 0 + 0j, 
    "^": 1 + 0j, 
    "A": 2 + 0j, 
    "<": 0 + 1j, 
    "v": 1 + 1j, 
    ">": 2 + 1j
}

@cache
def path(start: str, end: str) -> str:
    pad = numpad if (start in numpad and end in numpad) else robot
    diff = pad[end] - pad[start]
    dx, dy = int(diff.real), int(diff.imag)
    yy = "^" * -dy if dy < 0 else "v" * dy
    xx = "<" * -dx if dx < 0 else ">" * dx
    bad = pad[" "] - pad[start]
    prefer_yy_first = (dx > 0 or bad == dx) and bad != dy * 1j
    return (yy + xx if prefer_yy_first else xx + yy) + "A"


@cache
def length(code: str, depth: int, s: int = 0) -> int:
    if depth == 0:
        return len(code)
    for i, c in enumerate(code):
        s += length(path(code[i - 1], c), depth - 1)
    return s

part1 = sum(int(code[:-1]) * length(code, 3) for code in codes)
part2 = sum(int(code[:-1]) * length(code, 26) for code in codes)
print(f'{part1} {part2}')