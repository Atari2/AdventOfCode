import numpy as np

def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

n_cycles = 1000
max_energy_level = 9
rows = 10
columns = 10

tot_flashes = 0

def filter_coordinates(coords: list[tuple[int, int]], x: int, y: int) -> list[tuple[int, int]]:
    actual_coords = []
    for x1, y1 in coords:
        if x1 + x >= 0 and x1 + x < columns and y1 + y >= 0 and y1 + y < rows:
            actual_coords.append((x1 + x, y1 + y))
    return actual_coords

class Octopus:
    has_already_flashed: bool
    energy_level: int
    x: int
    y: int

    def __init__(self, energy_level, x, y, has_already_flashed = False) -> None:
        self.has_already_flashed = has_already_flashed
        self.energy_level = energy_level
        self.x = x
        self.y = y

    def __add__(self, value):
        return Octopus(self.energy_level + value, self.x, self.y, self.has_already_flashed)

    def __iadd__(self, value):
        self.energy_level += value

    def inc(self):
        self.energy_level += 1

    def __repr__(self):
        return str(self.energy_level)
    
    def should_flash(self) -> bool:
        return self.energy_level > max_energy_level and not self.has_already_flashed

    def flash(self):
        self.has_already_flashed = True
        global tot_flashes
        tot_flashes += 1
    
    def reset_flashed_flag(self):
        self.has_already_flashed = False

    def reset_flashed_value(self):
        if self.has_already_flashed:
            self.energy_level = 0
            return True
        return False

input_mat: list[list[Octopus]] = np.array([[Octopus(int(x), i, j) for j, x in enumerate(line.strip())] for i, line in enumerate(read_from_input())])

base_coordinates = [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]
cycle = 0
while True:
    cycle += 1
    # increment all by 1
    input_mat += 1

    for row in input_mat:
        for o in row:
            o.reset_flashed_flag()

    for i in range(rows):
        for j in range(columns):
            to_flash: list[Octopus] = [input_mat[i][j]]
            while len(to_flash) > 0:
                o = to_flash.pop()
                if o.should_flash():
                    o.flash()
                    coords = filter_coordinates(base_coordinates, o.x, o.y)
                    for x, y in coords:
                        input_mat[x][y].inc()
                        if input_mat[x][y].should_flash():
                            to_flash.append(input_mat[x][y])
    all_flashed = 0
    for row in input_mat:
        for o in row:
            all_flashed += 1 if o.reset_flashed_value() else 0
    if cycle == 100:
        print(tot_flashes)
    if all_flashed == 100:
        print("all flashed", cycle)
        exit(0)