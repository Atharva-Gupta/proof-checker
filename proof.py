from sentence import TwoSided, Atomic, Negation, Sentence, True_Sym, False_Sym
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
    true_intro = "TI"
    false_elim = "FE"

    contra = "IP"

class Sequent:
    gamma: List[Sentence]
    conclusion: Sentence
    rule: InferenceRule
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

    def check_sequent(self, potential: Sequent):
        if potential.rule == InferenceRule.axiom:
            for sentence in potential.gamma:
                if sentence == potential.conclusion:
                    return True
            return False

        elif potential.rule == InferenceRule.and_intro:
            assert isinstance(potential.conclusion, TwoSided) and potential.conclusion.oper == Operator.AND
            if self.proof_exists(potential.gamma, potential.conclusion.left) and self.proof_exists(potential.gamma, potential.conclusion.right):
                return True
            return False

        elif potential.rule == InferenceRule.and_elim:
            for seq in self.sequents:
                if isinstance(seq.conclusion, TwoSided) and seq.conclusion.oper == Operator.AND:
                    if self.gamma_equal(seq.gamma, potential.gamma):
                        if seq.conclusion.right == potential.conclusion or seq.conclusion.left == potential.conclusion:
                            return True
            return False

        elif potential.rule == InferenceRule.or_intro:
            assert isinstance(potential.conclusion, TwoSided) and potential.conclusion.oper == Operator.OR
            if self.proof_exists(potential.gamma, potential.conclusion.left) or self.proof_exists(potential.gamma, potential.conclusion.right):
                return True
            return False

        elif potential.rule == InferenceRule.or_elim:
            phi_psi_options = []
            for seq in self.sequents:
                if self.gamma_equal(seq.gamma, potential.gamma):
                    if isinstance(seq.conclusion, TwoSided) and seq.conclusion.oper == Operator.OR:
                        phi_psi_options.append(seq.conclusion)

            for option in phi_psi_options:
                gamma_prime_one = potential.gamma + [option.left]
                gamma_prime_two = potential.gamma + [option.right]

                if self.proof_exists(gamma_prime_one, potential.conclusion) and self.proof_exists(gamma_prime_two, potential.conclusion):
                    return True
            return False

        elif potential.rule == InferenceRule.implies_intro:
            assert isinstance(potential.conclusion, TwoSided) and potential.conclusion.oper == Operator.IMPLIES
            gamma_prime = potential.gamma + [potential.conclusion.left]
            if self.proof_exists(gamma_prime, potential.conclusion.right):
                return True
            return False

        elif potential.rule == InferenceRule.implies_elim:
            for seq in self.sequents:
                if isinstance(seq.conclusion, TwoSided) and seq.conclusion.oper == Operator.IMPLIES:
                    if self.gamma_equal(seq.gamma, potential.gamma):
                        if seq.conclusion.right == potential.conclusion and self.proof_exists(seq.gamma, seq.conclusion.left):
                            return True

            return False

        elif potential.rule == InferenceRule.not_intro:
            assert isinstance(potential.conclusion, Negation) and potential.conclusion.oper == Operator.NOT
            gamma_prime = potential.gamma + [potential.conclusion.inner]
            if self.proof_exists(gamma_prime, False_Sym):
                return True
            return False

        elif potential.rule == InferenceRule.not_elim:
            assert isinstance(potential.conclusion, False_Sym)
            for seq in self.sequents:
                if self.gamma_equal(seq.gamma, potential.gamma) and self.proof_exists(seq.gamma, Negation(seq.conclusion)):
                    return True

            return False

        elif potential.rule == InferenceRule.true_intro:
            return True

        elif potential.rule == InferenceRule.false_elim:
            assert potential.conclusion == False_Sym()
            if self.proof_exists(potential.gamma, False_Sym()):
                return True
            return False

        elif potential.rule == InferenceRule.contra:
            gamma_prime = potential.gamma + [Negation(potential.conclusion)]
            if self.proof_exists(gamma_prime, False_Sym()):
                return True
            return False

        else:
            raise ValueError(f"Rule of inference {potential.rule} not supported!")

        return False


def main():
    g1 = parse_string(r"A \or B")
    g2 = parse_string(r"A \implies C")
    g3 = parse_string(r"B \implies C")
    gamma = [g1, g2, g3]

    as1 = parse_string(r"A")
    as2 = parse_string(r"B")

    c = parse_string(r"C")

    pr = Proof()
    print(pr.add_sequent(Sequent(gamma, g1, InferenceRule.axiom)))
    print(pr.add_sequent(Sequent(gamma, g2, InferenceRule.axiom)))
    print(pr.add_sequent(Sequent(gamma, g3, InferenceRule.axiom)))
    print(pr.add_sequent(Sequent(gamma + [as1], as1, InferenceRule.axiom)))
    print(pr.add_sequent(Sequent(gamma + [as1], g2, InferenceRule.axiom)))
    print(pr.add_sequent(Sequent(gamma + [as1], c, InferenceRule.implies_elim)))

    print(pr.add_sequent(Sequent(gamma + [as2], as2, InferenceRule.axiom)))
    print(pr.add_sequent(Sequent(gamma + [as2], g3, InferenceRule.axiom)))
    print(pr.add_sequent(Sequent(gamma + [as2], c, InferenceRule.implies_elim)))

    print(pr.add_sequent(Sequent(gamma, c, InferenceRule.or_elim)))

    # g1 = parse_string(r"A")
    # g2 = parse_string(r"B \implies (\not A)")
    # g3 = parse_string(r"B")

    # c = parse_string(r"\not A")
    # d = parse_string(r"\false")

    # gamma = [g1, g2, g3]
    # pr = Proof()
    # print(pr.add_sequent(Sequent(gamma, g1, InferenceRule.axiom)))
    # print(pr.add_sequent(Sequent(gamma, g2, InferenceRule.axiom)))
    # print(pr.add_sequent(Sequent(gamma, g3, InferenceRule.axiom)))
    # print(pr.add_sequent(Sequent(gamma, c, InferenceRule.implies_elim)))
    # print(pr.add_sequent(Sequent(gamma, d, InferenceRule.not_elim)))


if __name__ == "__main__":
    main()
