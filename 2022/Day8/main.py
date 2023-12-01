import numpy

SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename, 'r') as f:
    data = f.read().splitlines()

visible_count = 0
scenic_score = 1
tree_map = numpy.array([[int(x, 10) for x in line] for line in data])
rows, cols = tree_map.shape
for i in range(rows):
    for j in range(cols):
        num = tree_map[i,j]
        slices = [tree_map[i,:j][::-1], tree_map[i, j+1:], tree_map[0: i, j][::-1], tree_map[i+1:, j]]
        # part 1
        visible_count += (on_edge := any((x.size == 0 for x in slices))) or any((x.max() < num for x in slices))
        # part 2
        if on_edge:
            continue
        cur_tree_scenic_score = 1
        for line in slices:
            score_line: numpy.ndarray = line < num
            if score_line.all():
                cur_line_score = line.size
            else:
                cur_line_score = int(score_line.argmin()) + 1
            cur_tree_scenic_score *= cur_line_score
        scenic_score = max(scenic_score, cur_tree_scenic_score)

print(f'{visible_count} {scenic_score}')