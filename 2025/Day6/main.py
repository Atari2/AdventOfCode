import re
import numpy
SAMPLE_DATA: bool = False 
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()


symbols = re.split(r"\s+", data[-1].strip())
numbers = [list(map(int, re.split(r"\s+", line.strip()))) for line in data[:-1]]
matdata = numpy.array([[c for c in line.strip('\n')] for line in data], dtype=str).T
n = len(numbers[0])
p1 = 0
for i in range(n):
    col = [row[i] for row in numbers]
    symbol = symbols[i]
    if symbol == "+":
        result = sum(col)
    elif symbol == "*":
        result = 1
        for num in col:
            result *= num
    p1 += result

op = ''
p2 = 0
num = 0
for row in matdata:
    n = ''.join(c for c in row if c != ' ')
    if not n:
        continue
    if n[-1] == '+':
        p2 += num
        op = '+'
        num = int(n[:-1])
    elif n[-1] == '*':
        p2 += num
        op = '*'
        num = int(n[:-1])
    else:
        if op == '+':
            num += int(n)
        elif op == '*':
            num *= int(n)
p2 += num
print(f'{p1} {p2}')