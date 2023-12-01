from __future__ import annotations
from functools import reduce
from typing import Literal, Callable
import copy
import re

op_patt = re.compile(r"Operation: new = (old|\d+) (\W) (old|\d+)")

SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename, 'r') as f:
    data = list(map(lambda x: x.strip(), filter(lambda x: len(x) > 0, f.read().splitlines())))

class Item:
    worry_level: int

    def __init__(self, worry_level: int) -> None:
        self.worry_level = worry_level


class Monkey:
    _items: list[Item]
    _count_inspected_items: int
    _op: Callable[[int, int], int]
    _test: Callable[[int], int]
    _selector: int
    op_dict = {
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y
    }

    def __init__(self):
        self._count_inspected_items = 0

    def receive_item(self, item: Item) -> None:
        self._items.append(item)

    def add_items(self, items: str) -> None:
        self._items = [Item(int(item)) for item in items[len("Starting items: "):].split(", ")]
    
    def add_operation(self, operation: str) -> None:
        m = op_patt.match(operation)
        if m:
            op1, op0, op2 = m.groups()
            func = self.op_dict[op0]
            if op1 == 'old' and op2 == 'old':
                self._op = lambda x, y: func(x, y)
            elif op1 == 'old':
                op2 = int(op2)
                self._op = lambda x, _: func(x, op2)
            else:
                op1 = int(op1)
                self._op = lambda _, y: func(op1, y)
    
    
    def add_test(self, test: str, true: str, false: str) -> None:
        self._selector = int(test[len("Test: divisible by "):])
        test_true = int(true[len("If true: throw to monkey"):])
        test_false = int(false[len("If false: throw to monkey"):])
        self._test = lambda arg: test_true if arg % self._selector == 0 else test_false

    def inspect_items(self, monkeys: list[Monkey], reducer: int|None = None) -> None:
        to_remove = []
        for item in self._items:
            self._count_inspected_items += 1
            if reducer is None:
                cur_worry_level = self._op(item.worry_level, item.worry_level) // 3
                other_monkey = self._test(cur_worry_level)
                item.worry_level = cur_worry_level
                monkeys[other_monkey].receive_item(item)
            else:
                cur_worry_level = self._op(item.worry_level, item.worry_level) % reducer
                other_monkey = self._test(cur_worry_level)
                item.worry_level = cur_worry_level
                monkeys[other_monkey].receive_item(item)
            to_remove.append(item)
        for item in to_remove:
            self._items.remove(item)
    
    @property
    def count_inspected_items(self) -> int:
        return self._count_inspected_items
    
    @property
    def selector(self) -> int:
        return self._selector



monkeys_1: list[Monkey] = []
split_data = [data[i:i+6] for i in range(0, len(data), 6)]
for _, items, operation, test, true, false in split_data:
    monkey = Monkey()
    monkey.add_items(items)
    monkey.add_operation(operation)
    monkey.add_test(test, true, false)
    monkeys_1.append(monkey)
monkeys_2 = copy.deepcopy(monkeys_1)

for _ in range(20):
    for m in monkeys_1:
        m.inspect_items(monkeys_1)
part1 = reduce(lambda x, y: x * y, (sorted((map(lambda x: x.count_inspected_items, monkeys_1)), reverse=True)[:2]))

reducer = reduce(lambda x, y: x * y, map(lambda x: x.selector, monkeys_2))
for i in range(10_000):
    for m in monkeys_2:
        m.inspect_items(monkeys_2, reducer)
part2 = reduce(lambda x, y: x * y, (sorted((map(lambda x: x.count_inspected_items, monkeys_2)), reverse=True)[:2]))

print(part1, part2)