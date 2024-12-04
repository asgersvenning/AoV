# Problem:
#   a small Elf who lives on the station tugs on your shirt; 
#   she'd like to know if you could help her with her word search (your puzzle input). 
#   She only has to find one word: XMAS.
#   This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. 
#   It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them.
#   How many times does XMAS appear?
# Restate:
#   Given a matrix of characters, find all sequences "XMAX" either forward, backward and diagonally.

import torch
import re
from itertools import cycle
from matplotlib import pyplot as plt

CMAP = {
    "X" : 10,
    "M" : 100,
    "A" : 1000,
    "S" : 10000,
    "." : -1
}

PATTERN = 10 ** torch.tensor([1, 2, 3, 4])
MATCH = (PATTERN ** 2).sum().item()

def parse_input(path):
    with open(path, "r") as f:
        input =  list(map(lambda x : re.sub("[^XMAS]", ".", x.strip()), f.readlines()))
    return torch.tensor([[CMAP[c] for c in line] for line in input]).float()

kern_flat = torch.zeros([1, 4]) + PATTERN
kern_diag = torch.eye(4) * PATTERN

def matches(map, kern):
    osmap = map.shape
    mdimmap = max(0, 4 - len(osmap))
    if mdimmap:
        map = map.view(*[1] * mdimmap, *osmap)
    oskern = kern.shape
    mdimkern = max(0, 4 - len(oskern))
    if mdimkern:
        kern = kern.view(*[1] * mdimkern, *oskern)
    return (torch.nn.functional.conv2d(map, kern) == MATCH).sum(dim = 1).view(*[md - (kd - 1) for md, kd in zip(osmap, cycle(kern.shape[2:]))])

def part1(t_map : torch.Tensor) -> int:
    kern_fb = torch.stack([kern_flat, kern_flat.flip(1)]).unsqueeze(1)
    kern_tb = kern_fb.transpose(3, 2)
    kern_cr = torch.stack([kern_diag, kern_diag.flip(1), kern_diag.flip(0), kern_diag.flip(1).flip(0)]).unsqueeze(1)
    # fig, axs = plt.subplots(2, 2)
    # for ax, m in zip(axs.flatten(), kern_cr.view(4, 4, 4)):
    #     ax.matshow(m.log())
    # plt.show()
    return sum(map(torch.sum, map(lambda k : matches(t_map, k), [kern_fb, kern_tb, kern_cr]))).item()
    # maps = [t_map, t_map.flip(1), t_map.T, t_map.T.flip(1)]
    # print()
    # for m in maps:
    #     print("\n".join(["".join([str(e.int().item()) for e in r]) for r in m]) + "\n")
    # return [[matches(m, k).sum().item() for m in maps] for k in [kern_flat, kern_diag]]

print("Test (part 1):", part1(parse_input("2024/inputs/04.test")))
print("Part 1:", part1(parse_input("2024/inputs/04.input")))