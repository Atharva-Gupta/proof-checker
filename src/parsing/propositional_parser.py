from src.core.errors import ParseError
from src.core.sentence import Atomic,  Negation, TwoSided, Operator, True_Sym, False_Sym

import re

def insert_spaces(expression):
    """
    Splits a logical expression into an array where each element is a symbol (removes whitespaces, and separates
    out parentheses).
    """
    return [part for part in re.split(r'(\(|\)|\s+)', expression) if part and not re.match(r'^\s+$', part)]

def parse_atomic(atomic_expr):
    if atomic_expr == r"\true":
        return True_Sym()
    elif atomic_expr == r"\false":
        return False_Sym()
    else:
        if atomic_expr[0] == "\\":
            raise ParseError(r"Atomic symbols cannot begin with a backslash!")
        return Atomic(atomic_expr)

def parse_single(s):
    if isinstance(s, str):
        return parse_atomic(s)
    else:
        return s

def balanced_parentheses(expression):
    count = 0
    for char in expression:
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
        raise ParseError(f"Must have the same number of opening and closing parentheses!")

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

            # note that ns[0] = "(" and ns[-1] = ")"
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