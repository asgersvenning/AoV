import re
import string

from functools import reduce

alphabet = string.ascii_letters

input_path = "input_03.txt"

priority = {c : i + 1 for i, c in enumerate(alphabet)}

def split_rucksack(s):
    half_n = len(s) // 2
    return [set(i) for i in re.findall(".{" + str(half_n) + ",}", s)]

with open(input_path, "r") as f:
    lines = f.read().strip().split("\n")
    
rucksacks = [split_rucksack(l) for l in lines] 

# Part 1 
    
def find_common_element(s1, s2):
    # Assumes only one common element in s1 and s2
    common = (s1 & s2).__iter__().__next__()
    return common

Answer_1 = sum([priority[find_common_element(*r)] for r in rucksacks])

print("Part 1:", Answer_1)

# Part 2

rucksacks = [set(l) for l in lines]

#Answer_2 = sum([priority[reduce(set.intersection, rucksacks[i:(i + 3)]).__iter__().__next__()] for i in range(0, len(rucksacks), 3)])

overlaps = [reduce(set.intersection, rucksacks[i:(i + 3)]) for i in range(0, len(rucksacks), 3)]
total = sum([priority[s] for o in overlaps for s in o])

print("Part 2:", total)

