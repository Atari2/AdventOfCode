from enum import IntEnum

SAMPLE_DATA: bool = False
if SAMPLE_DATA:
    filename = "sample_data.txt"
else:
    filename = "data.txt"

class ReportType(IntEnum):
    Unk = -1
    Desc = 0
    Asc = 1

def check_valid_p1(report: list[int]) -> bool:
    latest_v = report[0]
    report_type = ReportType.Unk
    for v in report[1:]:
        diff = abs(v - latest_v)
        if report_type == ReportType.Unk:
            if v > latest_v and 1 <= diff <= 3:
                report_type = ReportType.Asc
            elif v < latest_v and 1 <= diff <= 3:
                report_type = ReportType.Desc
            else: 
                return False
        elif report_type == ReportType.Asc:
            if v < latest_v:
                return False
            if not 1 <= diff <= 3:
                return False
        elif report_type == ReportType.Desc:
            if v > latest_v:
                return False
            if not 1 <= diff <= 3:
                return False
        latest_v = v
    return True

def check_valid_p2(report: list[int]) -> bool:
    if check_valid_p1(report):
        return True
    else:
        for i in range(len(report)):
            if check_valid_p1(report[:i] + report[i+1:]):
                return True
    return False


with open(filename, 'r') as f:
    lines = [list(map(int, line.split())) for line in f.readlines()]
    part1 = sum(map(check_valid_p1, lines))
    part2 = sum(map(check_valid_p2, lines))
    print(f'{part1} {part2}')
    

