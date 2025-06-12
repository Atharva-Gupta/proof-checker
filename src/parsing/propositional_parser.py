from src.core.errors import ParseError
from src.core.sentence import Atomic,  Negation, TwoSided, Operator, True_Sym, False_Sym

import re

def insert_spaces(text):
    return [part for part in re.split(r'(\(|\)|\s+)', text) if part and not re.match(r'^\s+$', part)]

def parse_atomic(s):
    if s == r"\true":
        return True_Sym()
    elif s == r"\false":
        return False_Sym()
    else:
        return Atomic(s)

def parse_single(s):
    if isinstance(s, str):
        return parse_atomic(s)
    else:
        return s

def parse_string(s):
    s = "(" + s + ")"
    s = insert_spaces(s)

    stack = []
    for char in s:
        stack.append(char)

        if char == ")":
            ns = []
            while True:
                x = stack.pop()
                ns.append(x)

                if x == "(":
                    break

            ns = ns[::-1]

            if len(ns) == 3:
                stack.append(parse_single(ns[1]))
            elif len(ns) == 4:
                assert ns[1] == r"\not"

                inner = parse_single(ns[2])
                stack.append(Negation(inner))
            elif len(ns) == 5:
                str_to_oper = {r"\or": Operator.OR, r"\and": Operator.AND, r"\implies": Operator.IMPLIES}
                oper = str_to_oper[ns[2]]

                left = parse_single(ns[1])
                right = parse_single(ns[3])

                stack.append(TwoSided(left, right, oper))

    if stack:
        return stack[0]
    else:
        return None