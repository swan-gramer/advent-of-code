from collections import defaultdict


def parse_coordinate(value):
    return list(map(int, value.split(',')))


def is_horizontal_line(start, end):
    return start[1] == end[1]


def is_vertical_line(start, end):
    return start[0] == end[0]


def is_diagonal_line(start, end):
    return abs(start[0] - end[0]) == abs(start[1] - end[1])


def get_points_for_line(start, end):
    if is_horizontal_line(start, end):
        row = start[1]
        column_start, column_end = sorted([start[0], end[0]])
        return [(column, row) for column in range(column_start, column_end + 1)]
    elif is_vertical_line(start, end):
        row_start, row_end = sorted([start[1], end[1]])
        column = start[0]
        return [(column, row) for row in range(row_start, row_end + 1)]
    elif is_diagonal_line(start, end):
        row_step = 1 if end[1] > start[1] else -1
        column_step = 1 if end[0] > start[0] else -1
        row_values = range(start[1], end[1] + row_step, row_step)
        column_values = range(start[0], end[0] + column_step, column_step)
        return zip(column_values, row_values)
    else:
        return []


with open('input') as f:
    overlap_counter_p1 = defaultdict(int)
    overlap_counter_p2 = defaultdict(int)
    for line in f:
        start, end = list(map(parse_coordinate, line.strip().split(' -> ')))
        points_to_mark = get_points_for_line(start, end)
        p2_only = is_diagonal_line(start, end)
        for point in points_to_mark:
            if not p2_only:
                overlap_counter_p1[point] += 1
            overlap_counter_p2[point] += 1

    print('Part one answer: {}'.format(sum([int(val > 1) for val in overlap_counter_p1.values()])))
    print('Part two answer: {}'.format(sum([int(val > 1) for val in overlap_counter_p2.values()])))
