import math
import numpy

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()

type Coordinate = tuple[int, int, int]
    
def from_str(s: str) -> Coordinate:
    x, y, z = map(int, s.strip().split(","))
    return (x, y, z)


def distance(p1: Coordinate, p2: Coordinate) -> float:
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    return dist  

points: list[Coordinate] = [from_str(line) for line in data]
distances: numpy.ndarray = numpy.zeros((len(points), len(points)), dtype=numpy.float64)
circuits: numpy.ndarray = numpy.zeros((len(points),), dtype=numpy.int32) - 1
def connect_min_distance(points: list[Coordinate]) -> tuple[Coordinate, Coordinate]:
    min_pos = numpy.where(distances == distances.min())
    i, j = min_pos[0][0], min_pos[1][0]
    p1, p2 = points[i], points[j]
    distances[i, j] = float('inf')
    c1, c2 = circuits[i], circuits[j]
    if c1 == -1 and c2 == -1:
        new_circuit_id = numpy.max(circuits) + 1
        circuits[i] = new_circuit_id
        circuits[j] = new_circuit_id
    elif c1 != -1 and c2 == -1:
        circuits[j] = c1
    elif c1 == -1 and c2 != -1:
        circuits[i] = c2
    elif c1 != c2:  
        circuits[circuits == c2] = c1
    return p1, p2

for i, p in enumerate(points):
    for j, q in enumerate(points):
        distances[i, j] = distance(p, q)

distances = numpy.tril(distances)
distances[distances == 0] = float('inf')

for i in range(10 if SAMPLE_DATA else 1000):
    connect_min_distance(points)
circuits_length = [numpy.count_nonzero(circuits == uc) for uc in numpy.unique(circuits) if uc != -1]
circuits_length.sort()
p1 = math.prod(circuits_length[-3:])

last_connection: tuple[Coordinate, Coordinate] = (0, 0, 0), (0, 0, 0)
while not numpy.all(circuits == circuits[0]):
    last_connection = connect_min_distance(points)
p2 = last_connection[0][0] * last_connection[1][0]
print(f'{p1} {p2}')