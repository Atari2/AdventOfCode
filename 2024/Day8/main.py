import numpy as np
from string import ascii_letters, digits
import itertools

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

all_chars = ascii_letters + digits
with open(filename, 'r') as f:
    data = np.array([list(l.strip()) for l in f.readlines()], dtype=str)

def part1():
    antinodes = set()
    for c in all_chars:
        positions = np.argwhere(data == c)
        for (x1, y1), (x2, y2) in itertools.combinations(positions, 2):
            deltax = x1 - x2
            deltay = y1 - y2
            first_antinode = (x1 + deltax, y1 + deltay)
            second_antinode = (x2 - deltax, y2 - deltay)
            if first_antinode[0] >= 0 and first_antinode[1] >= 0 and first_antinode[0] < data.shape[0] and first_antinode[1] < data.shape[1]:
                antinodes.add(first_antinode)
            if second_antinode[0] >= 0 and second_antinode[1] >= 0 and second_antinode[0] < data.shape[0] and second_antinode[1] < data.shape[1]:
                antinodes.add(second_antinode)
    return len(antinodes)

def part2():
    antinodes = set()
    for c in all_chars:
        positions = np.argwhere(data == c)
        for (x1, y1), (x2, y2) in itertools.combinations(positions, 2):
            assert x1 != x2
            assert y1 != y2
            def line_eq(x: int) -> int | None:
                res: float = ((x - x1) / (x2 - x1)) * (y2 - y1) + y1
                if res.is_integer():
                    return int(res)
                return None
            for x in range(0, data.shape[0]):
                y = line_eq(x)
                if y is not None and y >= 0 and y < data.shape[1]:
                    antinodes.add((x, y))
    return len(antinodes)



print(f'{part1()} {part2()}')