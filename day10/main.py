import functools

OPEN_BRACKETS = frozenset("([{<")
CLOSE_BRACKETS = frozenset(")]}>")
MAP = {"(": ")", "[": "]", "{": "}", "<": ">"}


def find_first_incorrect(line: str) -> tuple[int, str]:
    stack = []
    for index, char in enumerate(line.strip()):
        if char in OPEN_BRACKETS:
            stack.append(char)
        elif char in CLOSE_BRACKETS:
            open_bracket = stack.pop()
            expected_closing_bracket = MAP[open_bracket]
            found_closing_bracket = char
            if found_closing_bracket != expected_closing_bracket:
                return index, found_closing_bracket
        else:
            raise NotImplementedError(char)
    # incomplete, but not corrupted
    return -1, ""


def autocomplete(line: str) -> str | None:
    stack = []
    for index, char in enumerate(line.strip()):
        if char in OPEN_BRACKETS:
            stack.append(char)
        elif char in CLOSE_BRACKETS:
            open_bracket = stack.pop()
            expected_closing_bracket = MAP[open_bracket]
            found_closing_bracket = char
            if found_closing_bracket != expected_closing_bracket:
                # To be discarded
                return None
        else:
            raise NotImplementedError(char)

    return ''.join(MAP[open_bracket] for open_bracket in reversed(stack))


def score_autocomplete(complete: str) -> int:
    scores = {")": 1, "]": 2, "}": 3, ">": 4}

    def consume_score(s: int, char: str) -> int:
        return 5 * s + scores[char]

    return functools.reduce(consume_score, complete, 0)


def solve_p1(path: str) -> int:
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137, "": 0}
    with open(path) as fh:
        return sum(
            scores[find_first_incorrect(line)[1]]
            for line in fh
        )


def solve_p2(path: str) -> int:
    scores: list[int] = []
    with open(path) as fh:
        for line in fh:
            ac = autocomplete(line)
            if ac is None:
                continue
            score = score_autocomplete(ac)
            scores.append(score)
    scores.sort()
    middle_index = len(scores) // 2
    return scores[middle_index]


assert find_first_incorrect("{([(<{}[<>[]}>{[]{[(<()>") == (12, "}")
assert solve_p1("ex.txt") == 26397
print(solve_p1("input.txt"))
assert autocomplete("[({(<(())[]>[[{[]{<()<>>") == "}}]])})]"
assert score_autocomplete("}}]])})]") == 288957
assert solve_p2("ex.txt") == 288957
print(solve_p2("input.txt"))
