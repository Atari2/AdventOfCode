def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

def part2():
    class Submarine:
        horz: int
        depth: int
        aim: int

        def __init__(self, horz, depth, aim):
            self.horz = horz
            self.depth = depth
            self.aim = aim

        def move(self, direction, quantity):
            if direction == 'forward':
                self.horz += quantity
                self.depth += quantity * self.aim
            elif direction == 'down':
                self.aim += quantity
            elif direction == 'up':
                self.aim -= quantity
            else:
                raise ValueError('Invalid direction')
        
        def get_multiplied_position(self):
            return self.horz * self.depth


    sub = Submarine(0, 0, 0)
    input = [line.split() for line in read_from_input()]
    input = [(direction, int(quantity)) for direction, quantity in input]
    for direction, quantity in input:
        sub.move(direction, quantity)
    print(sub.get_multiplied_position())

def part1():
    class Submarine:
        horz: int
        depth: int

        def __init__(self, horz, depth):
            self.horz = horz
            self.depth = depth

        def move(self, direction, quantity):
            if direction == 'forward':
                self.horz += quantity
            elif direction == 'down':
                self.depth += quantity
            elif direction == 'up':
                self.depth -= quantity
            else:
                raise ValueError('Invalid direction')
        
        def get_multiplied_position(self):
            return self.horz * self.depth

    sub = Submarine(0, 0)
    input = [line.split() for line in read_from_input()]
    input = [(direction, int(quantity)) for direction, quantity in input]
    for direction, quantity in input:
        sub.move(direction, quantity)
    print(sub.get_multiplied_position())


part1()
part2()