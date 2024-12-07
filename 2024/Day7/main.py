import itertools
from typing import Literal

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()

class Equation:
    expected_result: int
    numbers: list[int]

    def __init__(self, line: str): 
        expected_result, numbers = line.split(':', maxsplit=1)
        self.expected_result = int(expected_result)
        self.numbers = [int(n) for n in numbers.split()]

    def solve(self, part: Literal[1, 2]) -> int:
        possible_ops = ['*', '+', '||'] if part == 2 else ['*', '+']
        for ops in itertools.product(possible_ops, repeat=len(self.numbers) - 1):
            result = self.numbers[0]
            for i, n in enumerate(self.numbers[1:]):
                if ops[i] == '+':
                    result += n
                elif ops[i] == '*':
                    result *= n
                elif ops[i] == '||':
                    result = int(str(result) + str(n))
            if result == self.expected_result:
                return self.expected_result
        return 0

equations = [Equation(line) for line in data]
part1 = sum([eq.solve(1) for eq in equations])
part2 = sum([eq.solve(2) for eq in equations])
print(f"{part1} {part2}")