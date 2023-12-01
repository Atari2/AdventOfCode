SAMPLE_DATA: bool = False
filename = "sample_data.txt" if SAMPLE_DATA else "data.txt"
with open(filename, 'r') as f:
    data = f.read()
[next((print(i + n, end=' ') for i in range(len(data) - n) if len(set(data[i:i+n])) == n)) for n in [4, 14]]
