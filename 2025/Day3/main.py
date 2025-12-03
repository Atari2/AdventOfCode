SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()

banks = [list(map(int, iter(line.strip()))) for line in data]

p1 = 0
for b in banks:
    max1 = max(b[:-1])
    index1 = b.index(max1)
    max2 = max(b[index1+1:])
    num = max1 * 10 + max2
    p1 += num

p2 = 0
for b in banks:
    digits = 11
    num = 0
    maxindex = 0
    for i in range(digits, -1, -1):
        partial = b[maxindex:-i] if i != 0 else b[maxindex:]
        maxv = max(partial)
        partialindex = partial.index(maxv)
        maxindex = maxindex + partialindex
        b[maxindex] = -1
        num = (num * 10) + maxv
    p2 += num

print(p1, p2)