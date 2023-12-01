from __future__ import annotations

def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()


class Bit:
    idx: int
    zeros: int
    ones: int

    def __init__(self, idx):
        self.idx = idx
        self.zeros = 0
        self.ones = 0
    
    def add(self, bit):
        if bit == '0':
            self.zeros += 1
        else:
            self.ones += 1

    def most_common(self):
        if self.zeros > self.ones:
            return 0
        elif self.zeros < self.ones:
            return 1
        else:
            return 1

    def least_common(self):
        if self.zeros > self.ones:
            return 1
        elif self.zeros < self.ones:
            return 0
        else:
            return 0

    @classmethod
    def combine_most_common(cls, *mostcommonbits: list[Bit]):
        result = 0
        for bit in mostcommonbits:
            result |= bit.most_common() << bit.idx
        return result
    
    @classmethod
    def combine_least_common(cls, *leastcommonbits: list[Bit]):
        result = 0
        for bit in leastcommonbits:
            result |= bit.least_common() << bit.idx
        return result


def part1():
    lines = [line.strip() for line in read_from_input()]

    binary_len = len(lines[0])
    bits = [Bit(binary_len - i - 1) for i in range(binary_len)]
    for line in lines:
        for i in range(binary_len - 1, -1, -1):
            bits[i].add(line[i])
    gamma_rate = Bit.combine_most_common(*bits)
    epsilon_rate = Bit.combine_least_common(*bits)
    print(gamma_rate * epsilon_rate)


def part2():
    lines = [line.strip() for line in read_from_input()]
    binary_len = len(lines[0])

    # oxygen
    bits = [Bit(binary_len - i - 1) for i in range(binary_len)]
    filtered = lines
    idx = 0
    while len(filtered) > 1:
        for line in filtered:
            bits[idx].add(line[idx])
        filtered = [line for line in filtered if bits[idx].most_common() == int(line[idx])]
        idx += 1
    oxygen_rating = int(filtered[0], 2)

    # co2
    bits = [Bit(binary_len - i - 1) for i in range(binary_len)]
    filtered = lines
    idx = 0
    while len(filtered) > 1:
        for line in filtered:
            bits[idx].add(line[idx])
        filtered = [line for line in filtered if bits[idx].least_common() == int(line[idx])]
        idx += 1
    co2_rating = int(filtered[0], 2)
    
    print(oxygen_rating * co2_rating)

part1()
part2()