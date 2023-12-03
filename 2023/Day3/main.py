from __future__ import annotations
import numpy
import functools

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


def is_symbol(c: str) -> bool:
    return not (c.isdigit() or c == ".")

def is_gear(c: str, adjacent_nums: list[SchemNum]) -> bool:
    return c == "*" and len(adjacent_nums) == 2

with open(filename, "r") as f:
    lines = f.read().splitlines()
data = numpy.array([list(line) for line in lines])

adjacency_list = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


class SchemNum:
    value: int
    pos_begin: tuple[int, int]
    pos_end: tuple[int, int]
    _h_pos: int

    def __init__(
        self, value: int, pos_begin: tuple[int, int], pos_end: tuple[int, int]
    ):
        self.value = value
        self.pos_begin = pos_begin
        self.pos_end = pos_end
        self._h_pos = self.pos_begin[0] * data.shape[1] + self.pos_begin[1]

    def is_adjacent(self, point: tuple[int, int]) -> bool:
        xb, yb = self.pos_begin
        xe, ye = self.pos_end
        for y in range(yb, ye + 1):
            if any(
                (xb + dx, y + dy) == point
                for dx, dy in adjacency_list
            ):
                return True
        return False

    def __hash__(self):
        return self._h_pos

    def __repr__(self):
        return f"SchemNum({self.value}, {self.pos_begin} -> {self.pos_end})"


def get_schem_nums(data: numpy.ndarray) -> list[SchemNum]:
    schem_nums = []
    rows, cols = data.shape
    accum = ""
    start_pos = None
    end_pos = None
    for x in range(rows):
        for y in range(cols):
            if data[x, y].isdigit():
                if accum == "":
                    start_pos = (x, y)
                accum += data[x, y]
            else:
                if accum != "" and start_pos is not None:
                    end_pos = (x, y - 1)
                    schem_nums.append(SchemNum(int(accum), start_pos, end_pos))
                    accum = ""
                    start_pos = None
                    end_pos = None
        if accum != "" and start_pos is not None:
            end_pos = (x, cols - 1)
            schem_nums.append(SchemNum(int(accum), start_pos, end_pos))
            accum = ""
            start_pos = None
            end_pos = None
    return schem_nums


schem_nums = get_schem_nums(data)

totalp2 = 0
numsp1 = set()
for x, y in numpy.ndindex(data.shape):
    if is_symbol(data[x, y]):
        adjacent_nums = list(filter(lambda n: n.is_adjacent((x, y)), schem_nums))
        for num in adjacent_nums:
            numsp1.add(num)
        if is_gear(data[x, y], adjacent_nums):
            gear_ratio = functools.reduce(lambda a, b: a * b, (num.value for num in adjacent_nums))
            totalp2 += gear_ratio

totalp1 = sum(num.value for num in numsp1)

print(f"{totalp1} {totalp2}")
