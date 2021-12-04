count = []
num_lines = 0
source = []
with open('input') as f:
    for line in f:
        bits = [int(x) for x in line.strip()]
        source.append(bits)
        if num_lines == 0:
            count = bits
        else:
            count = [sum(x) for x in zip(count, bits)]
        num_lines += 1

half = int(num_lines / 2)
most_common = [int(x >= half) for x in count]
least_common = [int(not x) for x in most_common]

most_common = '0b' + ''.join(map(str, most_common))
least_common = '0b' + ''.join(map(str, least_common))

print(eval(most_common) * eval(least_common))

def filter(inputs, index, mode):
    if len(inputs) == 1:
        return inputs[0]
    elif len(inputs) > 1:
        list_zero = []
        list_one =[]
        for x in inputs:
            list_zero.append(x) if x[index] == 0 else list_one.append(x)
        if mode == 'most_common':
            return filter(list_one if len(list_one) >= len(list_zero) else list_zero, index + 1, mode)
        else:
            return filter(list_zero if len(list_zero) <= len(list_one) else list_one, index + 1, mode)
    else:
        raise Exception('Invalid inputs.')

oxygen_generator_rating = '0b' + ''.join(map(str, filter(source, 0, 'most_common')))
co2_scrubber_rating = '0b' + ''.join(map(str, filter(source, 0, 'least_common')))

print(eval(oxygen_generator_rating) * eval(co2_scrubber_rating))