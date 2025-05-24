from errors import ParseError
from sentence import Atomic,  Negation, TwoSided, Operator, True_Sym, False_Sym

def parse_string(s):
    s = s.strip()
    if s[0] == "(":
        if s[-1] == ")":
            s = s[1:-1]

    if len(s) == 1 and s[0] not in "\(":
        return Atomic(s[0])

    if s[0] == "\\":
        if s[:5] == r"\true":
            return True_Sym()
        elif s[:6] == r"\false":
            return False_Sym()

        if s[:4] != r"\not":
            raise ParseError("Only not operand is unary!")

        return Negation(parse_string(s[4:]))

    count = 0
    ind = 0
    split = [""]
    while ind < len(s):
        char = s[ind]

        if char == "(":
            count += 1
        elif char == ")":
            count -= 1

        if count < 0:
            raise ParseError("Every closing parenthesis must have a corresponding opening parenthesis!")

        if count == 0 and char == "\\":
            split.append("")

        if len(split) == 2 and char == " ":
            split.append("")

        split[-1] += char

        ind += 1

    if count > 0:
        raise ParseError("Every opening parenthesis must have a corresponding closed parenthesis!")

    split[1] = split[1].strip()

    str_to_oper = {r"\or": Operator.OR, r"\and": Operator.AND, r"\implies": Operator.IMPLIES}

    return TwoSided(parse_string(split[0]), parse_string(split[2]), str_to_oper[split[1]])

def main():
    s = r"\false"
    print(parse_string(s))

    s = r"((B) \implies A)"
    print(parse_string(r"((\not B) \implies B)"))

    variable_assgn = {"B": True, "A": False}

    print(parse_string(s).evaluate(variable_assgn))
    print(parse_string(s).get_atomics())

    # print(parse_string("A"))

if __name__ == "__main__":
    main()
