from __future__ import annotations
from functools import cmp_to_key
SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = [l.strip() for l in f]

class OrderingRule:
    pageX: int
    pageY: int

    def __init__(self, x: int, y: int):
        self.pageX = x
        self.pageY = y

    @staticmethod
    def from_string(s: str):
        x, y = s.split("|")
        return OrderingRule(int(x), int(y))
    
    def is_update_valid(self, update: Update):
        try:
            return update.pages.index(self.pageX) < update.pages.index(self.pageY)
        except ValueError:
            return True
    
    def __repr__(self):
        return f"OrderingRule: {self.pageX} | {self.pageY}"

class Update:
    pages: list[int]

    def __init__(self, pages: list[int]):
        self.pages = pages

    @staticmethod
    def from_string(s: str):
        return Update([int(x) for x in s.split(',')])
    
    def center_page(self):
        return self.pages[len(self.pages) // 2]
    
    def fix_update(self, rules: list[OrderingRule]):
        def comparer(lhs: int, rhs: int):
            for r in rules:
                if r.pageX == lhs and r.pageY == rhs:
                    return -1
                if r.pageX == rhs and r.pageY == lhs:
                    return 1
            raise ValueError(f"Invalid ordering: {lhs} {rhs}")
        self.pages.sort(key=cmp_to_key(comparer))
    
    def __repr__(self):
        return f"Update: {self.pages}"
    

divider_idx = data.index('')
rules = [OrderingRule.from_string(x) for x in data[:divider_idx]]
updates = [Update.from_string(x) for x in data[divider_idx+1:]]
part1 = 0
part2 = 0
for up in updates:
    if all((rule.is_update_valid(up) for rule in rules)):
        part1 += up.center_page()
    else:
        up.fix_update(rules)
        part2 += up.center_page() 
print(f'{part1} {part2}')
