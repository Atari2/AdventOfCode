from __future__ import annotations
from typing import Union
from enum import IntEnum
from functools import reduce

def read_from_input():
    with open('input.txt', 'r') as f:
        return f.read()

tot_version = 0

class PacketType(IntEnum):
    LITERAL = 4
    OPERATOR_SUM = 0
    OPERATOR_PRODUCT = 1
    OPERATOR_MINIMUM = 2
    OPERATOR_MAXIMUM = 3
    OPERATOR_GREATER = 5
    OPERATOR_LESS = 6
    OPERATOR_EQUAL = 7

    def get_op_from_type(self):
        operations = {
            PacketType.LITERAL: lambda x: x,
            PacketType.OPERATOR_SUM: lambda packets: sum([p.value for p in packets]),
            PacketType.OPERATOR_PRODUCT: lambda packets: reduce(lambda x, y: x * y, [p.value for p in packets]),
            PacketType.OPERATOR_MINIMUM: lambda packets: min([p.value for p in packets]),
            PacketType.OPERATOR_MAXIMUM: lambda packets: max([p.value for p in packets]),
            PacketType.OPERATOR_GREATER: lambda packets: 1 if packets[0].value > packets[1].value else 0,
            PacketType.OPERATOR_LESS: lambda packets: 1 if packets[0].value < packets[1].value else 0,
            PacketType.OPERATOR_EQUAL: lambda packets: 1 if packets[0].value == packets[1].value else 0,
        }
        return operations[self]

class Packet:
    packet_type: PacketType
    version: int
    rest: str
    value: Union[int, list[Packet]]
    packet_len: int

    def __init__(self, p_type: int, version: int, rest: str, idx: int, comes_from_operator: bool = False):
        self.packet_type = PacketType(p_type)
        global tot_version
        self.version = version
        tot_version += self.version
        self.packet_len = 0
        self.value = 0 if self.packet_type == PacketType.LITERAL else []
        self.parse_packet(rest, idx, comes_from_operator)
        self.value = self.packet_type.get_op_from_type()(self.value)

    def parse_packet(self, packet: str, idx: int, comes_from_operator: bool = False):
        if self.packet_type == PacketType.LITERAL:
            self.parse_literal_packet(packet, idx, comes_from_operator)
        else:
            self.parse_operator_packet(packet, idx, comes_from_operator)
        
    def parse_literal_packet(self, binary_data: str, idx: int, comes_from_operator: bool = False):
        start = idx
        while binary_data[idx] == '1': 
            idx += 5
        idx += 5
        self.packet_len = idx - start
        if comes_from_operator:
            slack = 0
        else:
            slack = 8 - (idx % 8)
        sht = (self.packet_len // 5) - 1
        for i in range(start, idx - slack, 5):
            self.value |= int(binary_data[i+1:i+5], 2) << (sht * 4)
            sht -= 1
        self.packet_len += slack

    def parse_operator_packet(self, binary_data: str, idx: int, comes_from_operator: bool = False):
        start = idx
        mode = binary_data[idx]
        idx += 1
        if mode == '0':
            tot_length_in_bits = int(binary_data[idx:idx+15], 2)
            idx += 15
            end_of_packet = idx + tot_length_in_bits
            while idx < end_of_packet:
                packet, idx = self.create_packet(binary_data, idx, True)
                self.value.append(packet)
        elif mode == '1':
            num_of_packets = int(binary_data[idx:idx+11], 2)
            idx += 11
            for _ in range(num_of_packets):
                packet, idx = self.create_packet(binary_data, idx, True)
                self.value.append(packet)
        self.packet_len = idx - start
        if comes_from_operator:
            slack = 0
        else:
            slack = 8 - (idx % 8)
        self.packet_len += slack

    @staticmethod
    def create_packet(bitstream: str, idx: int, comes_from_operator: bool = False) -> tuple[Packet, int]:
        p_version = int(bitstream[idx:idx+3], 2)
        idx += 3
        p_type = int(bitstream[idx:idx+3], 2)
        idx += 3
        packet = Packet(p_type, p_version, bitstream, idx, comes_from_operator)
        idx += packet.packet_len
        return packet, idx


def parse_packet_stream(packet_stream: str):
    bitstream = ''.join([bin(int(c, 16))[2:].zfill(4) for c in packet_stream])
    packet, _ = Packet.create_packet(bitstream, 0)
    print(f"Packet value: {packet.value}")
    print(f"Total version: {tot_version}")
    
parse_packet_stream(read_from_input())
