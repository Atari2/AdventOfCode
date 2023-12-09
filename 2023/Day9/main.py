from __future__ import annotations

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

with open(filename, "r") as f:
    lines = f.read().splitlines()

class Sequence:
    numbers: list[list[int]]

    def __init__(self, line: str):
        self.numbers = [list(map(int, line.split(" ")))]
    
    def extrapolate_p1(self):
        current_line = self.numbers[0]
        while any(self.numbers[-1]):
            next_line = []
            for i in range(len(current_line) - 1):
                next_line.append(current_line[i + 1] - current_line[i])
            self.numbers.append(next_line)
            current_line = next_line
        zeros = self.numbers[-1]
        zeros.append(0)
        val_below = zeros[-1]
        for num in range(len(self.numbers) - 2, -1, -1):
            val_below = self.numbers[num][-1] + val_below
            self.numbers[num].append(val_below)
        return self.numbers[0][-1]
    
    def extrapolate_p2(self):
        current_line = self.numbers[0]
        while any(self.numbers[-1]):
            next_line = []
            for i in range(len(current_line) - 1):
                next_line.append(current_line[i + 1] - current_line[i])
            self.numbers.append(next_line)
            current_line = next_line
        zeros = self.numbers[-1]
        zeros.insert(0, 0)
        val_below = zeros[-1]
        for num in range(len(self.numbers) - 2, -1, -1):
            val_below = self.numbers[num][0] - val_below
            self.numbers[num].insert(0, val_below)
        return self.numbers[0][0]


seqs = [Sequence(line) for line in lines]
part1 = sum([seq.extrapolate_p1() for seq in seqs])
part2 = sum([seq.extrapolate_p2() for seq in seqs])
print(f'{part1} {part2}')
    
