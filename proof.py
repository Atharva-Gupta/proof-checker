from sentence import TwoSided, Atomic, Negation, Sentence
from sentence import Operator
from propositional_parser import parse_string
from typing import List
from enum import Enum

class InferenceRule(Enum):
    axiom = "AX"

    and_intro = "AI"
    and_elim = "AE"
    or_intro = "OI"
    or_elim = "OE"
    implies_intro = "II"
    implies_elim = "IE"
    not_intro = "NI"
    not_elim = "NE"

    contra = "IP"

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

    def check_sequent(self, possible: Sequent):
        if possible.rule == InferenceRule.axiom:
            for sentence in possible.gamma:
                if sentence == possible.conclusion:
                    return True
            return False

        elif possible.rule == InferenceRule.and_intro:
            assert isinstance(possible.conclusion, TwoSided) and possible.conclusion.oper == Operator.AND
            if self.proof_exists(possible.gamma, possible.conclusion.left) and self.proof_exists(possible.gamma, possible.conclusion.right):
                return True
            return False

        elif possible.rule == InferenceRule.and_elim:
            for seq in self.sequents:
                if isinstance(seq.conclusion, TwoSided) and seq.conclusion.oper == Operator.AND:
                    if self.gamma_equal(seq.gamma, possible.gamma):
                        if seq.conclusion.right == possible.conclusion or seq.conclusion.left == possible.conclusion:
                            return True
            return False

        elif possible.rule == InferenceRule.or_intro:
            assert isinstance(possible.conclusion, TwoSided) and possible.conclusion.oper == Operator.OR
            if self.proof_exists(possible.gamma, possible.conclusion.left) or self.proof_exists(possible.gamma, possible.conclusion.right):
                return True
            return False

        elif possible.rule == InferenceRule.or_elim:
            # I'll come back to this one (has to do with gamma + another formula)
            pass

        elif possible.rule == InferenceRule.implies_intro:
            pass

        elif possible.rule == InferenceRule.implies_elim:
            for seq in self.sequents:
                if isinstance(seq.conclusion, TwoSided) and seq.conclusion.oper == Operator.IMPLIES:
                    if self.gamma_equal(seq.gamma, possible.gamma):
                        if seq.conclusion.right == possible.conclusion and self.proof_exists(seq.gamma, seq.conclusion.left):
                            return True

            return False

        elif possible.rule == InferenceRule.not_intro:
            pass

        elif possible.rule == InferenceRule.not_elim:
            pass

        elif possible.rule == InferenceRule.contra:
            pass

        return False


def main():
    g1 = parse_string(r"A")
    g2 = parse_string(r"B \or A")
    c = parse_string(r"B")
    # c = parse_string(r"\not A")

    gamma = [g1]
    pr = Proof()
    print(pr.add_sequent(Sequent(gamma, g1, InferenceRule.axiom)))
    print(pr.add_sequent(Sequent(gamma, g2, InferenceRule.or_intro)))
    print(pr.add_sequent(Sequent(gamma, c, InferenceRule.or_elim)))


if __name__ == "__main__":
    main()
