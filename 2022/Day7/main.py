from __future__ import annotations
from typing import Callable

SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename, 'r') as f:
    data = f.read().splitlines()

class File:
    def __init__(self, size, name, parent):
        self.name = name
        self.parent = parent
        self.size = int(size)
    
    def __contains__(self, item):
        return False
    
    @property
    def children(self):
        return []
    
    def __eq__(self, other):
        if isinstance(other, File):
            return self.name == other.name and self.size == other.size and self.parent == other.parent
        elif isinstance(other, str):
            return self.name == other
        raise ValueError(f'Cannot compare File with {type(other)}')

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children: list[Directory|File] = []
        self._cache_size = None
    
    def add_child(self, child):
        self.children.append(child)
    
    def __eq__(self, other):
        if isinstance(other, Directory):
            return self.name == other.name and self.parent == other.parent and self.children == other.children
        elif isinstance(other, str):
            return self.name == other
        raise ValueError(f'Cannot compare Directory with {type(other)}')

    def __contains__(self, item):
        return item in self.children
    
    def format_self(self, depth):
        ret = f'{" "*depth}- {self.name} (dir, size={self.total_size()})\n'
        for i in self.children:
            if isinstance(i, Directory):
                ret += i.format_self(depth+1)
            else:
                ret += f'{" "*(depth+1)}- {i.name} (file, size={i.size})\n'
        return ret

    def total_size(self):
        if self._cache_size:
            return self._cache_size
        ret = 0
        for i in self.children:
            if isinstance(i, Directory):
                ret += i.total_size()
            else:
                ret += i.size
        self._cache_size = ret
        return ret
    
    def __str__(self) -> str:
        return self.format_self(0)
    
    def filter_directories(self, cond: Callable):
        if cond(self):
            yield self
        for i in self.children:
            if isinstance(i, Directory):
                yield from i.filter_directories(cond)
    

root_dir = Directory('/', None)
curr_dir: Directory = root_dir
in_ls = False

for line in data:
    if line.startswith('$ cd'):
        in_ls = False
        if curr_dir:
            new_dir_name = line.split(' ')[-1]
            if new_dir_name == '..':
                if not curr_dir.parent:
                    raise ValueError('Cannot go up from root directory')
                curr_dir = curr_dir.parent
            elif new_dir_name == '/':
                curr_dir = root_dir
            elif new_dir_name in curr_dir:
                curr_dir = curr_dir.children[curr_dir.children.index(new_dir_name)] # type: ignore
            else:
                curr_dir = Directory(new_dir_name, curr_dir)
                curr_dir.parent.add_child(curr_dir)
        else:
            curr_dir = Directory(line.split(' ')[-1], None)
            root_dir = curr_dir
    elif line.startswith('$ ls'):
        in_ls = True
    else:
        if in_ls:
            if line.startswith('dir'):
                curr_dir.add_child(Directory(line.split(' ')[-1], curr_dir))
            else:
                size, name = line.split(' ', 1)
                curr_dir.add_child(File(size, name, curr_dir))
        else:
            raise ValueError(f'Invalid line: {line}')
total_space_available = 70_000_000
wanted_space = 30_000_000
part1 = sum(map(lambda x: x.total_size(), root_dir.filter_directories(lambda x: x.total_size() <= 100_000)))
needed_space = wanted_space - (total_space_available - root_dir.total_size())
part2 = sorted(list(root_dir.filter_directories(lambda x: x.total_size() >= needed_space)), key=lambda x: x.total_size())[0].total_size()
print(f'{part1} {part2}')