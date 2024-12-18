import numpy as np
from collections import deque
import sys

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

GRID_SIZE = 6+1 if SAMPLE_DATA else 70+1
NUM_FALLING_BYTES = 12 if SAMPLE_DATA else 1024

with open(filename, 'r') as f:
    data = [tuple(map(int, line.split(','))) for line in f]

grid = np.full((GRID_SIZE, GRID_SIZE), 0, dtype=np.uint8)

def shortest_path(start, end):
    rows, cols = grid.shape
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    queue = deque([(start, 0)])
    visited = set()
    visited.add(start)

    while queue:
        (current_row, current_col), steps = queue.popleft()
        if (current_row, current_col) == end:
            return steps
        for row_offset, col_offset in directions:
            neighbor_row = current_row + row_offset
            neighbor_col = current_col + col_offset
            neighbor = (neighbor_row, neighbor_col)

            if (0 <= neighbor_row < rows and 0 <= neighbor_col < cols and
                neighbor not in visited and 
                grid[neighbor_row, neighbor_col] == 0): 

                visited.add(neighbor)
                queue.append((neighbor, steps + 1))

    return -1

starting_position = (0, 0)
ending_position = (GRID_SIZE - 1, GRID_SIZE - 1)
fallen_bytes = data[:NUM_FALLING_BYTES]
rest = data[NUM_FALLING_BYTES:]
for x, y in fallen_bytes:
    grid[y, x] = 1
part1 = shortest_path(starting_position, ending_position)
for x, y in rest:
    grid[y, x] = 1
    if shortest_path(starting_position, ending_position) == -1:
        part2 = f'{x},{y}'
        break
print(f'{part1} {part2}')