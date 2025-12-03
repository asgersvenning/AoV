from helpers import get_lines, get_path

START = 50

def parse_input(input : list[str]):
    return [(1 if l[0] == "R" else -1) * int(l[1:]) for l in input]

def cumsum(seq : list[int], init : int=0):
    r = init
    for v in seq:
        r += v
        r = r % 100
        yield r

# Part 1
input = parse_input(get_lines(get_path("input")))
result = len(list(filter(lambda x : x == 0, cumsum(input, START))))
print("PART 1:", result) # = 1123

# Part 2
def roll(start : int, by : int):
    return (tmp := start - (by + (-1 if by > 0 else 1) * (r := abs(by) // 100) * 100)) % 100, r + int(not start == 0 and (tmp <= 0 or tmp > 99))

def part2(seq : list[int], init : int=0):
    return sum([rtc[1] for v in [0] + seq if (rtc := roll(rtc[0], v))]) if (rtc := (init, 0)) else None

print("Part 2:", part2(input, START)) # = 6695
        