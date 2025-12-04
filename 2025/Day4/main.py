import numpy

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()


def count_adjacent_rolls(data: numpy.ndarray, pos: tuple[int, int]) -> bool:
    r, c = pos
    v = numpy.count_nonzero(data[max(0, r-1):r+2, max(0, c-1):c+2])
    return (v - 1) < 4

grid = numpy.array([list(map(lambda x: 0 if x == '.' else 1, line.strip())) for line in data], dtype=numpy.uint8)
grid_copy = grid.copy()
p1 = 0
p2 = 0
turn = 0
while True:
    found = False
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                adj = count_adjacent_rolls(grid, (r, c))
                if turn == 0:
                    p1 += adj
                p2 += adj
                if adj:
                    found = True
                    grid_copy[r][c] = 0
    turn += 1
    if not found:
        break
    grid = grid_copy.copy()
print(f'{p1} {p2}')