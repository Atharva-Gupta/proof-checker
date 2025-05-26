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

        print(stack)

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
                    if ns[2] == r"\true":
                        inner = True_Sym()
                    elif ns[2] == r"\false":
                        inner = False_Sym()
                    else:
                        inner = Atomic(ns[2])
                else:
                    inner = ns[2]

                stack.append(Negation(inner))

            elif len(ns) == 5:
                str_to_oper = {r"\or": Operator.OR, r"\and": Operator.AND, r"\implies": Operator.IMPLIES}
                oper = str_to_oper[ns[2]]

                if isinstance(ns[1], str):
                    if ns[1] == r"\true":
                        left = True_Sym()
                    elif ns[1] == r"\false":
                        left = False_Sym()
                    else:
                        left = Atomic(ns[1])
                else:
                    left = ns[1]

                if isinstance(ns[3], str):
                    if ns[3] == r"\true":
                        right = True_Sym()
                    elif ns[3] == r"\false":
                        right = False_Sym()
                    else:
                        right = Atomic(ns[3])
                else:
                    right = ns[3]

                stack.append(TwoSided(left, right, oper))

    print(stack[0])
    return stack[0]