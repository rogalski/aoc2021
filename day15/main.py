import itertools
import queue
import sys
from typing import TypeVar, Generic

import numpy as np
import heapq


def get_input(path: str) -> list[list[int]]:
    with open(path) as fh:
        return [[*map(int, line.strip())] for line in fh]


def fix(arr: np.array) -> np.array:
    a2 = arr.copy()
    a2[a2 >= 10] -= 9
    return a2


def get_input2(path: str) -> np.array:
    N = 5
    a1 = np.array(get_input(path), dtype=np.uint8)
    a2 = np.concatenate([fix(a1 + i) for i in range(N)], axis=1)
    return np.concatenate([fix(a2 + i) for i in range(N)], axis=0)


def djikstra(input_graph: list[list[int]] | np.ndarray) -> int:
    num_rows = len(input_graph)
    num_cols = len(input_graph[0])
    source = (0, 0)
    target = (num_rows - 1, num_cols - 1)
    vertices = [(r, c) for r, c in itertools.product(range(num_rows), range(num_cols))]
    distances = {v: sys.maxsize for v in vertices}
    distances[source] = 0
    visited = {v: False for v in vertices}

    # https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    # Quick and dirty implementation from stdlib
    pq = []  # list of entries arranged in a heap
    entry_finder = {}  # mapping of tasks to entries
    REMOVED = '<removed-task>'  # placeholder for a removed task
    counter = itertools.count()  # unique sequence count

    def add_task(task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in entry_finder:
            remove_task(task)
        count = next(counter)
        entry = [priority, count, task]
        entry_finder[task] = entry
        heapq.heappush(pq, entry)

    def remove_task(task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = entry_finder.pop(task)
        entry[-1] = REMOVED

    def pop_task():
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while pq:
            priority, count, task = heapq.heappop(pq)
            if task is not REMOVED:
                del entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    for v in vertices:
        add_task(v, 0 if v == source else sys.maxsize)

    while pq:
        vertex = pop_task()
        if vertex == target:
            break
        visited[vertex] = True
        a, b = vertex
        for neighbor in [(a + 1, b), (a, b + 1), (a - 1, b), (a, b - 1)]:
            if not 0 <= neighbor[0] < num_rows:
                continue
            if not 0 <= neighbor[1] < num_cols:
                continue
            alt = distances[vertex] + input_graph[neighbor[0]][neighbor[1]]
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                add_task(neighbor, alt)
    return distances[num_rows - 1, num_cols - 1]


assert djikstra(get_input("ex.txt")) == 40
print(djikstra(get_input("input.txt")))

assert djikstra(get_input2("ex.txt")) == 315
print(djikstra(get_input2("input.txt")))
