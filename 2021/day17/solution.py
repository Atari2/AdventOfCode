import re

def read_from_input():
    with open('input.txt', 'r') as f:
        return f.read()

def solve_equation(sum_tot):
    rad = 1 - (-4*2*sum_tot)
    if rad < 0:
        return None
    else:
        sol1 = (-1 + rad**0.5) // 2
        sol2 = (-1 - rad**0.5) // 2
        return int(max(sol1, sol2))

class Probe:
    pos_x: int
    pos_y: int
    vel_x: int
    vel_y: int
    max_y: int

    def __init__(self, starting_vel_x, starting_vel_y):
        self.pos_x = 0
        self.pos_y = 0
        self.vel_x = starting_vel_x
        self.vel_y = starting_vel_y
        self.max_y = 0
    
    def move(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        if self.pos_y > self.max_y:
            self.max_y = self.pos_y
        if self.vel_x != 0:
            self.vel_x = (self.vel_x - 1 if self.vel_x > 0 else self.vel_x + 1)
        self.vel_y -= 1

class Target:
    x_range: tuple[int, int]
    y_range: tuple[int, int]

    def __init__(self, target: str):
        pos_re = re.compile(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)')
        pos_match = pos_re.match(target)
        self.x_range = (int(pos_match.group(1)), int(pos_match.group(2)))
        min_x_range = min(self.x_range)
        max_x_range = max(self.x_range)
        self.x_range = (min_x_range, max_x_range)
        self.y_range = (int(pos_match.group(3)), int(pos_match.group(4)))
        min_y_range = min(self.y_range)
        max_y_range = max(self.y_range)
        self.y_range = (min_y_range, max_y_range)
    
    def contains(self, probe: Probe):
        return self.x_range[0] <= probe.pos_x <= self.x_range[1] and \
               self.y_range[0] <= probe.pos_y <= self.y_range[1]
    
    def skipped(self, probe: Probe):
        return self.y_range[0] > probe.pos_y or self.x_range[1] < probe.pos_x

target = Target(read_from_input())

def part1():
    possible_x_velocities = set()
    for x in range(target.x_range[0], target.x_range[1]):
        sol = solve_equation(x)
        if sol is not None:
            possible_x_velocities.add(sol)
    y_starting_vel = abs(target.y_range[0]) - 1

    max_height = 0
    for x in possible_x_velocities:
        probe = Probe(x, y_starting_vel)
        while not target.contains(probe): 
            probe.move()
            if target.skipped(probe):
                break
        if probe.max_y > max_height:
            max_height = probe.max_y
    print(f"Part 1: max height reached was {max_height}")

def part2():
    possible_x_velocities = [i for i in range(1, target.x_range[1] + 1)]
    possible_y_velocities = [i for i in range(target.y_range[0], -target.y_range[0])]
    count = 0
    for x_vel in possible_x_velocities:
        for y_vel in possible_y_velocities:
            probe = Probe(x_vel, y_vel)
            skipped = False
            while not target.contains(probe): 
                probe.move()
                if target.skipped(probe):
                    skipped = True
                    break
            if not skipped:
                count += 1
    print(f"Part 2: number of probes that can reach the target area is {count}")

part1()
part2()