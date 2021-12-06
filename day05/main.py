from __future__ import annotations

import collections
import dataclasses
import os
import pathlib
import re
from typing import MutableMapping, Iterator


@dataclasses.dataclass(eq=True, frozen=True)
class Coord:
    x: int
    y: int

    def enumerate_simple(self, other: Coord) -> Iterator[Coord]:
        x0 = min(self.x, other.x)
        x1 = max(self.x, other.x)
        y0 = min(self.y, other.y)
        y1 = max(self.y, other.y)
        if x0 == x1:
            for y in range(y0, y1 + 1):
                yield Coord(x0, y)
        elif y0 == y1:
            for x in range(x0, x1 + 1):
                yield Coord(x, y0)
        else:
            # For now, only consider horizontal and vertical lines
            return

    def enumerate_with_diagonal(self, other: Coord) -> Iterator[Coord]:
        x0 = min(self.x, other.x)
        x1 = max(self.x, other.x)
        y0 = min(self.y, other.y)
        y1 = max(self.y, other.y)
        if x0 == x1:
            for y in range(y0, y1 + 1):
                yield Coord(x0, y)
        elif y0 == y1:
            for x in range(x0, x1 + 1):
                yield Coord(x, y0)
        elif x1 - x0 == y1 - y0:
            # ugly, probably can be simplified
            dx = (other.x - self.x) // (x1 - x0)
            dy = (other.y - self.y) // (y1 - y0)
            for i in range(x1 - x0 + 1):
                yield Coord(self.x + i * dx, self.y + i * dy)
        else:
            raise ValueError


Input = list[tuple[Coord, Coord]]
Map = MutableMapping[Coord, int]


def input_from_file(path: os.PathLike) -> Input:
    with open(path) as fh:
        return [parse_line(line) for line in fh]


def parse_line(line: str) -> tuple[Coord, Coord]:
    m = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line)
    assert m is not None
    x0, y0, x1, y1 = map(int, m.groups())
    return Coord(x0, y0), Coord(x1, y1)


def solve(inputs: Input) -> int:
    vent_map: Map = collections.defaultdict(int)
    for p0, p1 in inputs:
        for p in p0.enumerate_simple(p1):
            vent_map[p] += 1
    return sum(v > 1 for v in vent_map.values())


def solve_second(inputs: Input) -> int:
    vent_map: Map = collections.defaultdict(int)
    for p0, p1 in inputs:
        for p in p0.enumerate_with_diagonal(p1):
            vent_map[p] += 1
    return sum(v > 1 for v in vent_map.values())


if __name__ == "__main__":
    assert solve(input_from_file(pathlib.Path("ex.txt"))) == 5
    print(solve(input_from_file(pathlib.Path("input.txt"))))
    assert solve_second(input_from_file(pathlib.Path("ex.txt"))) == 12
    print(solve_second(input_from_file(pathlib.Path("input.txt"))))
