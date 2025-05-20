from abc import ABC
from enum import Enum
from typing import Iterable

from errors import VariableNotAssignedError

class Sentence(ABC):
    def evaluate(self, variable_assignment: dict) -> bool:
        raise NotImplementedError()

    def get_atomics(self) -> Iterable:
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

class Operator(Enum):
    OR = "OR"
    AND = "AND"
    IMPLIES = "IMPLIES"
    NOT = "NOT"

class Atomic(Sentence):
    name: str
    def __init__(self, name: str):
        self.name = name

    def evaluate(self, variable_assignment: dict) -> bool:
        try:
            return variable_assignment[self.name]
        except KeyError as e:
            raise VariableNotAssignedError(f"Variable {self.name} not found in variable assignment!") from None

    def get_atomics(self) -> Iterable:
        s = set()
        s.add(self.name)
        return s

    def __str__(self):
        return self.name

class Negation(Sentence):
    inner: Sentence
    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def evaluate(self, variable_assignment) -> bool:
        return not self.inner.evaluate(variable_assignment)

    def get_atomics(self) -> Iterable:
        return self.inner.get_atomics()

    def __str__(self):
        return f"({Operator.NOT.value} {self.inner})"

class TwoSided(Sentence):
    left: Sentence
    right: Sentence
    oper: Operator
    def __init__(self, left, right, oper):
        super().__init__()
        self.oper = oper
        self.left = left
        self.right = right

    def get_atomics(self):
        return self.left.get_atomics() | self.right.get_atomics()

    def evaluate(self, variable_assignment):
        if self.oper == Operator.AND:
            return self.left.evaluate(variable_assignment) and self.right.evaluate(variable_assignment)
        if self.oper == Operator.OR:
            return self.left.evaluate(variable_assignment) or self.right.evaluate(variable_assignment)
        if self.oper == Operator.IMPLIES:
            return (not self.left.evaluate(variable_assignment)) or self.right.evaluate(variable_assignment)
        else:
            raise NotImplementedError()

    def __str__(self):
        return "(" + self.left.__str__() + " " + self.oper.value + " " + self.right.__str__() + ")"