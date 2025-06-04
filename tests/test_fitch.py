import pytest
from proof import Proof, Sequent, InferenceRule, Gamma
from sentence import Negation
from propositional_parser import parse_string
from fitch_style import FitchSubProof

def test_1():
    g1 = parse_string(r"A \or B ")
    g2 = parse_string(r"A \implies C")
    g3 = parse_string(r"(B \implies C)")

    fi = FitchSubProof()
    assert fi.add_assumption(g1)
    assert fi.add_assumption(g2)
    assert fi.add_assumption(g3)

    inner_1 = fi.add_subproof()
    assert inner_1.add_assumption(parse_string(r"A"))
    assert inner_1.add_conclusion(parse_string(r"C"), InferenceRule.implies_elim)

    inner_2 = fi.add_subproof()
    assert inner_2.add_assumption(parse_string(r"B"))
    assert inner_2.add_conclusion(parse_string(r"C"), InferenceRule.implies_elim)

    print(fi.pr)

    assert fi.add_conclusion(parse_string(r"C"), InferenceRule.or_elim)

def test_2():
    g1 = parse_string(r"A")
    g2 = parse_string(r"B \implies (\not A)")
    g3 = parse_string(r"B")

    c = parse_string(r"\not A")
    d = parse_string(r"\false")

    fi = FitchSubProof()

    assert fi.add_assumption(g1)
    assert fi.add_assumption(g2)
    assert fi.add_assumption(g3)

    assert fi.add_conclusion(c, InferenceRule.implies_elim)
    assert fi.add_conclusion(d, InferenceRule.not_elim)

def test_3():
    g1 = parse_string(r"A \and (B \and C)")

    c1 = parse_string(r"A")
    c2 = parse_string(r"(B \and C)")
    c3 = parse_string(r"B")
    c4 = parse_string(r"C")
    c5 = parse_string(r"(A \and B)")

    c = parse_string(r"(A \and B) \and C")

    fi = FitchSubProof()
    assert fi.add_assumption(g1)

    assert fi.add_conclusion(c1, InferenceRule.and_elim)
    assert fi.add_conclusion(c2, InferenceRule.and_elim)
    assert fi.add_conclusion(c3, InferenceRule.and_elim)
    assert fi.add_conclusion(c4, InferenceRule.and_elim)

    assert fi.add_conclusion(c5, InferenceRule.and_intro)
    assert fi.add_conclusion(c, InferenceRule.and_intro)

def test_5():
    g1 = parse_string(r"R")

    as1 = parse_string(r"L")
    c1 = parse_string(r"L \and R")

    c = parse_string(r"L \implies (L \and R)")

    fi = FitchSubProof()
    fi.add_assumption(g1)

    inner1 = fi.add_subproof()
    inner1.add_assumption(as1)
    inner1.add_conclusion(c1, InferenceRule.and_intro)

    fi.add_conclusion(c, InferenceRule.implies_intro)
