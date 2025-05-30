from proof import Proof, Sequent, InferenceRule, Gamma
from sentence import Sentence, TwoSided, Atomic, Negation, Operator, True_Sym, False_Sym

class FitchSubProof():
    # note to self: outer_proof will have to be a slice looking at the parts
    # of the outer proof that come BEFORE this inner proof. Don't want to have
    # access to lines that come after the inner proof, and any updates to
    # the parts of the outer proof that come before will need to be reflected in the
    # Subproof
    assumptions: Gamma
    def __init__(self, outer_proof: "FitchSubProof"=None):
        if outer_proof:
            has_outer = True
        else:
            has_outer = False

        self.outer_proof = outer_proof

        if has_outer:
            self.gamma = self.outer_proof.gamma + self.outer_proof.assumptions._items  # technically incorrect by note above
        else:
            self.gamma = Gamma()

        self.assumptions = Gamma()
        self.assumptions_loaded = False

        # self.pr = Proof()
        self.l = []

    def add_assumption(self, sentence) -> bool:
        self.assumptions += [sentence]
        self.assumptions_loaded = False
        return True

    def load_assumptions(self):
        self.pr = Proof()
        for assumption in self.assumptions:
            self.pr.add_sequent(Sequent(self.assumptions, assumption, InferenceRule.axiom))
        self.assumptions_loaded = True

    def add_conclusion(self, sentence: Sentence, inf_rule: InferenceRule) -> bool:
        if not self.assumptions_loaded:
            self.load_assumptions()

        return self.pr.add_sequent(Sequent(self.assumptions, sentence, inf_rule))

    def sequent_style(self) -> Proof:
        return self.pr

    def add_subproof(self):
        cpy = self.pr.sequents[:]  # bad access
        FitchSubProof(cpy)
        return True
