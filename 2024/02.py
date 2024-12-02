# Problem:
#   The unusual data (your puzzle input) consists of many reports, one report per line. 
#   Each report is a list of numbers called levels that are separated by spaces.
#   The engineers are trying to figure out which reports are safe. 
#   The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. 
#   So, a report only counts as safe if both of the following are true:
#     - The levels are either all increasing or all decreasing.
#     - Any two adjacent levels differ by at least one and at most three.
#   Analyze the unusual data from the engineers. How many reports are safe?
# Restate:
#   Calculate how many lists are composed of a monotonic series with step-sizes strictly between 1-3.

def parse_input(path):
    with open(path, "r") as f:
        return [[int(n) for n in line.strip().split(" ")] for line in f.readlines()]

def part1(*lists):
    return sum(map(lambda l : not (((d := l[1] - l[0]) == 0) or not all([abs((- (last - n) * d / abs(d) - 2)) <= 1 for last, n in zip(l, l[1:])])), lists))

# Test
print("Test (part 1):", part1(*parse_input("2024/inputs/02.test")))

# Part 1
print("Part 1:", part1(*parse_input("2024/inputs/02.input")))

# Part 2
# Problem:
#   Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.
# Restate:
#   Calculate how many lists are composed of a monotonic series with step-sizes strictly between 1-3 if up to one element is removed.

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


# Test
print("Test (part 2):", part2(*parse_input("2024/inputs/02.test")))

# Part 1
print("Part 1:", part2(*parse_input("2024/inputs/02.input")))