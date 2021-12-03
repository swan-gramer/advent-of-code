position = 0
depth = 0
aim = 0

with open('input.txt') as f:
    for line in f:
        instruct, value = line.split(' ')
        value = int(value)
        if instruct == 'forward':
            position += value
            depth += aim * value
        elif instruct == 'down':
            aim += value
        elif instruct == 'up':
            aim -= value

print(position * depth)