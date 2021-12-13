def parse_input(f):
    dots = set()
    instructions = []
    instruction_line = False
    for line in f:
        input = line.strip()
        if not input:
            instruction_line = True
            continue

        if instruction_line:
            p1, p2 = input.split('=')
            instructions.append((p1[-1], int(p2)
            ))
        else:
            x, y = input.split(',')
            dots.add((int(x), int(y)))

    return dots, instructions


def fold(dots, instruction):
    temp = set()
    offset = 0
    fold_type, fold_value = instruction
    for p in dots:
        x, y = p
        new_p = None
        if fold_type == 'x':
            dist = x - fold_value
            new_x = x - dist * 2
            offset = min(offset, new_x)
            new_p = (new_x, y) if dist > 0 else p
        else:
            dist = y - fold_value
            new_y = y - dist * 2
            offset = min(offset, new_y)
            new_p = (x, new_y) if dist > 0 else p
        temp.add(new_p)

    result = set()
    for p in temp:
        x, y = p
        if fold_type == 'x':
            result.add((x - offset, y))
        else:
            result.add((x, y - offset))
    return result

with open('input') as f:
    dots, instructions = parse_input(f)
    result = dots
    for i in range(len(instructions)):
        result = fold(result, instructions[i])
        if i == 0:
            print('Part one answer is {}'.format(len(result)))

    size_x = size_y = 0
    for p in result:
        x, y = p
        size_x = max(size_x, x)
        size_y = max(size_y, y)

    print("Part two answer is:")
    for row in range(size_y + 1):
        line = ''
        for column in range(size_x + 1):
            if (column, row) in result:
                line += '#'
            else:
                line += '.'
        print(line)
