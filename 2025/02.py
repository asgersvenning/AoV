from helpers import get_path, get_lines
import re

def parse_input(lines : list[str]):
    if len(lines) != 1:
        RuntimeError("?")
    line = lines[0]
    parts = line.split(",")
    ranges = [tuple(map(int, part.split("-"))) for part in parts]
    return ranges

input = parse_input(get_lines(get_path("input")))

# Part 1
def part1(ranges : list[tuple[int, ...]]):
    i = 0
    for l, r in ranges:
        for v in range(l, r+1):
            vs = str(v)
            if len(vs) % 2 != 0:
                continue
            l = len(vs) // 2
            if vs[:l] == vs[l:]:
                i += v
    return i

print("Part 1:", part1(input)) # = 38310256125

# Part 2
def part2(ranges : list[tuple[int, ...]]):
    repeating_subsequence = re.compile(r"^([\d]+)\1+$")
    return sum(v for l, r in ranges for v in range(l, r+1) if re.match(repeating_subsequence, str(v)))

print("Part 2:", part2(input)) # = 58961152806