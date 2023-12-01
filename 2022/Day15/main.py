from __future__ import annotations
import re
import numpy

in_patt = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', re.MULTILINE)

SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename, 'r') as f:
    data = f.read()

class Range:
    s: int
    e: int

    def __init__(self, s: int, e: int):
        self.s = s
        self.e = e
    
    def __str__(self):
        return f"Range({self.s}, {self.e})"
    
    def __repr__(self):
        return self.__str__()
    
    def intersect(self, other: Range):
        if self.s <= other.s <= self.e:
            return True
        if self.s <= other.e <= self.e:
            return True
        if other.s <= self.s <= other.e:
            return True
        if other.s <= self.e <= other.e:
            return True
        return False

    @staticmethod
    def merge(r1: Range, r2: Range) -> Range:
        return Range(min(r1.s, r2.s), max(r1.e, r2.e))

class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

def md(a: Point, b: Point):
    return abs(a.x - b.x) + abs(a.y - b.y)

class Sensor(Point):
    beacon: Point
    area: tuple[Point, Point]

    def __init__(self, x: int, y: int, beacon: Point):
        super().__init__(x, y)
        self.beacon = beacon
        dist = md(self, beacon)
        v3 = Point(self.x, self.y - dist)
        v4 = Point(self.x, self.y + dist)
        self.area = (v3, v4)

    def intersects_row(self, row: int) -> Range|None:
        if self.y <= row <= self.area[1].y:
            diff = self.area[1].y - row
            vp = self.area[1]
        elif self.area[0].y <= row <= self.y:
            diff = self.area[0].y - row
            vp = self.area[0]
        else:
            return None
        occupies = (diff * 2) + 1
        x1 = vp.x - (occupies // 2)
        x2 = vp.x + (occupies // 2)
        startx, endx = (x1, x2) if x1 < x2 else (x2, x1)
        return Range(startx, endx)
    
    def __str__(self):
        return f"Sensor({self.x}, {self.y}, {self.beacon}, {self.area})"
    
    def __repr__(self):
        return self.__str__()

def _reduce_ranges(points: list[Range]) -> tuple[list[Range], int]:
    reduced: list[Range] = []
    reduced_by = 0
    merged_indexes = numpy.zeros(len(points), dtype=bool)
    for i in range(len(points)):
        if merged_indexes[i]:
            continue
        r1 = points[i]
        merged_range: None|Range = None
        for j in range(i + 1, len(points)):
            if merged_indexes[j]:
                continue
            r2 = points[j]
            if r1.intersect(r2):
                merged_range = Range.merge(r1, r2)
                merged_indexes[i] = True
                merged_indexes[j] = True
                reduced_by += 1
                break
        if merged_range:
            reduced.append(merged_range)
        else:
            reduced.append(r1)
    return reduced, reduced_by

def reduce_ranges(points: list[Range]) -> list[Range]:
    points.sort(key=lambda r: r.s)
    while (red := _reduce_ranges(points))[1] > 0:
        points = red[0]
    return points

def create_intersect_ranges(sensors: list[Sensor], row: int) -> list[Range]:
    intersect_ranges: list[Range] = []
    for s in sensors:
        if i := s.intersects_row(row):
            intersect_ranges.append(i)
    return reduce_ranges(intersect_ranges)

sensors: list[Sensor] = []
for m in in_patt.finditer(data):
    sensor = Sensor(int(m.group(1)), int(m.group(2)), Point(int(m.group(3)), int(m.group(4))))
    sensors.append(sensor)

# part1
intersect_ranges: list[Range] = []
row_to_search = 10 if SAMPLE_DATA else 2_000_000
intersect_ranges = create_intersect_ranges(sensors, row_to_search)
min_x = min(map(lambda r: r.s, intersect_ranges))
max_x = max(map(lambda r: r.e, intersect_ranges))
part1 = abs(min_x) + max_x

# part2
if SAMPLE_DATA:
    y_range = (0, 20)
else:
    y_range = (0, 4_000_000)
part2 = 0
r = y_range[0]
while r < y_range[1]:
    p = create_intersect_ranges(sensors, r)
    if len(p) > 1:
        part2 = (p[0].e + 1)*4000000 + r
        break
    r += 1
print(part1, part2)