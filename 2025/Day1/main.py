SAMPLE_DATA = False 
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

with open(filename, 'r') as f:
    data = f.readlines()

def part1():
    p = 50
    r = sum((p := (p + int(l[1:]) * [1, -1][l[0] == 'R']) % 100) == 0 for l in data)
    return r


def part2():
    p = 50
    r = 0
    for l in data:
        r += (a := int(l[1:])) // 100 + (((t := (p - m)) <= 0 and p > 0) if ((m := a % 100) != 100) and l[0] == 'L' else ((t := (p + m)) >= 100))
        p = t % 100
    return r

print(f"{part1()} {part2()}")