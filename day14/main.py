import collections
import functools
import re


class frozendict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def get_input(path: str) -> tuple[list[str], dict[str, str]]:
    rules: dict[str, str] = {}
    with open(path) as fh:
        template: list[str] = list(next(fh).strip())
        _ = next(fh)
        for line in fh:
            m = re.search(r"([A-Z]{2}) -> ([A-Z])", line)
            assert m is not None
            k, v = m.groups()
            rules[k] = v
    return template, rules


def epoch(template: list[str], rules: dict[str, str]) -> list:
    """Epoch - in place"""
    i1 = iter(template)
    i2 = iter(template)
    next(i2)
    inserts: dict[int, str] = {}
    for idx, (c1, c2) in enumerate(zip(i1, i2), start=1):
        inserts[idx] = rules[f"{c1}{c2}"]
    output = template.copy()
    for idx in sorted(inserts, reverse=True):
        output.insert(idx, inserts[idx])
    return output


def test_ex():
    tpl, rules = get_input("ex.txt")
    assert ''.join(epoch(tpl, rules)) == "NCNBCHB"


def solve_p1() -> int:
    tpl, rules = get_input("input.txt")
    for _ in range(10):
        tpl = epoch(tpl, rules)
    counter = collections.Counter(tpl)
    most_common = counter.most_common()
    return most_common[0][1] - most_common[-1][1]


@functools.cache
def _count(atom: tuple[str, str], rules: dict[str, str], n: int) -> collections.Counter:
    """Count single atom"""
    if n == 0:
        return collections.Counter(atom)
    c1, c2 = atom
    insert = rules[f"{c1}{c2}"]
    return _count((c1, insert), rules, n - 1) + _count((insert, c2), rules, n - 1) - collections.Counter(insert)


def count_smart(template: list[str], rules: dict[str, str], n: int) -> collections.Counter:
    i1 = iter(template)
    i2 = iter(template)
    next(i2)
    count_total = sum((_count((c1, c2), rules, n) for (c1, c2) in zip(i1, i2)), collections.Counter())
    # fix for items counted twice
    count_total -= collections.Counter(template[1:-1])
    return count_total


def solve_p2() -> int:
    tpl, rules = get_input("input.txt")
    counts = count_smart(tpl, frozendict(rules), 40)
    most_common = counts.most_common()
    return most_common[0][1] - most_common[-1][1]


def test_ex_p2():
    tpl, rules = get_input("ex.txt")
    assert count_smart(tpl, frozendict(rules), 0) == collections.Counter("NNCB")
    assert count_smart(tpl, frozendict(rules), 1) == collections.Counter("NCNBCHB")
    assert count_smart(tpl, frozendict(rules), 2) == collections.Counter("NBCCNBBBCBHCB")
    assert count_smart(tpl, frozendict(rules), 3) == collections.Counter("NBBBCNCCNBBNBNBBCHBHHBCHB")
    assert count_smart(tpl, frozendict(rules), 4) == collections.Counter(
        "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")


test_ex()
print(solve_p1())
test_ex_p2()
print(solve_p2())
