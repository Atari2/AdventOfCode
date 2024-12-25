from functools import cache
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

string_changes = ["".join(map(str, c)) for c in changes]

@cache
def count_occurrences(seq: str) -> int:
    pricings = 0
    for i, change in enumerate(string_changes):
        idx = 0
        while (idx := change.find(seq, idx)) != -1:
            if change[idx - 1] == '-':
                idx += 1
                continue
            pricings += secrets[i][idx + len(seq) - change[0:idx + len(seq)].count('-')] % 10
            break
    return pricings

current_max = 0

for change in changes:
    for i in range(0, len(change) - 4):
        seq = ''.join(map(str, change[i:i+4]))
        pr = count_occurrences(seq)
        current_max = max(current_max, pr)

part1 = sum(map(lambda v: v[-1], secrets))
print(f'{part1} {current_max}')