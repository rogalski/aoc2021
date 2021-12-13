SparseMatrix = dict[tuple[int, int], bool]
FoldInstruction = tuple[str, int]


def get_input(path: str) -> tuple[SparseMatrix, list[FoldInstruction]]:
    d: SparseMatrix = {}
    folds: list[FoldInstruction] = []
    with open(path) as fh:
        for line in fh:
            try:
                x, y = map(int, line.split(","))
            except ValueError:
                if line.startswith("fold along "):
                    instruction = line.split()[-1]
                    axis, val = instruction.split("=")
                    folds.append((axis, int(val)))
            else:
                d[x, y] = True
    return d, folds


def fold_x(m: SparseMatrix, xf: int) -> SparseMatrix:
    m2 = m.copy()
    for x, y in list(m):
        assert m[x, y] is True
        if x > xf:
            m2[xf + (xf - x), y] = True
            del m2[x, y]

    return m2


def fold_y(m: SparseMatrix, yf: int) -> SparseMatrix:
    m2 = m.copy()
    for x, y in list(m):
        assert m[x, y] is True
        if y > yf:
            m2[x, yf + (yf - y)] = True
            del m2[x, y]

    return m2


def print_matrix(m: SparseMatrix):
    x_max = max(m, key=lambda t: t[0])[0]
    y_max = max(m, key=lambda t: t[1])[1]
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            if m.get((x, y)):
                print("#", end="")
            else:
                print(' ', end="")
        print()
    print()


def test_ex():
    m, folds = get_input("ex.txt")
    fold = folds[0]
    fold_func = {'x': fold_x, 'y': fold_y}
    mp = fold_func[fold[0]](m, fold[1])
    assert sum(mp.values()) == 17


def solve1():
    m, folds = get_input("input.txt")
    fold = folds[0]
    fold_func = {'x': fold_x, 'y': fold_y}
    mp = fold_func[fold[0]](m, fold[1])
    print(sum(mp.values()))


def solve2():
    m, folds = get_input("input.txt")
    fold_func = {'x': fold_x, 'y': fold_y}
    for fold in folds:
        m = fold_func[fold[0]](m, fold[1])
    print_matrix(m)


if __name__ == "__main__":
    test_ex()
    solve1()
    solve2()
