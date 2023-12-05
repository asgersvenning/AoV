from typing import Any


class Range:
    def __init__(self, string : str) -> list[int]:
        string = string.strip().split(" ")
        self.destination, self.source, self.length = [int(part) for part in string]
        self.offset = self.destination - self.source

    def includes(self, n : int) -> bool:
        return self.source <= n <= self.source + self.length - 1
    
    def __call__(self, n : int, get_remainder : bool=False) -> int:
        if self.includes(n):
            if get_remainder:
                return n + self.offset, (self.source + self.length - 1) - n
            else:
                return n + self.offset
        else:
            raise ValueError(f"{n} is not in range {self}")

    def __str__(self):
        return f"{self.source} -> {self.destination} ({self.length})"
    
    def invert(self):
        return Range(f"{self.source} {self.destination} {self.length}")
    

class Map:
    def __init__(self, string : str):
        # print(string)
        lines = string.strip().splitlines()
        title = lines.pop(0)
        # print(lines)
        self.name = title.removesuffix(" map:")
        self.ranges = [Range(line) for line in lines]
        self.get_remainder = False
        
    def __getitem__(self, key):
        for r in self.ranges:
            if r.includes(key):
                return r(key, self.get_remainder)
        else:
            if self.get_remainder:
                distances = [r.source - key for r in self.ranges if r.source > key]
                if len(distances) > 0:
                    remainder = min(distances)
                else:
                    remainder = "inf"
                return key, remainder
            else:
                return key
        
    def min_key(self):
        """
        This function finds the key that is mapped to the smallest value.

        The minimum key is 0 and the minimum value is also 0.
        """
        for r in self.ranges:
            if r.destination == 0:
                return r.source
        else:
            return 0
        
    def __str__(self):
        return self.name + ": " + ", ".join([str(r) for r in self.ranges])
    
    def invert(self):
        inverse_ranges = [r.invert() for r in self.ranges]
        new_name = self.name.split("-")[::-1]
        new_name = "-".join(new_name)
        inverse_map = Map(new_name + " map:")
        inverse_map.ranges = inverse_ranges
        return inverse_map
    
def length_of_step(remainders : list) -> int:
    """
    This function takes a list of remainders and returns the amount of steps left before the next jump.
    """
    remainders = [r for r in remainders if r != "inf"]
    return min(remainders)
    
path = "inputs/05.input"

with open(path, "r") as f:
    # Part 1
    data = f.read().split("\n\n")
    seeds = data[0].strip().removeprefix("seeds: ").split(" ")
    seeds = [int(s) for s in seeds]

    maps = [Map(m) for m in data[1:]]

    locations = []
    for seed in seeds:
        for m in maps:
            seed = m[seed]
        locations.append(seed)
    print(min(locations))

    # Part 2
    #inverse_maps = [m.invert() for m in reversed(maps)]
    for m in maps:
        m.get_remainder = True
    seed_ranges = [[i, j] for i, j in zip(seeds[::2], seeds[1::2])]
    initial_seeds = []
    locations = []
    old_location = None
    for start, length in seed_ranges:
        seed = start
        did_jump = False
        while seed < start + length:
            initial_seeds += [seed]
            remainders = []
            intermediary = seed
            for m in maps:
                intermediary, remaining = m[intermediary]
                remainders.append(remaining)
            if not did_jump:
                # Jump to the next seed (last in the current linear range)
                seed += length_of_step(remainders)
                did_jump = True
            else:
                # Jump to the next seed (first in the next linear range)
                seed += 1
                did_jump = False
            
            # Score for the current seed
            location = intermediary
            locations.append(location)
    print(min(locations))








