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


rules = template = None
with open('input') as f:
    template, rules = parse_input(f)


def process(polymer):
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
    return ''.join(result), counter

def process_rule(step):
    result = {}
    for key, _ in rules.items():
        result_rule = list(key)
        counter = 0
        for i in range(step):
            result_rule, counter = process(result_rule)
        result[key] = (result_rule, counter)
    return result

rules_map_20 = process_rule(20)

def get_count_40(map_20, pair):
    polymer_20, _ = map_20[pair]
    result = defaultdict(int)
    for i in range(len(polymer_20) - 1):
        temp = polymer_20[i:i+2]
        _, count = map_20[temp]
        for key, value in count.items():
            result[key] += value

    for i in range(1, len(polymer_20) - 1):
        result[polymer_20[i]] -= 1

    return result


def map_20_to_40():
    result = {}
    for key, _ in rules_map_20.items():
        result[key] = get_count_40(rules_map_20, key)
    return result


map_40 = map_20_to_40()

counter = defaultdict(int)
template_str = ''.join(template)
for i in range(len(template_str) - 1):
    pair = template_str[i:i+2]
    count = map_40[pair]
    for key, value in count.items():
        counter[key] += value

for i in range(1, len(template_str) - 1):
    counter[template_str[i]] -= 1

sorted_val = sorted(counter.values())
print("Answer is {}".format(sorted_val[-1] - sorted_val[0]))
