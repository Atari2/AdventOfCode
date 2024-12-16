import numpy as np
SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = [line.strip() for line in f]

warehouse = np.array([[c for c in l] for l in data[:data.index('')]], dtype=str)
wider_warehouse = []
for row in warehouse:
    new_row = []
    for col in row:
        match col:
            case '#':
                new_row.extend(['#', '#'])
            case '.':
                new_row.extend(['.', '.'])
            case 'O':
                new_row.extend(['[', ']'])
            case '@':
                new_row.extend(['@', '.'])
    wider_warehouse.append(new_row)
wider_warehouse = np.array(wider_warehouse)
movements = ''.join(data[data.index('')+1:])

def part1():
    robot = np.argwhere(warehouse == '@')[0]

    def move_box(box_position, direction) -> bool:
        if warehouse[*(box_position + direction)] == '.':
            # empty space
            warehouse[*box_position] = '.'
            box_position += direction
            warehouse[*box_position] = 'O'
            return True
        elif warehouse[*(box_position + direction)] == 'O':
            # another box
            if not move_box(box_position + direction, direction):
                return False
            warehouse[*box_position] = '.'
            box_position += direction
            warehouse[*box_position] = 'O'
            return True
        else:
            return False
    
    def move(direction):
        nonlocal robot
        new_position = np.add(robot, direction)
        if (cell := warehouse[*new_position]) == '.':
            warehouse[*robot] = '.'
            robot = new_position
            warehouse[*robot] = '@'
        elif cell == 'O':
            # box
            if move_box(new_position, direction):
                warehouse[*robot] = '.'
                robot += direction
                warehouse[*robot] = '@'

    for m in movements:
        match m:
            case '^':
                move([-1, 0])
            case 'v':
                move([1, 0])
            case '<':
                move([0, -1])
            case '>':
                move([0, 1])
    tot = 0
    for x, y in np.argwhere(warehouse == 'O'):
        tot += (x * 100) + y
    return tot

def part2():
    robot = np.argwhere(wider_warehouse == '@')[0]

    def move_box_horizontal(box_positions, direction) -> bool:
        lbox, rbox = box_positions
        if (direction == [0, 1] and wider_warehouse[*(rbox + direction)] == '.') or \
            (direction == [0, -1] and wider_warehouse[*(lbox + direction)] == '.'):
            # empty space
            wider_warehouse[*lbox] = '.'
            wider_warehouse[*rbox] = '.'
            lbox += direction
            rbox += direction
            wider_warehouse[*lbox] = '['
            wider_warehouse[*rbox] = ']'
            return True       
        elif (direction == [0, 1] and wider_warehouse[*(rbox + direction)] == '[') or \
              (direction == [0, -1] and wider_warehouse[*(lbox + direction)] == ']'):
            # box in the direction, either left or right
            # [][][]
            #   ^^ current box
            if not move_box_horizontal([lbox + np.multiply(direction, 2), rbox + np.multiply(direction, 2)], direction):
                return False
            wider_warehouse[*lbox] = '.'
            wider_warehouse[*rbox] = '.'
            lbox += direction
            rbox += direction
            wider_warehouse[*lbox] = '['
            wider_warehouse[*rbox] = ']'
            return True
        else:
            return False
            

    def move_box_vertical(box_positions, direction) -> bool:
        lbox, rbox = box_positions
        global wider_warehouse
        if wider_warehouse[*(lbox + direction)] == '.' and wider_warehouse[*(rbox + direction)] == '.':
            # empty space
            # ..
            # [] -> current box
            # ..
            wider_warehouse[*lbox] = '.'
            wider_warehouse[*rbox] = '.'
            lbox += direction
            rbox += direction
            wider_warehouse[*lbox] = '['
            wider_warehouse[*rbox] = ']'
            return True
        elif wider_warehouse[*(lbox + direction)] == '[':  # two boxes on top of each other
            # another box on top or bottom
            # []
            # [] -> current box
            # []
            if not move_box_vertical([lbox + direction, rbox + direction], direction):
                return False
            wider_warehouse[*lbox] = '.'
            wider_warehouse[*rbox] = '.'
            lbox += direction
            rbox += direction
            wider_warehouse[*lbox] = '['
            wider_warehouse[*rbox] = ']'
            return True
        elif wider_warehouse[*(lbox + direction)] == ']' and wider_warehouse[*(rbox + direction)] == '[':
            # a box with 2 boxes on top or on bottom, each half
            # [][]
            # .[]. -> current box
            # [][]
            box1 = [lbox + direction + [0,-1], lbox + direction]
            box2 = [rbox + direction, rbox + direction + [0,1]]
            saved_warehouse = np.copy(wider_warehouse)
            b1m = move_box_vertical(box1, direction)
            b2m = move_box_vertical(box2, direction)
            if b1m and b2m:
                wider_warehouse[*lbox] = '.'
                wider_warehouse[*rbox] = '.'
                lbox += direction
                rbox += direction
                wider_warehouse[*lbox] = '['
                wider_warehouse[*rbox] = ']'
                return True
            else:
                # if one of the boxes can't move, revert the changes
                wider_warehouse = saved_warehouse
                return False
        elif wider_warehouse[*(lbox + direction)] == ']' and wider_warehouse[*(rbox + direction)] == '.':
            # a box with another box on top or bottom but shifted left
            # [].
            # .[] -> current box
            # [].
            box1 = [lbox + direction + [0, -1], lbox + direction]
            if not move_box_vertical(box1, direction):
                return False
            wider_warehouse[*lbox] = '.'
            wider_warehouse[*rbox] = '.'
            lbox += direction
            rbox += direction
            wider_warehouse[*lbox] = '['
            wider_warehouse[*rbox] = ']'
            return True
        elif wider_warehouse[*(rbox + direction)] == '[' and wider_warehouse[*(lbox + direction)] == '.':
            # a box with another box on top or bottom but shifted right
            # .[]
            # []. -> current box
            # .[]
            box2 = [rbox + direction, rbox + direction + [0, 1]]
            if not move_box_vertical(box2, direction):
                return False
            wider_warehouse[*lbox] = '.'
            wider_warehouse[*rbox] = '.'
            lbox += direction
            rbox += direction
            wider_warehouse[*lbox] = '['
            wider_warehouse[*rbox] = ']'
            return True
        else:
            return False
    
    def move(direction):
        nonlocal robot
        new_position = np.add(robot, direction)
        if (cell := wider_warehouse[*new_position]) == '.':
            wider_warehouse[*robot] = '.'
            robot = new_position
            wider_warehouse[*robot] = '@'
        elif cell == '[' or cell == ']':
            if direction == [0, 1] or direction == [0, -1]:
                boxes = [new_position, new_position + [0, 1]] if cell == '[' else [new_position + [0, -1], new_position]
                if move_box_horizontal(boxes, direction):
                    wider_warehouse[*robot] = '.'
                    robot += direction
                    wider_warehouse[*robot] = '@'
            else:
                boxes = [new_position, new_position + [0, 1]] if cell == '[' else [new_position + [0, -1], new_position]
                if move_box_vertical(boxes, direction):
                    wider_warehouse[*robot] = '.'
                    robot += direction
                    wider_warehouse[*robot] = '@'

    for m in movements:
        match m:
            case '^':
                move([-1, 0])
            case 'v':
                move([1, 0])
            case '<':
                move([0, -1])
            case '>':
                move([0, 1])
    tot = 0
    for x, y in np.argwhere(wider_warehouse == '['):
        tot += (x * 100) + y
    return tot
print(f'{part1()} {part2()}')