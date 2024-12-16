import numpy as np
import sys
import itertools
from heapq import heappop, heappush

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = [line.strip() for line in f]

maze = np.array([[c for c in l] for l in data], dtype=str)
start_tile = tuple(np.argwhere(maze == 'S')[0])
end_tile = tuple(np.argwhere(maze == 'E')[0])

def find_shortest_path(start: tuple[int, int], end: tuple[int, int], start_direction: str) -> tuple[int, list[list[tuple[int, int]]]]:
    rows, cols = maze.shape
    directions = {
        'N': [
            (-1, 0, 'N'),  # North
            (0, 1, 'E'),   # East
            (0, -1, 'W')   # West
        ],
        'S': [
            (1, 0, 'S'),   # South
            (0, -1, 'W'),  # West
            (0, 1, 'E')    # East
        ],
        'W': [
            (0, -1, 'W'),  # West
            (-1, 0, 'N'),  # North
            (1, 0, 'S')    # South
        ],
        'E': [
            (0, 1, 'E'),   # East
            (1, 0, 'S'),   # South
            (-1, 0, 'N')   # North
        ]
    }
    pq = []
    heappush(pq, (0, start[0], start[1], start_direction, []))
    visited = {}
    min_cost = sys.maxsize
    all_paths = []
    while pq:
        cost, row, col, prev_orientation, path = heappop(pq)
        path = path + [(row, col)]
        if (row, col) == end:
            if cost < min_cost:
                min_cost = cost
                all_paths = [path]
            elif cost == min_cost:
                all_paths.append(path)
            continue
        if visited.get((row, col, prev_orientation), sys.maxsize) < cost: 
            continue
        visited[(row, col, prev_orientation)] = cost
        for dr, dc, orientation in directions[prev_orientation]:
            new_row, new_col = row + dr, col + dc
            if not (0 <= new_row < rows and 0 <= new_col < cols) or maze[new_row, new_col] == '#':
                continue
            turning_cost = 0 if prev_orientation == orientation else 1000
            heappush(pq, (cost + 1 + turning_cost, new_row, new_col, orientation, path))
    return (min_cost, all_paths)

part1, paths = find_shortest_path(start_tile, end_tile, 'E')
part2 = len(set(itertools.chain.from_iterable(paths)))

print(f'{part1} {part2}')