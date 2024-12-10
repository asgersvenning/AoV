from helpers import get_lines, get_path

def parse_input(type : str):
    return zip(*[[int(n) for n in line.split("   ")] for line in get_lines(get_path(type))])

part1 = lambda left, right : sum(abs(l - r) for l, r in zip(sorted(left), sorted(right)))

# print(part1(*parse_input("test")))
print(part1(*parse_input("input")))

part2 = lambda left, right : sum(n * freq.get(n, 0) for n in left) if ([freq.update({n : freq.get(n, 0) + 1}) for n in right] if not (freq := {}) else []) else 0

# print(part2(*parse_input("test")))
print(part2(*parse_input("input")))
