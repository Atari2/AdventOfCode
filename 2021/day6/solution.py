from __future__ import annotations
import functools

def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

tot_days = 256
cycle_count = 6

@functools.lru_cache(maxsize=None)
def count_spawned(*, days_left = cycle_count + 2, days = tot_days):
    if days < days_left:
        return 0
    fishes_count = ((days - days_left - 1) // (cycle_count + 1)) + 1
    spawned_tot = fishes_count
    for i in range(spawned_tot):
        days -= (cycle_count if i > 0 else days_left) + 1
        fishes_count += count_spawned(days=days)
    return fishes_count
        
line = read_from_input()[0].split(',')
total = [count_spawned(days_left=int(f)) for f in line]
print(sum(total) + len(line))