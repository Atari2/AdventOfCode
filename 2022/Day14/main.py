from __future__ import annotations
import re

patt = re.compile(r"(\d+),(\d+)(?: ->)?")

SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename, "r") as f:
    data = f.read().splitlines()


class Point:
    x: int
    y: int
    _cache_hash: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self._cache_hash = hash((self.x, self.y))

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"Point({self.x},{self.y})"

    def __eq__(self, other: Point):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self._cache_hash

class Path:
    _path: list[Point]

    def __init__(self, path: str):
        ms = patt.finditer(path)
        self._path = []
        for m in ms:
            self._path.append(Point(int(m.group(1)), int(m.group(2))))

    def __str__(self):
        return str(self._path)

    def __repr__(self):
        return f'Path({" -> ".join([str(p) for p in self._path])})'

    def min_x(self):
        return min([p.x for p in self._path])

    def max_x(self):
        return max([p.x for p in self._path])

    def min_y(self):
        return min([p.y for p in self._path])

    def max_y(self):
        return max([p.y for p in self._path])

    def normalize(self, min_x: int):
        for p in self._path:
            p.x -= min_x

    def draw(self, grid: list[list[str]]):
        for p1, p2 in zip(self._path[:-1], self._path[1:]):
            if p1.x == p2.x:
                s = min(p1.y, p2.y)
                e = max(p1.y, p2.y)
                for y in range(s, e + 1):
                    grid[y][p1.x] = "#"
            else:
                s = min(p1.x, p2.x)
                e = max(p1.x, p2.x)
                for x in range(s, e + 1):
                    grid[p1.y][x] = "#"
        return grid

def move_sand_part1(grid: list[list[str]], sand: Point) -> bool:
    while True:
        try:
            b = grid[sand.y + 1][sand.x]
            bl = grid[sand.y + 1][sand.x - 1]
            br = grid[sand.y + 1][sand.x + 1]
        except IndexError:
            return False
        if b == '.':
            sand.y += 1
        elif bl == '.':
            sand.x -= 1
            sand.y += 1
        elif br == '.':
            sand.x += 1
            sand.y += 1
        else:
            grid[sand.y][sand.x] = 'o'
            return True

def move_sand_part2(sand: Point, occupied_points: set[Point], max_depth: int) -> bool:
    depth = 0
    while depth < max_depth - 2:
        b = Point(sand.x, sand.y + 1)
        bl = Point(sand.x - 1, sand.y + 1)
        br = Point(sand.x + 1, sand.y + 1)
        if b in occupied_points:
            if bl in occupied_points:
                if br in occupied_points:
                    occupied_points.add(sand)
                    return True if depth > 0 else False
                else:
                    sand = br
            else:
                sand = bl
        else:
            sand = b
        depth += 1
    occupied_points.add(sand)
    return True

paths = [Path(line) for line in data]
min_x = min([p.min_x() for p in paths])
max_x = max([p.max_x() for p in paths]) - min_x
max_y = max([p.max_y() for p in paths])
for p in paths:
    p.normalize(min_x)
grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
for p in paths:
    grid = p.draw(grid)

# part 1
part1 = 0
while move_sand_part1(grid, Point(500 - min_x, 0)):
    part1 += 1

# part 2
grid.append(['.' for _ in range(len(grid[0]))])
grid.append(['#' for _ in range(len(grid[0]))])
occupied_points = set()
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == '#':
            occupied_points.add(Point(j, i))
part2 = 0
while move_sand_part2(Point(500 - min_x, 0), occupied_points, len(grid)):
    part2 += 1
print(part1, part2+1)