from helpers import get_lines, get_path

def parse_input(input : list[str]):
    return [(1 if l[0] == "R" else -1) * int(l[1:]) for l in input]

input = parse_input(get_lines(get_path("input")))
START = 50

# Part 1
def cumsum(seq : list[int], r : int=0):
    yield from ((r := (r + v) % 100) for v in seq)

def part1(turns : list[int]):
    return sum(1 for x in cumsum(turns, START) if x == 0)

print("PART 1:", part1(input)) # = 1123

# Part 2
def roll(start : int, by : int):
    return (tmp := start - (by + (-1 if by > 0 else 1) * (r := abs(by) // 100) * 100)) % 100, r + int(not start == 0 and (tmp <= 0 or tmp > 99))

def part2(seq : list[int], init : int=0):
    return sum(rtc[1] for v in [0] + seq if (rtc := roll(rtc[0], v))) if (rtc := (init, 0)) else None

print("Part 2:", part2(input, START)) # = 6695
        