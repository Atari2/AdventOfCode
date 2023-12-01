import re
SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename) as f:
    count_part1 = 0
    count_part2 = 0
    [(count_part1 := count_part1 + (((y1 <= y2) and (x1 >= x2)) or ((y1 >= y2) and (x1 <= x2))), count_part2 := count_part2 + (((x1 >= x2) and (x1 <= y2)) or ((x2 >= x1) and (x2 <= y1)))) for x1, y1, x2, y2 in ((int(x) for x in re.split(r"[-,]", line)) for line in f.readlines())]
print(f'{count_part1} {count_part2}')