from copy import deepcopy

from sentence import TwoSided, Atomic, Negation, Sentence, True_Sym, False_Sym
from sentence import Operator
from propositional_parser import parse_string
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

    contra = "IP"


class Gamma(MutableSequence):
    _items: List[Sentence]
    def __init__(self, *args):
        if len(args) == 0:
            self._items = []
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, Sentence):
                self._items = [arg]
            elif isinstance(arg, (list, tuple)):
                self._items = list(arg)
            else:
                pass
        else:
            self._items = list(args)

    def __getitem__(self, index) -> Sentence:
        return self._items[index]

    def __setitem__(self, index, value: Sentence):
        self._items[index] = value

    def __delitem__(self, index):
        del self._items[index]

    def __len__(self):
        return len(self._items)

    def insert(self, index, value: Sentence):
        self._items.insert(index, value)

    def __eq__(self, other_gamma):
        if not isinstance(other_gamma, Gamma):
            return False

        if len(self) != len(other_gamma):
            return False

        for sentence in self._items:
            if sentence not in other_gamma._items:
                return False

        return True

    def __iadd__(self, values):
        self._items.__iadd__(values)
        return self

    def __add__(self, values):
        print(self._items, values)
        new_items = deepcopy(self._items).__add__(values)
        print(self)
        print([item.__str__() for item in new_items])
        print(Gamma(new_items))
        return Gamma(new_items)

    def __str__(self):
        return [item.__str__() for item in self._items].__str__()


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
        s += self.gamma[-1].__str__()
        s += "] proves "
        s += self.conclusion.__str__()
        s += f" :{self.rule.value}"
        return s


class Proof:
    sequents: List[Sequent]
    def __init__(self):
        self.sequents = []

    def gamma_equal(self, gamma1, gamma2):
        if len(gamma1) != len(gamma2):
            return False

        for i in range(len(gamma1)):
            if gamma1[i] not in gamma2:
                return False

        return True

    def proof_exists(self, gamma, conclusion):
        for sequent in self.sequents:
            if gamma.__eq__(sequent.gamma) and sequent.conclusion == conclusion:
            # if self.gamma_equal(gamma, sequent.gamma) and sequent.conclusion == conclusion:
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
            assert isinstance(potential.conclusion, Negation)
            gamma_prime = potential.gamma + [potential.conclusion.inner]

            if self.proof_exists(gamma_prime, False_Sym()):
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
