from helpers import get_lines, get_path

from functools import lru_cache

# from tqdm.contrib.concurrent import thread_map
from tqdm import tqdm

from collections import defaultdict

def parse_input(type : str):
    return list(map(int, get_lines(get_path(type))))

def mix(a : int, b : int):
    return a ^ b

def prune(n : int, m : int=16777216):
    return n % m

@lru_cache(None)
def evolve(n : int):
    n = prune(mix(n, n * 64))   # +  6: >>>>>>
    n = prune(mix(n, n // 32))  # -  5: <<<<<
    n = prune(mix(n, n * 2048)) # + 11: >>>>>>>>>>>
    return n

@lru_cache(None)
def evolve_many(v : int, n : int):
    for _ in range(n):
        v = evolve(v)
    return v

def expand_evolve(v : int, n : int):
    seq = [v]
    for _ in range(n - 1):
        v = evolve(v)
        seq.append(v)
    if len(seq) != n:
        raise RuntimeError()
    return seq


def part1(type : str):
    return sum(map(lambda x : evolve_many(x, 2000), parse_input(type)))

# print(part1("input"))

def part2(type : str):
    sequences = {n : expand_evolve(n, 2000) for n in parse_input(type)}
    prices = {n : [int(str(v)[-1]) for v in s] for n, s in sequences.items()}
    deltas = {n : [l - v for v, l in zip(s, s[1:])] for n, s in prices.items()}
    
    bananas = defaultdict(lambda : 0)
    
    for init, sequence in tqdm(deltas.items()):
        seen = set()
        for i, window in [(i, tuple(sequence[i:(i+4)])) for i in range(len(sequence) - 4)]:
            if window in seen:
                continue
            bananas[window] += prices[init][i+4]
            seen.add(window)
    
    mb = max(bananas.values())
    wb = [k for k, v in enumerate(bananas.items()) if v == mb][0]
    return mb, wb
    
    

print(part2("input"))
    