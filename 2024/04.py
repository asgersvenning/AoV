# Problem:
#   a small Elf who lives on the station tugs on your shirt; 
#   she'd like to know if you could help her with her word search (your puzzle input). 
#   She only has to find one word: XMAS.
#   This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. 
#   It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them.
#   How many times does XMAS appear?
# Restate:
#   Given a matrix of characters, find all sequences "XMAX" either forward, backward and diagonally.

import re

import torch

CMAP = {"X" : 2 ** (1/2), "M" : 3 ** (1/2), "A" : 5 ** (1/2), "S" : 7 ** (1/2), "." : 0}

def parse_input(path):
    with open(path, "r") as f:
        return torch.tensor([[CMAP[c] for c in line] for line in map(lambda x : re.sub("[^XMAS]", ".", x.strip()), f.readlines())]).float()

def matches(map : torch.Tensor, kern : torch.Tensor):
    map = map.view(*[1] * max(0, 4 - len(map.shape)), *map.shape)if max(0, 4 - len(map.shape)) else map
    kern = kern.view(*[1] * max(0, 4 - len(kern.shape)), *kern.shape) if max(0, 4 - len(kern.shape)) else kern       
    return torch.isclose(torch.nn.functional.conv2d(map, kern, padding="same"), (kern ** 2).sum(2, keepdim=True).sum(3, keepdim=True).squeeze(1).unsqueeze(0))

def part1(t_map : torch.Tensor) -> int:
    PATTERN = torch.tensor([CMAP[c] for c in "XMAS"])
    kern_flat = torch.zeros([5, 5]).index_put_((torch.zeros(4).long(), torch.arange(4)), PATTERN)
    kern_diag = torch.zeros([5, 5]).index_put_((torch.arange(4), torch.arange(4)), PATTERN)
    return matches(torch.nn.functional.pad(t_map, [5] * 4), torch.stack([kern_flat, kern_flat.flip(1), kern_flat.T, kern_flat.flip(1).T, kern_diag, kern_diag.flip(1), kern_diag.flip(0), kern_diag.flip(0).flip(1)]).unsqueeze(1)).squeeze(0).sum(1).sum(1).sum().item()

print("Test (part 1):", part1(parse_input("2024/inputs/04.test")))
print("Part 1:", part1(parse_input("2024/inputs/04.input")))

# Problem:
#   you're supposed to find two MAS in the shape of an X. 
#   One way to achieve that is like this:
#       M.S
#       .A.
#       M.S
#   Irrelevant characters have again been replaced with . in the above diagram. 
#   Within the X, each MAS can be written forwards or backwards.
#   How many times does an X-MAS appear?
# Restate:
#   Same as before, but different pattern.

def part2(t_map : torch.Tensor) -> int:
    HALF_PATTERN = torch.tensor([CMAP[c] for c in "MAS"])
    kerns = torch.zeros((4, 1, 3, 3))
    [kerns[i + j * 2, 0].index_put_((torch.arange(3), torch.arange(3)), HALF_PATTERN if j == 0 else HALF_PATTERN.flip(0)) + kerns[i + j * 2, 0].index_put_((-torch.arange(1, 4), torch.arange(3)), HALF_PATTERN if i == 0 else HALF_PATTERN.flip(0)) for j in range(2) for i in range(2)]
    return matches(torch.nn.functional.pad(t_map, [3] * 4), kerns).squeeze(0).sum(1).sum(1).sum().item()

print("Test (part 2):", part2(parse_input("2024/inputs/04.test")))
print("Part 2:", part2(parse_input("2024/inputs/04.input")))