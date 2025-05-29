from proof import Proof, Sequent, InferenceRule
from sentence import TwoSided, Atomic, Negation, Operator, True_Sym, False_Sym

class FitchSubProof():
    # note to self: outer_proof will have to be a slice looking at the parts
    # of the outer proof that come BEFORE this inner proof. Don't want to have
    # access to lines that come after the inner proof, and any updates to
    # the parts of the outer proof that come before will need to be reflected in the
    # Subproof
    def __init__(self, outer_proof: "FitchSubProof"=None):
        if outer_proof:
            self.has_outer = True

        self.outer_proof = outer_proof

        if self.has_outer:
            self.gamma = self.outer_proof.gamma  # technically incorrect by note above
        else:
            self.gamma = []

    def add_assumption(self, sentence) -> bool:
        self.gamma.append(sentence)

    def sequent_style(self) -> Proof:
        raise NotImplementedError()

    def add_subproof(self, sentence) -> "FitchSubProof":
        pass