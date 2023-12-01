import numpy as np

def read_from_input():
    with open('input.txt', 'r') as f:
        return f.read()

dots, folds = [x.split('\n') for x in read_from_input().split('\n\n')]

max_x = 0
max_y = 0

class Point:
    def __init__(self, x, y):
        global max_x, max_y
        self.x = x
        self.y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def __repr__(self):
        return self.__str__()

class Fold:
    axis: str
    value: int

    def __init__(self, axis: str, value: str):
        self.axis = axis
        self.value = int(value)
    
    def __str__(self):
        return f"(axis: {self.axis}, value: {self.value})"
    
    def __repr__(self):
        return self.__str__()


dots = [Point(*map(int, x.split(','))) for x in dots]
folds = [Fold(*x.split(' ')[-1].split('=')) for x in folds]

matrix = np.zeros(shape=(max_y+1, max_x+1))
for dot in dots:
    matrix[dot.y][dot.x] = 1

def do_fold(matrix: np.array, fold: Fold):
    rows, cols = matrix.shape
    if fold.axis == 'y':
        new_matrix = matrix[0:fold.value, :]
    else:
        new_matrix = matrix[:, 0:fold.value]
    if fold.axis == 'x':
        for i in range(rows):
            for j in range(fold.value):
                if new_matrix[i][j] == 0:
                    new_matrix[i][j] = matrix[i][cols - j - 1]
    elif fold.axis == 'y':
        for i in range(fold.value):
            for j in range(cols):
                if new_matrix[i][j] == 0:
                    new_matrix[i][j] = matrix[rows - i - 1][j]

    return new_matrix

def visible_dots(matrix: np.array):
    rows, cols = matrix.shape
    visible = 0
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1:
                visible += 1
    return visible

for i, f in enumerate(folds):
    matrix = do_fold(matrix, f)
    if i == 0:
        print(f"Visible dots after first fold: {visible_dots(matrix)}")

for row in matrix:
    for value in row:
        print('#' if value == 1 else '.', end='')
    print('\n')