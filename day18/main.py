import ast
import copy
import functools
import itertools


def add(s1, s2):
    result = [s1, s2]
    result = reduce(result)
    return result


def summarize(numbers):
    return functools.reduce(add, numbers)


# def explode(snailfish):
#     s0 = copy.deepcopy(snailfish)
#
#     leftmost_owner = None
#     rightmost_owner = None
#     nested_owner = None
#     nested_index = -1
#     s = s0
#
#     for _ in range(4):
#         first, second = s
#         if isinstance(first, list):
#             if isinstance(second, int):
#                 rightmost_owner = s
#
#             nested_owner = s
#             nested_index = 0
#             s = first
#             continue
#         if isinstance(second, list):
#             if isinstance(first, int):
#                 leftmost_owner = s
#
#             nested_owner = s
#             nested_index = 1
#             s = second
#             continue
#         else:
#             break
#     else:
#         print(s, nested_owner, nested_index, leftmost_owner, rightmost_owner)
#         # new_left = (0 if leftmost_owner is None else leftmost_value) + nested_owner[nested_index][0]
#         # new_right = (0 if rightmost_owner is None else rightmost_value) + nested_owner[nested_index][1]
#         if leftmost_owner:
#             leftmost_owner[0] += nested_owner[nested_index][0]
#         if rightmost_owner:
#             rightmost_owner[1] += nested_owner[nested_index][1]
#         nested_owner[nested_index] = 0
#         print(s0)
#     return s0
#
#
# def _find_leftmost_owner(s, parent=None):
#     if isinstance(s, list):
#         return _find_leftmost_owner(s[1], s)
#     else:
#         assert parent is not None
#         return s, parent
#
#
# def _find_rightmost_owner(s, parent=None):
#     if isinstance(s, list):
#         return _find_rightmost_owner(s[0], s)
#     else:
#         assert parent is not None
#         return s, parent
#


def explode(snailfish):
    """Explode using recursion"""
    exploded, modified, leftpad, rightpad = _explode(snailfish, 4)
    # print(snailfish, exploded, leftpad, rightpad)
    # # Compensate for non-recursive "closest" value
    # if modified == 0 and rightpad:
    #     parent = exploded
    #     value = exploded[1]
    #     while isinstance(value, list):
    #         parent = value
    #         value = value[0]
    #     parent[0] += rightpad
    # elif modified == 1 and leftpad:
    #     parent = exploded
    #     value = exploded[0]
    #     while isinstance(value, list):
    #         parent = value
    #         value = value[1]
    #     parent[1] += leftpad
    return exploded


def _explode(snailfish, n):
    """Recursion internals"""
    s = copy.deepcopy(snailfish)
    if n == 0:
        assert isinstance(s[0], int) and isinstance(s[1], int)
        return 0, None, s[0], s[1]
    else:
        if isinstance(s[0], list):
            exploded, modified, leftpad, rightpad = _explode(s[0], n - 1)
            if exploded != s[0]:
                s[0] = exploded
                if isinstance(s[1], int):
                    s[1] += rightpad
                    rightpad = 0
                else:
                    # traverse to rightmost and apply
                    parent = s
                    value = s[1]
                    while isinstance(value, list):
                        parent = value
                        value = value[0]
                    parent[0] += rightpad
                    rightpad = 0
                return s, 0, leftpad, rightpad
        if isinstance(s[1], list):
            exploded, modified, leftpad, rightpad = _explode(s[1], n - 1)
            if exploded != s[1]:
                s[1] = exploded
                if isinstance(s[0], int):
                    s[0] += leftpad
                    leftpad = 0
                else:
                    # traverse to leftmost and apply
                    parent = s
                    value = s[0]
                    while isinstance(value, list):
                        parent = value
                        value = value[1]
                    parent[1] += leftpad
                    leftpad = 0
                return s, 1, leftpad, rightpad

    return s, None, 0, 0


assert explode([[[[[9, 8], 1], 2], 3], 4]) == [[[[0, 9], 2], 3], 4]
assert explode([7, [6, [5, [4, [3, 2]]]]]) == [7, [6, [5, [7, 0]]]]
assert explode([[6, [5, [4, [3, 2]]]], 1]) == [[6, [5, [7, 0]]], 3]
assert explode([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]) == [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
assert explode([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]) == [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]


def split(snailfish):
    s = copy.deepcopy(snailfish)
    first, second = s
    if isinstance(first, list):
        s0_split = split(first)
        if s0_split != s[0]:
            s[0] = s0_split
            return s
    elif first >= 10:
        new = [first // 2, first // 2 + (first % 2)]
        s[0] = new
        return s
    if isinstance(second, list):
        s1_split = split(second)
        if s1_split != s[1]:
            s[1] = s1_split
            return s
    elif second >= 10:
        new = [second // 2, second // 2 + (second % 2)]
        s[1] = new
        return s
    return s


assert split([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]) == [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]


def reduce(snailfish):
    s = snailfish
    while True:
        s0 = s
        s = explode(s0)
        if s != s0:
            continue
        s = split(s0)
        if s != s0:
            continue
        # reduction is done
        return s


assert reduce([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]


def magnitude(snailfish):
    if isinstance(snailfish, int):
        return snailfish
    return 3 * magnitude(snailfish[0]) + 2 * magnitude(snailfish[1])


assert magnitude([9, 1]) == 29
assert magnitude([1, 9]) == 21
assert magnitude([[1, 2], [[3, 4], 5]]) == 143
assert magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]) == 3488


def get_input(path: str):
    with open(path) as fh:
        return [ast.literal_eval(line) for line in fh]


def solve(numbers):
    return magnitude(summarize(numbers))


def solve2(numbers):
    solution = -1
    for s1, s2 in itertools.combinations(numbers, 2):
        mag = magnitude(add(s1, s2))
        if mag > solution:
            solution = mag
        mag = magnitude(add(s2, s1))
        if mag > solution:
            solution = mag
    return solution


assert summarize([[1, 1], [2, 2], [3, 3], [4, 4]]) == [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]
assert summarize([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]) == [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]
assert summarize([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]) == [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]

assert summarize(get_input("ex.txt")) == [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]

print(solve(get_input("input.txt")))
print(solve2(get_input("input.txt")))
