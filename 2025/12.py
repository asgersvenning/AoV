import numpy as np
from helpers import get_lines, get_path
from tqdm.contrib.concurrent import thread_map


def parse_input(input : list[str]) -> tuple[list[np.ndarray], list[tuple[tuple[int, int], np.ndarray]]]:
    shapes, trees = [], []
    element = []
    for line in input:
        if not line:
            shapes.append(np.array(element))
            element = []
        elif ":" in line:
            desc, other = line.split(":")
            if other:
                trees.append((tuple(map(int, desc.split("x"))), np.fromiter(map(int, other[1:].split(" ")), int)))
        else:
            element.append([c == "#" for c in line])
    return shapes, trees

input = parse_input(get_lines(get_path("input")))

def part1(shapes : list[np.ndarray], tree : tuple[tuple[int, int], np.ndarray]):
    sizes = np.array([shp.sum() for shp in shapes])
    (h, w), requirements = tree
    if (h * w) < sizes.repeat(requirements).sum():
        return False
    def search(state : np.ndarray, remainder : np.ndarray):
        if np.all(remainder == 0):
            return True
        flag = True
        while flag and state.size:
            flag = False
            if np.all(state[:2].any(0)):
                state = state[1:]
                flag = True
            if np.all(state[-2:].any(0)):
                state = state[:-1]
                flag = True
            if np.all(state[:,:2].any(1)):
                state = state[:,1:]
                flag = True
            if np.all(state[:,-2:].any(1)):
                state = state[:,:-1]
                flag = True
        h, w = state.shape
        area = h * w
        if area < 9 or h < 3 or w < 3:
            return False
        emptyrows = np.flatnonzero((~state).all(1))
        if not emptyrows.size:
            mh = h
        else:
            mh = min(emptyrows.min()+3,h)
        emptycols = np.flatnonzero((~state).all(0))
        if not emptycols.size:
            mw = w
        else:
            mw = min(emptycols.min()+3,w)
        retval = False
        for e in np.flatnonzero(remainder):
            shpo = shapes[e]
            if area < shpo.sum():
                continue
            new_remainder = remainder.copy()
            new_remainder[e] -= 1
            rots = [0]
            if not np.all(shpo == shpo.T):
                rots.append(1)
            if not np.all(shpo == shpo[:,::-1]):
                rots.append(2)
            if len(rots) == 3:
                rots.append(3)
            for i in rots:
                shp = [shpo, shpo.T, shpo[:,::-1], shpo[:,::-1].T][i]
                sh, sw = shp.shape
                if sh > h or sw > w:
                    continue
                for i in range(mh-sh+1):
                    if retval:
                        return retval
                    for j in range(mw-sw+1):
                        if retval:
                            return retval
                        sel = slice(i,(i+sh)), slice(j,(j+sw))
                        if np.any(np.logical_and(state[*sel], shp)):
                            continue
                        if not (
                            j == 0 and i == 0 or
                            j > 0 and np.any(state[sel[0], j-1]) or 
                            (j + sw) < w and np.any(state[sel[0], j+sw]) or
                            i > 0 and np.any(state[i-1,sel[1]]) or
                            (i + sh) < h and np.any(state[i+sh,sel[1]])
                        ):
                            continue  
                        new_state = state.copy()
                        new_state[*sel] |= shp
                        retval = retval or search(new_state, new_remainder)
        return retval
    return search(np.zeros((h,w),bool),requirements)
    
print("Part 1:", sum(thread_map(lambda tree : part1(input[0], tree), sorted(input[1], key=lambda x : x[0][0] * x[0][1] / sum(x[1])), desc="Fitting presents under trees...", leave=False, max_workers=4)))