from __future__ import annotations

import os
import pathlib
from typing import Sequence, Dict

BingoIndex = tuple[int, int]


class Bingo:
    def __init__(self, n: int = 5) -> None:
        self._n = n
        self._values: dict[int, BingoIndex] = {}
        self._marked: dict[BingoIndex, bool] = {
            (i, j): False for i in range(self._n) for j in range(self._n)
        }

    @classmethod
    def from_lines(cls, lines: Sequence[str]) -> Bingo:
        bingo = cls()
        for row_number, line in enumerate(lines):
            for col_number, value_str in enumerate(line.split()):
                value = int(value_str)
                bingo.set_value((row_number, col_number), value)
        return bingo

    def set_value(self, idx: BingoIndex, value: int) -> None:
        self._values[value] = idx

    def mark(self, value: int) -> None:
        if value not in self._values:
            return
        idx = self._values[value]
        self._marked[idx] = True
        del self._values[value]

    def is_solved(self) -> bool:
        return any(
            self.is_row_solved(n) or self.is_col_solved(n) for n in range(self._n)
        )

    def is_row_solved(self, row_number: int) -> bool:
        if row_number >= self._n:
            raise ValueError(row_number)
        return all(self._marked[row_number, n] for n in range(self._n))

    def is_col_solved(self, col_number: int) -> bool:
        if col_number >= self._n:
            raise ValueError(col_number)
        return all(self._marked[n, col_number] for n in range(self._n))

    def score(self) -> int:
        if not self.is_solved():
            raise RuntimeError
        return sum(self._values)


def get_input_from_file(file_path: os.PathLike) -> tuple[list[int], list[Bingo]]:
    with open(file_path) as fh:
        input_str, *input_bingos = fh.read().split("\n\n")

    values = [int(v) for v in input_str.split(",")]
    bingos = [
        Bingo.from_lines(input_bingo.splitlines()) for input_bingo in input_bingos
    ]
    return values, bingos


def solve_problem(file_path: os.PathLike) -> int:
    values, bingos = get_input_from_file(file_path)
    value = -1
    for value in values:
        for bingo in bingos:
            bingo.mark(value)
        if any(bingo.is_solved() for bingo in bingos):
            break
    last_number = value
    solved_bingo = next(bingo for bingo in bingos if bingo.is_solved())
    score = solved_bingo.score()
    final_score = score * last_number
    return final_score


def solve_second_problem(file_path: os.PathLike) -> int:
    values, bingos = get_input_from_file(file_path)
    value = -1
    solved_bingos: list[Bingo] = []
    for value in values:
        for bingo in bingos:
            if bingo in solved_bingos:
                continue
            bingo.mark(value)
            if bingo.is_solved():
                solved_bingos.append(bingo)
        if all(bingo.is_solved() for bingo in bingos):
            break
    last_number = value
    last_solved_bongo = solved_bingos[-1]
    score = last_solved_bongo.score()
    final_score = score * last_number
    return final_score


if __name__ == "__main__":
    assert solve_problem(pathlib.Path("ex.txt")) == 4512
    print(solve_problem(pathlib.Path("input.txt")))
    assert solve_second_problem(pathlib.Path("ex.txt")) == 1924
    print(solve_second_problem((pathlib.Path("input.txt"))))
