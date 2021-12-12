from collections import defaultdict, deque
from queue import Queue

small_caves = set()
big_caves = set()
cave_map = defaultdict(set)
with open('input') as f:
    for line in f:
        path = line.strip().split('-')
        for cave in path:
            big_caves.add(cave) if cave.isupper() else small_caves.add(cave)
        cave_map[path[0]].add(path[1])
        cave_map[path[1]].add(path[0])


result = []
def find_path(path, processed_caves, special_cave):
    if len(path) == 0:
        return

    end_cave = path[-1]
    if end_cave == 'end':
        if path not in result:
            result.append(path)
        return

    if end_cave in small_caves:
        if end_cave == special_cave:
            special_cave = None
        else:
            processed_caves.add(end_cave)

    for cave in cave_map[end_cave]:
        if cave not in processed_caves:
            new_path = path.copy()
            new_path.append(cave)
            find_path(new_path, processed_caves.copy(), special_cave)

for special_cave in small_caves - {'start', 'end'}:
    find_path(['start'], set(), special_cave)

print("Answer is {}".format(len(result)))



