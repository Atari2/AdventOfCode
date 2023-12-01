from __future__ import annotations 
import numpy as np

def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

base_coordinates = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def filter_coordinates(x: int, y: int, columns: int, rows: int) -> filter:
    return filter(lambda point: point[0] + x >= 0 and point[0] + x < columns and point[1] + y >= 0 and point[1] + y < rows, base_coordinates)

class Point:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return (53 + self.x) * 53 + self.y

class Node:
    point: Point
    cost: float
    children: list[Node]

    def __init__(self, point, cost):
        self.point = point
        self.cost = cost
        self.children = []
    
    def __str__(self):
        return f'({self.point}, {self.cost})'

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self):
        return (53 + self.point.x) * 53 + self.point.y

    def __gt__(self, cost):
        return self.cost > cost

    def __lt__(self, cost):
        return self.cost < cost

    def __add__(self, val): 
        return Node(self.point, self.cost + val)
    
    def __sub__(self, val):
        return Node(self.point, self.cost - val)
    
def get_node_list_from_coords(coords: filter[Point], matrix: np.ndarray, pos_x: int, pos_y: int) -> list[Node]:
    nodes: list[Node] = []
    for x, y in coords:
        nodes.append(matrix[pos_x + x, pos_y + y])
    return nodes
    
    
def create_graph(matrix):
    max_x = len(matrix)
    max_y = len(matrix[0])
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j].children = get_node_list_from_coords(filter_coordinates(i, j, max_x, max_y), matrix, i, j)
    return matrix[0][0], matrix[max_x - 1][max_y - 1]

def expand_ocean_map(matrix: np.ndarray):
    rows = len(matrix)
    cols = len(matrix[0])
    full_matrix = np.array([[Node(Point(i, j), 0) for j in range(rows * 5)] for i in range(cols * 5)])
    for i in range(5):
        mm = matrix + i
        mm[mm > 9] -= 9
        for j in range(5):
            nn = mm + j
            nn[nn > 9] -= 9
            for k in range(rows):
                for l in range(cols):
                    full_matrix[i * cols + k][j * rows + l].cost = nn[k][l].cost
    return full_matrix

def min_distance(nodes: list[Node], distances: dict[Node, float]):
    min_node = None
    min_val = np.inf
    for node in nodes:
        if distances[node] < min_val:
            min_node = node
            min_val = distances[node]
    if min_node is None:
        raise Exception('No node found')
    return min_node

def construct_path(cameFrom: dict[Node, Node], current: Node, start: Node):
    total_path = current.cost
    while current in cameFrom:
        current = cameFrom[current]
        total_path += current.cost
    return total_path - start.cost

def astar(nodes: np.ndarray, start: Node, end: Node) -> float:
    gScore: dict[Node, float] = {}
    fScore: dict[Node, float] = {}
    cameFrom: dict[Node, Node] = {}
    openSet: list[Node] = []
    openSet.append(start)
    for row in nodes:
        for node in row:
            gScore[node] = np.inf
            fScore[node] = np.inf
    
    gScore[start] = 0
    fScore[start] = start.cost

    while len(openSet) > 0:
        u = min_distance(openSet, fScore)
        if u == end:
            return construct_path(cameFrom, u, start)
        openSet.remove(u)
        for v in u.children:
            alt = gScore[u] + v.cost
            if alt < gScore[v]:
                cameFrom[v] = u
                gScore[v] = alt
                fScore[v] = alt + v.cost
                if v not in openSet:
                    openSet.append(v)
    raise Exception('No path found')

lines = read_from_input()

ocean_map = np.array([[Node(Point(x, y), float(cost)) for x, cost in enumerate(line.strip())] for y, line in enumerate(lines)])
ocean_map = expand_ocean_map(ocean_map)
start, end = create_graph(ocean_map)
print(astar(ocean_map, start, end))