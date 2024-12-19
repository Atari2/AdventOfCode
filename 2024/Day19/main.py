from functools import cache

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()

towels = [t.strip() for t in data[0].split(',')]
arrangements = [l.strip() for l in data[2:]]

@cache
def build_all_arrangements(arrangement: str, current_arrangement: str = '') -> int:
    count = 0
    for towel in towels:
        next_arrangement = current_arrangement + towel
        if next_arrangement == arrangement:
            count += 1
        if arrangement.startswith(next_arrangement) and (c := build_all_arrangements(arrangement, next_arrangement)):
            count += c
    return count

arrangs = [c for arrangement in arrangements if (c := build_all_arrangements(arrangement))]

print(f'{len(arrangs)} {sum(arrangs)}')