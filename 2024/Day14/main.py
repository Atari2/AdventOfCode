import re
import numpy as np
SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

SPACE_HEIGHT = 7 if SAMPLE_DATA else 103
SPACE_WIDTH = 11 if SAMPLE_DATA else 101

with open(filename, 'r') as f:
    data = f.readlines()

ROBOT_PATT = re.compile(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')

class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]

    def __init__(self, line: str):
        match = ROBOT_PATT.match(line)
        if not match:
            raise ValueError(f"Invalid line: {line}")
        self.position = (int(match.group(1)), int(match.group(2)))
        self.velocity = (int(match.group(3)), int(match.group(4)))

    def move(self, steps: int = 1):
        self.position = (self.position[0] + self.velocity[0] * steps, self.position[1] + self.velocity[1] * steps)
        self.position = (self.position[0] % SPACE_WIDTH, self.position[1] % SPACE_HEIGHT)


def part1():
    space = np.zeros((SPACE_HEIGHT, SPACE_WIDTH), dtype=np.uint8)
    robots = [Robot(line.strip()) for line in data]
    for r in robots:
        r.move(100)
        space[r.position[1], r.position[0]] += 1
    # split the space into 4 quadrants, skipping the middle line and column
    quadrant1 = space[:SPACE_HEIGHT//2, :SPACE_WIDTH//2]
    quadrant2 = space[:SPACE_HEIGHT//2, SPACE_WIDTH//2 + 1:]
    quadrant3 = space[SPACE_HEIGHT//2 + 1:, :SPACE_WIDTH//2]
    quadrant4 = space[SPACE_HEIGHT//2 + 1:, SPACE_WIDTH//2 + 1:]
    safety_factor = quadrant1.sum() * quadrant2.sum() * quadrant3.sum() * quadrant4.sum()
    return safety_factor

def part2():
    space = np.zeros((SPACE_HEIGHT, SPACE_WIDTH), dtype=np.uint8)
    robots = [Robot(line.strip()) for line in data]
    for r in robots:
        space[r.position[1], r.position[0]] += 1
    i = 0
    while True:
        i += 1
        for r in robots:
            space[r.position[1], r.position[0]] -= 1
            r.move(1)
            space[r.position[1], r.position[0]] += 1
        padded_space = np.pad(space > 0, ((0, 0), (1, 1)), constant_values=0)
        transitions = np.diff(padded_space.astype(int), axis=1)
        run_lengths = np.where(transitions == -1)[1] - np.where(transitions == 1)[1]
        if np.any(run_lengths >= 20): # heuristically assume that any run of 20 consecutive robots or more is part of a christmas tree.
            return i

print(f'{part1()} {part2()}')