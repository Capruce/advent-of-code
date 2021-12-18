from __future__ import annotations

from dataclasses import dataclass
import fileinput
from math import prod
from typing import Callable, Union


@dataclass
class BitStream:
    _bits: str
    index: int = 0

    @classmethod
    def from_hex(cls, hex: str) -> BitStream:
        return BitStream("".join(f"{int(d, 16):>04b}" for d in hex), 0)

    def read(self, size: int) -> str:
        next_index = self.index + size
        substring = self._bits[self.index:next_index]
        self.index = next_index
        return substring


def load_bits() -> BitStream:
    return BitStream.from_hex("".join(fileinput.input()).strip())


OpFunc = Callable[[list[int]], int]
TYPE_TO_FUNCTION: dict[int, OpFunc] = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    # 4 is literal
    5: lambda packets: int(packets[0] > packets[1]),
    6: lambda packets: int(packets[0] < packets[1]),
    7: lambda packets: int(packets[0] == packets[1]),
}


PACKET_TYPE_LITERAL = 4


@dataclass(frozen=True)
class Packet:
    version: int
    type: PacketType

    @classmethod
    def read_from(cls, bits: BitStream) -> Packet:
        version     = int(bits.read(3), 2)
        packet_type = int(bits.read(3), 2)

        if packet_type == PACKET_TYPE_LITERAL:
            component: PacketType = Literal.read_from(bits)
        else:
            op = TYPE_TO_FUNCTION[packet_type]
            component = Operator.read_from(bits, op)

        return Packet(version, component)

    def sum_of_versions(self) -> int:
        return self.version + self.type.sum_of_versions()

    def value(self) -> int:
        return self.type.value


@dataclass(frozen=True)
class Literal:
    value: int

    @staticmethod
    def read_chunk(bits: BitStream) -> tuple[bool, str]:
        return bits.read(1) == "0", bits.read(4)

    @classmethod
    def read_from(cls, bits: BitStream) -> Literal:
        literal = ""
        while True:
            is_last, chunk = cls.read_chunk(bits)
            literal += chunk

            if is_last:
                break

        return Literal(int(literal, 2))

    def sum_of_versions(self) -> int:
        return 0


@dataclass(frozen=True)
class Operator:
    op: OpFunc
    packets: list[Packet]

    @classmethod
    def read_from(cls, bits: BitStream, op: OpFunc) -> Operator:
        packets = []
        length_type = bits.read(1)

        if length_type == "0":
            length = int(bits.read(15), 2)
            start_i = bits.index

            while bits.index < start_i + length:
                packets.append(Packet.read_from(bits))

        else:
            length = int(bits.read(11), 2)
            for _ in range(length):
                packets.append(Packet.read_from(bits))

        return Operator(op, packets)

    def sum_of_versions(self) -> int:
        return sum(p.sum_of_versions() for p in self.packets)

    @property
    def value(self) -> int:
        return self.op([packet.value() for packet in self.packets])


PacketType = Union[Literal, Operator]


if __name__ == "__main__":
    BITS = load_bits()
    PACKET = Packet.read_from(BITS)
    print("Part 1:", PACKET.sum_of_versions())
    print("Part 2:", PACKET.value())
