import re

import torch
import torch.nn.functional as F

from helpers import get_lines, get_path

CMAP = {"X" : 2 ** (1/2), "M" : 3 ** (1/2), "A" : 5 ** (1/2), "S" : 7 ** (1/2), "." : 0}

def parse_input(type : str):
    return torch.tensor([[CMAP[c] for c in line] for line in map(lambda x : re.sub("[^XMAS]", ".", x), get_lines(get_path(type)))]).float()

matches = lambda map, kern : torch.isclose(torch.conv2d((map.view(*[1] * max(0, 4 - len(map.shape)), *map.shape) if max(0, 4 - len(map.shape)) else map), (kern := kern.view(*[1] * max(0, 4 - len(kern.shape)), *kern.shape) if max(0, 4 - len(kern.shape)) else kern), padding="same"), (kern ** 2).sum(2, keepdim=True).sum(3, keepdim=True).squeeze(1).unsqueeze(0))

def part1(t_map : torch.Tensor) -> int:
    return matches(F.pad(t_map, [5] * 4), torch.stack([(kern_flat := torch.zeros([5, 5]).index_put_((torch.zeros(4).long(), torch.arange(4)), (PATTERN := torch.tensor([CMAP[c] for c in "XMAS"])))), kern_flat.flip(1), kern_flat.T, kern_flat.flip(1).T, (kern_diag := torch.zeros([5, 5]).index_put_((torch.arange(4), torch.arange(4)), PATTERN)), kern_diag.flip(1), kern_diag.flip(0), kern_diag.flip(0).flip(1)]).unsqueeze(1)).squeeze(0).sum(1).sum(1).sum().item()

# print(part1(parse_input("test")))
print(part1(parse_input("input")))

def part2(t_map : torch.Tensor) -> int:
    HALF_PATTERN = torch.tensor([CMAP[c] for c in "MAS"])
    kerns = torch.zeros((4, 1, 3, 3))
    [kerns[i + j * 2, 0].index_put_((torch.arange(3), torch.arange(3)), HALF_PATTERN if j == 0 else HALF_PATTERN.flip(0)) + kerns[i + j * 2, 0].index_put_((-torch.arange(1, 4), torch.arange(3)), HALF_PATTERN if i == 0 else HALF_PATTERN.flip(0)) for j in range(2) for i in range(2)]
    return matches(F.pad(t_map, [3] * 4), kerns).squeeze(0).sum(1).sum(1).sum().item()

# print(part2(parse_input("test")))
print(part2(parse_input("input")))
