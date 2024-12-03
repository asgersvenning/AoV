# Problem:
#   The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. 
#   All of the instructions have been jumbled up!
#   It seems like the goal of the program is just to multiply some numbers. 
#   It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers.
#   For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. 
#   Similarly, mul(123,4) would multiply 123 by 4.
#   However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. 
#   Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.
#   What do you get if you add up all of the results of the multiplications?
# Restate:
#   Given a string of characters, find all subsequences matching the pattern "mul(X,Y)" and calculate the sum of all products X*Y.

import re
from math import prod

def parse_input(path):
    with open(path, "r") as f:
        return "".join(map(str.strip, f.readlines()))
    
def part1(memory : str) -> int:
    return sum([prod(map(int, match.split(","))) for match in re.findall(r"(?<=mul\()\d+,\d+(?=\))", memory)])

print("Test (part 1):", part1(parse_input("2024/inputs/03.test1")))
print("Part 1:", part1(parse_input("2024/inputs/03.input")))

# Problem:
#   As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. 
#   If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.
#   There are two new instructions you'll need to handle:
#       - The do() instruction enables future mul instructions.
#       - The don't() instruction disables future mul instructions.
#   Only the most recent do() or don't() instruction applies. 
#   At the beginning of the program, mul instructions are enabled.
#   what do you get if you add up all of the results of just the enabled multiplications?
# Restate:
#   Given a string, find all subsequences matching the pattern "mul(X, Y)" that are not preceded by "don't()" later than "do()"

def part2(memory : str) -> int:
    return sum([prod(map(int, match.split(","))) for match in re.findall(r"(?<=mul\()\d+,\d+(?=\))", re.sub(r"don't\(\).*?(do\(\)|$)", "", memory))])

print("Test (part 2):", part2(parse_input("2024/inputs/03.test2")))
print("Part 2:", part2(parse_input("2024/inputs/03.input")))