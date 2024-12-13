import re
from typing import Literal
SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

MACHINE_PATTERN = re.compile(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)")
A_TOKENS_PRICE = 3
B_TOKENS_PRICE = 1
class Machine:
    ax: int
    ay: int
    bx: int
    by: int
    prizex: int
    prizey: int

    def __init__(self, ax: int, ay: int, bx: int, by: int, prizex: int, prizey: int):
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.prizex = prizex
        self.prizey = prizey

    # ax * x + bx * y = prizex
    # ay * x + by * y = prizey
    def solve(self, part: Literal[1] | Literal[2]) -> int | None:
        prizex = self.prizex
        prizey = self.prizey
        if part == 2:
            prizex += 10000000000000
            prizey += 10000000000000
        determinant = self.ax * self.by - self.ay * self.bx
        if determinant == 0:
            return None
        x = (prizex * self.by - prizey * self.bx) / determinant
        y = (self.ax * prizey - self.ay * prizex) / determinant
        if x.is_integer() and y.is_integer():
            return int(x) * A_TOKENS_PRICE + int(y) * B_TOKENS_PRICE
        return None

with open(filename, 'r') as f:
    data = f.read()
machines = [Machine(*map(int, match.groups())) for match in MACHINE_PATTERN.finditer(data)]
part1 = sum(filter(None, (machine.solve(part=1) for machine in machines)))
part2 = sum(filter(None, (machine.solve(part=2) for machine in machines)))
print(f'{part1} {part2}')