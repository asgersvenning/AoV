import re

input_path = "input_04.txt"

with open(input_path, "r") as f:
    lines = f.readlines()
    
    lines = [[int(i) for i in re.split(",|-", l.strip())] for l in lines]

# Part 1
def contained_in(s1, e1, s2, e2):
    # s1 s2 e2 e1 
    return (s1 <= s2 and e2 <= e1) or (s2 <= s1 and e1 <= e2)

Answer_1 = sum([contained_in(*l) for l in lines])

print("Part 1:", Answer_1)

# Part 2
def overlaps(s1, e1, s2, e2):
    # s1----e1 s2----e2
    # s2----e2 s1----e1
    
    return not (e1 < s2 or e2 < s1)

Answer_2 = sum([overlaps(*l) for l in lines])

print("Part 2:", Answer_2)