SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.read()

def is_repeating_digits_twice(n_str: str) -> bool:
    k = len(n_str)
    if k % 2 != 0:
        return False
    half_k = k // 2
    first_half = n_str[:half_k]
    second_half = n_str[half_k:]
    return first_half == second_half

def is_repeating_digits_at_least_twice(n_str: str) -> bool:
    k = len(n_str)
    for size in range(1, k // 2 + 1):
        if k % size == 0:
            num_repeats = k // size
            part = n_str[:size]
            if part * num_repeats == n_str:
                return True
    return False

ranges = [tuple(map(int, data_part.split('-'))) for data_part in data.split(',')]
p1 = 0
p2 = 0
for s, e in ranges:
    for n in range(s, e + 1):
        n_str = str(n)
        if is_repeating_digits_twice(n_str):
            p1 += n
            p2 += n
        elif is_repeating_digits_at_least_twice(n_str):
            p2 += n
print(f'{p1} {p2}')