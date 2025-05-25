from errors import ParseError
from sentence import Atomic,  Negation, TwoSided, Operator, True_Sym, False_Sym

import re

def insert_spaces(text):
    return [part for part in re.split(r'(\(|\)|\s+)', text) if part and not re.match(r'^\s+$', part)]

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
                if isinstance(ns[1], str):
                    if ns[1] == r"\true":
                        stack.append(True_Sym())
                    elif ns[1] == r"\false":
                        stack.append(False_Sym())
                    else:
                        stack.append(Atomic(ns[1]))
                else:
                    stack.append(ns[1])
            elif len(ns) == 4:
                assert ns[1] == r"\not"

                if isinstance(ns[2], str):
                    inner = Atomic(ns[2])
                else:
                    inner = ns[2]

                stack.append(Negation(inner))

            elif len(ns) == 5:
                str_to_oper = {r"\or": Operator.OR, r"\and": Operator.AND, r"\implies": Operator.IMPLIES}
                oper = str_to_oper[ns[2]]

                if isinstance(ns[1], str):
                    left = Atomic(ns[1])
                else:
                    left = ns[1]

                if isinstance(ns[3], str):
                    right = Atomic(ns[3])
                else:
                    right = ns[3]

                stack.append(TwoSided(left, right, oper))

    return stack[0]

def main():
    s = r"\false"
    print(parse_string(s))

    s = r"((B) \implies A)"
    print(parse_string(r"((\not B) \implies B)"))

    print(parse_string(r"(\not B) \implies B"))

    # variable_assgn = {"B": True, "A": False}

    # print(parse_string(s).evaluate(variable_assgn))
    # print(parse_string(s).get_atomics())

    print(parse_string("A"))

if __name__ == "__main__":
    main()
