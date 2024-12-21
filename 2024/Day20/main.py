import numpy as np

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = [line.strip() for line in f]

maze = np.array([[c for c in l] for l in data], dtype=str)

rows, cols = maze.shape

def is_valid(x: int, y: int) -> bool:
    return  x >= 0 and x < rows and y>=0 and y < cols and maze[x, y] != '#'

def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

offsets = [ (0,1),(-1,0), (0,-1), (1,0) ]

def find_path(start: tuple[int, int], end: tuple[int, int]):
    distances = {}
    current = end
    target = end
    count = 0
    while start != target:
        distances[target] = count
        count += 1
        for (xoff, yoff) in offsets:
            neighbor = (target[0]+xoff, target[1]+yoff)
            if neighbor != current and is_valid(*neighbor):
                current = target 
                target = neighbor
                break
    distances[start] = count
    return distances

start = tuple(np.argwhere(maze == 'S')[0])
end = tuple(np.argwhere(maze == 'E')[0])

distances = find_path(start, end)

part1 = 0 
part2 = 0
for p1, c1 in reversed(distances.items()):
    for p2, c2 in distances.items():
        dist = manhattan(p1, p2) 
        if dist <= 2 and c2 - c1 - dist >= 100:
            part1 += 1
        if dist <= 20 and c2 - c1 - dist >= 100:
            part2 += 1
print(f'{part1} {part2}')