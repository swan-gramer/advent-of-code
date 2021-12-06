# class Fish:
#     def __init__(self, timer=8):
#         self.timer = timer
#         self.make_new = False


#     def update(self):
#         if self.timer == 0:
#             self.timer = 6
#             self.make_new = True
#         else:
#             self.timer -= 1
#             self.make_new = False


# with open('input_test') as f:
#     line = map(int, f.readline().strip().split(','))
#     fishes = [Fish(timer) for timer in line]
#     new_fishes = []
#     for day in range(0, 256):
#         for fish in fishes:
#             fish.update()
#             if fish.make_new:
#                 new_fishes.append(Fish())
#         fishes = fishes + new_fishes
#         new_fishes = []

#     print("Part one answer: {}".format(len(fishes)))

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
