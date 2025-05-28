from proof import Proof, Sequent, InferenceRule
from sentence import TwoSided, Atomic, Negation, Operator, True_Sym, False_Sym

class SubProof():
    def __init__(self, earlier_results):
        pass

    def add_assumption(self, sentence) -> bool:
        raise NotImplementedError()

    def sequent_style(self) -> Proof:
        raise NotImplementedError()

    def add_subproof(self, sentence) -> "SubProof":
        pass