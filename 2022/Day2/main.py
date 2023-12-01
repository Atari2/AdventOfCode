SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"
PART = 2

with open(filename, 'r') as f:
    lines = f.readlines()

scores = [
    [3, 6, 0],
    [0, 3, 6],
    [6, 0, 3]
]
tot_score = 0
for line in lines:
    other, me = line.strip().split(' ')
    tot_score += scores[ord(other) - ord('A')][ord(me) - ord('X')] + (ord(me) - ord('X') + 1)
transforms: dict[tuple[str, str], tuple[int, int]] = {
    ('A', 'X'): (3, 0),
    ('A', 'Y'): (1, 3),
    ('A', 'Z'): (2, 6),
    ('B', 'X'): (1, 0),
    ('B', 'Y'): (2, 3),
    ('B', 'Z'): (3, 6),
    ('C', 'X'): (2, 0),
    ('C', 'Y'): (3, 3),
    ('C', 'Z'): (1, 6),
}
print(f'{tot_score} {sum([sum(transforms[tuple(line.strip().split(" "))]) for line in lines])}')