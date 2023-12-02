from functools import reduce


SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

class Game:
    number: int
    cubesubsets: list[list[tuple[int, str]]]
    def __init__(self, line):
        number, cubesubsets = line.split(":", 1)
        self.number = int(number.split(' ', 1)[-1])
        self.cubesubsets = []
        for cubesubset in cubesubsets.split(';'):
            for cube in cubesubset.split(','):
                qty, color = cube.strip().split(' ', 1)
                self.cubesubsets.append((int(qty), color.strip()))
    
    def is_possible(self, bag: dict[str, int]) -> bool:
        for qty, color in self.cubesubsets:
            if color not in bag or bag[color] < qty:
                return False
        return True
    
    def min_bag_power(self) -> int:
        gbag = { color: 0 for _, color in self.cubesubsets }
        for qty, color in self.cubesubsets:
            gbag[color] = max(gbag[color], qty)
        return reduce(lambda a, b: a * b, gbag.values())
    
    def __repr__(self):
        return f"Game {self.number}: {self.cubesubsets}"


bag = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

with open(filename, 'r') as f:
    games = [Game(line) for line in f.readlines()]
totalp1 = sum(g.number if g.is_possible(bag) else 0 for g in games)
totalp2 = sum(g.min_bag_power() for g in games)

print(f'{totalp1} {totalp2}')