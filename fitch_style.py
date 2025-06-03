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
        for sentence in self.gamma:
            # if self.has_outer:
            self.add_conclusion(sentence, InferenceRule.axiom, Gamma(), True)
            # else:
            #     self.add_conclusion(sentence, InferenceRule.axiom, Gamma(), True)

        self.loaded = True

        if self.has_outer:
            self.outer_proof.load_assumptions(self.gamma + additional_gamma)

    def add_conclusion(self, sentence: Sentence, inf_rule: InferenceRule, additional_gamma: Gamma = Gamma(), is_assumption: bool = False) -> bool:
        if not is_assumption and not self.loaded:
            self.load_assumptions()

        if self.has_outer:
            # return self.outer_proof.add_conclusion(sentence, inf_rule, self.gamma + additional_gamma)
            return self.outer_proof.add_conclusion(sentence, inf_rule, self.gamma + additional_gamma, is_assumption)
        else:
            print(self.gamma + additional_gamma, sentence, inf_rule)

            # print("tp", (self.gamma))
            # print("addtp", (additional_gamma))
            # print()

            # print(self.pr.__str__())
            # print("added", self.gamma + additional_gamma, sentence, inf_rule)

            # return self.pr.add_sequent(Sequent(self.gamma + additional_gamma, sentence, inf_rule))
            return self.pr.add_sequent(Sequent(self.gamma + additional_gamma, sentence, inf_rule))

    def sequent_style(self) -> Proof:
        if self.has_outer:
            raise ValueError("Inner-level fitch proofs do not have their own sequent proofs!")
        return self.pr

    def add_subproof(self) -> "FitchSubProof":
        sp = FitchSubProof(self)
        self.inners.append(sp)
        return sp
