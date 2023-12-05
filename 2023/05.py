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

class Map:
    def __init__(self, string : str):
        lines = string.strip().splitlines()
        title = lines.pop(0)
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
                remainder = min(distances) if len(distances) > 0 else "inf"
                return key, remainder
            else:
                return key
    
def length_of_step(remainders : list) -> int:
    remainders = [r for r in remainders if r != "inf"]
    return min(remainders)
    
path = "inputs/05.input"

with open(path, "r") as f:
    # Part 1 - Calculate all locations
    data = f.read().split("\n\n")
    seeds = data[0].strip().removeprefix("seeds: ").split(" ")
    seeds = [int(s) for s in seeds]
    maps = [Map(m) for m in data[1:]]

    locations = []
    for seed in seeds:
        intermediary = seed
        for m in maps:
            intermediary = m[intermediary]
        locations.append(intermediary)
    print(min(locations))

    # Part 2 - Skip linear ranges
    for map in maps:
        map.get_remainder = True
    seed_ranges = [[i, j] for i, j in zip(seeds[::2], seeds[1::2])]
    locations = []
    for start, length in seed_ranges:
        seed = start
        while seed < start + length:
            intermediary, remainders = seed, []
            for map in maps:
                intermediary, remaining = map[intermediary]
                remainders.append(remaining)
            seed += length_of_step(remainders) + 1
    
            locations.append(intermediary)
    print(min(locations))
