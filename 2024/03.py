import re
from math import prod


def parse_input(path):
    with open(path, "r") as f:
        return "".join(map(str.strip, f.readlines()))
    
def part1(memory : str) -> int:
    return sum([prod(map(int, match.split(","))) for match in re.findall(r"(?<=mul\()\d+,\d+(?=\))", memory)])

# print(part1(parse_input("2024/inputs/03.test1")))
print(part1(parse_input("2024/inputs/03.input")))

def part2(memory : str) -> int:
    return sum([prod(map(int, match.split(","))) for match in re.findall(r"(?<=mul\()\d+,\d+(?=\))", re.sub(r"don't\(\).*?(do\(\)|$)", "", memory))])

# print(part2(parse_input("2024/inputs/03.test2")))
print(part2(parse_input("2024/inputs/03.input")))