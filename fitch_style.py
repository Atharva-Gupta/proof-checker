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

        self.inners = []

    def add_assumption(self, sentence) -> bool:
        self.gamma += [sentence]

        # TODO: need to re-implement the loading stuff because this cannot handle more than one assumption
        # per subproof at a time.
        if self.has_outer:
            self.add_conclusion(sentence, InferenceRule.axiom, self.gamma)
        else:
            self.add_conclusion(sentence, InferenceRule.axiom, Gamma())

        return True

    def add_conclusion(self, sentence: Sentence, inf_rule: InferenceRule, additional_gamma: Gamma = Gamma()) -> bool:
        if self.has_outer:
            return self.outer_proof.add_conclusion(sentence, inf_rule, self.gamma + additional_gamma)
        else:
            print(sentence, inf_rule, additional_gamma)

            # print("tp", (self.gamma))
            # print("addtp", (additional_gamma))
            # print()

            # print(self.pr.__str__())
            # print("added", self.gamma + additional_gamma, sentence, inf_rule)

            return self.pr.add_sequent(Sequent(self.gamma + additional_gamma, sentence, inf_rule))

    def sequent_style(self) -> Proof:
        if self.has_outer:
            raise ValueError("Inner-level sequent proofs do not have their own proofs!")
        return self.pr

    def add_subproof(self):
        self.inners.append(FitchSubProof(self))
        return True
