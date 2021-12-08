from collections import defaultdict, namedtuple

wire_digit_map = {
    'abcefg': 0,
    'cf': 1,
    'acdef': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9
}


length_wire_map = defaultdict(list)
for key in wire_digit_map.keys():
    length_wire_map[len(key)].append(key)

print(length_wire_map)

def deduce_segment_wire_map(inputs):
    result = [None] * 10
    input_map = defaultdict(list)
    for entry in inputs:
        input_map[len(entry)].append(entry)

    result[1] = input_map[2][0]
    result[4] = input_map[4][0]
    result[7] = input_map[3][0]
    result[8] = input_map[7][0]

    set_1 = set(result[1])
    for entry in input_map[6]:
        set_entry = set(entry)
        if len(set_entry.intersection(set_1)) == 1:
            result[6] = entry
            input_map[6].remove(entry)
            break

    set_6 = set(result[6])
    for entry in input_map[5]:
        set_entry = set(entry)
        if len(set_entry.intersection(set_6)) == 5:
            result[5] = entry
            input_map[5].remove(entry)
            break

    set_5 = set(result[5])
    for entry in input_map[6]:
        set_entry = set(entry)
        if len(set_entry.intersection(set_5)) == 4:
            result[0] = entry
        elif len(set_entry.intersection(set_5)) == 5:
            result[9] = entry

    set_9 = set(result[9])
    for entry in input_map[5]:
        set_entry = set(entry)
        if len(set_entry.intersection(set_9)) == 4:
            result[2] = entry
        elif len(set_entry.intersection(set_9)) == 5:
            result[3] = entry

    sorted_result = [''.join(sorted(x)) for x in result]
    return dict(zip(sorted_result, list('0123456789')))


def get_number(inputs, outputs):
    digit_map = deduce_segment_wire_map(inputs)

    return int(''.join(map(lambda x: digit_map[''.join(sorted(x))], outputs)))


p1_answer = 0
p2_answer = 0
with open('input') as f:
    for line in f:
        wire_segment_map = {}
        inputs, outputs = [entries.strip().split(' ') for entries in line.split('|')]
        for output in outputs:
            if len(output) in {2, 3, 4, 7}:
                p1_answer += 1

        p2_answer += get_number(inputs, outputs)


print('Part one answer is: {}'.format(p1_answer))
print('Part two answer is: {}'.format(p2_answer))