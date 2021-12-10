from functools import reduce
from os import close

score_map = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

open_characters = ['(', '[', '{', '<']
close_characters = [')', ']', '}', '>']

open_to_close = dict(zip(open_characters, close_characters))
close_to_open = dict(zip(close_characters, open_characters))

def cal_total_score(characters):
    return reduce(lambda total, x: score_map.get(x, 0) + total, characters, 0)

def get_corrupted_character(line):
    processed = []
    for c in line:
        if c in open_characters:
            processed.append(c)
        elif c in close_characters:
            if len(processed) == 0:
                return c
            if processed[-1] != close_to_open[c]:
                return c
            processed.pop()
    return None

with open('input') as f:
    corrupted_characters = []
    for line in f:
        first_corruption = get_corrupted_character(line.strip())
        if first_corruption:
            corrupted_characters.append(first_corruption)

    print("Part one answer is: {}".format(cal_total_score(corrupted_characters)))