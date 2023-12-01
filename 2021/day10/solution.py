def read_from_input():
    with open('input.txt', 'r') as f:
        return f.readlines()

points = {
    '(': 3,
    ')': 3,
    '[': 57,
    ']': 57,
    '}': 1197,
    '{': 1197,
    '<': 25137,
    '>': 25137,
}

openers_match = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

openers = ['(', '[', '{', '<']
closers = [')', ']', '}', '>']

tot_points = 0
scores = []
for i, line in enumerate(read_from_input()):
    stack = []
    for c in line.strip():
        if c in openers:
            stack.append(c)
        elif c in closers:
            if len(stack) == 0:
                print(f'Too many closer characters at line {i}, exiting')
                exit(1)
            if points[c] != points[stack.pop()]:
                tot_points += points[c]
                stack.clear()
                break
        else:
            print(f'Unknown character {c} at line {i}, exiting')
            exit(1)
    score = 0
    while len(stack) > 0:
        score *= 5
        c = stack.pop()
        p = openers_match[c]
        score += p
    if score != 0:
        scores.append(score)
print(sorted(scores)[len(scores) // 2])
print(tot_points)