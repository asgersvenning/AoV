import torch
import numpy as np

def parse_input(path):
    with open(path, "r") as f:
        data = [[c for c in line.strip()] for line in f.readlines()]
    h, w = len(data), len(data[0])
    if h != w:
        raise NotImplementedError("Input must be square not", h, w)
    antennas = {}
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == ".":
                continue
            if not c in antennas:
                antennas[c] = []
            antennas[c].append([i,j])

    return data, {k : torch.tensor(v, dtype=torch.double) for k, v in antennas.items()}

def find_antinodes(coords : torch.Tensor):
    return (coords.unsqueeze(1) - (coords.unsqueeze(0) - coords.unsqueeze(1))).reshape(-1, 2)[(coords.unsqueeze(0) - coords.unsqueeze(1)).abs().sum(-1).flatten() != 0]

def part1(path):
    data, antennas = parse_input(path)
    all_antinodes = torch.cat([v for _, v in {frequency : find_antinodes(antennas[frequency]) for frequency in antennas}.items()])
    all_antinodes = all_antinodes[((all_antinodes >= 0) & (all_antinodes < len(data))).all(1)]
    return (all_antinodes * torch.tensor([1, len(data)]).unsqueeze(0)).sum(1).unique().shape[0]

print(part1("2024/inputs/08.test"))
print(part1("2024/inputs/08.input"))

def make_lines(coords : torch.Tensor):
    i, j = torch.tril_indices(len(coords), len(coords), offset=-1)
    deltas = (coords.unsqueeze(0) - coords.unsqueeze(1))[i, j, :]
    slope = deltas[:, 0] / deltas[:, 1]
    intercept = coords[i, 0] - (slope * coords[i, 1])
    return torch.stack([slope, intercept], dim=1)

def get_integer_solutions(slope : torch.Tensor, intercept : torch.Tensor, ran : tuple) -> torch.Tensor:
    xs = torch.arange(ran[0], ran[1] + 1).unsqueeze(-1).repeat(1, len(slope))
    int_coords = torch.zeros((len(xs), len(slope), 2))
    int_coords[:, :, 1] = xs
    int_coords[:, :, 0] = intercept + slope * xs
    int_coords = int_coords.reshape(-1, 2)
    
    return int_coords

def clean_solutions(int_coords : torch.Tensor, ran : tuple[int, int], eps : float=1e-3) -> torch.Tensor:
    int_coords = int_coords[((int_coords >= (ran[0] - eps)) & (int_coords < (ran[1] + eps)) & ((int_coords % 1).abs() < eps)).all(1)].long()
    return int_coords[np.unique(((int_coords[:, 1]) + (int_coords[:, 0] * int_coords.max() * 10)).numpy(), True)[1]]

def part2(path):
    data, antennas = parse_input(path)
    return len(clean_solutions(get_integer_solutions(*torch.cat([make_lines(antennas[frequency]) for frequency in antennas]).T, (0, len(data) - 1)), (0, len(data) - 1), 1/(2 * len(data))))

print(part2("2024/inputs/08.test"))
print(part2("2024/inputs/08.input"))