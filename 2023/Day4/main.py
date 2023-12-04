from __future__ import annotations

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

with open(filename, "r") as f:
    lines = f.read().splitlines()

class Card:
    points: int
    matching_numbers: int
    total_qty: int

    def _calc_points(self, winning_numbers: list[int], total_numbers: list[int]) -> int:
        total = 0
        for n in winning_numbers:
            if n in total_numbers:
                total = 1 if total == 0 else total * 2
        return total

    def __init__(self, line: str):
        _, numbers = line.split(":", 1)
        winning_numbers, total_numbers = [n.strip() for n in numbers.split("|", 1)]
        winning_numbers = [int(x) for x in winning_numbers.split(" ") if x]
        total_numbers = [int(x) for x in total_numbers.split(" ") if x]
        self.points = self._calc_points(winning_numbers, total_numbers)
        self.total_qty = 1
        self.matching_numbers = sum((1 for n in winning_numbers if n in total_numbers))


cards = [Card(line) for line in lines]
totalp1 = sum((card.points for card in cards))

for i, card in enumerate(cards):
    for other in cards[i+1:i+1+card.matching_numbers]:
        other.total_qty += card.total_qty

totalp2 = sum((card.total_qty for card in cards))

print(f"{totalp1} {totalp2}")
