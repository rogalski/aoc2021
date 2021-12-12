import collections

Graph = dict[str, list[str]]
G: Graph = {'start': ['A', 'b'], 'A': ['c', 'b', 'end'], 'c': ['A'], 'b': ['d', 'A', 'end'], 'd': ['b'], 'end': []}


def get_input(path: str) -> Graph:
    g = collections.defaultdict(list)
    with open(path) as fh:
        for line in fh:
            src, dst = line.strip().split("-")
            g[src].append(dst)
            g[dst].append(src)
    return g


def yield_paths(g: Graph):
    # DFS (?)
    visited = {node: False for node in g}
    for p in _dfs(g, 'start', 'end', visited, []):
        yield p


def _dfs(g: Graph, start: str, end: str, visited: dict[str, bool], path: list[str]):
    # hacked DFS to allow revisit
    if start == 'start' or start.islower():
        visited[start] = True
    path.append(start)
    if start == end:
        yield path
    for node in g[start]:
        if not visited[node]:
            yield from _dfs(g, node, end, visited, path)
    path.pop()
    visited[start] = False


def yield_paths2(g: Graph):
    # DFS (?)
    visited = {node: 0 for node in g}
    small_nodes = [node for node in g if node not in {'start', 'end'} and node.islower()]
    paths: set[tuple[str, ...]] = set()
    for small_node in small_nodes:
        for p in _dfs2(g, 'start', 'end', visited, [], small_node):
            pt = tuple(p)
            if pt not in paths:
                yield pt
            paths.add(pt)


def _dfs2(g: Graph, start: str, end: str, visited: dict[str, int], path: list[str], visit_twice: str):
    visited[start] += 1
    path.append(start)
    if start == end:
        yield path
    for node in g[start]:
        if node == 'start':
            continue
        if _can_visit(node, visited, visit_twice):
            yield from _dfs2(g, node, end, visited, path, visit_twice)
    path.pop()
    visited[start] -= 1


def _can_visit(node: str, visited: dict[str, int], visit_twice: str) -> bool:
    if node.isupper():
        return True
    elif node == visit_twice:
        return visited[node] < 2
    return visited[node] == 0


assert len([*yield_paths(G)]) == 10
assert len([*yield_paths(get_input("ex.txt"))]) == 19
assert len([*yield_paths(get_input("ex2.txt"))]) == 226
print(len([*yield_paths(get_input("input.txt"))]))

assert len([*yield_paths2(G)]) == 36
assert len([*yield_paths2(get_input("ex.txt"))]) == 103
assert len([*yield_paths2(get_input("ex2.txt"))]) == 3509
print(len([*yield_paths2(get_input("input.txt"))]))
