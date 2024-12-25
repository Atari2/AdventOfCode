import numpy as np
import numpy.typing as npt
import itertools

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = [l for line in f if (l := line.strip())]

class Key:
    pin_heights: npt.NDArray
    key: npt.NDArray

    def __init__(self, key: npt.NDArray):
        self.key = key
        self.pin_heights = np.count_nonzero(key == "#", axis=0)

    def __repr__(self) -> str:
        return f"Key({self.pin_heights})"

class Lock:
    pin_heights: npt.NDArray
    lock: npt.NDArray

    def __init__(self, lock: npt.NDArray):
        self.lock = lock
        self.pin_heights = np.count_nonzero(lock == "#", axis=0)

    def __repr__(self) -> str:
        return f"Lock({self.pin_heights})"
    
def fits(key: Key, lock: Lock):
    return np.all((key.pin_heights + lock.pin_heights) <= 5)

keys = []
locks = []

for schematic in itertools.batched(data, 7):
    assert len(schematic) == 7
    if schematic[0] == "#####" and schematic[6] == ".....":
        locks.append(Lock(np.array([[c for c in line] for line in schematic[1:6]])))
    elif schematic[0] == "....." and schematic[6] == "#####":
        keys.append(Key(np.array([[c for c in line] for line in schematic[1:6]])))
    else:
        raise ValueError("Invalid schematic")


part1 = sum(1 for key in keys for lock in locks if fits(key, lock))
print(f'{part1} 0') # 0 is the placeholder answer for part2