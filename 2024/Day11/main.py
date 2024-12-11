from __future__ import annotations
SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


class Stone:
    value: str
    occurrences: int 

    def __init__(self, value: str, occurrences: int = 1):
        self.occurrences = occurrences
        self.value = v if len(v := value.lstrip('0')) != 0 else '0'

    def blink(self) -> list[Stone]:
        if self.value == '0':
            return [Stone('1', self.occurrences)]
        elif (vlen := len(self.value)) % 2 == 0:
            return [Stone(self.value[:vlen // 2], self.occurrences), Stone(self.value[vlen // 2:], self.occurrences)]
        else:
            return [Stone(str(int(self.value) * 2024), self.occurrences)]
        
    def __repr__(self):
        return f"{self.value}({self.occurrences})"

    def __eq__(self, other: Stone):
        return self.value == other.value

with open(filename, 'r') as f:
    data = [Stone(x) for x in f.read().split(' ')]

part1 = 0
for i in range(75):
    if i == 25:
        part1 = sum(map(lambda s: s.occurrences, data))
    new_data: list[Stone] = []
    for stone in data:
        for new_stone in stone.blink():
            try:
                idx = new_data.index(new_stone)
                new_data[idx].occurrences += new_stone.occurrences
            except ValueError:
                new_data.append(new_stone)
    data = new_data
part2 = sum(map(lambda s: s.occurrences, data))
print(f'{part1} {part2}')