from __future__ import annotations
from copy import deepcopy
from enum import IntEnum
import itertools

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()

class Wire:
    name: str
    value: bool | None

    def __init__(self, name: str, value: bool | None):
        self.value = value
        self.name = name

    def __repr__(self):
        return f'{self.name} = {self.value}'

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: str | Wire):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name
    
    def has_value(self) -> bool:
        return self.value is not None


class GateType(IntEnum):
    AND = 0
    OR = 1
    XOR = 2

class Gate:
    gate_type: GateType
    inputs: tuple[Wire, Wire]
    output: Wire

    def __init__(self, input1: Wire, input2: Wire, output: Wire, gate_type: GateType):
        self.inputs = (input1, input2)
        self.output = output
        self.gate_type = gate_type

    @staticmethod
    def from_string(input: str, existing_wires: list[Wire]):
        inputs_and_type, output = input.split('->')
        try:
            output = existing_wires[existing_wires.index(output.strip())] 
        except ValueError:
            output = Wire(output.strip(), None)
            existing_wires.append(output)
        input1, gate_type, input2 = inputs_and_type.strip().split(' ')
        try:
            input1 = existing_wires[existing_wires.index(input1.strip())] 
        except ValueError:
            input1 = Wire(input1.strip(), None)
            existing_wires.append(input1)
        try:
            input2 = existing_wires[existing_wires.index(input2.strip())] 
        except ValueError:
            input2 = Wire(input2.strip(), None)
            existing_wires.append(input2)
        gate_type = GateType[gate_type.upper()]
        return Gate(input1, input2, output, gate_type)

    def __repr__(self):
        return f'{self.inputs[0]} {self.gate_type} {self.inputs[1]} -> {self.output}'

    def can_be_calculated(self) -> bool:
        return all(w.has_value() for w in self.inputs)
    
    def calculated(self) -> bool:
        return self.output.has_value()
    
    def calculate(self):
        match self.gate_type:
            case GateType.AND:
                self.output.value = self.inputs[0].value & self.inputs[1].value
            case GateType.OR:
                self.output.value = self.inputs[0].value | self.inputs[1].value
            case GateType.XOR:
                self.output.value = self.inputs[0].value ^ self.inputs[1].value

wires: list[Wire] = []
for v in data[0:data.index('\n')]:
    name, value = v.strip().split(':')
    wires.append(Wire(name.strip(), value.strip() == '1'))
gates: list[Gate] = []
for v in data[data.index('\n')+1:]:
    gates.append(Gate.from_string(v, wires))
z_wires = sorted([w for w in wires if w.name[0] == 'z'], key=lambda w: w.name, reverse=True)
while not all(w.has_value() for w in z_wires):
    for g in gates:
        if g.can_be_calculated() and not g.calculated():
            g.calculate()

part1 = int(''.join(map(lambda w: '1' if w.value else '0', z_wires)), 2)

highest_z = z_wires[0]

wrong: set[Wire] = set()
for gate in gates:
    if gate.output.name[0] == "z" and gate.gate_type != GateType.XOR and gate.output != highest_z:
        wrong.add(gate.output)
    if (
        gate.gate_type == GateType.XOR
        and gate.output.name[0] not in ["x", "y", "z"]
        and gate.inputs[0].name[0] not in ["x", "y", "z"]
        and gate.inputs[1].name[0] not in ["x", "y", "z"]
    ):
        wrong.add(gate.output)
    if gate.gate_type == GateType.AND and "x00" not in gate.inputs:
        for subgate in gates:
            if gate.output in subgate.inputs and subgate.gate_type != GateType.OR:
                wrong.add(gate.output)
    if gate.gate_type == GateType.XOR:
        for subgate in gates:
            if gate.output in subgate.inputs and subgate.gate_type == GateType.OR:
                wrong.add(gate.output)

part2 = ",".join(sorted(map(lambda w: w.name, wrong)))

print(f'{part1} {part2}')
