from helpers import get_path, get_lines

def parse_input(lines : list[str]):
    return [tuple(map(int, part.split("-"))) for part in lines[0].split(",")]

input = parse_input(get_lines(get_path("input")))

# Part 1
def part1(ranges : list[tuple[int, ...]]):
    return sum(v for l, r in ranges for v in range(l, r+1) if len(vs := str(v)) % 2 == 0 and vs[:(vl := len(vs) // 2)] == vs[vl:])

print("Part 1:", part1(input)) # = 38310256125

# Part 2
import re

def part2(ranges : list[tuple[int, ...]]):
    repeating_subsequence = re.compile(r"^([\d]+)\1+$")
    return sum(v for l, r in ranges for v in range(l, r+1) if re.match(repeating_subsequence, str(v)))

print("Part 2:", part2(input)) # = 58961152806