import re
from math import prod

from helpers import *

def parse_input(type : str):
    return "".join(get_lines(get_path(type)))

def part1(memory : str) -> int:
    return sum(prod(map(int, match.split(","))) for match in re.findall(r"(?<=mul\()\d+,\d+(?=\))", memory))

# print(part1(parse_input("test1")))
print(part1(parse_input("input")))

def part2(memory : str) -> int:
    return sum(prod(map(int, match.split(","))) for match in re.findall(r"(?<=mul\()\d+,\d+(?=\))", re.sub(r"don't\(\).*?(do\(\)|$)", "", memory)))

# print(part2(parse_input("test2")))
print(part2(parse_input("input")))