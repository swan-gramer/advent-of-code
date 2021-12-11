from queue import Queue

def step_forward(input):
    dqueue = Queue()
    processed = set()
    adjacent_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    flashes = 0
    for key in input:
        input[key] += 1
        if input[key] >= 9:
            dqueue.put(key)
    while dqueue:
        key = dqueue.get()
        if key in processed:
            continue
        if key not in input:
            continue
        processed.add(key)
        flashes += 1
        input[key] = 0
        row, column = key
        for adjacent in [(row+i, column+j) for i, j in adjacent_offsets]:
            if adjacent in input:
                input[adjacent] += 1
                if input[adjacent] >= 9:
                    dqueue.put(adjacent)
    
    return flashes


input = dict()
with open('input_test') as f:
    row = 0
    for line in f:
        column = 0
        for c in list(line.strip()):
            input[(row, column)] = int(c)
            column += 1
        row += 1

total_flashes = 0
for i in range(100):
    flashes = step_forward(input) 
    total_flashes += flashes

print("Answer is {}".format(total_flashes))