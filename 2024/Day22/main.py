import numpy as np

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = [int(l.strip()) for l in f]


def calculate_next(val: int) -> int:
    val = ((val << 6) ^ val) & 0b111111111111111111111111
    val = ((val >> 5) ^ val) & 0b111111111111111111111111
    val = ((val << 11) ^ val) & 0b111111111111111111111111
    return val

def save_nth(val: int, n: int) -> list[int]:
    result = [val]
    for _ in range(n):
        result.append(val := calculate_next(val))
    return result

secrets: list[list[int]] = [
    save_nth(v, 2000) for v in data
]

changes: list[list[int]] = [
    [(s[i + 1] % 10) - (s[i] % 10) for i in range(len(s) - 1)] for s in secrets
]

bananas_sold = np.zeros((20, 20, 20, 20), dtype=np.int16)
already_set = np.zeros((20, 20, 20, 20), dtype=np.int16)
for n, (secret, change) in enumerate(zip(secrets, changes)):
    for i in range(0, len(change) - 4):
        array_indexes = (change[i], change[i + 1], change[i + 2], change[i + 3])
        if already_set[array_indexes] != n:
            bananas_sold[array_indexes] += secret[i + 4] % 10
            already_set[array_indexes] = n


part1 = sum(map(lambda v: v[-1], secrets))
part2 = np.max(bananas_sold)
print(f'{part1} {part2}')