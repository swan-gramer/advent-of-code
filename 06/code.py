from collections import defaultdict
with open('input') as f:
    line = map(int, f.readline().strip().split(','))
    fishes = defaultdict(int)
    for timer in line:
        fishes[timer] += 1

    answer_one = answer_two = 0
    for day in range(0, 256):
        fishes_new = defaultdict(int)
        for timer, count in fishes.items():
            if timer == 0:
                fishes_new[6] += count
                fishes_new[8] = count
            else:
                fishes_new[timer-1] += count
        fishes = fishes_new
        if day == 79:
            answer_one = sum(fishes.values())

    answer_two = sum(fishes.values())
    print("Part one answer: {}".format(answer_one))
    print("Part two answer: {}".format(answer_two))
