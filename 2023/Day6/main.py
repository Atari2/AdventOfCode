from __future__ import annotations
import re

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

with open(filename, "r") as f:
    lines = f.read().splitlines()

def part1():
    times = map(int, filter(None, lines[0].split(":")[-1].strip().split(" ")))
    distances = map(int, filter(None, lines[1].split(":")[-1].strip().split(" ")))

    total = 1
    for total_time, distance_to_beat in zip(times, distances):
        times_beat = 0
        for ms in range(total_time):
            left_time = total_time - ms
            distance_travelled = left_time * ms
            if distance_travelled > distance_to_beat:
                times_beat += 1
        total *= times_beat

    return total

def part2():
    time = int(''.join(map(str.strip, filter(None, lines[0].split(":")[-1].strip()))))
    distance = int(''.join(map(str.strip, filter(None, lines[1].split(":")[-1].strip()))))
    times_beat = 0
    for ms in range(time):
        left_time = time - ms
        distance_travelled = left_time * ms
        if distance_travelled > distance:
            times_beat += 1
    return times_beat

print(f'{part1()} {part2()}')