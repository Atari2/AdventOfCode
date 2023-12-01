from __future__ import annotations
from enum import IntEnum

SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename, 'r') as f:
    data = f.read().splitlines()

class Direction(IntEnum):
    L = 0
    R = 1
    U = 2
    D = 3


class Instruction:
    
    steps: int
    direction: Direction

    def __init__(self, line: str):
        direction, steps = line.split(' ', 1)
        self.steps = int(steps)
        self.direction = Direction[direction]
    
    def __repr__(self) -> str:
        return f"Instruction({self.direction}, {self.steps})"
    
    def __str__(self) -> str:
        return f"{str(self.direction)} {self.steps}"

class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __eq__(self, o: Point) -> bool:
        if not isinstance(o, Point):
            raise TypeError(f"Cannot compare Point to {type(o)}")
        return self.x == o.x and self.y == o.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

class Head(Point):
    def _make_step(self, direction: Direction, tails: list[Tail]):
        if direction == Direction.L:
            self.x -= 1
        elif direction == Direction.R:
            self.x += 1
        elif direction == Direction.U:
            self.y += 1
        elif direction == Direction.D:
            self.y -= 1
        tails[0]._make_step(tails)

    def move(self, insn: Instruction, tails: list[Tail]):
        for _ in range(insn.steps):
            self._make_step(insn.direction, tails)

class Tail(Point):
    visited: set[Point]
    head: Head|Tail

    def __init__(self, x: int, y: int, head: Head|Tail):
        super().__init__(x, y)
        self.head = head
        self.visited = {Point(x, y)}
    
    def _make_step(self, tails: list[Tail], index = 0):
        vdist = self.head.y - self.y
        hdist = self.head.x - self.x

        if abs(vdist) <= 1 and abs(hdist) <= 1:
            return

        # If the head is ever two steps directly up, down, left, or right from the tail, 
        # the tail must also move one step in that direction so it remains close enough
        if abs(vdist) == 2 and hdist == 0:
            if (vdist > 0):
                self.y += 1
            else:
                self.y -= 1
        elif abs(hdist) == 2 and vdist == 0:
            if (hdist > 0):
                self.x += 1
            else:
                self.x -= 1
        # Otherwise, if the head and tail aren't touching and aren't in the same row or column, 
        # the tail always moves one step diagonally to keep up
        else:
            if vdist > 0:
                self.y += 1
            else:
                self.y -= 1
            if hdist > 0:
                self.x += 1
            else:
                self.x -= 1
        self.visited.add(Point(self.x, self.y))
        try:
            tails[index + 1]._make_step(tails, index + 1)
        except IndexError:
            pass
    
    def total_visited(self):
        return len(self.visited)

instructions = [Instruction(line) for line in data]
head = Head(0, 0)
tail = Tail(0, 0, head)
tails = [tail]

for _ in range(8):
    tail = Tail(0, 0, tail)
    tails.append(tail)

for insn in instructions:
    head.move(insn, tails)

print(tails[0].total_visited(), tail.total_visited())