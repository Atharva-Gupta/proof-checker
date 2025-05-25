import pytest
from proof import Proof, Sequent, InferenceRule
from propositional_parser import parse_string
from sentence import Atomic, TwoSided, Operator, Negation

def test_1():
    assert parse_string(r"(A) \and (B)") == TwoSided(Atomic("A"), Atomic("B"), Operator.AND)

def test_2():
    assert parse_string(r"(\not A) \and (B)") == TwoSided(Negation(Atomic("A")), Atomic("B"), Operator.AND)