from __future__ import annotations
import numpy as np
import enum
from functools import cached_property
SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = np.array([[ord(c) for c in line.strip()] for line in f], dtype=np.uint8)
areas = np.unique(data)

offsets = ((0, 1), (0, -1), (1, 0), (-1, 0))
class VertexAngle(enum.IntEnum):
    TL = 0
    TR = 1
    BL = 2
    BR = 3


class Vertex:
    original_point: tuple[int, int]
    point: tuple[float, float]
    _count: int | None

    def __init__(self, point: tuple[int, int], angle: VertexAngle):
        self.original_point = point
        match angle:
            case VertexAngle.TL:
                self.point = (point[0] - 0.5, point[1] - 0.5)
            case VertexAngle.TR:
                self.point = (point[0] - 0.5, point[1] + 0.5)
            case VertexAngle.BL:
                self.point = (point[0] + 0.5, point[1] - 0.5)
            case VertexAngle.BR:
                self.point = (point[0] + 0.5, point[1] + 0.5)

    def count(self, neighbors: list[Vertex]) -> int:
        nlen = len(neighbors) + 1
        if nlen == 2:
            diff = np.subtract(self.original_point, neighbors[0].original_point)
            if np.all(diff != 0):
                return 2
            else:
                return 0
        if nlen == 1 or nlen == 3:
            return 1
        return 0
    
    def __hash__(self):
        return hash(self.point)
    
    def __eq__(self, other: Vertex):
        return self.point == other.point


class FencedArea:
    indices: list[tuple[int, int]]

    def __init__(self, indices: list[tuple[int, int]]):
        self.indices = indices

    def extend(self, indices: list[tuple[int, int]]):
        for idx in indices:
            if idx not in self.indices:
                self.indices.append(idx)

    def sides(self):
        if len(self.indices) == 1 or len(self.indices) == 2:
            return 4
        vertices: dict[Vertex, list[Vertex]] = {}
        for index in self.indices:
            for v in (
                Vertex(index, VertexAngle.TL),
                Vertex(index, VertexAngle.TR),
                Vertex(index, VertexAngle.BL),
                Vertex(index, VertexAngle.BR)
            ):
                if (e := vertices.get(v)) is not None:
                    e.append(v)
                else:
                    vertices[v] = []
        sides = sum((vertex.count(neighbors) for vertex, neighbors in vertices.items()))
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
    part1 += sum((fence.area() * fence.perimeter() for fence in fences))
    part2 += sum((fence.area() * fence.sides() for fence in fences))
print(f'{part1} {part2}')