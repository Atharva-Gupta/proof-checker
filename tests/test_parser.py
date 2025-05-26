import pytest
from proof import Proof, Sequent, InferenceRule
from propositional_parser import parse_string
from sentence import Atomic, TwoSided, Operator, Negation, True_Sym, False_Sym

def test_1():
    assert parse_string(r"(A) \and (B)") == TwoSided(Atomic("A"), Atomic("B"), Operator.AND)

def test_2():
    assert parse_string(r"(\not A) \and (B)") == TwoSided(Negation(Atomic("A")), Atomic("B"), Operator.AND)

def test_3():
    assert parse_string(r"((A \and B))") == TwoSided(Atomic("A"), Atomic("B"), Operator.AND)

def test_4():
    assert parse_string(r"\true \and B") == TwoSided(True_Sym(), Atomic("B"), Operator.AND)

def test_5():
    assert parse_string(r"(\true) \and B") == TwoSided(True_Sym(), Atomic("B"), Operator.AND)

def test_6():
    assert parse_string(r"((((\not \false) \and B)))") == TwoSided(Negation(False_Sym()), Atomic("B"), Operator.AND)
