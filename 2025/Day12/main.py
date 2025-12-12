import numpy
import re

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

REGION_PATT = re.compile(r'(?P<width>\d+)x(?P<height>\d+): (?P<quantities>(?:(?:\d+) ?)+)')

with open(filename, 'r') as f:
    data = f.readlines()

class Present:
    shape: numpy.ndarray
    index: int
    area: int
    min_b: int
    max_b: int

class Region:
    width: int
    height: int
    quantities: list[int]

presents: list[Present] = []
index = 0
present = []
regions: list[Region] = []
index = 0
while index < len(data):
    line = data[index].strip()
    if not line:
        index += 1
    elif line[0].isdigit() and line[1] == ':':
        digit = int(line[0])
        index += 1
        while index < len(data) and (l := data[index].strip()) and not (l[0].isdigit() and ':' in l):
            present.append([1 if c == '#' else 0 for c in l])
            index += 1
        p = Present()
        p.shape = numpy.array(present)
        p.index = digit
        presents.append(p)
        present = []
        continue
    elif line:
        match = REGION_PATT.match(line)
        if match:
            width = int(match.group('width'))
            height = int(match.group('height'))
            quantities = [int(q) for q in match.group('quantities').split()]
            region = Region()
            region.width = width
            region.height = height
            region.quantities = quantities
            regions.append(region)
        index += 1

for p in presents:
    p.area = int(numpy.sum(p.shape))
    stats = []
    curr = p.shape
    for _ in range(2):
        for _ in range(4):
            y, x = numpy.where(curr == 1)
            b = int(numpy.sum((y + x) % 2 == 0))
            stats.extend([b, p.area - b])
            curr = numpy.rot90(curr)
        curr = numpy.flipud(curr)
    p.min_b, p.max_b = min(stats), max(stats)

valid_regions = 0
for r in regions:
    grid_area = r.width * r.height
    grid_black = (grid_area + 1) // 2
    grid_white = grid_area // 2
    req_area, req_min_b, req_max_b = 0, 0, 0
    for i, qty in enumerate(r.quantities):
        req_area += qty * presents[i].area
        req_min_b += qty * presents[i].min_b
        req_max_b += qty * presents[i].max_b
    if req_area <= grid_area:
        needed_min = max(req_min_b, req_area - grid_white)
        needed_max = min(req_max_b, grid_black)
        if needed_min <= needed_max:
            valid_regions += 1
print(f'{valid_regions} 0')