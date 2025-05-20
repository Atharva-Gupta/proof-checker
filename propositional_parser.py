from abc import ABC
from enum import Enum

class ParseError(Exception):
    pass

class Sentence(ABC):
    def evaluate(self, variable_assignment: dict):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

class Operator(Enum):
    OR = "OR"
    AND = "AND"
    IMPLIES = "IMPLIES"
    NOT = "NOT"

class Atomic(Sentence):
    def __init__(self, name):
        self.name = name

    def evaluate(self, variable_assignment: dict):
        return variable_assignment[self.name]

    def __str__(self):
        return self.name

class Negation(Sentence):
    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def __str__(self):
        return f"({Operator.NOT.value} {self.inner})"

    def evaluate(self, variable_assignment):
        return not self.inner.evaluate(variable_assignment)

class TwoSided(Sentence):
    def __init__(self, left, right, oper):
        super().__init__()
        self.oper = oper
        self.left = left
        self.right = right

    def __str__(self):
        return "(" + self.left.__str__() + " " + self.oper.value + " " + self.right.__str__() + ")"

    def evaluate(self, variable_assignment):
        if self.oper == Operator.AND:
            return self.left.evaluate(variable_assignment) and self.right.evaluate(variable_assignment)
        if self.oper == Operator.OR:
            return self.left.evaluate(variable_assignment) or self.right.evaluate(variable_assignment)
        if self.oper == Operator.IMPLIES:
            return (not self.left.evaluate(variable_assignment)) or self.right.evaluate(variable_assignment)
        else:
            raise NotImplementedError()

def parse_string(s):
    s = s.strip()
    if s[0] == "(":
        if s[-1] == ")":
            s = s[1:-1]
        else:
            raise ParseError("Last character must be a closing parentheses!")

    if len(s) == 1 and s[0] not in "\(":
        return Atomic(s[0])

    if s[0] == "\\":
        if s[:4] != r"\not":
            raise ParseError("Only not operand is unary!")

        return Negation(parse_string(s[4:]))

    count = 0
    ind = 0
    split = [""]
    while ind < len(s):
        char = s[ind]

        if char == "(":
            count += 1
        elif char == ")":
            count -= 1

        if count == 0 and char == "\\":
            split.append("")

        if len(split) == 2 and char == " ":
            split.append("")

        split[-1] += char

        ind += 1

    split[1] = split[1].strip()

    str_to_oper = {r"\or": Operator.OR, r"\and": Operator.AND, r"\implies": Operator.IMPLIES}

    return TwoSided(parse_string(split[0]), parse_string(split[2]), str_to_oper[split[1]])

def main():
    s = r"((B) \implies B)"
    print(parse_string(r"((\not B) \implies B)"))
    # print(parse_string(r"((\and B) \or B)"))
    # print(parse_string(r"((\and B) \implies B)"))

    variable_assgn = {"B": False}

    print(parse_string(s).evaluate(variable_assgn))

if __name__ == "__main__":
    main()
