def num_unique(filepath: str) -> int:
    with open(filepath) as fh:
        lines = fh.readlines()

    output_signals = [line.split(" | ")[1] for line in lines]
    output_words = [s.split() for s in output_signals]
    return sum(len(word) in {2, 3, 4, 7} for word_group in output_words for word in word_group)


Encoded = set[str]


class Decoder:
    """Stateful decode of encoded digits"""

    def __init__(self, inputs: list[Encoded]) -> None:
        self.inputs = inputs
        self._decoded: dict[int, Encoded] = {}
        self._deduce()

    def _deduce(self):
        # deduce segment A - difference between 3-segment digit (7) and 2-segment digit (1)
        d = self._decoded

        d[1] = self._assert_one(self._inputs_of_len(2))
        d[4] = self._assert_one(self._inputs_of_len(4))
        d[7] = self._assert_one(self._inputs_of_len(3))
        d[8] = self._assert_one(self._inputs_of_len(7))

        bd = set(d[4]) - set(d[1])
        cf = set(d[1])

        d[5] = self._assert_one([i for i in self._inputs_of_len(5) if bd <= i])
        d[3] = self._assert_one([i for i in self._inputs_of_len(5) if i != d[5] and cf <= i])
        d[2] = self._assert_one([i for i in self._inputs_of_len(5) if i != d[5] and i != d[3]])

        d[9] = self._assert_one([i for i in self._inputs_of_len(6) if bd <= i and cf < i])
        d[0] = self._assert_one([i for i in self._inputs_of_len(6) if i != d[9] and cf < i])
        d[6] = self._assert_one([i for i in self._inputs_of_len(6) if i != d[9] and i != d[0]])

    def _inputs_of_len(self, n: int) -> list[Encoded]:
        return [i for i in self.inputs if len(i) == n]

    @staticmethod
    def _assert_one(v: list[Encoded]) -> Encoded:
        assert len(v) == 1
        return v[0]

    def decode(self, encoded: str) -> int:
        return next(k for k, v in self._decoded.items() if set(encoded) == v)


def solve_p2(filepath: str) -> int:
    summary = 0
    with open(filepath) as fh:
        for line in fh:
            input_str, output_str = line.split(" | ")
            inputs = [set(word) for word in input_str.split()]
            outputs = output_str.split()
            decoder = Decoder(inputs)
            summary += int(''.join(str(decoder.decode(out)) for out in outputs))
    return summary


assert 26 == num_unique("ex.txt")
print(num_unique("input.txt"))

assert 61229 == solve_p2("ex.txt")
print(solve_p2("input.txt"))
