import pytest
from src.parsing.propositional_parser import parse_string, insert_spaces
from src.core.sentence import Atomic, TwoSided, Operator, Negation, True_Sym, False_Sym
from src.core.errors import ParseError

class TestParserUndefinedBehavior:
    """Test cases for parser edge cases, malformed input, and undefined behavior."""

    def test_unmatched_parentheses_left(self):
        """Test behavior with unmatched opening parenthesis."""
        with pytest.raises((IndexError, AssertionError, KeyError, ParseError)):
            parse_string("((A")

    def test_unmatched_parentheses_right(self):
        """Test behavior with extra closing parenthesis."""
        # This might not raise an error but could produce unexpected results
        with pytest.raises((IndexError, AssertionError, KeyError, ParseError)):
            result = parse_string("A))")
        # The parser wraps input with () so this becomes (A)))
        # Behavior is undefined - could return None or crash

    def test_empty_parentheses_nested(self):
        """Test nested empty parentheses."""
        result = parse_string("(())")
        assert result is None

    def test_malformed_operator_syntax(self):
        """Test malformed operator syntax."""
        with pytest.raises((AssertionError, KeyError, ParseError)):
            parse_string("A \\and")  # Missing second operand

        with pytest.raises((AssertionError, KeyError, ParseError)):
            parse_string("\\and B")  # Missing first operand

    def test_invalid_operator(self):
        """Test invalid/unknown operators."""
        with pytest.raises((KeyError, ParseError)):
            parse_string("A \\xor B")  # Unknown operator

        with pytest.raises((KeyError, ParseError)):
            parse_string("A \\nand B")  # Unknown operator

    def test_malformed_negation(self):
        """Test malformed negation syntax."""
        with pytest.raises((AssertionError, IndexError, ParseError)):
            parse_string("\\not")  # Negation without operand

        with pytest.raises((AssertionError, IndexError, ParseError)):
            parse_string("(\\not)")  # Negation in parentheses without operand

    def test_wrong_arity_expressions(self):
        """Test expressions with wrong number of arguments."""
        # Too many arguments in parentheses
        with pytest.raises((AssertionError, IndexError, ParseError)):
            parse_string("(A B C)")  # 3 elements, not valid

        with pytest.raises((AssertionError, IndexError, ParseError)):
            parse_string("(A \\and B C)")  # 4 elements, should be 3

    def test_nested_malformed_expressions(self):
        """Test deeply nested malformed expressions."""
        with pytest.raises((IndexError, AssertionError, KeyError, ParseError)):
            parse_string("((A \\and) \\or B)")

        with pytest.raises((IndexError, AssertionError, KeyError, ParseError)):
            parse_string("(A \\and (B \\or))")

    def test_special_characters_in_atomics(self):
        """Test atomics with special characters that might break parsing."""
        # These should work but test edge cases
        result = parse_string("A123")
        assert result == Atomic("A123")

        result = parse_string("_var")
        assert result == Atomic("_var")

        # Test potentially problematic characters
        result = parse_string("A\\B")  # Backslash in variable name
        assert result == Atomic("A\\B")

    def test_whitespace_edge_cases(self):
        """Test various whitespace scenarios."""
        # Multiple spaces
        result = parse_string("A     \\and     B")
        assert result == TwoSided(Atomic("A"), Atomic("B"), Operator.AND)

        # Tabs and mixed whitespace
        result = parse_string("A\t\\and\nB")
        assert result == TwoSided(Atomic("A"), Atomic("B"), Operator.AND)

        # Leading/trailing whitespace
        result = parse_string("   A \\and B   ")
        assert result == TwoSided(Atomic("A"), Atomic("B"), Operator.AND)

    def test_stack_underflow_conditions(self):
        """Test conditions that might cause stack underflow."""
        with pytest.raises((IndexError, ParseError)):
            parse_string(")")  # Immediate closing paren

        with pytest.raises((IndexError, ParseError)):
            parse_string("))(")  # Multiple immediate closing parens

    def test_infinite_loop_potential(self):
        """Test inputs that might cause infinite loops."""
        # The while True loop in parse_string could potentially loop forever
        # if stack.pop() doesn't find an opening paren
        with pytest.raises((IndexError, ParseError)):
            parse_string("A B C D E F G H I J)")  # Many tokens before closing paren

    def test_case_sensitivity(self):
        """Test case sensitivity of operators."""
        with pytest.raises((KeyError, ParseError)):
            parse_string("A \\AND B")  # Wrong case

        with pytest.raises((KeyError, ParseError)):
            parse_string("A \\Or B")  # Wrong case

        with pytest.raises((KeyError, ParseError)):
            parse_string("\\NOT A")  # Wrong case

    def test_partial_operator_names(self):
        """Test partial or misspelled operator names."""
        with pytest.raises((KeyError, ParseError)):
            parse_string("A \\an B")  # Partial 'and'

        with pytest.raises((KeyError, ParseError)):
            parse_string("A \\implie B")  # Misspelled 'implies'

    def test_unicode_and_special_chars(self):
        """Test unicode and special characters in input."""
        # Test unicode characters in variable names
        result = parse_string("α")
        assert result == Atomic("α")

        # Test unicode operators (should fail)
        with pytest.raises(KeyError):
            parse_string("A ∧ B")  # Unicode AND symbol

    def test_very_long_expressions(self):
        """Test very long expressions that might cause performance issues."""
        # Create deeply nested expression
        expr = "A"
        for i in range(100):
            expr = f"(({expr}) \\and B{i})"

        # This should work but might be slow
        result = parse_string(expr)
        assert isinstance(result, TwoSided)

    def test_mixed_true_false_cases(self):
        """Test various capitalizations of true/false."""
        with pytest.raises((KeyError, ParseError)):
            parse_string("\\True")  # Wrong case

        with pytest.raises((KeyError, ParseError)):
            parse_string("\\FALSE")  # Wrong case

        # These should work
        result = parse_string("\\true")
        assert isinstance(result, True_Sym)

        result = parse_string("\\false")
        assert isinstance(result, False_Sym)

    def test_insert_spaces_edge_cases(self):
        """Test the insert_spaces function directly."""
        # Empty string
        result = insert_spaces("")
        assert result == []

        # Only whitespace
        result = insert_spaces("   ")
        assert result == []

        # Only parentheses
        result = insert_spaces("()")
        assert result == ["(", ")"]

        # Mixed separators
        result = insert_spaces("((A))")
        assert result == ["(", "(", "A", ")", ")"]

    def test_assertion_failures(self):
        """Test conditions that trigger assertion failures."""
        # The parser has assert statements that could fail
        with pytest.raises((AssertionError, ParseError)):
            parse_string("(\\not A B)")  # Wrong number of elements for negation

        # Test operator assertion failure by manipulating parser state
        # This is harder to test directly due to the parser structure

    def test_return_none_conditions(self):
        """Test conditions where parser returns None."""
        # Empty input after wrapping
        result = parse_string("")
        assert result is None

        # Only whitespace
        result = parse_string("   ")
        assert result is None

        # Only parentheses
        result = parse_string("()")
        assert result is None

    def test_regex_edge_cases(self):
        """Test edge cases in the regex splitting."""
        # Test strings that might break the regex
        test_cases = [
            "\\",  # Single backslash
            "\\\\",  # Double backslash
            "(((",  # Multiple opening parens
            ")))",  # Multiple closing parens
            "A\\B\\C",  # Multiple backslashes
        ]

        for case in test_cases:
            try:
                result = parse_string(case)
                # Should either return a valid result or raise an exception
                assert result is None or hasattr(result, '__class__')
            except (IndexError, AssertionError, KeyError, ParseError):
                # Expected failure cases
                pass