from __future__ import annotations
import re

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

with open(filename, "r") as f:
    lines = f.read().splitlines()

MAP_PATTERN = re.compile(r'(?P<source>\w+)-to-(?P<dest>\w+) map:', re.IGNORECASE)

class MapRange:
    dest_range: int
    source_range: int
    len_range: int

    def __init__(self, dest_range: int, source_range: int, len_range: int):
        self.dest_range = dest_range
        self.source_range = source_range
        self.len_range = len_range

    def __contains__(self, item: int | MapRange):
        return item in range(self.source_range, self.source_range + self.len_range)

    def __repr__(self):
        return f"({self.source_range:10}, {self.source_range + self.len_range:10}) -> ({self.dest_range:10}, {self.dest_range + self.len_range:10})"

OverlapRest = range | tuple[range | None, range | None]    

class MapRanges:
    dest_name: str
    ranges: list[MapRange]

    def __init__(self, dest_name: str):
        self.dest_name = dest_name
        self.ranges = []

    def add_range(self, range: MapRange):
        self.ranges.append(range)

    def map_seed(self, seed: int) -> int:
        for r in self.ranges:
            if seed in r:
                return r.dest_range + seed - r.source_range
        else:
            return seed
    
    def _overlap(self, sr: range, r: MapRange) -> tuple[range | None, OverlapRest]:
        output = None
        overlap = range(max(sr.start, r.source_range), min(sr.stop, r.source_range + r.len_range))
        if len(overlap) > 0:
            dstart = r.dest_range + overlap.start - r.source_range
            dend = dstart + len(overlap)
            output = range(dstart, dend)
            if overlap.start > sr.start:
                left = range(sr.start, overlap.start)
            else:
                left = None
            if overlap.stop < sr.stop:
                right = range(overlap.stop, sr.stop)
            else:
                right = None
            return output, (left, right)
        return output, sr
    
    def map_range(self, seed_range: range) -> set[range]:
        dest_ranges = set()
        seed_ranges = [seed_range]
        for r in self.ranges:
            new_seed_ranges = []
            for sr in seed_ranges:
                o, rest = self._overlap(sr, r)
                if o:
                    dest_ranges.add(o)
                if isinstance(rest, range):
                    new_seed_ranges.append(rest)
                else:
                    new_seed_ranges.extend(filter(None, rest))
            seed_ranges = new_seed_ranges
            if not seed_ranges:
                break
        if len(dest_ranges) == 0:
            dest_ranges.add(seed_range)
        return dest_ranges

    def __repr__(self):
        return f"{self.dest_name}: {self.ranges}"

class LocMap:
    mappers: dict[str, MapRanges] = {}


    def __init__(self, lines: list[str]):
        source = None
        dest = None
        for l in filter(None, lines):
            if m := MAP_PATTERN.match(l):
                source, dest = m.group('source'), m.group('dest')
                self.mappers.setdefault(source, MapRanges(dest))
            elif source and dest:
                self.mappers[source].add_range(MapRange(*map(int, l.split(" "))))

    def find_seed_location(self, seed: int) -> int:
        cur_loc = 'seed'
        while cur_loc != 'location':
            rangemap = self.mappers[cur_loc]
            seed = rangemap.map_seed(seed)
            cur_loc = rangemap.dest_name
        return seed
    
    def find_seed_range_location(self, seed_range: set[range] | range) -> int:
        cur_loc = 'seed'
        while cur_loc != 'location':
            rangemap = self.mappers[cur_loc]
            if isinstance(seed_range, range):
                seed_range = rangemap.map_range(seed_range)
            else:
                new_seed_ranges = set()
                for sr in seed_range:
                    new_seed_ranges.update(rangemap.map_range(sr))
                seed_range = new_seed_ranges
            cur_loc = rangemap.dest_name
        if isinstance(seed_range, range):
            return seed_range.start
        return min(map(lambda r: r.start, seed_range))

    def __str__(self):
        return str(self.mappers)


seeds = [int(n) for n in lines.pop(0).split(":", 1)[-1].strip().split(" ")]
locmap = LocMap(lines)

def part1():
    mapped_seeds = [locmap.find_seed_location(seed) for seed in seeds]  
    part1 = min(mapped_seeds)
    return part1

def part2():
    seed_ranges = [range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
    mapped_seeds = [locmap.find_seed_range_location(seed) for seed in seed_ranges]
    part2 = min(mapped_seeds)
    return part2

print(f"{part1()} {part2()}")