import functools
import heapq


def get_input(path: str) -> list[list[int]]:
    with open(path) as fh:
        return [[*map(int, line.strip())] for line in fh]


def solve(heightmap: list[list[int]]) -> int:
    ret = 0
    num_rows = len(heightmap)
    num_cols = len(heightmap[0])
    for row_number, row in enumerate(heightmap):
        for col_number, value in enumerate(row):
            to_compare: set[int] = set()
            if row_number > 0:
                to_compare.add(heightmap[row_number - 1][col_number])
            if col_number > 0:
                to_compare.add(heightmap[row_number][col_number - 1])
            if row_number < num_rows - 1:
                to_compare.add(heightmap[row_number + 1][col_number])
            if col_number < num_cols - 1:
                to_compare.add(heightmap[row_number][col_number + 1])
            if all(c > value for c in to_compare):
                ret += value + 1
    return ret


def solve_p2(heightmap: list[list[int]]) -> int:
    # this is basically problem of finding connected components
    visited = [[False] * len(heightmap[0]) for _ in range(len(heightmap))]
    sizes: list[int] = []
    for row_number, row in enumerate(heightmap):
        for col_number, value in enumerate(row):
            size = dfs(visited, heightmap, row_number, col_number)
            if size > 0:
                sizes.append(size)
    return functools.reduce(lambda x, y: x*y, heapq.nlargest(3, sizes))


def dfs(visited: list[list[bool]], heightmap: list[list[int]], row_number: int, col_number: int):
    size = 0
    num_rows = len(heightmap)
    num_cols = len(heightmap[0])
    if not visited[row_number][col_number]:
        visited[row_number][col_number] = True
        if heightmap[row_number][col_number] == 9:
            return 0
        size += 1
        if row_number > 0:
            size += dfs(visited, heightmap, row_number - 1, col_number)
        if col_number > 0:
            size += dfs(visited, heightmap, row_number, col_number - 1)
        if row_number < num_rows - 1:
            size += dfs(visited, heightmap, row_number + 1, col_number)
        if col_number < num_cols - 1:
            size += dfs(visited, heightmap, row_number, col_number + 1)
    return size


assert 15 == solve(get_input("ex.txt"))
print(solve(get_input("input.txt")))
assert 1134 == solve_p2(get_input("ex.txt"))
print(solve_p2(get_input("input.txt")))
