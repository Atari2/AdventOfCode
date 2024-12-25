from __future__ import annotations
SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()

computers: dict[str, set[str]] = {c: set() for line in data for c in line.strip().split('-')}

for line in data:
    c1, c2 = line.strip().split('-', maxsplit=1)
    computers[c1].add(c2)
    computers[c2].add(c1)

def part1():
    def find_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
        def dfs_cycle(node: str, start: str, visited: set[str], stack: list[str], cycles: list[list[str]]):
            visited.add(node)
            stack.append(node)

            for neighbor in graph.get(node, []):
                if neighbor == start and len(stack) == 3:
                    cycles.append(stack[:])
                elif neighbor not in visited and len(stack) < 3:
                    dfs_cycle(neighbor, start, visited, stack, cycles)

            stack.pop()
            visited.remove(node)

        cycles = []
        for node in graph:
            dfs_cycle(node, node, set(), [], cycles)

        return cycles

    sorted_cycles = set([tuple(sorted(cycle)) for cycle in find_cycles(computers)])

    count = sum(1 for cycle in sorted_cycles if any(node[0] == 't' for node in cycle))
    return count


def part2():
    all_cliques = []
    # https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    def bron_kerbosch1(r: set[str], p: set[str], x: set[str]):
        if len(p) == 0 and len(x) == 0:
            return r
        for v in p.copy():
            ret = bron_kerbosch1(r.union({v}), p.intersection(computers[v]), x.intersection(computers[v]))
            if ret is not None:
                all_cliques.append(ret)
            p.remove(v)
            x.add(v)
    bron_kerbosch1(set(), set(computers.keys()), set())
    longest_clique = max(all_cliques, key=len)
    return ','.join(sorted(longest_clique))

print(f'{part1()} {part2()}')