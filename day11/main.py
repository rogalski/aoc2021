def visit(energies: list[list[int]], row_number: int, col_number: int) -> None:
    num_rows = len(energies)
    num_cols = len(energies[0])
    if row_number not in range(0, num_rows):
        return
    if col_number not in range(0, num_cols):
        return
    if energies[row_number][col_number] == 0:
        return
    if energies[row_number][col_number] >= 10:
        energies[row_number][col_number] = 0
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                if drow == 0 and dcol == 0:
                    continue
                neighbor_row_number = row_number + drow
                neighbor_col_number = col_number + dcol
                if neighbor_row_number < 0 or neighbor_row_number >= num_rows or neighbor_col_number < 0 or neighbor_col_number >= num_cols:
                    continue
                if energies[neighbor_row_number][neighbor_col_number] != 0:
                    energies[neighbor_row_number][neighbor_col_number] += 1
                    visit(energies, neighbor_row_number, neighbor_col_number)


def epoch(energies: list[list[int]]) -> None:
    for row_number, row in enumerate(energies):
        for col_number, value in enumerate(row):
            energies[row_number][col_number] += 1
    for row_number, row in enumerate(energies):
        for col_number, value in enumerate(row):
            visit(energies, row_number, col_number)


def get_input(path: str) -> list[list[int]]:
    with open(path) as fh:
        return [[*map(int, line.strip())] for line in fh]


def print_energies(energies: list[list[int]]) -> None:
    for row in energies:
        for value in row:
            print(value, end="")
        print()
    print()


def solve(energies: list[list[int]], n: int) -> int:
    summary = 0
    for i in range(n):
        epoch(energies)
        summary += sum(value == 0 for row in energies for value in row)
    return summary


def solve2(energies: list[list[int]]) -> int:
    i = 0
    while True:
        epoch(energies)
        i += 1
        if all(value == 0 for row in energies for value in row):
            return i


i1 = get_input("ut1.txt")
print_energies(i1)
epoch(i1)
print_energies(i1)
epoch(i1)
print_energies(i1)

i2 = get_input("ut2.txt")
print_energies(i2)
epoch(i2)
print_energies(i2)
epoch(i2)
print_energies(i2)

in_p1 = get_input("input.txt")
print(solve(in_p1, 100))

in_p2 = get_input("input.txt")
print(solve2(in_p2))
