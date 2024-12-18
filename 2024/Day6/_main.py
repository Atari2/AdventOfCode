import numpy as np

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = np.array([list(l.strip()) for l in f.readlines()], dtype=str)

direction_map = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}
turn_map = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^'
}

def pos_in_bounds(new_pos) -> bool:
    return new_pos[0] >= 0 and new_pos[0] < data.shape[0] and new_pos[1] >= 0 and new_pos[1] < data.shape[1]

starting_pos = tuple(np.argwhere(data == '^')[0])
def part1(data):
    current_dir = '^'
    current_pos = tuple(starting_pos)
    while True:
        direction = direction_map[current_dir]
        data[*current_pos] = 'X'
        new_pos = np.add(current_pos, direction)
        if not pos_in_bounds(new_pos):
            break
        if data[*new_pos] != '#':
            current_pos = new_pos
        else:
            current_dir = turn_map[current_dir]
        data[*current_pos] = current_dir

    return np.count_nonzero(data == 'X')

# FIXME: brute-force solution, could be optimized, currently takes too long to make it run on CI.
def part2(data):
    loops = 0
    obstacles_possible_pos = np.argwhere(data == 'X')
    visited_stack = set()
    for obstacle_pos in obstacles_possible_pos:
        current_pos = tuple(starting_pos)
        current_dir = '^'
        data[*obstacle_pos] = '#'
        visited_stack.clear()
        while True:
            current_tup = (tuple(current_pos), current_dir)
            if current_tup in visited_stack:
                loops += 1
                break
            visited_stack.add(current_tup)
            direction = direction_map[current_dir]
            new_pos = np.add(current_pos, direction)
            if not pos_in_bounds(new_pos):
                break
            if data[*new_pos] != '#':
                current_pos = new_pos
            else:
                current_dir = turn_map[current_dir]
        data[*obstacle_pos] = '.'
    return loops

print(f'{part1(data)} {part2(data)}')