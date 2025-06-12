from abc import ABC
from enum import Enum
from typing import List, Iterable, MutableSequence
from copy import deepcopy
from .errors import VariableNotAssignedError

class Sentence(ABC):
    def evaluate(self, variable_assignment: dict) -> bool:
        raise NotImplementedError()

    def get_atomics(self) -> Iterable:
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def __eq__(self, value):
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

    def __eq__(self, value):
        if not isinstance(value, Atomic):
            return False
        return self.name == value.name

    def __str__(self):
        return self.name


class True_Sym(Atomic):
    def __init__(self):
        super().__init__("TRUE")

    def evaluate(self, variable_assignment):
        return True

    def __eq__(self, value):
        return isinstance(value, True_Sym)


class False_Sym(Atomic):
    def __init__(self):
        super().__init__("FALSE")

    def evaluate(self, variable_assignment):
        return False

    def __eq__(self, value):
        return isinstance(value, False_Sym)


class Negation(Sentence):
    inner: Sentence
    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def evaluate(self, variable_assignment) -> bool:
        return not self.inner.evaluate(variable_assignment)

    def get_atomics(self) -> Iterable:
        return self.inner.get_atomics()

    def __eq__(self, value):
        if not isinstance(value, Negation):
            return False
        return self.inner.__eq__(value.inner)

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

    def __eq__(self, value):
        if not isinstance(value, TwoSided):
            return False

        if self.oper != value.oper:
            return False

        return self.left.__eq__(value.left) and self.right.__eq__(value.right)

    def __str__(self):
        return "(" + self.left.__str__() + " " + self.oper.value + " " + self.right.__str__() + ")"


class Gamma(MutableSequence):
    _items: List[Sentence]
    def __init__(self, *args):
        if len(args) == 0:
            self._items = []
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, Sentence):
                self._items = [arg]
            elif isinstance(arg, (list, tuple)):
                self._items = list(arg)
            else:
                pass
        else:
            self._items = list(args)

    def __getitem__(self, index) -> Sentence:
        return self._items[index]

    def __setitem__(self, index, value: Sentence):
        self._items[index] = value

    def __delitem__(self, index):
        del self._items[index]

    def __len__(self):
        return len(self._items)

    def insert(self, index, value: Sentence):
        self._items.insert(index, value)

    def __eq__(self, other_gamma):
        if not isinstance(other_gamma, Gamma):
            return False

        if len(self) != len(other_gamma):
            return False

        for sentence in self._items:
            if sentence not in other_gamma._items:
                return False

        return True

    def is_subset_of(self, other):
        for sentence in self._items:
            if sentence not in other:
                return False

        return True

    def __iadd__(self, values):
        self._items.__iadd__(values)
        return self

    def __add__(self, values):
        if isinstance(values, Gamma):
            new_items = deepcopy(self._items).__add__(deepcopy(values._items))
        elif isinstance(values, list):
            new_items = deepcopy(self._items).__add__(values)
        else:
            raise AttributeError(f"values type {type(values)} not supported!")
        return Gamma(new_items)

    def __str__(self):
        return [item.__str__() for item in self._items].__str__()