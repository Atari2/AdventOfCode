SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()

def compress_ranges(ranges: list[range]) -> list[range]:
    if not ranges:
        return []
    sorted_ranges = sorted(ranges, key=lambda r: r.start)
    compressed = []
    for r in sorted_ranges:
        was_compressed = False
        for c in compressed:
            if r.start <= c.stop and r.stop >= c.start:
                c_start = min(c.start, r.start)
                c_stop = max(c.stop, r.stop)
                compressed.remove(c)
                compressed.append(range(c_start, c_stop))
                was_compressed = True
                break
        if not was_compressed:
            compressed.append(r)
    return compressed

parsing_ranges = True
fresh_ranges = []
fresh_quantity = 0
total_fresh = 0
for line in data:
    line = line.strip()
    if len(line) == 0:
        parsing_ranges = False
        continue
    if parsing_ranges:
        s, e = line.split('-')
        fresh_ranges.append(range(int(s), int(e)+1))
    else:
        number = int(line)
        is_fresh = any(number in r for r in fresh_ranges)
        fresh_quantity += int(is_fresh)

compressed_ranges = compress_ranges(fresh_ranges)
for r in compressed_ranges:
    total_fresh += r.stop - r.start

print(f'{fresh_quantity} {total_fresh}')