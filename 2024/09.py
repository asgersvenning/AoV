import os
import bisect
from sortedcontainers import SortedDict
import numpy as np

def parse_input(path : str):
    with open(path, "r") as file:
        return list(map(int, file.read().strip()))
    
def get_input(type : str="test"):
    dir, file = os.path.split(__file__)    
    day, _ = os.path.splitext(file)
    return parse_input(os.path.join(dir, "inputs", day + "." + type))
    
def expand_view(data : list[int], ids : list[bool]) -> list[str]:
    out = []
    for size, id in zip(data, ids):
        out.extend([str(id) if id != -1 else "."] * size)
    return out

def spans(indices, max):
    breaks = np.where(np.diff(np.array(indices, dtype=np.int32), 1) > 1)[0].tolist()
    return SortedDict({indices[start + 1] : indices[start + 1] + end - start for start, end in zip(([-1] + breaks), (breaks + [max]))})

class File:
    def __init__(self, id, disk, start=None, size=None, indices=None, maintain_disk : bool=True, with_spans : bool=False):
        self.disk = disk
        self._maintain_disk = maintain_disk
        self.file = id != -1
        self.id = id if self.file else None
        if indices is None:
            self.indices = list(range(start, start+size))
        else:
            if not (start is None and size is None):
                raise ValueError("Cannot supply both indices and start/stop")
            self.indices = sorted(indices)
        self._with_spans = with_spans
        if self._with_spans:
            self.spans = spans(self.indices, len(self))
    
    def __len__(self):
        return len(self.indices)
    
    def __iadd__(self, i : int):
        bisect.insort(self.indices, i)
        if self._maintain_disk:
            self.disk[i] = str(self.id) if self.file else "."
        if self._with_spans:
            check_merge = False
            for j, (start, end) in enumerate(self.spans.items()):
                overshoot = i - (end - 1)
                undershoot = start - i
                if overshoot == 1 or undershoot == 1:
                    check_merge = True
                    break
                if overshoot > 1:
                    break
            if check_merge:
                if overshoot == 1:
                    next_start, next_end = self.spans.peekitem(j + 1)
                    if (next_start - end) <= 2:
                        self.spans.pop(next_start)
                        self.spans[start] = next_end                   
                    else:
                        self.spans[start] += 1
                if undershoot == 1:
                    prev_start, prev_end = self.spans.peekitem(j - 1)
                    self.spans.pop(start)
                    if (start - prev_end) <= 2:
                        self.spans[prev_start] = end
                    else:
                        self.spans[start - 1] = end
            else:
                self.spans[i] = i + 1
        return self
    
    def __isub__(self, i : int):
        self.indices.pop(bisect.bisect(self.indices, i) - 1)
        if self._maintain_disk:
            self.disk[i] = "?"
        if self._with_spans:
            for start, end in self.spans.items():
                if start <= i and i < end:
                    break
            if (end - start) <= 1:
                self.spans.pop(start)
            else:
                if i == start:
                    self.spans.pop(start)
                    self.spans[start + 1] = end
                elif i == end:
                    self.spans[start] -= 1
                else:
                    self.spans[start] = i
                    self.spans[i+1] = end                    
        return self
    
    def swap(self, other : "File", i : int, j : int):
        if i in self.indices and j in other.indices:
            self -= i
            other -= j
            self += j
            other += i            
        else:
            raise RuntimeError(f"Swap index ({i}) must be present in left or right object")
        
    def checksum(self):
        if not self.file:
            raise TypeError("Cannot compute checksum for space-type file", self)
        id = int(self.id)
        return sum([i * id for i in self.indices])
        
    def __repr__(self):
        name = "FILE" if self.file else "SPACE"
        if self.file:
            name += f"[{self.id}]"
        return f"{name} | [{','.join(map(str, self.indices))}]"
        

def part1(data : list[int], visualize : slice | bool | None=False):    
    ids = [int(i // 2) if i % 2 == 0 else -1 for i in range(len(data))]
    disk = expand_view(data, ids)
    n = len(disk)
    
    if isinstance(visualize, bool):
        visualize = None if not visualize else slice(0, n, 1)
    if not visualize is None:
        vis = "|".join(disk[visualize])
        print(vis)
    
    files, space = {}, []
    for i, e in enumerate(disk):
        if e == ".":
            space.append(i)
        else:
            if not e in files:
                files[e] = []
            files[e].append(i)
    files = {str(id) : File(id, disk, indices=i) for id, i in files.items()}
    space = File(-1, disk, indices=space)
    i, j = 0, n - 1
    while True:
        if disk[i] == ".":
            while not disk[j].isdigit():
                j -= 1
            if i >= j:
                break
            space.swap(files[disk[j]], i, j)
            if not visualize is None:
                next_vis = "|".join(disk[visualize])
                if vis != next_vis:
                    vis = next_vis
                    print(vis)
        i += 1
    return sum([file.checksum() for _, file in files.items()])
    
# print(part1(get_input(), True))
print(part1(get_input("input")))

from tqdm import tqdm

def part2(data : list[int], visualize : slice | bool | None=False):    
    ids = [int(i // 2) if i % 2 == 0 else -1 for i in range(len(data))]
    disk = expand_view(data, ids)
    n = len(disk)
    
    if isinstance(visualize, bool):
        visualize = None if not visualize else slice(0, n, 1)
    if not visualize is None:
        vis = "|".join(disk[visualize])
        print(vis)
    
    files, space = {}, []
    for i, e in enumerate(disk):
        if e == ".":
            space.append(i)
        else:
            if not e in files:
                files[e] = []
            files[e].append(i)
    files = SortedDict({int(id) : File(id, disk, indices=i, maintain_disk=not visualize is None) for id, i in files.items()})
    space = File(-1, disk, indices=space, maintain_disk=not visualize is None, with_spans=True)
    
    iterator = tqdm(reversed(files), total=len(files)) if visualize is None else reversed(files)
    for id in iterator:
        file = files[id]
        for start in space.spans:
            if start > file.indices[0]:
                    break
            end = space.spans[start]
            if (end - start) >= len(file):
                for i, j in zip(range(start, start + len(file)), file.indices.copy()):
                    space.swap(file, i, j)
                break
        if not visualize is None:
            next_vis = "|".join(disk[visualize])
            if vis != next_vis:
                vis = next_vis
                print(vis)
    return sum([file.checksum() for _, file in files.items()])

# print(part2(get_input(), True))
print(part2(get_input("input")))