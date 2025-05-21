from sentence import TwoSided, Atomic, Negation, Sentence
from sentence import Operator
from propositional_parser import parse_string
from typing import List
from enum import Enum

class InferenceRule(Enum):
    and_intro = "AI"
    and_elim = "AE"
    or_intro = "OI"
    or_elim = "OE"
    implies_intro = "II"
    implies_elim = "IE"
    not_intro = "NI"
    not_elim = "NE"

    contra = "IP"
    axiom = "AX"

class Sequent:
    def __init__(self, gamma: List[Sentence], conclusion: Sentence, rule: InferenceRule):
        self.gamma = gamma
        self.conclusion = conclusion
        self.rule = rule

class Proof:
    sequents: List[Sequent]
    def __init__(self):
        self.sequents = []

    def gamma_equal(self, gamma1, gamma2):
        if len(gamma1) != len(gamma2):
            return False

        for i in range(len(gamma1)):
            if gamma1[i] != gamma2[i]:
                return False

        return True

    def proof_exists(self, gamma, conclusion):
        for sequent in self.sequents:
            if self.gamma_equal(gamma, sequent.gamma) and sequent.conclusion == conclusion:
                return True

        return False

    def add_sequent(self, sequent: Sequent) -> bool:
        if self.check_sequent(sequent):
            self.sequents.append(sequent)
            return True
        else:
            return False

    def check_sequent(self, sequent: Sequent):
        if sequent.rule == InferenceRule.axiom:
            for sentence in sequent.gamma:
                if sentence == sequent.conclusion:
                    return True
            return False

        elif sequent.rule == InferenceRule.implies_elim:
            for seq in self.sequents:
                if isinstance(seq.conclusion, TwoSided) and seq.conclusion.oper == Operator.IMPLIES:
                    if self.gamma_equal(seq.gamma, sequent.gamma):
                        if seq.conclusion.right == sequent.conclusion and self.proof_exists(seq.gamma, seq.conclusion.left):
                            return True

            return False

        elif sequent.rule == InferenceRule.and_intro:
            assert isinstance(sequent.conclusion, TwoSided) and sequent.conclusion.oper == Operator.AND
            if self.proof_exists(sequent.gamma, sequent.conclusion.left) and self.proof_exists(sequent.gamma, sequent.conclusion.right):
                return True
            return False

        return False


def main():
    g1 = parse_string(r"A")
    g2 = parse_string(r"A \implies (\not A)")
    c = parse_string(r"\not A")
    # g1 = parse_string(r"(A \implies B)")
    # g2 = parse_string(r"(A)")
    # c = parse_string(r"B")

    gamma = [g1, g2]
    pr = Proof()
    pr.add_sequent(Sequent(gamma, g1, InferenceRule.axiom))
    pr.add_sequent(Sequent(gamma, g2, InferenceRule.axiom))
    print(pr.add_sequent(Sequent(gamma, c, InferenceRule.implies_elim)))


if __name__ == "__main__":
    main()
