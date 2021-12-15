from collections import defaultdict

def parse_input(f):
    polymer = None
    rules = {}
    counter = 0
    for line in f:
        if counter == 0:
            polymer = list(line.strip())
        elif len(line.strip()) == 0:
            continue
        else:
            p1, _, p2 = line.strip().split()
            rules[p1] = p2
        counter += 1
    return polymer, rules


def process(polymer, rules):
    counter = defaultdict(int)
    result = []
    for i in range(len(polymer) - 1):
        a, b = polymer[i:i+2]
        if i == 0:
            result.append(a)
            counter[a] += 1
        counter[b] += 1
        pair = a + b
        if pair in rules:
            insertion = rules[pair]
            counter[insertion] += 1
            result.extend([insertion, b])
        else:
            result.extend([b])
    return result, counter

with open('input_test') as f:
    polymer, rules = parse_input(f)
    counter = None
    for i in range(10):
        polymer, counter = process(polymer, rules)

    quanties = sorted(counter.values())
    print("Answer is {}".format(quanties[-1] - quanties[0]))