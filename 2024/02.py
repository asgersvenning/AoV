def parse_input(path):
    with open(path, "r") as f:
        return [[int(n) for n in line.strip().split(" ")] for line in f.readlines()]

def part1(*lists):
    return sum(map(lambda l : not (((d := l[1] - l[0]) == 0) or not all([abs((- (last - n) * d / abs(d) - 2)) <= 1 for last, n in zip(l, l[1:])])), lists))

# print(part1(*parse_input("2024/inputs/02.test")))
print(part1(*parse_input("2024/inputs/02.input")))

def part2(*lists):
    def check1(l):
        return not (((d := l[1] - l[0]) == 0) or not all([abs((- (last - n) * d / abs(d) - 2)) <= 1 for last, n in zip(l, l[1:])]))
            
    def search(l : list):
        if check1(l):
            return True
        for i in range(len(l)):
            nl = l.copy()
            nl.pop(i)
            if check1(nl):
                return True
        return False
    
    return sum(map(search, lists))

# print(part2(*parse_input("2024/inputs/02.test")))
print(part2(*parse_input("2024/inputs/02.input")))