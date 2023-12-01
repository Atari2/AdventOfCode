def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

crab_pos = [int(x) for x in read_from_input()[0].split(',')]

min_sum = None
max_pos = max(crab_pos)
for pos in range(max_pos+1):
    tot_sum = 0
    for crab in crab_pos:
        cost = abs(pos - crab)
        # sum([i for i in range(1, n + 1)]) -> n * (n + 1) / 2
        tot_sum += (cost * (cost + 1)) // 2
        # exit loop early if sum is already known to be larger
        if min_sum and tot_sum > min_sum:
            break
    if min_sum is None or tot_sum < min_sum:
        min_sum = tot_sum
print(min_sum)