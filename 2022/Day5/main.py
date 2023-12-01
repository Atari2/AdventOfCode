import re
SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"

numpatt = re.compile(r"^ ((\d+\s*)+)$")
instpatt = re.compile(r"move (\d+) from (\d+) to (\d+)")

class Instruction:
    _crates: int
    _from: int
    _to: int

    def __init__(self, crates: int, from_: int, to: int):
        self._crates = crates
        self._from = from_
        self._to = to

    def execute(self, stacks: list[list[str]], part: int):
        if part == 1:
            for _ in range(self._crates):
                stacks[self._to - 1].insert(0, stacks[self._from - 1].pop(0))
        else:
            to_move = stacks[self._from - 1][:self._crates]
            stacks[self._from - 1] = stacks[self._from - 1][self._crates:]
            stacks[self._to - 1] = to_move + stacks[self._to - 1]

with open(filename) as f:
    lines = f.read().splitlines()
num_stacks = 0
crate_lines = []
instructions: list[Instruction] = []
in_instruction = False
for line in lines:
    if numpatt.match(line):
        num_stacks = len(re.findall(r"\d+", line))
    elif len(line) == 0:
        in_instruction = True
    elif in_instruction and (m := re.match(instpatt, line)):
        instructions.append(Instruction(*map(int, m.groups())))
    else:
        crate_lines.append(line)
crate_stacks_p1 = [[] for _ in range(num_stacks)]
crate_stacks_p2 = [[] for _ in range(num_stacks)]
cratepatt = re.compile(r' '.join([r"(?:(\[\w\])|   )"] * num_stacks))
for create_line in crate_lines:
    m = re.match(cratepatt, create_line)
    if not m:
        continue
    for i, g in enumerate(m.groups()):
        if g:
            crate_stacks_p1[i].append(g[1])
            crate_stacks_p2[i].append(g[1])

for i in instructions:
    i.execute(crate_stacks_p1, 1)

for i in instructions:
    i.execute(crate_stacks_p2, 2)

print(''.join([stack[0] for stack in crate_stacks_p1]), end=' ')
print(''.join([stack[0] for stack in crate_stacks_p2]), end='')