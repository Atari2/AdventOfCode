def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

lines = read_from_input()
template = lines.pop(0).strip()
pair_dict = {}
n_pairs_dict = {}
for line in filter(lambda x: not x.isspace(), lines):
    pair, sub = line.split('->')
    pair = pair.strip()
    sub = sub.strip()
    assert(len(pair) == 2 and len(sub) == 1)
    pair_dict[pair] = pair[0] + sub
    n_pairs_dict[pair] = 0

loops = 40
part1_loops = 10

letters = {x: 0 for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}
for i in range(len(template) - 1):
    pair = template[i:i+2]
    n_pairs_dict[pair] += 1

for c in template:
    letters[c] += 1

for l in range(loops):
    new_pairs_dict = {}
    for pair, value in filter(lambda v: v[1] != 0, n_pairs_dict.items()):
        inserted_pair = pair_dict[pair]
        other_inserted_pair = inserted_pair[1] + pair[1]
        if inserted_pair in new_pairs_dict:
            new_pairs_dict[inserted_pair] += value
        else:
            new_pairs_dict[inserted_pair] = value
        if other_inserted_pair in new_pairs_dict:
            new_pairs_dict[other_inserted_pair] += value
        else:
            new_pairs_dict[other_inserted_pair] = value
        letters[inserted_pair[1]] += value
    if l == part1_loops - 1:
        max_letter = max(letters.values())
        min_letter = min(filter(lambda x: x != 0, letters.values()))
        print("First part: " + str(max_letter - min_letter))
    n_pairs_dict = new_pairs_dict

max_letter = max(letters.values())
min_letter = min(filter(lambda x: x != 0, letters.values()))

print("Second part: " + str(max_letter - min_letter))