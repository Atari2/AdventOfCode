def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

lines = [int(line) for line in read_from_input()]

number_of_increases = 0
subgroups = [sum(lines[i:i+3]) for i in range(0, len(lines) - 2)]

number_of_increases = sum([subgroups[i] < subgroups[i + 1] for i in range(0, len(subgroups) - 1)])

print(number_of_increases)
