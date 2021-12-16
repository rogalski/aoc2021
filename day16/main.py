import binascii
import dataclasses
import enum
import functools


class OpMode(enum.Enum):
    FixLength = 0
    NumPackets = 1

    def __repr__(self):
        return f"{self}"


@dataclasses.dataclass(eq=True)
class Packet:
    version: int
    type: int

    @property
    def bitlength(self):
        raise NotImplementedError


@dataclasses.dataclass(eq=True)
class LiteralPacket(Packet):
    value: int
    _num_chunks: int

    @property
    def bitlength(self):
        return 3 + 3 + 5 * self._num_chunks


@dataclasses.dataclass(eq=True)
class OperatorPacket(Packet):
    mode: OpMode
    mode_len: int
    packets: list[Packet]

    @property
    def bitlength(self):
        return (
            3
            + 3
            + 1
            + (15 if self.mode is OpMode.FixLength else 11)
            + sum(p.bitlength for p in self.packets)
        )


def decode_str(s):
    stream = bitstream_from_str(s)
    while True:
        try:
            yield from decode_packet(stream, pad=True)
        except (StopIteration, RuntimeError):
            return


def decode_packet(stream, pad=True):
    version = int_from_bitstream(stream, 3)
    packet_type = int_from_bitstream(stream, 3)
    if packet_type == 4:
        value_bits = []
        while True:
            value_first_bit = next(stream)
            for _ in range(4):
                value_bits.append(next(stream))
            if value_first_bit == 0:
                break

        value = sum(v << len(value_bits) - i - 1 for i, v in enumerate(value_bits))
        packet = LiteralPacket(version, packet_type, value, len(value_bits) // 4)
        if pad:
            padding = 4 - (packet.bitlength % 4)
            for p in range(padding):
                assert next(stream) == 0
        yield packet
    else:
        # operator packet
        mode_bit = next(stream)
        if mode_bit == 0:
            total_length = int_from_bitstream(stream, 15)
            packets = []
            while sum(p.bitlength for p in packets) < total_length:
                packet = next(decode_packet(stream, pad=False))
                packets.append(packet)
            packet = OperatorPacket(
                version,
                packet_type,
                OpMode.FixLength,
                total_length,
                packets,
            )
            yield packet
            if pad:
                padding = 4 - (packet.bitlength % 4)
                for p in range(padding):
                    assert next(stream) == 0
        else:
            num_of_subpackets = int_from_bitstream(stream, 11)
            packet = OperatorPacket(
                version,
                packet_type,
                OpMode.NumPackets,
                num_of_subpackets,
                [
                    next(decode_packet(stream, pad=False))
                    for _ in range(num_of_subpackets)
                ],
            )
            yield packet
            if pad:
                padding = 4 - (packet.bitlength % 4)
                for p in range(padding):
                    assert next(stream) == 0


def int_from_bitstream(stream, n):
    s = 0
    for i in range(n - 1, -1, -1):
        s += next(stream) << i
    return s


def bitstream_from_str(s):
    for byte in binascii.unhexlify(s):
        yield bool(byte & (1 << 7))
        yield bool(byte & (1 << 6))
        yield bool(byte & (1 << 5))
        yield bool(byte & (1 << 4))
        yield bool(byte & (1 << 3))
        yield bool(byte & (1 << 2))
        yield bool(byte & (1 << 1))
        yield bool(byte & (1 << 0))


assert [*decode_str("D2FE28")] == [
    LiteralPacket(version=6, type=4, value=2021, _num_chunks=3)
]
assert [*decode_str(2 * "D2FE28")] == 2 * [
    LiteralPacket(version=6, type=4, value=2021, _num_chunks=3)
]
assert [*decode_str("38006F45291200")] == [
    OperatorPacket(
        version=1,
        type=6,
        mode=OpMode.FixLength,
        mode_len=27,
        packets=[
            LiteralPacket(version=6, type=4, value=10, _num_chunks=1),
            LiteralPacket(version=2, type=4, value=20, _num_chunks=2),
        ],
    )
]
assert [*decode_str("EE00D40C823060")] == [
    OperatorPacket(
        version=7,
        type=3,
        mode=OpMode.NumPackets,
        mode_len=3,
        packets=[
            LiteralPacket(version=2, type=4, value=1, _num_chunks=1),
            LiteralPacket(version=4, type=4, value=2, _num_chunks=1),
            LiteralPacket(version=1, type=4, value=3, _num_chunks=1),
        ],
    )
]


def sum_versions(packets: list[Packet]) -> int:
    total = 0
    for p in packets:
        total += p.version
        if isinstance(p, OperatorPacket):
            total += sum_versions(p.packets)
    return total


assert sum_versions([*decode_str("8A004A801A8002F478")]) == 16
assert sum_versions([*decode_str("620080001611562C8802118E34")]) == 12
assert sum_versions([*decode_str("C0015000016115A2E0802F182340")]) == 23
assert sum_versions([*decode_str("A0016C880162017C3686B18A3D4780")]) == 31

print(sum_versions([*decode_str(open("input.txt").read())]))


def solve(packet: Packet):
    if isinstance(packet, LiteralPacket):
        return packet.value
    else:
        assert isinstance(packet, OperatorPacket)
        if packet.type == 0:
            return sum(solve(p) for p in packet.packets)
        elif packet.type == 1:
            return functools.reduce(
                lambda a, b: a * b, (solve(p) for p in packet.packets), 1
            )
        elif packet.type == 2:
            return min(solve(p) for p in packet.packets)
        elif packet.type == 3:
            return max(solve(p) for p in packet.packets)
        elif packet.type == 5:
            assert len(packet.packets) == 2
            return int(solve(packet.packets[0]) > solve(packet.packets[1]))
        elif packet.type == 6:
            assert len(packet.packets) == 2
            return int(solve(packet.packets[0]) < solve(packet.packets[1]))
        elif packet.type == 7:
            assert len(packet.packets) == 2
            return int(solve(packet.packets[0]) == solve(packet.packets[1]))


print(solve([*decode_str(open("input.txt").read())][0]))
