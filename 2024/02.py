from helpers import *

def parse_input(type : str):
    return [list(map(int, line.split(" "))) for line in get_lines(get_path(type))]

def part1(*lists : list[int]):
    return sum(map(lambda l : not (((d := l[1] - l[0]) == 0) or not all(abs((- (last - n) * d / abs(d) - 2)) <= 1 for last, n in zip(l, l[1:]))), lists))

# print(part1(*parse_input("test")))
print(part1(*parse_input("input")))

def part2(*lists : list[int]):
    def check1(l : list[int]):
        return not (((d := l[1] - l[0]) == 0) or not all(abs((- (last - n) * d / abs(d) - 2)) <= 1 for last, n in zip(l, l[1:])))

    def search(l : list[int]):
        if check1(l):
            return True
        for i in range(len(l)):
            nl = l.copy()
            nl.pop(i)
            if check1(nl):
                return True
        return False

    return sum(map(search, lists))

# print(part2(*parse_input("test")))
print(part2(*parse_input("input")))
