from .proof import Proof, Sequent, InferenceRule, Gamma
from .sentence import Sentence, TwoSided, Atomic, Negation, Operator, True_Sym, False_Sym

class FitchSubProof():
    assumptions: Gamma
    outer_proof: "FitchSubProof"
    def __init__(self, outer_proof: "FitchSubProof"=None):
        if outer_proof:
            self.has_outer = True
        else:
            self.has_outer = False

        self.outer_proof = outer_proof

        self.gamma = Gamma()
        self.pr = Proof()

        self.loaded = False

        self.inners = []

    def add_assumption(self, sentence) -> bool:
        if not self.loaded:
            self.gamma += [sentence]
            return True
        else:
            return False

    def load_assumptions(self, additional_gamma: Gamma = Gamma()):
        temp_gamma = self.gamma + additional_gamma
        if not self.has_outer:
            # need to load both combinations of assumptions (current assumptions as well as
            # current assumptions + inner proof assumptions), eventually though maybe
            # we can switch to only loading one and updating the inference rules.
            for sentence in self.gamma:
                self.pr.add_sequent(Sequent(self.gamma, sentence, InferenceRule.axiom))

            for sentence in temp_gamma:
                self.pr.add_sequent(Sequent(temp_gamma, sentence, InferenceRule.axiom))
        else:
            # again, loading both combinations of assumptions
            self.outer_proof.load_assumptions(temp_gamma)
            self.outer_proof.load_assumptions(self.gamma)

        self.loaded = True

    def add_conclusion(self, sentence: Sentence, inf_rule: InferenceRule, additional_gamma: Gamma = Gamma(), is_assumption: bool = False) -> bool:
        if not is_assumption and not self.loaded:
            self.load_assumptions()

        if self.has_outer:
            return self.outer_proof.add_conclusion(sentence, inf_rule, self.gamma + additional_gamma, is_assumption)
        else:
            return self.pr.add_sequent(Sequent(self.gamma + additional_gamma, sentence, inf_rule))

    def sequent_style(self) -> Proof:
        if self.has_outer:
            raise ValueError("Inner-level fitch proofs do not have their own sequent proofs!")
        return self.pr

    def add_subproof(self) -> "FitchSubProof":
        sp = FitchSubProof(self)
        self.inners.append(sp)
        return sp
