from __future__ import annotations
from typing import Union

def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

paths: list[list[str]] = []

class Cave:
    name: str
    is_big: bool
    visited_count: int
    connected_to: set[Cave]
    is_end: False

    def __init__(self, name: str, connected_to: Cave):
        self.name = name
        self.is_big = name.isupper()
        self.visited_count = 0
        if connected_to is not None:
            self.connected_to = {connected_to}
        else:
            self.connected_to = set()
    
    def __str__(self):
        return f"{self.name} connected to {', '.join([c.name for c  in self.connected_to])}"

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: Union[Cave, str]):
        if isinstance(other, Cave):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        raise ValueError(f'{other} is not a Cave or str')
    
    def __hash__(self):
        return hash(self.name)

    def visitable(self, already_counted: bool):
        return (self.visited_count == 0 if already_counted else self.visited_count < 2) or self.is_big

    def explore(self, current_path: list[Cave] = [], already_counted: bool = False):
        if not self.visitable(already_counted):
            return
        if self.name == 'end':
            current_path.append(self)
            paths.append([c.name for c in current_path])
            current_path.pop()
            return
        self.visited_count += 1
        for cave in filter(lambda c: c.name != 'start', self.connected_to):
            current_path.append(self)
            if already_counted:
                cave.explore(current_path, already_counted)
            else:
                cave.explore(current_path, False if self.is_big else self.visited_count > 1)
            current_path.pop()
        self.visited_count -= 1
            

caves: dict[str, Cave] = {

}

for line in read_from_input():
    line = line.strip()
    first_cave, second_cave = line.split('-', 1)
    if first_cave in caves and second_cave in caves:
        caves[first_cave].connected_to.add(caves[second_cave])
        caves[second_cave].connected_to.add(caves[first_cave])
    elif first_cave in caves:
        second = Cave(second_cave, caves[first_cave])
        caves[first_cave].connected_to.add(second)
        caves[second_cave] = second
    elif second_cave in caves:
        first = Cave(first_cave, caves[second_cave])
        caves[second_cave].connected_to.add(first)
        caves[first_cave] = first
    else:
        first = Cave(first_cave, None)
        second = Cave(second_cave, first)
        first.connected_to = {second}
        caves[first_cave] = first
        caves[second_cave] = second

start_cave: Cave = caves['start']
end_cave: Cave = caves['end']

start_cave.explore()
print(len(paths))