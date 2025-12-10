import re
from collections import deque

import numpy as np
from helpers import get_lines, get_path
from scipy.optimize import Bounds, LinearConstraint, milp


class Machine:
    def __init__(self, lights : np.ndarray, buttons : list[np.ndarray], joltage : np.ndarray):
        self.lights, self.buttons, self.joltage = lights, [np.isin(np.arange(len(lights)), button) for button in buttons], joltage
    
    def solve_lights(self):
        init, paths, visited = np.zeros(len(self.lights), bool), deque(), set()
        paths.append((init, [])) or visited.add(self.hash(init))
        while paths:
            state, path = paths.popleft()
            if np.all(state == self.lights):
                return path
            [visited.add(new_hash) or paths.append((new_state, path + [tuple(button.tolist())])) for button in self.buttons if not ((new_hash := self.hash(new_state := state ^ button)) in visited)]
    
    def solve_joltage(self):
        return round(milp(
                ONE := np.ones((len(self.buttons),),int), 
                integrality=ONE, 
                bounds=Bounds(lb=0, ub=np.inf), 
                constraints=LinearConstraint(
                    np.column_stack(self.buttons), 
                    lb=self.joltage-0.5, 
                    ub=self.joltage+0.5
                )
            ).fun)
    
    @staticmethod
    def hash(state : np.ndarray):
        return state.tobytes()

def parse_input(input : list[str]):
    LIGHT, BUTTON, JOLTAGE = map(re.compile, [r"\[([\.#]+)\]", r"\(([\d,]+)\)", r"\{([\d,]+)\}"])
    return [
        Machine(
            lights=np.array([0 if c == "." else 1 for c in re.search(LIGHT, line).group(1)], bool), 
            buttons=[np.array(list(map(int, match.split(","))), int) for match in re.findall(BUTTON, line)], 
            joltage=np.array(list(map(int, re.search(JOLTAGE, line).group(1).split(","))), np.uint32)
        ) for line in input
    ]

input = parse_input(get_lines(get_path("input")))

# Part 1
def part1(machines : list[Machine]):
    return sum(map(len, (machine.solve_lights() for machine in machines)))

print("Part 1:", part1(input)) # = 432

# Part 2
def part2(machines : list[Machine]):
    return sum(machine.solve_joltage() for machine in machines)

print("Part 2:", part2(input)) # = 18011