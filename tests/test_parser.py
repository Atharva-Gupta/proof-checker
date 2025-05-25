import pytest
from proof import Proof, Sequent, InferenceRule
from propositional_parser import parse_string

def test_1():
    parse_string("(A) \and (B)")