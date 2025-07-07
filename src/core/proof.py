from .sentence import TwoSided, Atomic, Negation, Sentence, True_Sym, False_Sym
from .sentence import Operator, Gamma
from typing import List, MutableSequence
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

    expand = "EX"
    contra = "IP"


class Sequent:
    gamma: Gamma
    conclusion: Sentence
    rule: InferenceRule
    def __init__(self, gamma: Gamma, conclusion: Sentence, rule: InferenceRule):
        self.gamma = gamma
        self.conclusion = conclusion
        self.rule = rule

    def __str__(self):
        s = "["
        for sent in self.gamma[:-1]:
            s += sent.__str__() + ", "
        if self.gamma:
            s += self.gamma[-1].__str__()
        s += "] proves "
        s += self.conclusion.__str__()
        s += f" :{self.rule.value}"
        return s


class Proof:
    sequents: List[Sequent]
    def __init__(self):
        self.sequents = []

    def proof_exists(self, gamma, conclusion):
        for sequent in self.sequents:
            if gamma == sequent.gamma and sequent.conclusion == conclusion:
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
            if not isinstance(potential.conlcusion, TwoSided) or potential.conclusion.oper != Operator.AND:
                return False
            if self.proof_exists(potential.gamma, potential.conclusion.left) and self.proof_exists(potential.gamma, potential.conclusion.right):
                return True
            return False

        elif potential.rule == InferenceRule.and_elim:
            for seq in self.sequents:
                if isinstance(seq.conclusion, TwoSided) and seq.conclusion.oper == Operator.AND:
                    if seq.gamma == potential.gamma:
                        if seq.conclusion.right == potential.conclusion or seq.conclusion.left == potential.conclusion:
                            return True
            return False

        elif potential.rule == InferenceRule.or_intro:
            if not isinstance(potential.conclusion, TwoSided) or potential.conclusion.oper != Operator.OR:
                return False
            if self.proof_exists(potential.gamma, potential.conclusion.left) or self.proof_exists(potential.gamma, potential.conclusion.right):
                return True
            return False

        elif potential.rule == InferenceRule.or_elim:
            phi_psi_options = []
            for seq in self.sequents:
                if seq.gamma == potential.gamma:
                    if isinstance(seq.conclusion, TwoSided) and seq.conclusion.oper == Operator.OR:
                        phi_psi_options.append(seq.conclusion)

            for option in phi_psi_options:
                gamma_prime_one = potential.gamma + [option.left]
                gamma_prime_two = potential.gamma + [option.right]

                if self.proof_exists(gamma_prime_one, potential.conclusion) and self.proof_exists(gamma_prime_two, potential.conclusion):
                    return True
            return False

        elif potential.rule == InferenceRule.implies_intro:
            if not isinstance(potential.conclusion, TwoSided) and potential.conclusion.oper != Operator.IMPLIES:
                return False
            gamma_prime = potential.gamma + [potential.conclusion.left]
            if self.proof_exists(gamma_prime, potential.conclusion.right):
                return True
            return False

        elif potential.rule == InferenceRule.implies_elim:
            for seq in self.sequents:
                if isinstance(seq.conclusion, TwoSided) and seq.conclusion.oper == Operator.IMPLIES:
                    if seq.gamma == potential.gamma:
                        if seq.conclusion.right == potential.conclusion and self.proof_exists(seq.gamma, seq.conclusion.left):
                            return True

            return False

        elif potential.rule == InferenceRule.not_intro:
            if not isinstance(potential.conclusion, Negation):
                return False
            gamma_prime = potential.gamma + [potential.conclusion.inner]

            if self.proof_exists(gamma_prime, False_Sym()):
                return True
            return False

        elif potential.rule == InferenceRule.not_elim:
            if not isinstance(potential.conclusion, False_Sym):
                return False
            for seq in self.sequents:
                if seq.gamma == potential.gamma and self.proof_exists(seq.gamma, Negation(seq.conclusion)):
                    return True

            return False

        elif potential.rule == InferenceRule.true_intro:
            if not isinstance(potential.conclusion, True_Sym):
                return False
            return True

        elif potential.rule == InferenceRule.false_elim:
            if self.proof_exists(potential.gamma, False_Sym()):
                return True
            return False

        elif potential.rule == InferenceRule.contra:
            gamma_prime = potential.gamma + [Negation(potential.conclusion)]
            if self.proof_exists(gamma_prime, False_Sym()):
                return True
            return False

        elif potential.rule == InferenceRule.expand:
            for seq in self.sequents:
                if seq.gamma.is_subset_of(potential.gamma) and potential.conclusion == seq.conclusion:
                    return True

            return False

        else:
            raise ValueError(f"Rule of inference {potential.rule} not supported!")

    def __str__(self):
        return "Proof begins: [\n" + "\n".join([seq.__str__() for seq in self.sequents]) + "\n]"
