from __future__ import annotations
import re
import numpy
from enum import IntEnum

patt = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((?:\w+(?:, )?)+)', re.MULTILINE)

SAMPLE_DATA: bool = True
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename, 'r') as f:
    data = f.read()

MAX_MINUTES = 30

class State(IntEnum):
    OPEN = 1
    CLOSED = 2

class Valve:
    name: str
    _flow_rate: None|int
    time_flow_rate: numpy.ndarray
    tunnels: list[Valve]
    state: State

    def __init__(self, name: str, flow_rate: str|None = None, tunnels: str|None = None, valves: dict[str, Valve]|None = None):
        self.name = name
        self._flow_rate = int(flow_rate) if flow_rate else None
        self.tunnels = []
        self.state = State.CLOSED
        if tunnels and (valves is not None):
            self.set_tunnels(tunnels, valves)

    def can_open(self):
        return self.flow_rate > 0 and self.state == State.CLOSED
    
    def set_tunnels(self, tunnels: str, valves: dict[str, Valve]):
        connected_tunnels = tunnels.split(', ')
        for tunnel in connected_tunnels:
            if tunnel not in valves:
                valves[tunnel] = Valve(tunnel)
        self.tunnels = [valves[tunnel] for tunnel in connected_tunnels]
    
    @property
    def flow_rate(self):
        return self._flow_rate if self._flow_rate else 0
    
    @flow_rate.setter
    def flow_rate(self, value: int|str):
        self._flow_rate = value if isinstance(value, int) else int(value)
        if self._flow_rate > 0:
            self.time_flow_rate = numpy.array([i*self._flow_rate for i in range(MAX_MINUTES, 0, -1)], dtype=int)

    def flow_rate_at(self, minute: int):
        return self.time_flow_rate[minute - 1] if self._flow_rate else 0

    def __repr__(self):
        return f"Valve {self.name} has flow rate={self.flow_rate}; tunnels lead to valves {', '.join([valve.name for valve in self.tunnels])}"
    
    def __str__(self):
        return self.__repr__()

def print_dict(d: dict[str, Valve]):
    for key, value in d.items():
        print(f"{key}: {value}")


tot_pressure = 0
valves: dict[str, Valve] = {}
for match in patt.finditer(data):
    name, flow_rate, tunnels = match.groups()
    if valve := valves.get(name):
        valve.flow_rate = flow_rate
        valve.set_tunnels(tunnels, valves)
    else:
        valves[name] = Valve(name, flow_rate, tunnels, valves)

max_pressure = 0

class Move(IntEnum):
    MOVE = 1
    OPEN = 2

def format_tuple(t: tuple[Valve, Move]):
    return f"{'o' if t[1] == Move.OPEN else 'm'}{t[0].name}"

def update_pressure(pressure: int):
    global max_pressure
    if pressure > max_pressure:
        print(f'New max pressure: {pressure}')
        max_pressure = pressure

def visit(current_valve: Valve, pressure: int, minute: int):
    if minute >= MAX_MINUTES:
        update_pressure(pressure)
        return
    opened = False
    if current_valve.can_open():
        current_valve.state = State.OPEN
        minute += 1
        pressure += current_valve.flow_rate_at(minute)
        opened = True
    for valve in current_valve.tunnels:
        if valve.state == State.CLOSED:
            visit(valve, pressure, minute+1)
    if opened:
        minute -= 1
    current_valve.state = State.CLOSED
    for valve in current_valve.tunnels:
        if valve.state == State.CLOSED:
            visit(valve, pressure, minute+1)
    return


current_valve = valves['AA']
visit(current_valve, 1, 0)
print(max_pressure)