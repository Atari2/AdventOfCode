from __future__ import annotations
import numpy

SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename, 'r') as f:
    data = f.read().splitlines()

class CRT:
    _matrix: numpy.ndarray
    _width: int = 40
    _height: int = 6
    _row: int = 0
    _col: int = 0

    def __init__(self):
        self._matrix = numpy.zeros((self._height, self._width), dtype=str)
    
    def __str__(self):
        return '\n'.join([''.join(row) for row in self._matrix])

    def draw_pixel(self, pos: int):
        if self._col == self._width:
            self._col = 0
            self._row += 1
        if pos - 1 <= self._col <= pos + 1:
            self._matrix[self._row,self._col] = '#' 
        else:
            self._matrix[self._row,self._col] = '.'
        self._col += 1

class CPU:
    _x: int
    _cycles: int
    signal_strength: int
    _crt: CRT

    def __init__(self):
        self._x = 1
        self._cycles = 1
        self.signal_strength = 0
        self._crt = CRT()

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    def one_cycle(self):
        if self._cycles == 20:
            self.signal_strength += (self.x * self._cycles)
        elif self._cycles > 20 and ((self._cycles - 20) % 40) == 0:
            self.signal_strength += (self.x * self._cycles)
        self._cycles += 1
        self._crt.draw_pixel(self._x)
    
    @property
    def crt(self):
        return self._crt


    
class Instruction:
    def execute(self, cpu: CPU):
        raise ValueError("Not implemented")

class Addx(Instruction):
    def __init__(self, x: int):
        self.x = x
    
    def execute(self, cpu: CPU):
        cpu.one_cycle()
        cpu.one_cycle()
        cpu.x += self.x
    
class Noop(Instruction):
    def execute(self, cpu: CPU):
        cpu.one_cycle()

def create_instr(insn: str) -> Instruction:
    if insn.startswith("noop"):
        return Noop()
    elif insn.startswith("addx"):
        return Addx(int(insn.split(" ")[1]))
    raise ValueError(f"Unknown instruction: {insn}")


instructions = [create_instr(insn) for insn in data]
cpu = CPU()
for insn in instructions:
    insn.execute(cpu)


print(cpu.signal_strength, 'ZUPRFECL')
# this prints the ascii ART of the CRT.
# it says 'ZUPRFECL'
# print(cpu.crt)