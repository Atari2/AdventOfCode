from __future__ import annotations
import re
import heapq
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()


MACHINE_PATT = re.compile(r'\[(?P<lights>[.#]+)\] (?P<buttons>(?:\((?:\d+)(?:,(?:\d+))*\) ?)+) \{(?P<joltages>(?:\d+)(?:,(?:\d+))*)\}')

class Machine:
    target_lights: list[bool]
    lights: list[bool]
    buttons: list[tuple[int, ...]]
    target_joltage: list[int]
    joltage: list[int]

    def __init__(self, lights: list[bool], buttons: list[tuple[int, ...]], joltage: list[int]) -> None:
        self.target_lights = lights
        self.lights = [False] * len(lights)
        self.buttons = buttons
        self.target_joltage = joltage
        self.joltage = [0] * len(joltage)
    
    def press(self, button_index: int) -> None:
        for i in self.buttons[button_index]:
            self.lights[i] = not self.lights[i]
    
    def is_solved(self) -> bool:
        return self.lights == self.target_lights
    
    def __repr__(self):
        return f'Machine(lights={self.target_lights}, buttons={self.buttons}, joltage={self.target_joltage})'
    
    def solve_milp(self) -> int:
        n_buttons = len(self.buttons)
        n_counters = len(self.target_joltage)
        
        A = np.zeros((n_counters, n_buttons))
        for j, btn in enumerate(self.buttons):
            for i in btn:
                if i < n_counters:
                    A[i, j] = 1
        
        c = np.ones(n_buttons)
        target = self.target_joltage
        
        constraints = LinearConstraint(A, lb=target, ub=target)
        bounds = Bounds(lb=0, ub=np.inf)
        integrality = np.ones(n_buttons)
        
        res = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)
        
        if res.success:
            return int(round(res.fun))
        return 0
    
    def djikstra_lights(self) -> int:
        initial_state = tuple(self.lights)
        target_state = tuple(self.target_lights)

        pq: list[tuple[int, tuple[bool, ...]]] = []
        heapq.heappush(pq, (0, initial_state))
        visited: set[tuple[bool, ...]] = set()

        while pq:
            steps, state = heapq.heappop(pq)

            if state in visited:
                continue
            visited.add(state)

            if state == target_state:
                return steps

            for button_index in range(len(self.buttons)):
                new_state = list(state)
                for i in self.buttons[button_index]:
                    new_state[i] = not new_state[i]
                heapq.heappush(pq, (steps + 1, tuple(new_state)))

        return -1  # Unreachable

    @staticmethod
    def from_line(line: str) -> Machine:
        match = MACHINE_PATT.search(line.strip())
        if not match:
            raise ValueError(f"Invalid line format: {line}")

        lights_str = match.group('lights')
        buttons_str = match.group('buttons')
        joltage_str = match.group('joltages')

        lights = [c == '#' for c in lights_str]
        buttons = [tuple(map(int, b.strip('()').split(','))) for b in buttons_str.split() if b]
        joltage = list(map(int, joltage_str.split(',')))

        return Machine(lights, buttons, joltage)

p1 = 0
machines = [Machine.from_line(line) for line in data]
for machine in machines:
   p1 += machine.djikstra_lights()

p2 = 0
for machine in machines:
    steps = machine.solve_milp()
    p2 += steps
print(f'{p1} {p2}')