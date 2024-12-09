def parse_input(path):
    with open(path, "r") as f:
        return zip(*[[int(n) for n in line.strip().split("   ")] for line in f.readlines()])

part1 = lambda left, right : sum([abs(l - r) for l, r in zip(sorted(left), sorted(right))])

# print(part1(*parse_input("2024/inputs/01.test")))
print(part1(*parse_input("2024/inputs/01.input")))

part2 = lambda left, right : sum([n * freq.get(n, 0) for n in left]) if ([freq.update({n : freq.get(n, 0) + 1}) for n in right] if not (freq := {}) else []) else 0

# print(part2(*parse_input("2024/inputs/01.test")))
print(part2(*parse_input("2024/inputs/01.input")))
