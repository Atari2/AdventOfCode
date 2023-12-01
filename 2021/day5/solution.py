import numpy as np

max_x = 0
max_y = 0

def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

class Point:
    x: int
    y: int
    def __init__(self, x, y):
        global max_x, max_y
        self.x = x
        self.y = y
        if self.x > max_x:
            max_x = self.x
        if self.y > max_y:
            max_y = self.y

    def __repr__(self):
        return f'({self.x}, {self.y})'

class VentLine:
    begin: Point
    end: Point

    def __init__(self, line: str):
        points = line.split('->')
        self.begin = Point(*[int(point) for point in points[0].split(',')])
        self.end = Point(*[int(point) for point in points[1].split(',')])

    def __repr__(self):
        return f"{self.begin} -> {self.end}"

class OceanMap:
    map: np.array
    
    def __init__(self, vents: list[VentLine]):
        self.map = np.array([[0 for x in range(max_x+1)] for y in range(max_y+1)])
        for vent in vents:
            if vent.begin.y == vent.end.y:
                # Vertical line
                begin = min(vent.begin.x, vent.end.x)
                end = max(vent.begin.x, vent.end.x)
                for x in range(begin, end+1):
                    self.map[vent.begin.y][x] += 1
            elif vent.begin.x == vent.end.x:
                # Horizontal line
                begin = min(vent.begin.y, vent.end.y)
                end = max(vent.begin.y, vent.end.y)
                for y in range(begin, end+1):
                    self.map[y][vent.begin.x] += 1
            else:
                # Diagonal line
                if vent.begin.x > vent.end.x:
                    # left line
                    if vent.begin.y > vent.end.y:
                        # top line
                        self.handle_top_left_line(vent)
                    else:
                        # bottom line
                        self.handle_bottom_left_line(vent)
                else:
                    # right line
                    if vent.begin.y > vent.end.y:
                        # top line
                        self.handle_top_right_line(vent)
                    else:
                        # bottom line
                        self.handle_bottom_right_line(vent)
    
    def handle_top_left_line(self, vent: VentLine):
        begin_x = vent.begin.x
        begin_y = vent.begin.y
        while begin_x >= vent.end.x:
            self.map[begin_y][begin_x] += 1
            begin_x -= 1
            begin_y -= 1

    def handle_top_right_line(self, vent: VentLine):
        begin_x = vent.begin.x
        begin_y = vent.begin.y
        while begin_x <= vent.end.x:
            self.map[begin_y][begin_x] += 1
            begin_x += 1
            begin_y -= 1

    def handle_bottom_left_line(self, vent: VentLine):
        begin_x = vent.begin.x
        begin_y = vent.begin.y
        while begin_x >= vent.end.x:
            self.map[begin_y][begin_x] += 1
            begin_x -= 1
            begin_y += 1

    def handle_bottom_right_line(self, vent: VentLine):
        begin_x = vent.begin.x
        begin_y = vent.begin.y
        while begin_x <= vent.end.x:
            self.map[begin_y][begin_x] += 1
            begin_x += 1
            begin_y += 1

    def count_overlaps(self):
        count = 0
        for row in self.map:
            for value in row:
                if value > 1:
                    count += 1
        return count

lines = read_from_input()
vents = [VentLine(line) for line in lines]
map = OceanMap(vents)
print(map.count_overlaps())
