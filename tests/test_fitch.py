import pytest
from src.core.proof import Proof, Sequent, InferenceRule, Gamma
from src.core.sentence import Negation
from src.parsing.propositional_parser import parse_string
from src.core.fitch_style import FitchSubProof

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

def test_4():
    g1 = parse_string(r"R")

    as1 = parse_string(r"L")
    c1 = parse_string(r"L \and R")

    c = parse_string(r"L \implies (L \and R)")

    fi = FitchSubProof()
    assert fi.add_assumption(g1)

    inner1 = fi.add_subproof()
    assert inner1.add_assumption(as1)
    assert inner1.add_conclusion(c1, InferenceRule.and_intro)

    assert fi.add_conclusion(c, InferenceRule.implies_intro)

def test_5():
    g1 = parse_string(r"P \implies Q")
    g2 = parse_string(r"Q \implies R")

    as1 = parse_string("P")

    c1 = parse_string("Q")
    c2 = parse_string("R")

    c3 = parse_string(r"P \implies R")

    fs = FitchSubProof()
    assert fs.add_assumption(g1)
    assert fs.add_assumption(g2)

    inner1 = fs.add_subproof()
    assert inner1.add_assumption(as1)
    assert inner1.add_conclusion(c1, InferenceRule.implies_elim)
    assert inner1.add_conclusion(c2, InferenceRule.implies_elim)

    assert fs.add_conclusion(c3, InferenceRule.implies_intro)

def test_6():
    g1 = parse_string(r"A")

    as1 = parse_string(r"B")

    c1 = parse_string(r"B")
    c2 = parse_string(r"B \implies B")
    c = parse_string(r"B")

    fs = FitchSubProof()

    assert fs.add_assumption(g1)

    inner1 = fs.add_subproof()
    assert inner1.add_assumption(as1)
    assert inner1.add_conclusion(c1, InferenceRule.axiom)
    assert fs.add_conclusion(c2, InferenceRule.implies_intro)

    assert not fs.add_conclusion(c, InferenceRule.implies_elim)

def test_7():
    g1 = parse_string(r"A \and (B \or C)")

    c1 = parse_string(r"B \or C")

    as1 = parse_string(r"B")
    c2 = parse_string(r"A \and (B \or C)")
    c3 = parse_string(r"A")
    c4 = parse_string(r"(A \and B)")
    c5 = parse_string(r"(A \and B) \or (A \and C)")

    as2 = parse_string(r"C")
    c6 = parse_string(r"A \and (B \or C)")
    c7 = parse_string(r"A")
    c8 = parse_string(r"A \and C")
    c9 = parse_string(r"(A \and B) \or (A \and C)")

    c = parse_string(r"(A \and B) \or (A \and C)")

    fs = FitchSubProof()

    assert fs.add_assumption(g1)
    assert fs.add_conclusion(c1, InferenceRule.and_elim)

    inner1 = fs.add_subproof()
    assert inner1.add_assumption(as1)
    assert inner1.add_conclusion(c3, InferenceRule.and_elim)
    assert inner1.add_conclusion(c4, InferenceRule.and_intro)
    assert inner1.add_conclusion(c5, InferenceRule.or_intro)

    inner2 = fs.add_subproof()
    assert inner2.add_assumption(as2)
    assert inner2.add_conclusion(c7, InferenceRule.and_elim)
    assert inner2.add_conclusion(c8, InferenceRule.and_intro)
    assert inner2.add_conclusion(c9, InferenceRule.or_intro)

    assert fs.add_conclusion(c, InferenceRule.or_elim)

def test_8():
    g1 = parse_string(r"J \or L")
    g2 = parse_string(r"\not L")

    as1 = parse_string(r"J")
    as2 = parse_string(r"L")

    c1 = parse_string(r"\false")

    fs = FitchSubProof()
    fs.add_assumption(g1)
    fs.add_assumption(g2)

    inner1 = fs.add_subproof()
    assert inner1.add_assumption(as1)
    assert inner1.add_conclusion(as1, InferenceRule.axiom)

    inner2 = fs.add_subproof()
    assert inner2.add_assumption(as2)
    assert inner2.add_conclusion(c1, InferenceRule.not_elim)
    assert inner2.add_conclusion(as1, InferenceRule.false_elim)

    assert fs.add_conclusion(as1, InferenceRule.or_elim)

def test_9():
    as1 = parse_string(r"\not (A \or (\not A))")
    as2 = parse_string(r"A")

    c1 = parse_string(r"A \or (\not A)")
    c2 = parse_string(r"\false")

    c3 = parse_string(r"\not A")
    c4 = parse_string(r"A \or (\not A)")
    c5 = parse_string(r"\false")

    c6 = parse_string(r"A \or (\not A)")

    fs = FitchSubProof()

    inner1 = fs.add_subproof()
    assert inner1.add_assumption(as1)

    inner2 = inner1.add_subproof()
    assert inner2.add_assumption(as2)
    assert inner2.add_conclusion(c1, InferenceRule.or_intro)
    assert inner2.add_conclusion(c2, InferenceRule.not_elim)

    assert inner1.add_conclusion(c3, InferenceRule.not_intro)
    assert inner1.add_conclusion(c4, InferenceRule.or_intro)
    assert inner1.add_conclusion(c5, InferenceRule.not_elim)

    assert fs.add_conclusion(c6, InferenceRule.contra)

def test_10():
    g1 = parse_string(r"B")
    g2 = parse_string(r"\not A")

    fs = FitchSubProof()
    assert fs.add_assumption(g1)

    inner1 = fs.add_subproof()
    assert inner1.add_assumption(g2)
    assert inner1.add_conclusion(g1, InferenceRule.expand)