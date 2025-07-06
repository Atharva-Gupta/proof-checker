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

def balanced_parentheses(s):
    count = 0
    for char in s:
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1

        if count < 0:
            return False

    return count == 0

def parse_string(s):
    s = "(" + s + ")"
    s = insert_spaces(s)

    if not balanced_parentheses(s):
        raise ParseError(f"Must have the same number of inner and outer parentheses!")

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
                if isinstance(ns[1], str) and ns[1][0] == "\\" and ns[1] not in ("\\true", "\\false"):
                    raise ParseError("Expressions must be accompanied with at least one operand!")

                stack.append(parse_single(ns[1]))
            elif len(ns) == 4:
                if ns[1] != r"\not":
                    raise ParseError("Expression is ill-formed!")

                inner = parse_single(ns[2])
                stack.append(Negation(inner))
            elif len(ns) == 5:
                str_to_oper = {r"\or": Operator.OR, r"\and": Operator.AND, r"\implies": Operator.IMPLIES}
                try:
                    oper = str_to_oper[ns[2]]
                except KeyError:
                    raise ParseError(f"Operator {ns[2]} not defined!")

                left = parse_single(ns[1])
                right = parse_single(ns[3])

                stack.append(TwoSided(left, right, oper))
            elif len(ns) == 2:
                pass
            else:
                raise ParseError(f"All inner expressions require explicit surrounding parentheses! {len(ns)}")

    if stack:
        return stack[0]
    else:
        return None