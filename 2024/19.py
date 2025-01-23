from helpers import get_path, get_lines, Animation, pprint, SQUARE

from typing import Iterable, Mapping, Any

import numpy as np
from tqdm import tqdm

colors = {
    "w" : "white",
    "u" : "blue",
    "b" : "black",
    "r" : "red",
    "g" : "green"
}

nums = [2, 3, 5, 7, 11]
color_to_num = {c : nums[i] ** (1/2) for i, c in enumerate(colors.keys())}
num_to_color = {i : colors[c] for c, i in color_to_num.items()}
num_to_char = {i : c for c, i in color_to_num.items()}

def to_arr(s : str):
    return np.array([color_to_num[c] for c in s])

def render_arr(arr : np.ndarray, symbol : bool=True):
    return "".join(f'[{num_to_color[n]} bold]{SQUARE if symbol else num_to_char[n]}[reset]' for n in arr)

def parse_input(type : str):
    lines = get_lines(get_path(type))
    
    towels = sorted(map(to_arr, lines[0].split(", ")), key = lambda x : len(x), reverse=False)
    # towels = list(map(to_arr, lines[0].split(", ")))
    designs = list(map(to_arr, lines[2:]))
    
    return towels, designs

def tcat(*args : int | Iterable[int]):
    def _inner(element: int | Iterable[int]) -> list[int]:
        if isinstance(element, list):
            return element
        elif isinstance(element, int):
            return [element]
        else:
            return list(element)
    return tuple(sum((_inner(e) for e in args), start=[]))

class SumTreeCache(dict):
    def __init__(self, *args, base_class : type=tuple, **kwargs):
        super().__init__(*args, **kwargs)
        assert all(isinstance(value, set) for value in self.values())
        self.is_value = {k : True for k in self}
        self._do_expand = False
        self.base_class = base_class
    
    def sparse(self):
        self._do_expand = False
        return self
        
    def dense(self):
        self._do_expand = True
        return self
    
    def __setitem__(self, key, item):
        item = tuple(e for e in item if not (isinstance(e, (tuple, list, set, dict)) and not e))
        if not key in self:
            self.is_value[key] = False
        super().__setitem__(key, item)
        
    def subtreesize(self, key):
        try:
            if key in self:
                return list(map(lambda x : 1 if isinstance(x, int) else self.subtreesize(x), self[key]))
            out = sum(map(self.subtreesize, key), start=[])
            print(key, "==>", out)
            return out
        except Exception as e:
            print("KEY", key)
            print(self)
            raise e
        
    def __getitem__(self, key):
        if key in self:
            values = self.base_class(super().get(key, []))
        else:
            values = sum((self[v] for v in self[key]), start=self.base_class())
        if not self._do_expand:
            return values
        return sum((self[v] for v in self[values]), start=self.base_class())
    
    def get_one(self, key):
        values = self.base_class(super().get(key, []))
        if len(values) == 0:
            return values
        if len(values) == 1:
            value = values[0]
            if isinstance(value, int):
                return value
            return self.get_one(value)
        for reference in values:
            try:
                return sum(map(self.get_one, reference), start=self.base_class())
            except StopIteration:
                continue
        return self.base_class()

def cache_size(cache : Mapping[tuple[int, ...], Any]):
    def _recursive_size(elem):
        if not hasattr(elem, "__iter__"):
            return 1
        return sum(map(_recursive_size, elem), start=0)
    return _recursive_size(cache.values())

def combination(design : np.ndarray, towels : list[np.ndarray], first_only : bool=True, skippers : set[int] | None = None, cache : Mapping[tuple[int, ...], set[tuple[int, ...] | tuple[tuple[int, ...], ...]]] | None=None):
    if len(design) == 0:
        empty : set[tuple[int, ...]] = set()
        return empty
    if cache is None:
        cache : Mapping[tuple[int, ...], set[tuple[int, ...] | tuple[tuple[int, ...], ...]]] = {}
    tupdes : tuple[int, ...] = tuple((design ** 2).round().tolist())
    if tupdes in cache:
        # print(cache)
        # print(tupdes)
        return cache[tupdes]
    if skippers is None:
        skippers : set[int] = set()
    combinations : set[tuple[int, ...] | tuple[tuple[int, ...], ...]] = set()
    early_exit = False
    for ti, towel in zip(range(len(towels)-1,-1,-1), reversed(towels)):
        if early_exit:
            break
        if ti in skippers:
            continue
        if len(towel) > len(design):
            skippers.add(ti)
            continue
        if len(towel) == len(design) and (towel == design).all():
            combinations.add((ti,))
            if early_exit:
                break
            continue
        
        if len(towel) == 1:
            matches = np.where(design == towel)[0]
        else:
            mval = (towel ** 2).sum()
            matches = np.where(np.convolve(design, np.flip(towel), "valid") == mval)[0]
        if len(matches) == 0:
            skippers.add(ti)
            continue
        any_solution = False
        for mi in reversed(matches):
            right = design[(mi + len(towel)):]
            right_solutions = combination(right, towels, first_only, skippers.copy(), cache)
            if len(right) > 0 and len(right_solutions) == 0:
                continue
            left = design[:mi]
            left_solutions = combination(left, towels, first_only, skippers.copy(), cache)
            if len(left) > 0 and len(left_solutions) == 0:
                continue
            any_solution = True
            center = tuple((towel ** 2).round().tolist())
            this = (tuple((left ** 2).round().tolist()), center, tuple((right ** 2).round().tolist()))
            combinations.add(this)
            if first_only:
                early_exit = True
                cache[center] = (ti,)
                break
        if not any_solution:
            skippers.add(ti)
    cache[tupdes] = combinations
    return combinations

def finalize(comb : Iterable[int] | Iterable[Iterable[int]], towels : list[np.ndarray], all : bool=False) -> np.ndarray | list[np.ndarray]:
    def _one(c : Iterable[int]):
        if not c:
            return np.empty((0,))
        return np.concatenate([towels[i] for i in c if i is not None])
    if any(hasattr(c, "__iter__") for c in comb):
        if all:
            return list(map(_one, comb))
        comb = next(iter(comb))
        if isinstance(comb, int):
            raise RuntimeError()
    return _one(comb)
    
def part1(type : str, verbose : bool=False, timing : bool=False):
    towels, designs = parse_input(type)
    if verbose:
        pprint(f"Towels: ( {' | '.join(map(render_arr, towels))} )")
    shared_cache = SumTreeCache() # {tuple((towel ** 2).round().tolist()) : {(i,)} for i, towel in enumerate(towels)}
    [combination(design, towels, cache=shared_cache) for design in (tqdm(designs, desc="Solving designs...") if timing else designs)]
    if verbose:
        total = 0
        max_len = max(map(len, designs))
        shared_cache.dense()
        for design in designs:
            # solution = shared_cache.get_one(tuple((design ** 2).round().tolist()))
            tupdes = (tuple((design ** 2).round().tolist()))
            print(tupdes)
            # solution = shared_cache[tupdes]
            solution = shared_cache.get_one(tupdes)
            print("SOLUTION", solution)
            solution = finalize(solution, towels)
            if len(solution) > 0:
                total += 1
            pprint(f'{" " * (max_len - len(design))}{render_arr(design)}|{render_arr(solution[::-1]) or "-" * len(design)}')
        print(shared_cache)
        # for design, solutions in shared_cache.items():
        #     pprint(f'{render_arr(tuple(d ** (1/2) for d in design))}: ( {" | ".join("-".join(render_arr(finalize([e], towels, False)) for e in s if e != -1) for s in solutions)} )')
        return total
    return sum(map(lambda x : 1 if len(x) > 0 else 0, solutions))



def part2(type : str, verbose : bool=False, timing : bool=False):
    towels, designs = parse_input(type)
    if verbose:
        pprint(f"Towels: ( {' | '.join(map(render_arr, towels))} )")
    shared_cache = SumTreeCache()
    all_solutions = [combination(design, towels, first_only=False, cache=shared_cache) for design in (tqdm(designs, desc="Solving designs...") if timing else designs)]
    if verbose:
        total = 0
        max_len = max(map(len, designs))
        for design, solutions in zip(designs, all_solutions):
            tupdes = tuple((design ** 2).round().tolist())
            n = shared_cache.subtreesize(tupdes)
            pprint(f'{" " * (max_len - len(design))}{render_arr(design)}[{"X"}] ==> ', *map(len, n))
            total += n
        # for design, solutions in shared_cache.items():
        #     pprint(f'{render_arr(tuple(d ** (1/2) for d in design))}: ( {" | ".join("-".join(render_arr(finalize([e], towels, False)) for e in s if e != -1) for s in solutions)} )')
        return total
    return sum(map(lambda x : shared_cache.subtreesize(tuple((x ** 2).round().tolist())), designs))


if __name__ == "__main__":

    print(part1("test", True))
    # print(part1("input", timing=True))
    
    # print(part2_v1("test", False, True))
    # print(part2("test", True, False))
    # print(part2("input", False, True))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def combination_implicit(design : np.ndarray, towels : list[np.ndarray], first_only : bool=True, skippers : set[int] | None = None, cache : dict[tuple[int, ...], int] | None=None):
#     if len(design) == 0:
#         return 0
#     if cache is None:
#         cache = {}
#     tupdes = tuple((design ** 2).round().tolist())
#     if tupdes in cache:
#         return 0 # cache[tupdes]
#     if skippers is None:
#         skippers : set[int] = set()
#     combinations : int = 0
#     for ti, towel in zip(range(len(towels)-1,-1,-1), reversed(towels)):
#         if ti in skippers:
#             continue
#         if len(towel) > len(design):
#             skippers.add(ti)
#             continue
#         if len(towel) == len(design) and (towel == design).all():
#             combinations = 1
#             break
        
#         if len(towel) == 1:
#             matches = np.where(design == towel)[0]
#         else:
#             mval = (towel ** 2).sum()
#             matches = np.where(np.convolve(design, np.flip(towel), "valid") == mval)[0]
#         if len(matches) == 0:
#             skippers.add(ti)
#             continue
#         for mi in reversed(matches):
#             combinations += combination_implicit(design[(mi + len(towel)):], towels, first_only, skippers.copy(), cache) 
#             combinations += combination_implicit(design[:mi], towels, first_only, skippers.copy(), cache)
#     cache[tupdes] = combinations
#     # print("CACHE SIZE: ", cache_size(cache))
#     return combinations

# def part2_v1(type : str, verbose : bool=False, timing : bool=False):
#     towels, designs = parse_input(type)
#     shared_cache = {}
#     return sum(map(lambda x : combination_implicit(x, towels, False, None, shared_cache), (tqdm(designs, "Solving designs...") if timing else designs))) * 2