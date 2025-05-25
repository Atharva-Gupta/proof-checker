import pytest
from proof import Proof, Sequent, InferenceRule
from propositional_parser import parse_string

def test_1():
    g1 = parse_string(r"A \or B")
    g2 = parse_string(r"A \implies C")
    g3 = parse_string(r"B \implies C")
    gamma = [g1, g2, g3]

    as1 = parse_string(r"A")
    as2 = parse_string(r"B")

    c = parse_string(r"C")

    pr = Proof()
    assert (pr.add_sequent(Sequent(gamma, g1, InferenceRule.axiom)))
    assert (pr.add_sequent(Sequent(gamma, g2, InferenceRule.axiom)))
    assert (pr.add_sequent(Sequent(gamma, g3, InferenceRule.axiom)))
    assert (pr.add_sequent(Sequent(gamma + [as1], as1, InferenceRule.axiom)))
    assert (pr.add_sequent(Sequent(gamma + [as1], g2, InferenceRule.axiom)))
    assert (pr.add_sequent(Sequent(gamma + [as1], c, InferenceRule.implies_elim)))
    assert (pr.add_sequent(Sequent(gamma + [as2], as2, InferenceRule.axiom)))
    assert (pr.add_sequent(Sequent(gamma + [as2], g3, InferenceRule.axiom)))
    assert (pr.add_sequent(Sequent(gamma + [as2], c, InferenceRule.implies_elim)))
    assert (pr.add_sequent(Sequent(gamma, c, InferenceRule.or_elim)))

def test_2():
    g1 = parse_string(r"A")
    g2 = parse_string(r"B \implies (\not A)")
    g3 = parse_string(r"B")

    c = parse_string(r"\not A")
    d = parse_string(r"\false")

    gamma = [g1, g2, g3]
    pr = Proof()
    assert (pr.add_sequent(Sequent(gamma, g1, InferenceRule.axiom)))
    assert (pr.add_sequent(Sequent(gamma, g2, InferenceRule.axiom)))
    assert (pr.add_sequent(Sequent(gamma, g3, InferenceRule.axiom)))
    assert (pr.add_sequent(Sequent(gamma, c, InferenceRule.implies_elim)))
    assert (pr.add_sequent(Sequent(gamma, d, InferenceRule.not_elim)))

def test_3():
    g1 = parse_string(r"A \and (B \and C)")

    c1 = parse_string(r"A")
    c2 = parse_string(r"(B \and C)")
    c3 = parse_string(r"B")
    c4 = parse_string(r"C")
    c5 = parse_string(r"(A \and B)")

    c = parse_string(r"(A \and B) \and C")

    gamma = [g1]
    pr = Proof()
    assert pr.add_sequent(Sequent(gamma, g1, InferenceRule.axiom))

    assert pr.add_sequent(Sequent(gamma, c1, InferenceRule.and_elim))
    assert pr.add_sequent(Sequent(gamma, c2, InferenceRule.and_elim))
    assert pr.add_sequent(Sequent(gamma, c3, InferenceRule.and_elim))
    assert pr.add_sequent(Sequent(gamma, c4, InferenceRule.and_elim))
    assert pr.add_sequent(Sequent(gamma, c5, InferenceRule.and_intro))
    assert pr.add_sequent(Sequent(gamma, c, InferenceRule.and_intro))

def test_4():
    g1 = parse_string(r"R")

    as1 = parse_string(r"L")
    c1 = parse_string(r"L \and R")

    c = parse_string(r"L \implies (L \and R)")

    gamma = [g1]
    gamma_prime = [as1] + gamma

    pr = Proof()
    assert pr.add_sequent(Sequent(gamma, g1, InferenceRule.axiom))
    assert pr.add_sequent(Sequent(gamma_prime, g1, InferenceRule.axiom))
    assert pr.add_sequent(Sequent(gamma_prime, as1, InferenceRule.axiom))
    assert pr.add_sequent(Sequent(gamma_prime, c1, InferenceRule.and_intro))
    assert pr.add_sequent(Sequent(gamma, c, InferenceRule.implies_intro))

def test_5():
    g1 = parse_string(r"P \implies Q")
    g2 = parse_string(r"Q \implies R")

    as1 = parse_string("P")

    c1 = parse_string("Q")
    c2 = parse_string("R")

    c3 = parse_string(r"P \implies R")

    gamma = [g1, g2]
    gamma_prime = gamma + [as1]

    pr = Proof()
    pr.add_sequent(Sequent(gamma_prime, g1, InferenceRule.axiom))
    pr.add_sequent(Sequent(gamma_prime, g2, InferenceRule.axiom))
    pr.add_sequent(Sequent(gamma_prime, as1, InferenceRule.axiom))
    pr.add_sequent(Sequent(gamma_prime, c1, InferenceRule.implies_elim))
    pr.add_sequent(Sequent(gamma_prime, c2, InferenceRule.implies_elim))

    pr.add_sequent(Sequent(gamma, c3, InferenceRule.implies_intro))

def test_6():
    g1 = parse_string(r"A")

    as1 = parse_string(r"B")

    c1 = parse_string(r"B")
    c2 = parse_string(r"B \implies B")
    c = parse_string(r"B")

    gamma = [g1]
    gamma_prime = gamma + [as1]

    pr = Proof()
    assert pr.add_sequent(Sequent(gamma_prime, as1, InferenceRule.axiom))
    assert pr.add_sequent(Sequent(gamma, c2, InferenceRule.implies_intro))

    assert not pr.add_sequent(Sequent(gamma, c, InferenceRule.implies_elim))

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

    gamma = [g1]
    gamma_one = gamma + [as1]
    gamma_two = gamma + [as2]

    pr = Proof()
    assert pr.add_sequent(Sequent(gamma, g1, InferenceRule.axiom))
    assert pr.add_sequent(Sequent(gamma, c1, InferenceRule.and_elim))

    assert pr.add_sequent(Sequent(gamma_one, as1, InferenceRule.axiom))
    assert pr.add_sequent(Sequent(gamma_one, c2, InferenceRule.axiom))
    assert pr.add_sequent(Sequent(gamma_one, c3, InferenceRule.and_elim))
    assert pr.add_sequent(Sequent(gamma_one, c4, InferenceRule.and_intro))
    assert pr.add_sequent(Sequent(gamma_one, c5, InferenceRule.or_intro))

    assert pr.add_sequent(Sequent(gamma_two, as2, InferenceRule.axiom))
    assert pr.add_sequent(Sequent(gamma_two, c6, InferenceRule.axiom))
    assert pr.add_sequent(Sequent(gamma_two, c7, InferenceRule.and_elim))
    assert pr.add_sequent(Sequent(gamma_two, c8, InferenceRule.and_intro))
    assert pr.add_sequent(Sequent(gamma_two, c9, InferenceRule.or_intro))

    assert pr.add_sequent(Sequent(gamma, c, InferenceRule.or_elim))