SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()
left, right = [], []
for line in data:
    l, r = line.split('   ')
    left.append(int(l))
    right.append(int(r))
left.sort()
right.sort()

# part 1
totsum = 0
for l, r in zip(left, right):
    totsum += abs(l - r)

# part 2
simscore = 0
for n in left:
    simscore += (n * right.count(n))

print(f'{totsum} {simscore}')
