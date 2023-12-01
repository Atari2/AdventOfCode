import re

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

patt = re.compile(r'((?:\d+\n?)+)\n?', re.MULTILINE)

with open(filename, 'r') as f:
    calories = sorted([sum([int(s) for s in m.strip().split('\n')]) for m in patt.findall(f.read())], reverse=True)[:3]
print(f'{calories[0]} {sum(calories)}')

