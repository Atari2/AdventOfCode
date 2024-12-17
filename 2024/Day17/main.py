from typing import Literal
import copy

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = [line.strip() for line in f]

class Cpu:
    program: list[int]
    pc: int
    a: int
    b: int
    c: int
    output: list[str]
    part: Literal[1, 2]

    def __init__(self, data: list[str], part: Literal[1, 2] = 1):
        self.pc = 0
        self.a = int(data[0].split(':')[1].strip())
        self.b = int(data[1].split(':')[1].strip())
        self.c = int(data[2].split(':')[1].strip())
        self.program = [int(x) for x in data[4].split(':')[1].strip().split(',')]
        self.output = []
        self.part = part

    def combo(self):
        match (op := self.program[self.pc]):
            case 0 | 1 | 2 | 3:
                return op
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise ValueError(f"Invalid combo operand: {op}")

    def adv(self):
        self.a = self.a // (1 << self.combo())
        self.pc += 1

    def bxl(self):
        self.b ^= self.program[self.pc]
        self.pc += 1

    def bst(self):
        self.b = self.combo() & 7
        self.pc += 1

    def jnz(self):
        if self.a != 0:
            self.pc = self.program[self.pc]
        else:
            self.pc += 1
    
    def bxc(self):
        self.b ^= self.c
        self.pc += 1

    def out(self) -> int:
        operand = self.combo() & 7
        self.pc += 1
        self.output.append(str(operand))
        if self.part == 2:
            return operand

    def bdv(self):
        self.b = self.a // (1 << self.combo())
        self.pc += 1
    
    def cdv(self):
        self.c = self.a // (1 << self.combo())
        self.pc += 1

    def clear(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.output = []
        self.pc = 0

    def run(self) -> bool:
        proglen = len(self.program)
        instructions = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]
        while self.pc < proglen:
            opcode = self.program[self.pc]
            self.pc += 1
            if (out := instructions[opcode]()) is not None:
                return out

    def result(self) -> str:
        return ','.join(self.output)


def part1():
    cpu = Cpu(data)
    cpu.run()
    return cpu.result()

def part2():
    cpu = Cpu(data, part=2)
    place = len(cpu.program) - 1
    current_reg_as = [0]
    while place >= 0:
        next_reg_as = []
        expected_output = cpu.program[place]
        for a in current_reg_as:
            newa = a * 8
            for i in range(8):
                cpu.a = newa + i
                output = cpu.run()
                cpu.clear()
                if output == expected_output:
                    next_reg_as.append(newa + i)
        place -= 1
        current_reg_as = copy.deepcopy(next_reg_as)
    return min(current_reg_as)



print(f'{part1()} {part2()}')