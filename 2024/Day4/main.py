import math
SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = [l.strip() for l in f.readlines()]

word_to_find = "XMAS"
offsets = ((0, 1), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1))

def check_word(i, j) -> int:
    count = 0
    if data[i][j] != word_to_find[0]:
        return count
    for sxoff, syoff in offsets:
        # give me all directions from the current point
        for off, c in enumerate(word_to_find[1:]):
            # get the n-th character in that direction
            xoff = int(sxoff if sxoff == 0 else sxoff + math.copysign(off, sxoff))
            yoff = int(syoff if syoff == 0 else syoff + math.copysign(off, syoff))
            if i + xoff < 0 or j + yoff < 0:
                # n-th character would be out of bounds
                break
            if i + xoff >= len(data) or j + yoff >= len(data[i + xoff]):
                # n-th character would be out of bounds
                break
            if data[i + xoff][j + yoff] != c:
                # n-th character is not the expected character
                break
        else:
            count += 1
    return count

offsets_p2 = (((1, 1), (-1, -1)), ((-1, 1), (1, -1)))
def check_word_p2(i, j) -> bool:
    if data[i][j] != 'A':
        return 0
    for (sxoff1, syoff1), (sxoff2, syoff2) in offsets_p2:
        if i + sxoff1 < 0 or j + syoff1 < 0:
            return False
        if i + sxoff1 >= len(data) or j + syoff1 >= len(data[i + sxoff1]):
            return False
        if i + sxoff2 < 0 or j + syoff2 < 0:
            return False
        if i + sxoff2 >= len(data) or j + syoff2 >= len(data[i + sxoff2]):
            return False
        if (data[i + sxoff1][j + syoff1] == 'M' and data[i + sxoff2][j + syoff2] == 'S') or (data[i + sxoff1][j + syoff1] == 'S' and data[i + sxoff2][j + syoff2] == 'M'):
            continue
        return False
    else:
        return True

        

part1 = sum([check_word(i, j) for i in range(len(data)) for j in range(len(data[i]))])
part2 = sum([check_word_p2(i, j) for i in range(len(data)) for j in range(len(data[i]))])
print(f'{part1} {part2}')
