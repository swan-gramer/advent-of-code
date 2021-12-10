from functools import reduce
from os import close

score_map = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

open_characters = ['(', '[', '{', '<']
close_characters = [')', ']', '}', '>']

open_to_close = dict(zip(open_characters, close_characters))
close_to_open = dict(zip(close_characters, open_characters))

def get_winner(scores):
    p = int(len(scores)/2)
    return sorted(scores)[p]

def get_score(characters):
    return reduce(lambda score, x: score * 5 + score_map[x], characters, 0)

def get_complement(line):
    line.reverse()
    return [open_to_close[c] for c in line]

def get_incomplete(line):
    processed = []
    for c in line:
        if c in open_characters:
            processed.append(c)
        elif c in close_characters:
            if len(processed) == 0:
                return None
            if processed[-1] != close_to_open[c]:
                return None
            processed.pop()
    return processed if len(processed) else None

with open('input') as f:
    incompletes = []
    for line in f:
        incomplete = get_incomplete(line.strip())
        if incomplete:
            incompletes.append(incomplete)

    complements = map(get_complement, incompletes)
    scores = map(get_score, complements)

    print("Answer is: {}".format(get_winner(list(scores))))