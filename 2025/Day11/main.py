from __future__ import annotations

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"


with open(filename, 'r') as f:
    data = f.readlines()

class Device:
    name: str
    connections: list[Device]
    _hash: int

    def __init__(self, name: str):
        self.name = name
        self._hash = hash(name)
        self.connections = []
    
    def add_connection(self, device: Device):
        self.connections.append(device)

    def __repr__(self) -> str:
        return f"Device({self.name} -> {[d.name for d in self.connections]})"
    
    def __hash__(self):
        return self._hash
    
def find_all_paths(start: Device, end: Device, path: list[Device] = []) -> int:
    path = path + [start]
    if start == end:
        return 1
    path_count = 0
    for conn in start.connections:
        if conn not in path:
            path_count += find_all_paths(conn, end, path)
    return path_count

def find_all_paths_with_dac_and_fft(
    current: Device, 
    end: Device, 
    dac: Device, 
    fft: Device, 
    seen_dac: bool = False, 
    seen_fft: bool = False, 
    memo: dict = None
) -> int:
    if memo is None:
        memo = {}
    if current == dac:
        seen_dac = True
    if current == fft:
        seen_fft = True
    state = (current, seen_dac, seen_fft)
    if state in memo:
        return memo[state]
    if current == end:
        return 1 if seen_dac and seen_fft else 0
    total_paths = 0
    for conn in current.connections:
        total_paths += find_all_paths_with_dac_and_fft(
            conn, end, dac, fft, seen_dac, seen_fft, memo
        )
    memo[state] = total_paths
    return total_paths

devices: dict[str, Device] = {}

for line in data:
    device, connections = [l.strip() for l in line.strip().split(":")]
    if device not in devices:
        devices[device] = Device(device)
    for conn in connections.split(" "):
        if conn not in devices:
            devices[conn] = Device(conn)
        devices[device].add_connection(devices[conn])

you = devices.get("you")
out = devices["out"]
svr = devices["svr"]
dac = devices["dac"]
fft = devices["fft"]

p1 = 0
if you:
    p1 = find_all_paths(you, out)

p2 = find_all_paths_with_dac_and_fft(svr, out, dac, fft)

print(f'{p1} {p2}')