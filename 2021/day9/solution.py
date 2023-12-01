from __future__ import annotations
import numpy as np

def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()


class LowestPoint:
    x: int
    y: int
    value: int
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
    
    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other: LowestPoint):
        return self.x == other.x and self.y == other.y

class Map:
    map: np.array
    def __init__(self, input_lines: list[str]):
        self.map = np.array([[int(x) for x in line.strip()] for line in input_lines])

    def increment_indexes(self, i, j, x_direction: int, y_direction: int) -> tuple[int, int, bool]:
        row_count = len(self.map)
        col_count = len(self.map[i])
        if (i == 0 and x_direction == -1) or (i == row_count - 1 and x_direction == 1):
            return (i, j, False)
        elif (j == col_count - 1 and y_direction == 1) or (j == 0 and y_direction == -1):
            return (i, j, False)
        return (i+x_direction, j+y_direction, True)

    def count_basin_size(self, point: LowestPoint) -> int:
        stop_basin_value = 9
        basin_size = 1
        candidates = [point]
        explored = np.zeros(self.map.shape, dtype=bool)
        while len(candidates) > 0:
            p = candidates.pop()
            explored[p.x][p.y] = True
            for x_inc, y_inc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                (x, y, valid) = self.increment_indexes(p.x, p.y, x_inc, y_inc)
                if explored[x][y]:
                    continue
                explored[x][y] = True
                if valid:
                    if self.map[x][y] < stop_basin_value:
                        candidates.append(LowestPoint(x, y, self.map[x][y]))
                        basin_size += 1
        return basin_size

    def find_lowest_points(self) -> list[LowestPoint]:
        lowest_points = []
        row_count = len(self.map)
        for i in range(row_count):
            col_count = len(self.map[i])
            for j in range(col_count):
                value = self.map[i][j]
                if i == 0 and j == 0:
                    is_lowest = self.map[i+1][j] > value and self.map[i][j+1] > value
                elif i == row_count - 1 and j == col_count - 1:
                    is_lowest = self.map[i-1][j] > value and self.map[i][j-1] > value
                elif i == 0 and j == col_count - 1:
                    is_lowest = self.map[i+1][j] > value and self.map[i][j-1] > value
                elif j == 0 and i == row_count - 1:
                    is_lowest = self.map[i-1][j] > value and self.map[i][j+1] > value
                elif i == 0:
                    is_lowest = self.map[i+1][j] > value and self.map[i][j-1] > value and self.map[i][j+1] > value
                elif j == 0:
                    is_lowest = self.map[i-1][j] > value and self.map[i+1][j] > value and self.map[i][j+1] > value
                elif i == row_count - 1:
                    is_lowest = self.map[i-1][j] > value and self.map[i][j-1] > value and self.map[i][j+1] > value
                elif j == col_count - 1:
                    is_lowest = self.map[i-1][j] > value and self.map[i+1][j] > value and self.map[i][j-1] > value
                else:
                    is_lowest = self.map[i-1][j] > value and self.map[i+1][j] > value and self.map[i][j-1] > value and self.map[i][j+1] > value
                if is_lowest:
                    lowest_points.append(LowestPoint(i, j, value))
        return lowest_points


def part1():
    map = Map(read_from_input())
    lowest_points = map.find_lowest_points()
    print(sum([p.value for p in lowest_points]) + len(lowest_points))

def part2():
    map = Map(read_from_input())
    lowest_points = map.find_lowest_points()
    sizes = [map.count_basin_size(p) for p in lowest_points]
    max_sizes = sorted(sizes)[-3:]
    total = 1
    for size in max_sizes:
        total *= size
    print(total)

part2()