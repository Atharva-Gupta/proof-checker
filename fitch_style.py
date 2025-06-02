from proof import Proof, Sequent, InferenceRule, Gamma
from sentence import Sentence, TwoSided, Atomic, Negation, Operator, True_Sym, False_Sym

class FitchSubProof():
    assumptions: Gamma
    outer_proof: "FitchSubProof"
    def __init__(self, outer_proof: "FitchSubProof"=None):
        if outer_proof:
            self.has_outer = True
        else:
            self.has_outer = False

        self.outer_proof = outer_proof

        if self.has_outer:
            self.gamma = self.outer_proof.gamma + self.outer_proof.assumptions._items  # technically incorrect by note above
        else:
            self.gamma = Gamma()

        self.assumptions = Gamma()
        self.pr = Proof()

        self.inners = []

    def add_assumption(self, sentence) -> bool:
        self.assumptions += [sentence]
        return True

    def add_conclusion(self, sentence: Sentence, inf_rule: InferenceRule, additional_gamma: Gamma = Gamma()) -> bool:
        # return self.pr.add_sequent(Sequent(self.assumptions, sentence, inf_rule))
        if self.has_outer:
            return self.outer_proof.add_conclusion(sentence, inf_rule, self.gamma + additional_gamma)
        else:
            return self.pr.add_sequent(Sequent(self.gamma + additional_gamma, sentence, inf_rule))

    def sequent_style(self) -> Proof:
        if self.has_outer:
            raise ValueError("Inner-level sequent proofs do not have their own proofs!")
        return self.pr

    def add_subproof(self):
        self.inners.append(FitchSubProof(self))
        return True
