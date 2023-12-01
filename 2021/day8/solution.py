def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

one_len = 2
four_len = 4
seven_len = 3
eight_len = 7

unique_lengths = {
    one_len: 1, 
    four_len: 4,
    seven_len: 7,
    eight_len: 8
}

class Reading:
    input: list[str]
    output: list[str]
    mapping: dict[str, int]

    def __init__(self, line: str):
        input, output = line.split('|', 1)
        self.input = [''.join(sorted(l)) for l in input.split()]
        self.output = [''.join(sorted(l)) for l in output.split()]
        self.mapping = {}

    def find_letter_mapping(self):
        for value in self.input:
            l = len(value)
            num = unique_lengths.get(l)
            if num:
                self.mapping[value] = num
            else:
                continue
            if num == 1:
                d1 = value
            elif num == 7:
                d2 = value

        possible_cf = ''
        for i in range(seven_len):
            c = d2[i]
            if c in d1:
                possible_cf += c

        five_lengths = list(filter(lambda x: len(x) == 5, self.input))
        six_length = list(filter(lambda x: len(x) == 6, self.input))

        three = next(filter(lambda x: all(c in x for c in possible_cf), five_lengths))
        six = next(filter(lambda x: sum(c in x for c in possible_cf) == 1, six_length))
        
        missing_c_letter = next(filter(lambda x: x not in six, 'abcdefg'))
        missing_f_letter = possible_cf.replace(missing_c_letter, '')

        five = next(filter(lambda x: missing_f_letter in x and x != three, five_lengths))
        two = next(filter(lambda x: missing_c_letter in x and x != three, five_lengths))

        missing_e_letter = next(filter(lambda x: x not in five, six))

        nine = next(filter(lambda x: missing_e_letter not in x, six_length))
        zero = next(filter(lambda x: x != nine and x != six, six_length))
        
        self.mapping[zero] = 0
        self.mapping[two] = 2
        self.mapping[three] = 3
        self.mapping[five] = 5
        self.mapping[six] = 6
        self.mapping[nine] = 9

    
    def calculate_output(self):
        result = ''
        for value in self.output:
            result += str(self.mapping[value])
        return int(result)

    def count_unique(self):
        count = 0
        for value in self.output:
            num = unique_lengths.get(len(value))
            if not num:
                continue
            count += 1
        return count

                

lines = read_from_input()
def part1():
    result = sum([Reading(line).count_unique() for line in lines])
    assert(result == 456)
    print(result)

def part2():
    readings = [Reading(line) for line in lines]
    sum = 0
    for reading in readings:
        reading.find_letter_mapping()
        sum += reading.calculate_output()
    assert(sum == 1091609)
    print(sum)

part1()
part2()