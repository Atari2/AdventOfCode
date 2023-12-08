from __future__ import annotations
import re
import math
import functools

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

with open(filename, "r") as f:
    lines = f.read().splitlines()

MAPPING_PATTERN = re.compile(r'(?P<source>...) = \((?P<ltarget>...), (?P<rtarget>...)\)')

instructions = lines[0]

mappings = {}
for line in lines[1:]:
    if m := MAPPING_PATTERN.match(line):
        mappings[m.group('source')] = (m.group('ltarget'), m.group('rtarget'))

def part1():
    current = 'AAA'
    index = 0

    while current != 'ZZZ':
        lr = instructions[index % len(instructions)]
        if lr == 'L':
            current = mappings[current][0]
        else:
            current = mappings[current][1]
        index += 1
    return index

def part2():
    currents = list(filter(lambda c: c[-1] == 'A', mappings.keys()))
    current_values = []
    for current in currents:
        index = 0
        while current[-1] != 'Z':
            instruction = instructions[index % len(instructions)]
            if instruction == 'L':
                current = mappings[current][0]
            else:
                current = mappings[current][1]
            index += 1
        current_values.append(index)
    return functools.reduce(math.lcm, current_values)

    

print(f'{part1()} {part2()}')