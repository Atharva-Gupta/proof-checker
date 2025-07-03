import pytest
from src.core.proof import Proof, Sequent, InferenceRule
from src.parsing.propositional_parser import parse_string
from src.core.sentence import Atomic, TwoSided, Operator, Negation, True_Sym, False_Sym

def test_1():
    assert parse_string(r"(A) \and (B)") == TwoSided(Atomic("A"), Atomic("B"), Operator.AND)

def test_2():
    assert parse_string(r"(\not A) \and (B)") == TwoSided(Negation(Atomic("A")), Atomic("B"), Operator.AND)

def test_3():
    assert parse_string(r"((A \and B))") == TwoSided(Atomic("A"), Atomic("B"), Operator.AND)

def test_4():
    assert parse_string(r"\true \and B") == TwoSided(True_Sym(), Atomic("B"), Operator.AND)

def test_5():
    assert parse_string(r"\true \and B") == TwoSided(True_Sym(), Atomic("B"), Operator.AND)

def test_6():
    assert parse_string(r"((((\not \false) \and B)))") == TwoSided(Negation(False_Sym()), Atomic("B"), Operator.AND)

def test_7():
    assert parse_string(r"(((((A)))))") == Atomic("A")

def test_8():
    assert parse_string(r"(((\not ((A)))))") == Negation(Atomic("A"))

def test_9():
    assert parse_string(r"(((\not ((A) \implies B))))") == Negation(TwoSided(Atomic("A"), Atomic("B"), Operator.IMPLIES))

def test_10():
    assert not parse_string(r"")

def test_11():
    assert not parse_string(r"()")