import itertools
import copy

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = [int(c) for c in f.read()]

def part1(filesystem: list[str]):
    i = len(filesystem) - 1
    latest_idx = 0
    for c in reversed(filesystem):
        try:
            latest_idx = filesystem.index('.', latest_idx)
            filesystem[latest_idx] = c    
            filesystem[i] = '#'
            i -= 1
        except ValueError:
            break
    tot = 0
    for i, c in enumerate(filesystem):
        if c.isdigit():
            tot += (i * int(c))
        else:
            break
    return tot

def part2(filesystem: list[str]):
    curtype = f if (f := filesystem[0]) != '.' else -1
    spaces = [(0, 0)] if curtype == -1 else []
    files = [(0, 0)] if curtype != -1 else []
    for i, c in enumerate(filesystem):
        if curtype == -1:
            if c == '.':
                idx, size = spaces[-1]
                spaces[-1] = (idx, size + 1)
            else:
                curtype = c
                files.append((i, 1))
        else:
            if c == '.':
                curtype = -1
                spaces.append((i, 1))
            elif c == curtype:
                idx, size = files[-1]
                files[-1] = (idx, size + 1)
            else:
                curtype = c
                files.append((i, 1))
    for n, (file_idx, file_size) in zip(reversed(range(len(files))), reversed(files)):
        for i, (space_idx, space_size) in enumerate(spaces):
            if space_idx > file_idx: # file is before space
                break
            if file_size <= space_size: # file can fit in space
                for j in range(space_idx, space_idx + file_size):
                    filesystem[j] = str(n)
                for j in range(file_idx, file_idx + file_size):
                    filesystem[j] = '.'
                spaces[i] = (space_idx + file_size, space_size - file_size)
                break
    tot = 0
    for i, c in enumerate(filesystem):
        if c.isdigit():
            tot += (i * int(c))
    return tot

        

arranged: list[str] = []

for i, f in enumerate(itertools.batched(data, 2)):
    arranged.extend(itertools.repeat(str(i), f[0]))
    if len(f) == 2:
        arranged.extend(itertools.repeat('.', f[1]))
print(f'{part1(copy.deepcopy(arranged))} {part2(arranged)}')