SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()

part1 = 0
points = [tuple(map(int, line.strip().split(','))) for line in data]
for i, (x1, y1) in enumerate(points):
    for (x2, y2) in points[i+1:]:
        delta_x = abs(x1 - x2) + 1
        delta_y = abs(y1 - y2) + 1
        rect_area = delta_x * delta_y
        part1 = max(part1, rect_area)

n = len(points)
v_segs = []
h_segs = []
for i in range(n):
    p1 = points[i]
    p2 = points[(i + 1) % n]
    if p1[0] == p2[0]: 
        v_segs.append((p1[0], min(p1[1], p2[1]), max(p1[1], p2[1])))
    else:
        h_segs.append((p1[1], min(p1[0], p2[0]), max(p1[0], p2[0])))

part2 = 0
for i in range(n):
    x1, y1 = points[i]
    for j in range(i + 1, n):
        x2, y2 = points[j]
        width = abs(x1 - x2) + 1
        height = abs(y1 - y2) + 1
        area = width * height
        if area <= part2:
            continue
        rx_min, rx_max = min(x1, x2), max(x1, x2)
        ry_min, ry_max = min(y1, y2), max(y1, y2)
        vertex_inside = False
        for k in range(n):
            px, py = points[k]
            if rx_min < px < rx_max and ry_min < py < ry_max:
                vertex_inside = True
                break
        if vertex_inside:
            continue
        severed = False
        for vx, v_ymin, v_ymax in v_segs:
            if rx_min < vx < rx_max:
                if v_ymin <= ry_min and v_ymax >= ry_max:
                    severed = True
                    break
        if severed: 
            continue
        for hy, h_xmin, h_xmax in h_segs:
            if ry_min < hy < ry_max:
                if h_xmin <= rx_min and h_xmax >= rx_max:
                    severed = True
                    break
        if severed: 
            continue
        cx = (rx_min + rx_max) / 2
        cy = (ry_min + ry_max) / 2
        intersections = 0
        for vx, v_ymin, v_ymax in v_segs:
            if vx > cx:
                if v_ymin < cy < v_ymax:
                    intersections += 1
        if intersections % 2 == 1:
            part2 = area

print(f'{part1} {part2}')