import pytest
from proof import Proof, Sequent, InferenceRule, Gamma
from sentence import Negation
from propositional_parser import parse_string
from fitch_style import FitchSubProof

def test_0():
    gamma = Gamma()
    gamma += [parse_string("A")]
    assert gamma

def test_1():
    g1 = parse_string(r"A ")
    g2 = parse_string(r"A \implies C")
    g3 = parse_string(r"C")

    fi = FitchSubProof()
    assert fi.add_assumption(g1)
    assert fi.add_assumption(g2)

    assert fi.add_conclusion(g3, InferenceRule.implies_elim)

def test_2():
    g1 = parse_string(r"B ")
    g2 = parse_string(r"A \implies C")
    g3 = parse_string(r"B \and (A \implies C)")

    fi = FitchSubProof()
    assert fi.add_assumption(g1)
    assert fi.add_assumption(g2)

    assert fi.add_conclusion(g3, InferenceRule.and_intro)

def test_3():
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