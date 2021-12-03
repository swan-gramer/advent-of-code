def cal_inceases(input):
    count = 0
    successor = None;
    for value in input:
        if successor:
            count = count + 1 if value > successor else count
        successor = value

    print(count)


def make_slide_three(file):
    result = []
    window = []
    for line in file:
        value = int(line)
        window.append(value)
        if len(window) == 3:
            result.append(sum(window))
            window.pop(0)
    return result

with open('input.txt') as f:
    cal_inceases(make_slide_three(f))