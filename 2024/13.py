import re
from typing import Callable, Any

from helpers import get_path, get_lines

def line_fn(basis : tuple[int, int]) -> Callable[[int], tuple[int, int]]:
    # (X, Y) = t * {T[x], T[y]}
    return lambda t : tuple(d * t for d in basis)

def gcd(a : int, b : int):
    if a == 0 or b == 0:
        return max(a, b)
    return gcd(b, a % b)

def lcm(a : int, b : int):
    if a == 0 or b == 0:
        return 0
    if a == b:
        return abs(a)
    a, b = sorted((abs(b), abs(a)))
    if a == 1:
        return b
    return a * (b // gcd(a, b))

def binary_search(fun : Callable[[int], Any], target : Any, t_min : int, t_max : int, gt_fn = lambda x, y : any(xi > yi for xi, yi in zip(x, y))) -> int | float:
    if t_min == t_max:
        if fun(t_min) == target:
            return t_min
        return t_min + 1/2
    if (t_max - t_min) == 1:
        v_min = fun(t_min)
        v_max = fun(t_max)
        if v_min == target:
            return t_min
        if v_max == target:
            return t_max
        return (t_min + t_max) / 2
    t_mid = int((t_min + t_max) // 2)
    if gt_fn(fun(t_mid), target):
        return binary_search(fun, target, t_min, t_mid - 1, gt_fn)
    else:
        return binary_search(fun, target, t_mid, t_max, gt_fn)

def solve(fun : Callable[[int], tuple[int, int]], target : tuple[int, int]):
    t = 0
    current = fun(t)
    while not any(c > t for c, t in zip(current, target)):
        t = (t + 1) ** 2
        current = fun(t)
    return binary_search(fun, target, t ** (1/2) - 1, t)

def find_rem_loop(offset : int, delta : int, modulo : int):
    hits = []
    i = 0
    while len(hits) < 2:
        if i > (3 * modulo):
            return None, None
        current = (i * delta) % modulo
        if offset == current:
            hits.append(i)
        i += 1
    return hits[0], hits[-1] - hits[-2]

def figure_remainder(l0 : tuple[int, int], l1 : tuple[int, int], target : tuple[int, int]):
    # b0 + a0 * N = b1 + a1 * M
    # b0 - b1 = a1 * M - a0 * N
    i = min(tuple(t // v for v, t in zip(l0, target)))
    tr = tuple(t - v * i for t, v in zip(target, l0))
    
    lsx, ldx = find_rem_loop(tr[0], l1[0], l0[0])
    # print("lx", lsx, ldx)
    if lsx is None or ldx is None:
        return None
    lsy, ldy = find_rem_loop(tr[1], l1[1], l0[1])
    # print("ly", lsy, ldy)
    if lsy is None or ldy is None:
        return None
    # print("______________")
    # print(lsx, lsy)
    # print(ldx, ldy)
    # print("--------------")
    solutions = []
    for i in range(max(lsy + 2 * ldy + 2, lsx + 2 * ldx + 2)):
        left = lsx + ldx * i - lsy
        if left < 0:
            continue
        j = left / ldy
        if j % 1 != 0:
            continue
        # print(i, j)
        left = left + lsy
        right = lsy + ldy * j
        # print(left, right)
        if left != right:
            raise RuntimeError()
        solutions.append(left)
    if not solutions:
        return None
    return min(solutions)

class Machine:
    def __init__(self, A : tuple[int, int], B : tuple[int, int], Prize : tuple[int, int]):
        self.A, self.B, self.prize = A, B, Prize
        self.cost = (3, 1)
        # max_p = [i for i, v in enumerate(self.prize) if v == max(self.prize)][0]
        # self._order = "A" if (self.cost[0] * self.prize[max_p] / self.A[max_p]) < (self.cost[1] * self.prize[max_p] / self.B[max_p]) else "B"
        A_c, B_c = ([prize / (v / cost) for v, prize in zip(button, self.prize)] for button, cost in zip([self.A, self.B], self.cost))
        self._order = "B" if max(B_c) <= max(A_c) else "A"
        
        # self._order = "B"
        self._A, self._B = line_fn(self.A), line_fn(self.B)
        
    def __repr__(self):
        fmt = str(type(self)) + "\nButton A: X+{}, Y+{}\nButton B: X+{}, Y+{}\nPrize: X={}, Y={}\nOrder: {}\n"
        return fmt.format(*self.A, *self.B, *self.prize, self._order)
    
    def solve(self) -> dict[int, tuple[int, int]]:
        solutions = {}
        params = [self.B, self.A]
        buttons = [self._B, self._A]
        if self._order == "B":
            buttons = buttons[::-1]
            params = params[::-1]
        # to = solve(buttons[0], self.prize)
        # if not (to % 1 == 0):
        #     to = to + (to % 1)
        # # print(to)
        # i = -1
        # while to >= 0:
        #     xo, yo = buttons[0](to)
        #     # print(tuple(map(int, (xo, yo))))
        #     # print(self.prize)
        #     # print(self.prize[0] - xo, self.prize[1] - yo)
        #     if xo > self.prize[0] or yo > self.prize[1]:
        #         to -= 1
        #         continue
        #     ti = solve(buttons[1], tuple(p - o for p, o in zip(self.prize, (xo, yo))))
        #     # print(ti, to)
        #     if ti % 1 == 0:
        #         ta, tb = (ti, to) if self._order == "A" else (to, ti)
        #         solutions[3 * ta + 1 * tb] = (ta, tb)
        #         return solutions
        #     to -= 1
        # return solutions
        
        
        to = figure_remainder(*params, self.prize)
        if to is None:
            return solutions
        partial_prize = tuple(p - e for p, e in zip(self.prize, buttons[1](to)))
        # ti = solve(buttons[1], tuple(p - o for p, o in zip(self.prize, buttons[0](to))))
        ti = partial_prize[0] / params[0][0]
        if ti % 1 != 0:
            return solutions
        ta, tb = map(int, (ti, to) if self._order == "B" else (to, ti))
        solutions[3 * ta + 1 * tb] = (ta, tb)
        return solutions

def parse_input(type : str) -> list["Machine"]:
    machines = []
    machine = {}
    for line in get_lines(get_path(type)):
        if line == "":
            machines.append(Machine(**machine))
            machine = {}
            continue
        cls, x, y = re.findall(r"[A-Za-z]+(?=:)|\d+", line)
        machine[cls] = (int(x), int(y))
    if machine:
        machines.append(Machine(**machine))
    return machines

def part1(type : str):
    total = 0
    for machine in parse_input(type):
        print(machine)
        solutions = machine.solve()
        if not solutions:
            continue
        cost, solution = sorted(solutions.items())[0]
        if solution[-1] > 100:
            continue
        sA, sB = solution
        print(f"{sA} * {machine.A} + {sB} * {machine.B} = {tuple(i + j for i, j in zip(machine._A(sA), machine._B(sB)))}")
        print(machine.prize[1] % machine.B[1])
        print("COST:", cost)
        print("########################################")
        total += cost
    return total

print(part1("test"))
# print(part1("input"))

def part2(type : str):
    total = 0
    for machine in parse_input(type):
        machine.prize = tuple(v + 10000000000000 for v in machine.prize)
        print(machine)
        solutions = machine.solve()
        if not solutions:
            continue

        cost, solution = sorted(solutions.items())[0]
        # print(machine)
        sA, sB = solution
        print(f"{sA} * {machine.A} + {sB} * {machine.B} = {tuple(i + j for i, j in zip(machine._A(sA), machine._B(sB)))}")
        print(machine.prize[1] % machine.B[1])
        print("COST:", cost)
        total += cost
    return total

# print(part2("test"))