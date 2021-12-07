from collections import defaultdict

def fuel_cost(step, mode):
    if mode == 'p1':
        return step
    else:
        return sum(range(step + 1))

with open('input') as f:
    input = map(int, f.readline().strip().split(','))
    crab_map = defaultdict(int)
    for p in input:
        crab_map[p] += 1

    items = crab_map.items()
    moves_1 = [sum([fuel_cost(abs(px - py), 'p1') * cy for py, cy in items]) for px, cx in items]

    crab_positions = sorted(crab_map.keys())
    moves_2 = [sum([fuel_cost(abs(px - py), 'p2') * cy for py, cy in items]) for px in range(crab_positions[0], crab_positions[-1]+1)]

    print("Part one answer: {}".format(sorted(moves_1)[0]))
    print("Part two answer: {}".format(sorted(moves_2)[0]))
