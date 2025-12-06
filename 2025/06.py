import operator as ops
import re
from functools import reduce
from typing import Callable

from helpers import get_lines, get_path

OPERATORS = {
    "+" : ops.add,
    "-" : ops.sub,
    "*" : ops.mul,
    "/" : ops.truediv    
}

def parse_input(input : list[str]):
    numbers = []
    operators : list[Callable[[int, int], int]] = []
    for line in input:
        line = re.sub(r'\s+', " ", line, 0).strip()
        parts = line.split(" ")
        if parts[0].isdigit():
            numbers.append(list(map(int, parts)))
        else:
            operators = [OPERATORS[part] for part in parts]
    return numbers, operators
    

input = parse_input(get_lines(get_path("input")))

# Part 1
def part1(numbers : list[list[int]], operators : list[Callable[[int, int], int]]):
    return sum(reduce(op, col) for col, op in zip(zip(*numbers), operators))

print("Part 1:", part1(*input)) # = 5524274308182

# Part 2
def split(c : str, w : int):
    o = []
    s, e = 0, w
    while e < len(c):
        o.append(c[s:e])
        s, e = e + 1, min(e + 1 + w, len(c))
    return o

def cumsum(seq : list[int], t=0):
    return [(t := t + v) for v in seq]

def part2(input : str):
    with open(input, "r") as f:
        lines = [line for rawline in f.readlines() if (line := rawline.replace( '\n', ''))]
    colwidth = list(map(len, re.findall(r'\S\s+', lines[-1])))
    cumwidth = cumsum(colwidth)
    start, end = [0] + [cs for cs in cumwidth[:-1]], [cs - 1 for cs in cumwidth]
    end[-1] += 1
    numbers = []
    for line in lines:
        parts = [line[s:e] for s, e in zip(start, end)]
        (numbers.append(parts) if parts[0].strip().isdigit() else (operators := [OPERATORS[part.strip()] for part in parts]))
    return sum(reduce(op, col) for col, op in zip((map(lambda x : int("".join(x).strip()), zip(*col)) for col in zip(*numbers)), operators))

print("Part 2:", part2(get_path("input"))) # = 8843673199391