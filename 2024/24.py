from helpers import get_path, get_lines, Animation

import random
from random import randint

from collections import defaultdict
from itertools import zip_longest

OPS = {
    "OR" : lambda x, y : x | y, #int(x + y >= 1),
    "XOR": lambda x, y : x ^ y, #int(x + y == 1),
    "AND": lambda x, y : x & y, # int(x + y == 2)
}

def swap(a, b, gates):
    gates[a], gates[b] = gates[b], gates[a]

def parse_input(type : str):
    gates = {}
    for line in get_lines(get_path(type)):
        if not line:
            continue
        if ": " in line:
            gate, val = line.split(": ")
            gates[gate] = int(val)
        else:
            expr, dst = line.split(" -> ")
            # left, op, right = expr.split(" ")
            gates[dst] = expr.split(" ")
    return gates

def b2d(nums : list[int]):
    return sum(v * (2 ** i) for i, v in enumerate(reversed(nums)))

def d2b(num : int, size=None):
    out = [int(v) for v in bin(num).lstrip("0b")]
    if size is None:
        return out
    return [0] * (size - len(out)) + out

def get_gates(gates, prefix):
    return sorted([gate for gate in gates if gate.startswith(prefix)], key=lambda x : -int(x[1:]))

def get_expected(gates, type="ADD"):
    x_out, y_out = map(lambda x : get_output(gates, x), "xy")
    
    match type:
        case "ADD":
            operation = lambda x, y : x + y
        case "AND":
            operation = lambda x, y : x & y
        case _:
            raise ValueError("UNKNOWN EXPECTED OPERATION")
    
    return d2b(operation(b2d(x_out), b2d(y_out)), len([1 for gate in gates if gate.startswith("z")]))



def get_output(gates, prefix : str="z"):
    cache = {}
    # def evaluate(what, seen = None, depth=0):
    def evaluate(what):
        if what in cache:
            return cache[what]
        
        # if seen is None:
        #     seen = {what}
        
        val = gates[what]
        if isinstance(val, int):
            return val
        left, op, right = val
        
        # if {left, right} & seen:
        #     raise RecursionError(f"CYCLE DETECTED ({depth})")
        # cache[what] = OPS[op](evaluate(left, seen | {left}, depth+1), evaluate(right, seen | {right}, depth+1))
        
        cache[what] = OPS[op](evaluate(left), evaluate(right))
        
        return cache[what]
    return [evaluate(gate) for gate in get_gates(gates, prefix)]
    

def part1(type : str):
    return b2d(get_output(parse_input(type)))

print(part1("input")) 
    
def difference(a, b):
    return "⠀".join("⠀" if i == j else "|" for i, j in zip_longest(a, b))

import matplotlib.pyplot as plt
from tqdm import tqdm
import networkx as nx

def plot_directed_graph(graph_dict: dict[str, list[str]]) -> None:
    # Create a directed graph
    graph = nx.DiGraph()

    # Add edges to the graph from the dictionary
    for parent, children in graph_dict.items():
        for child in children:
            graph.add_edge(child, parent)

    # Create the layout for the graph
    # pos = nx.planar_layout(graph)
    pos = nx.kamada_kawai_layout(graph)
    # pos = nx.fruchterman_reingold_layout(graph)
    
    # Draw the graph
    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, node_size=100, node_color="lightblue", edge_color="gray", font_size=10, font_weight="bold")

    # Show the plot
    plt.show()
    
def neighborhood(center, graph, inv_graph, size : int=100, bans = None):
    if size < 0:
        return set()
    if bans is None:
        bans = set()
    parents = graph[center]
    if isinstance(parents, int):
        parents = []
    else:
        parents = parents.split(" ")
        parents = [parents[0], parents[2]]
    children : set = inv_graph[center]
    adjacent = set(parents) | children
    bans |= adjacent
    for n in adjacent - bans:
        new = neighborhood(n, graph, inv_graph, size-1, bans)
        adjacent |= new
        bans |= set(new)
    return adjacent

def cycleable(gate, expr):
    l, _, r = expr
    return not (l[0] in "xy" or r[0] in "xy" or gate[0] == "z")

def depth(gate, gates):
    if isinstance(gates[gate], int):
        return 1
    l, _, r = gates[gate]
    return depth(l, gates) + depth(r, gates)
    
def swaps(gates, bans=None, circuit="ADD"):
    inv_graph = defaultdict(set)
    for k, v in gates.items():
        if isinstance(v, int):
            continue
        l, _, r = v
        inv_graph[l].add(k)
        inv_graph[r].add(k)
        
    not_xy_gates = [gate for gate in gates if not gate[0] in "xy"] # and not cycleable(gate, gates[gate])

    candidates = defaultdict(set)
    j = 0
    n = 1000000000
    for i, gate_i in enumerate(not_xy_gates):
        if j > n:
                break
        for gate_j in not_xy_gates[:i]:
            if "x" in gate_j or "y" in gate_j:
                continue
            if j > n:
                break
            if gate_i in gates[gate_j] or gate_j in gates[gate_i]:
                continue
            pair = tuple(sorted((gate_i, gate_j)))
            if bans and pair in bans:
                continue
            try:
                improvement = calculate_improvement(gates, pair, circuit)
            except RecursionError:
                candidates[-9999].add(pair)
                swap(gate_i, gate_j, gates)
                j += 1
                continue
            if improvement != 0:
                if improvement < 0:
                    candidates[-9999].add(pair)
                else:
                    candidates[improvement].add(pair)
            j += 1
            
    return candidates

def set_random_input(gates, x_val : int | None=None, y_val : int | None=None, seed=None):
    if seed is not None:
        random.seed(seed)
    
    x_gates, y_gates = (
        sorted([gate for gate in gates if gate.startswith(c)], key=lambda x : -int(x[1:]))
        for c in "xy"
    )
    
    x_val, y_val = (d if isinstance(d, int) else randint(0, 2 ** (len(t)) - 1) for t, d in zip([x_gates, y_gates], [x_val, y_val]))
    [gates.update({g : v for g, v in zip_longest(this, d2b(value, len(this)), fillvalue=0)}) for this, value in zip([x_gates, y_gates], [x_val, y_val])]
    
    return gates

def calculate_improvement(gates, pair, circuit="ADD"):
    ex = get_expected(gates, circuit)
    vo = get_output(gates)
    do = sum(1 for e, v in zip(ex, vo) if e != v)
    swap(*pair, gates)
    va = get_output(gates)
    da = sum(1 for e, v in zip(ex, va) if e != v)
    swap(*pair, gates)
    return do - da

def part2(type : str, base_swaps : list | None=None, circuit_type="ADD"):
    gates = parse_input(type)
    
    # swap('jbp', 'z35', gates)
    # swap('jgc', 'z15', gates)
    # swap('drg', 'z22', gates)
    # swap('gvw', 'qjb', gates)
    
    if base_swaps is not None:
        [swap(*swp, gates) for swp in base_swaps]
    
    bans = set()
    all_candidates = defaultdict(lambda : 0)
    
    for _ in tqdm(range(100), leave=False):
        set_random_input(gates)

        # z_out = get_output(gates)
        # z_correct = get_expected(gates, circuit_type)
        # print(*z_out)
        # print(*z_correct)
        # print(difference(z_out, z_correct))
    
        candidates = swaps(gates, bans, circuit_type)

        for cost, swps in candidates.items():
            for swp in swps:
                all_candidates[swp] += cost
                if cost < 0:
                    bans.add(swp)
            
    all_candidates = {c : v for c, v in all_candidates.items() if c not in bans}
    validated_candidates, invalid_candidates = {}, set()
    
    for candidate in tqdm(sorted(all_candidates, key=lambda x : all_candidates[x], reverse=True), total=len(all_candidates)):
        if all_candidates[candidate] < 0:
            invalid_candidates.add(candidate)
        improvements = [calculate_improvement(gates, candidate, circuit_type) for _ in range(150) if set_random_input(gates)]
        if min(improvements) >= 0:
            validated_candidates[candidate] = sum(improvements) / len(improvements)
        else:
            invalid_candidates.add(candidate)
    
    four : list = base_swaps or []
    
    for p in sorted(validated_candidates, key=lambda x : validated_candidates[x], reverse=True):
        c = validated_candidates[p]
        selected = len(four) < 4 and not any(e in op for e in p for op in four)
        if selected:
            four.append(p)
        print(f'{p} ~ {c}{" *" if selected else ""}')
        break
        
    if len(four) < 4:
        four : list = part2(type, four, circuit_type)
        
    return four
    
            
print(",".join(sorted([e for p in part2("input") for e in p])))
# print(",".join(sorted(['jbp', 'z35', 'jgc', 'z15', 'drg', 'z22', 'gvw', 'qjb'])))


### ### ### ### ### ###