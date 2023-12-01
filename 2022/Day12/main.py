from __future__ import annotations
import itertools
import sys
from typing import Literal

SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename, 'r') as f:
    data = f.read().splitlines()

class Node:
    height: int
    neighbors: list[Node]
    distance: float

    def __init__(self, height: int):
        self.height = height
        self.neighbors = []
        self.distance = sys.maxsize
    
    def is_start(self) -> bool:
        return False
    def is_end(self) -> bool:
        return False
    
    def _add_check(self, node: Node):
        if node.height <= self.height + 1:
            self.neighbors.append(node)

    def add_neighbors(self, grid: list[list[Node]], i: int, j: int):
        if i > 0:
            self._add_check(grid[i - 1][j])
        if i < len(grid) - 1:
            self._add_check(grid[i + 1][j])
        if j > 0:
            self._add_check(grid[i][j - 1])
        if j < len(grid[i]) - 1:
            self._add_check(grid[i][j + 1])

class Start(Node):

    def __init__(self, height: int):
        super().__init__(height)
        self.distance = 0

    def is_start(self) -> bool:
        return True

class End(Node):

    def is_end(self) -> bool:
        return True


def make_node(c: str) -> Node|Start|End:
    if c == 'E':
        return End(25)
    elif c == 'S':
        return Start(0)
    else:
        return Node(ord(c) - ord('a'))

def dijsktra(grid: list[list[Node]], part: Literal[1, 2]):
    q: list[Node] = list(itertools.chain.from_iterable(grid))
    if part == 2:
        for n in q:
            if n.height == 0:
                n.distance = 0
    q.sort(key=lambda x: x.distance)
    end = next(filter(lambda n: n.is_end(), q))
    while len(q) > 0:
        u = q[0]
        q = q[1:]
        if u.is_end():
            break
        if u.distance == -1:
            break
        for n in u.neighbors:
            alt = u.distance + 1
            if alt < n.distance:
                n.distance = alt
                q.sort(key=lambda x: x.distance)
    return end.distance

grid = [[make_node(c) for c in line] for line in data]
for i in range(len(grid)):
    for j in range(len(grid[i])):
        grid[i][j].add_neighbors(grid, i, j)
part1 = dijsktra(grid, 1)
part2 = dijsktra(grid, 2)
print(part1, part2)