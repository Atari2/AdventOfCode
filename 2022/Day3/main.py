SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"
with open(filename) as f:
    data = f.read().splitlines()
part1 = sum(['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(list(set(a).intersection(b))[0]) + 1 for a, b in [(line[:len(line) // 2], line[len(line) // 2:]) for line in data]])
part2 = sum(['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(list(set(a).intersection(b).intersection(c))[0]) + 1 for a, b, c in [data[i:i+3] for i in range(0, len(data), 3)]])
print(f'{part1} {part2}')