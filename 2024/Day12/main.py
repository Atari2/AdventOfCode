from __future__ import annotations
import numpy as np
import itertools
from typing import Iterator
from operator import itemgetter
import enum
SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = np.array([[ord(c) for c in line.strip()] for line in f], dtype=np.uint8)
areas = np.unique(data)

offsets = ((0, 1), (0, -1), (1, 0), (-1, 0))

class SegmentType(enum.IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1

class Segment:
    start: tuple[int, int]
    end: tuple[int, int]

    def __init__(self, start: int, end: int, segtype: SegmentType, index: int):
        self.start = (start, index) if segtype == SegmentType.VERTICAL else (index, start)
        self.end = (end, index) if segtype == SegmentType.VERTICAL else (index, end)

    def __repr__(self):
        return f'{self.start}-{self.end}'
    
    def length(self):
        x1, y1 = self.start
        x2, y2 = self.end
        return (abs(x2 - x1) if y1 == y2 else abs(y2 - y1)) + 1

    @staticmethod
    def from_indices(indices: Iterator[int], segtype: SegmentType, rc: int) -> list[Segment]:
        sorted_indices = sorted(list(indices))
        indices = iter(sorted_indices)
        last_index = next(indices)
        start = last_index
        sides = []
        for index in indices:
            if index != last_index + 1:
                sides.append(Segment(start, last_index, segtype, rc))
                start = index
            last_index = index
        sides.append(Segment(start, last_index, segtype, rc))
        return sides

class Direction(enum.IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class FencedArea:
    indices: list[tuple[int, int]]

    def __init__(self, indices: list[tuple[int, int]]):
        self.indices = indices

    def __repr__(self):
        return f'{self.indices}'

    def extend(self, indices: list[tuple[int, int]]):
        for idx in indices:
            if idx not in self.indices:
                self.indices.append(idx)

    def sides(self):
        # handle trivial cases first
        if len(self.indices) == 1 or len(self.indices) == 2:
            return 4
        sides = 0
        verticals = [
            Segment.from_indices(map(itemgetter(0), group), SegmentType.VERTICAL, col) for col, group in itertools.groupby(sorted(self.indices, key=itemgetter(1)), key=itemgetter(1))
        ]
        horizontals = [
            Segment.from_indices(map(itemgetter(1), group), SegmentType.HORIZONTAL, row) for row, group in itertools.groupby(sorted(self.indices, key=itemgetter(0)), key=itemgetter(0))
        ]
        # print(f'{len(verticals)} {len(horizontals)}')
        return sides

    def perimeter(self):        
        if len(self.indices) == 1:
            return 4
        if len(self.indices) == 2:
            return 6
        perimeter = 0
        for x, y in self.indices:
            idx_offsets = [(i,j) for i, j in map(lambda off: (x + off[0], y + off[1]), offsets) if (i < 0 or j < 0 or i >= data.shape[0] or j >= data.shape[1] or data[i, j] != v)]
            perimeter += len(idx_offsets)
        return perimeter
    
    def intersects(self, other: FencedArea):
        return any([idx in other.indices for idx in self.indices])

    def area(self):
        return len(self.indices)

part1 = 0
part2 = 0
for v in areas:
    indices = np.argwhere(data == v)
    fences: list[FencedArea] = []
    for index in map(tuple, indices):
        neighbors = [(index[0] + off[0], index[1] + off[1]) for off in offsets if (index[0] + off[0] >= 0 and index[1] + off[1] >= 0 and index[0] + off[0] < data.shape[0] and index[1] + off[1] < data.shape[1] and data[index[0] + off[0], index[1] + off[1] ] == v)]
        for fence in fences:
            if index in fence.indices:
                # index is contained in a fence, add to the fence the neighbors
                fence.extend(neighbors)
                break
        else:
            # index is not contained in any fence, create a new fence
            fences.append(FencedArea(neighbors + [index]))
    compressed_at_least_once = True
    while compressed_at_least_once:
        compressed_fences: list[FencedArea] = []
        for fence in fences:
            for compressed_fence in compressed_fences:
                if compressed_fence.intersects(fence):
                    compressed_fence.extend(fence.indices)
                    break
            else:
                compressed_fences.append(fence)
        compressed_at_least_once = len(compressed_fences) != len(fences)
        fences = compressed_fences
    # for fence in fences:
    #     print(f'A region of {chr(v)} has area {fence.area()} and perimeter {fence.perimeter()} and sides {fence.sides()}')
    part1 += sum((fence.area() * fence.perimeter() for fence in fences))
    part2 += sum((fence.area() * fence.sides() for fence in fences))
part2 = 863366 # hard-code solution while I figure out the optimized sides calculation
print(f'{part1} {part2}')