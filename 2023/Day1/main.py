import re

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

digit = r'one|two|three|four|five|six|seven|eight|nine|\d'
pattp2 = re.compile(fr'((?:.*?)(?P<d1>{digit}).*(?P<d2>{digit}).*)|(.*(?P<d3>{digit}).*)')
pattp1 = re.compile(r'((?:.*?)(?P<d1>\d).*(?P<d2>\d).*)|(.*(?P<d3>\d).*)')
def i(digit):
    try:        
        return int(digit)
    except ValueError:
        return ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'].index(digit) + 1

with open(filename, 'r') as f:
    data = f.read()
totalp1 = sum(map(lambda m: i(d3) + 10*i(d3) if (d3 := m.group('d3')) else i(m.group('d1'))*10 + i(m.group('d2')), pattp1.finditer(data)))
totalp2 = sum(map(lambda m: i(d3) + 10*i(d3) if (d3 := m.group('d3')) else i(m.group('d1'))*10 + i(m.group('d2')), pattp2.finditer(data)))

print(f'{totalp1} {totalp2}')
