from __future__ import annotations
import numpy as np
SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = np.array([list(map(int, iter(line.strip()))) for line in f], dtype=int)

directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

def generate_neighbours(x, y):
    for dx, dy in directions:
        if 0 <= x + dx < data.shape[0] and 0 <= y + dy < data.shape[1]:
            yield x + dx, y + dy

MAX_HEIGHT = 9

class Node:
    value: int
    neighbors: list[Node]
    pos: tuple[int, int]

    def __init__(self, x, y):
        self.pos = (x, y)
        if data[x, y] == MAX_HEIGHT:
            self.value = MAX_HEIGHT
        else:
            self.value = data[x, y]

    def populate_neighbors(self, nodes: list[list[Node]]):
        if self.value == MAX_HEIGHT:
            self.neighbors = []
        else:
            self.neighbors = [nodes[nx][ny] for nx, ny in generate_neighbours(*self.pos) if data[nx, ny] == self.value + 1]
    
    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other: Node):
        return self.pos == other.pos

nodes = [[Node(x, y) for y in range(data.shape[1])] for x in range(data.shape[0])]
[node.populate_neighbors(nodes) for row in nodes for node in row]
starting_nodes = [node for row in nodes for node in row if node.value == 0]
ending_nodes = [node for row in nodes for node in row if node.value == MAX_HEIGHT]

def find_all_paths(node: Node, ending_node: Node, visited: set[Node]) -> int:
    if node.pos == ending_node.pos:
        return 1
    visited.add(node)
    tot = 0
    for neighbor in node.neighbors:
        if neighbor not in visited:
            tot += find_all_paths(neighbor, ending_node, visited)
    visited.remove(node)
    return tot

tot_score, tot_rating = 0, 0
for start in starting_nodes:
    for end in ending_nodes:
        rating = find_all_paths(start, end, set())
        tot_score += 1 if rating != 0 else 0
        tot_rating += rating
print(f'{tot_score} {tot_rating}')