# Problem:
#   Pair up the smallest number in the left list with the smallest number in the right list, 
#   then the second-smallest left number with the second-smallest right number, and so on.
#   Within each pair, figure out how far apart the two numbers are; 
#   you'll need to add up all of those distances.
# Input:
# Text file with two columns of numbers.
# Each column has the same number of numbers, and is separated by three spaces.
# Restate:
#   Given two lists of numbers, compute the element-wise absolute difference between the two sorted lists.

import os

def parse_input(path):
    with open(path, "r") as f:
        return zip(*[[int(n) for n in line.strip().split("   ")] for line in f.readlines()])

def part1(left, right):
    return sum([abs(l - r) for l, r in zip(sorted(left), sorted(right))])

# Test input
print(f"Test (part 1): {part1(*parse_input("2024/inputs/01.test"))}")

# Part 1
print(f"Part 1: {part1(*parse_input("2024/inputs/01.input"))}")

# Part 2
# Problem:
#   Calculate a total similarity score by adding up each number in the left list after multiplying it by the number of times that number appears in the right list.
# Restate:
#   Calculate the weighted sum of the first list, by the frequency of each number in the second list.

def part2(left, right):
    return sum([n * freq.get(n, 0) for n in left]) if ([freq.update({n : freq.get(n, 0) + 1}) for n in right] if not (freq := {}) else []) else 0

# Test input
print(f"Test (part 2): {part2(*parse_input("2024/inputs/01.test"))}")

# Part 2
print(f"Part 2: {part2(*parse_input("2024/inputs/01.input"))}")
