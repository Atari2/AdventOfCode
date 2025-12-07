import numpy

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()

mapper = {
    'S': 1,
    '.': 0,
    '^': 2
}
matdata = numpy.array([list(map(lambda x: mapper[x], list(line.strip()))) for line in data])
beams = frozenset(map(tuple, numpy.argwhere(matdata == 1)))
rows, cols = matdata.shape
_explore_cache = {}
split = 0
def explore(path: list[tuple[int, int]], beams: frozenset[tuple[int, int]]):
    global split
    if beams in _explore_cache:
        return _explore_cache[beams]
    if not beams:
        return 1
    total = 0
    new_beams = set()
    for beam in beams:
        r, c = beam
        r += 1
        if r >= rows:
            continue
        if matdata[r, c] == 0:
            new_beams.add((r, c))
        elif matdata[r, c] == 2:
            beam_left = (r, c - 1)
            beam_right = (r, c + 1)
            if c - 1 >= 0 and matdata[r, c - 1] != 2:
                split += 1
                total += explore(path + [beam_left], frozenset({beam_left}.union(new_beams)))
            if c + 1 < cols and matdata[r, c + 1] != 2:
                split += 1
                total += explore(path + [beam_right], frozenset({beam_right}.union(new_beams)))
            _explore_cache[beams] = total
            return total
    return explore(path, frozenset(new_beams))

timelines = explore([], beams)
print(f"{split // 2} {timelines}")