from collections import deque, namedtuple
from functools import reduce

risk_map = {}
size = 0
with open('input') as f:
    x = 0
    for line in f:
        y = 0
        for c in line.strip():
            val = int(c)
            risk_map[(x, y)] = val - 9 if val > 9 else val
            y += 1
        x += 1
    size = x

scale = 5
scaled_size = scale * size

risk_map_level2 = {}
for n in range(0, 10):
    value_map = {}
    for i in range(0, scale):
        for j in range(0, scale):
            if i == 0 and j == 0:
                value_map[(i, j)] = n
                continue
            p_value = value_map[(i, j - 1)] if (i, j-1) in value_map else value_map[(i-1, j)]
            new_value = 1 if p_value == 9 else p_value + 1
            value_map[(i, j)] = new_value
    risk_map_level2[n] = value_map


def get_risk(target):
    tx, ty = target
    dx = int(tx/size)
    dy = int(ty/size)
    qx = tx % size
    qy = ty % size
    base_risk = risk_map[(qx, qy)]
    return risk_map_level2[base_risk][(dx, dy)]

class PInfo:
    def __init__(self, p, r, total):
        self.previous = p
        self.risk = r
        self.total = total

path_map = {}
def update(target, source):
    source_info = path_map[source]
    if target not in path_map:
        risk = get_risk(target)
        target_info = PInfo(source, risk, source_info.total + risk)
        path_map[target] = target_info
        return True
    else:
        target_info = path_map[target]
        new_total = source_info.total + target_info.risk
        if new_total < target_info.total:
            target_info.total = new_total
            target_info.previous = source
            return True
        return False

def get_adjacents(p):
    px, py = p
    candidates = [(px + i, py + j) for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
    result = filter(lambda v: 0 <= v[0] < scaled_size and 0 <= v[1] < scaled_size, candidates)
    return result

def build_path_map():
    path_map[(0,0)] = PInfo(None, get_risk((0,0)), 0)

    waiting_list = deque()
    waiting_list.append((0, 0))
    while len(waiting_list):
        p = waiting_list.popleft()
        p_info = path_map[p]
        adjacents = get_adjacents(p)
        for ap in adjacents:
            if ap != p_info.previous:
                updated = update(ap, p)
                if updated and ap != (scaled_size - 1, scaled_size - 1):
                    waiting_list.append(ap)


build_path_map()

info = path_map[scaled_size - 1, scaled_size - 1]
print("Answer is {}".format(info.total))