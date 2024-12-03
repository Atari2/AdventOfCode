import re

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.read()

# single line solution to part 1
# part1 = sum(map(lambda m: int(m.group(1)) * int(m.group(2)), re.compile(r"mul\((\d{1,3}),(\d{1,3})\)").finditer(data)))

MULT_DO_DONT_PATT = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")
mult_enabled = True
part1, part2 = 0, 0
for m in MULT_DO_DONT_PATT.finditer(data):
    if (op := m.group(0)).startswith("mul"):
        res = int(m.group(1)) * int(m.group(2))
        if mult_enabled:
            part2 += res
        part1 += res
    elif op == "do()":
        mult_enabled = True
    elif op == "don't()":
        mult_enabled = False

print(f'{part1} {part2}')