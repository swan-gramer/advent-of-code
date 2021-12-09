def get_adjacents(x, y, height_map):
    adjacents = []
    max_x = len(height_map) - 1
    max_y = len(height_map[0]) - 1
    if x > 0:
        adjacents.append((x - 1,y))
    if x < max_x:
        adjacents.append((x + 1,y))
    if y > 0:
        adjacents.append((x,y - 1))
    if y < max_y:
        adjacents.append((x, y + 1))
    return adjacents


def get_basin_size(low_point, height_map):
    def get_higher_adjacents(point):
        x, y = point
        value = height_map[x][y]
        adjacents = get_adjacents(x, y, height_map)

        def filter_helper(p):
            pv = height_map[p[0]][p[1]]
            return pv != 9 and pv > value

        larger_adjacents = filter(filter_helper, adjacents)

        return {point}.union(*[get_higher_adjacents(p) for p in larger_adjacents])

    adjacents = get_higher_adjacents(low_point)
    return len(adjacents)


with open('input') as f:
    height_map = []
    for line in f:
        row = list(map(int, line.strip()))
        height_map.append(row)

    map_size = (len(height_map), len(height_map[0]))
    low_points = []
    p1_answer = 0
    for x in range(map_size[0]):
        for y in range(map_size[1]):
            adjacents = get_adjacents(x, y, height_map)
            adjacent_vals = [height_map[p[0]][p[1]] for p in adjacents]
            val = height_map[x][y]
            if val < min(adjacent_vals):
                low_points.append((x, y))
                p1_answer += val + 1

    basin_sizes = []
    for p in low_points:
        basin_sizes.append(get_basin_size(p, height_map))

    max_three = sorted(basin_sizes, reverse=True)[:3]

    print("Part one answer is: {}".format(p1_answer))
    print("Part two answer is: {}".format(max_three[0]*max_three[1]*max_three[2]))

