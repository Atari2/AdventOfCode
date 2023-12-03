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

def get_schem_nums(
    data: numpy.ndarray,
) -> tuple[int, dict[tuple[int, int], list[int]]]:
    schem_nums = 0
    gears: dict[tuple[int, int], list[int]] = {}
    rows, cols = data.shape
    accum = ""
    start_pos = None
    is_to_include = False
    gear_point = []
    for x in range(rows):
        for y in range(cols):
            if data[x, y].isdigit():
                for dx, dy in adjacency_list:
                    if (
                        0 <= x + dx < rows
                        and 0 <= y + dy < cols
                        and is_symbol(data[x + dx, y + dy])  # type: ignore
                    ):
                        if data[x + dx, y + dy] == "*":
                            gear_point.append((x + dx, y + dy))
                        is_to_include = True
                if accum == "":
                    start_pos = (x, y)
                accum += data[x, y]
            else:
                if accum != "" and start_pos is not None:
                    if is_to_include:
                        num = int(accum)
                        schem_nums += num
                        for point in gear_point:
                            if point not in gears:
                                gears[point] = []
                            if num not in gears[point]:
                                gears[point].append(num)
                    accum = ""
                    start_pos = None
                    is_to_include = False
                    gear_point.clear()
        if accum != "" and start_pos is not None:
            if is_to_include:
                num = int(accum)
                schem_nums += num
                for point in gear_point:
                    if point not in gears:
                        gears[point] = []
                    if num not in gears[point]:
                        gears[point].append(num)
            accum = ""
            start_pos = None
            is_to_include = False
            gear_point.clear()
    return schem_nums, gears

totalp1, gears = get_schem_nums(data)
totalp2 = sum(
    adjacent_nums[0] * adjacent_nums[1]
    for adjacent_nums in gears.values()
    if len(adjacent_nums) == 2
)
print(f"{totalp1} {totalp2}")
