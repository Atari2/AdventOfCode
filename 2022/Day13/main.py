from __future__ import annotations
from enum import IntEnum

SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename, 'r') as f:
    data = f.read().splitlines()

class ComparisonResult(IntEnum):
    OK = 0
    WRONG = 1
    NODECISION = 2

class Packet:
    _content: list[Packet|int]

    def __init__(self, content: list[Packet|int]):
        self._content = content

    def __repr__(self):
        return f"Packet({self._content})"
    
    def __str__(self):
        return f"[{','.join(map(str, self._content))}]"

    def __eq__(self, other: Packet|int):
        if isinstance(other, int):
            return self._compare(Packet([other])) == ComparisonResult.NODECISION
        return self._content == other._content

    def _compare(self, other: Packet, *, _depth = 0) -> ComparisonResult:
        for i in range(len(self._content)):
            obj1 = self._content[i]
            try:
                obj2 = other._content[i]
            except IndexError:
                return ComparisonResult.WRONG # right side ran out of items first
            if isinstance(obj1, Packet) and isinstance(obj2, Packet):
                # If both values are lists, compare the first value of each list, then the second value, and so on.
                res = obj1._compare(obj2, _depth=_depth + 1)
                if res == ComparisonResult.NODECISION:
                    continue
                return res
            elif isinstance(obj1, int) and isinstance(obj2, int):
                # If both values are integers, the lower integer should come first.
                if obj1 > obj2:
                    return ComparisonResult.WRONG
                elif obj1 < obj2:
                    return ComparisonResult.OK
            else:
                if isinstance(obj1, Packet):
                    res = obj1._compare(Packet([obj2]), _depth=_depth + 1)
                    if res == ComparisonResult.NODECISION:
                        continue
                    return res
                elif isinstance(obj2, Packet):
                    res = Packet([obj1])._compare(obj2, _depth=_depth + 1)
                    if res == ComparisonResult.NODECISION:
                        continue
                    return res
                else:
                    raise ValueError("Invalid comparison")
        return ComparisonResult.NODECISION if len(self._content) == len(other._content) else ComparisonResult.OK

    def compare(self, other: Packet) -> bool:
        res = self._compare(other) == ComparisonResult.OK
        return res

    def __lt__(self, other):
        return self.compare(other) == ComparisonResult.WRONG

    @staticmethod
    def _parse(data: str) -> tuple[Packet, int]:
        content = []
        depth = 0
        i = 0
        num = ''
        while i < len(data):
            c = data[i]
            if c == '[':
                if depth > 0:
                    c, j = Packet._parse(data[i:])
                    content.append(c)
                    i += j
                    continue
                else:
                    depth += 1
            elif c == ']':
                depth -= 1
                if num:
                    content.append(int(num))
                    num = ''
                if depth == 0:
                    return Packet(content), i+1
            elif c.isnumeric():
                num += c
            elif c == ',':
                if num:
                    content.append(int(num))
                    num = ''
            i += 1
        return Packet(content), i

    @staticmethod
    def parse(data: str) -> Packet:
        return Packet._parse(data)[0]


# part 1
pairs = [(Packet.parse(data[i]), Packet.parse(data[i+1])) for i in range(0, len(data), 3)]
r = list(filter(lambda x: x > 0, (i if pair[0].compare(pair[1]) else 0 for i, pair in enumerate(pairs, start=1))))
part1 = sum(r)

# part 2
divider_1 = Packet.parse('[[2]]')
divider_2 = Packet.parse('[[6]]')
packets = [Packet.parse(line) for line in data if line]
packets.append(divider_1)
packets.append(divider_2)
packets.sort()
part2 =(packets.index(divider_1) + 1) * (packets.index(divider_2) + 1)
print(part1, part2)