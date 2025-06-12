import pytest
import sys
from propositional_parser import parse_string
from sentence import Atomic, TwoSided, Operator, Negation, True_Sym, False_Sym

class TestParserBoundaryConditions:
    """Test boundary conditions and stress testing for the parser."""
    
    def test_maximum_nesting_depth(self):
        """Test maximum nesting depth before hitting recursion limits."""
        # Create expression with deep nesting
        base = "A"
        for i in range(50):  # Reasonable depth to avoid stack overflow
            base = f"(\\not {base})"
        
        result = parse_string(base)
        
        # Should be deeply nested Negation objects
        current = result
        depth = 0
        while isinstance(current, Negation):
            current = current.inner
            depth += 1
        
        assert depth == 50
        assert current == Atomic("A")
    
    def test_maximum_expression_width(self):
        """Test expressions with many operators at the same level."""
        # Create wide expression: A1 AND A2 AND A3 AND ... AND A50
        expr = "A1"
        for i in range(2, 51):
            expr = f"({expr} \\and A{i})"
        
        result = parse_string(expr)
        assert isinstance(result, TwoSided)
        assert result.oper == Operator.AND
    
    def test_very_long_atomic_names(self):
        """Test very long atomic variable names."""
        long_name = "A" * 1000
        result = parse_string(long_name)
        assert result == Atomic(long_name)
        
        # Test in compound expression
        result = parse_string(f"{long_name} \\and B")
        assert isinstance(result, TwoSided)
        assert result.left == Atomic(long_name)
    
    def test_many_whitespace_tokens(self):
        """Test expressions with excessive whitespace."""
        # Many spaces between tokens
        spaces = " " * 100
        expr = f"A{spaces}\\and{spaces}B"
        result = parse_string(expr)
        assert result == TwoSided(Atomic("A"), Atomic("B"), Operator.AND)
    
    def test_empty_and_minimal_inputs(self):
        """Test minimal valid inputs."""
        # Single character atomic
        result = parse_string("A")
        assert result == Atomic("A")
        
        # Single digit
        result = parse_string("1")
        assert result == Atomic("1")
        
        # Single symbol
        result = parse_string("_")
        assert result == Atomic("_")
    
    def test_complex_mixed_operators(self):
        """Test complex expressions mixing all operators."""
        expr = "((A \\and B) \\or (C \\implies D)) \\and (\\not (E \\or F))"
        result = parse_string(expr)
        
        assert isinstance(result, TwoSided)
        assert result.oper == Operator.AND
        
        # Left side should be OR
        assert isinstance(result.left, TwoSided)
        assert result.left.oper == Operator.OR
        
        # Right side should be negation
        assert isinstance(result.right, Negation)
    
    def test_stress_parentheses_balancing(self):
        """Test complex parentheses balancing scenarios."""
        test_cases = [
            "((A))",
            "(((A)))",
            "((((A))))",  # Deep nesting
            "((A \\and B) \\or (C \\and D))",  # Balanced complex
            "(A \\and (B \\or (C \\implies D)))",  # Right-heavy nesting
            "(((A \\or B) \\and C) \\implies D)",  # Left-heavy nesting
        ]
        
        for case in test_cases:
            result = parse_string(case)
            assert result is not None
            assert hasattr(result, '__class__')
    
    def test_operator_precedence_stress(self):
        """Test complex operator precedence scenarios."""
        # The parser doesn't implement precedence, so this tests explicit grouping
        cases = [
            ("A \\and B \\or C", "Should require explicit parentheses"),
            ("A \\or B \\and C", "Should require explicit parentheses"),
            ("A \\implies B \\and C", "Should require explicit parentheses"),
        ]
        
        for expr, description in cases:
            # These should fail because parser requires explicit parentheses
            with pytest.raises((AssertionError, IndexError, KeyError)):
                parse_string(expr)
    
    def test_all_operator_combinations(self):
        """Test all possible binary operator combinations."""
        operators = ["\\and", "\\or", "\\implies"]
        
        for op1 in operators:
            for op2 in operators:
                expr = f"((A {op1} B) {op2} (C {op1} D))"
                result = parse_string(expr)
                assert isinstance(result, TwoSided)
    
    def test_negation_combinations(self):
        """Test negation in various combinations."""
        test_cases = [
            "\\not A",
            "\\not (A \\and B)",
            "(\\not A) \\and B",
            "A \\and (\\not B)",
            "\\not (\\not A)",  # Double negation
            "\\not ((A \\and B) \\or C)",  # Complex negation
        ]
        
        for case in test_cases:
            result = parse_string(case)
            assert result is not None
    
    def test_true_false_combinations(self):
        """Test \\true and \\false in various combinations."""
        test_cases = [
            "\\true",
            "\\false",
            "\\true \\and A",
            "A \\or \\false",
            "\\not \\true",
            "\\not \\false",
            "(\\true \\and \\false) \\or A",
            "\\true \\implies (A \\and \\false)",
        ]
        
        for case in test_cases:
            result = parse_string(case)
            assert result is not None
    
    def test_memory_intensive_parsing(self):
        """Test parsing of expressions that might consume significant memory."""
        # Create expression with many unique atomic variables
        atomics = [f"VAR_{i:04d}" for i in range(100)]
        
        # Build large OR expression
        expr = atomics[0]
        for atomic in atomics[1:]:
            expr = f"({expr} \\or {atomic})"
        
        result = parse_string(expr)
        assert isinstance(result, TwoSided)
        assert result.oper == Operator.OR
    
    def test_stack_depth_limits(self):
        """Test expressions that might hit stack depth limits."""
        # Create deeply nested parentheses
        expr = "A"
        depth = 100
        for i in range(depth):
            expr = f"({expr})"
        
        result = parse_string(expr)
        assert result == Atomic("A")
    
    def test_parser_state_consistency(self):
        """Test that parser maintains consistent state across multiple calls."""
        # Parse multiple expressions in sequence
        expressions = [
            "A \\and B",
            "\\not C",
            "(D \\or E) \\implies F",
            "\\true",
            "\\false"
        ]
        
        results = []
        for expr in expressions:
            result = parse_string(expr)
            results.append(result)
            assert result is not None
        
        # Verify results are independent
        assert len(set(str(r) for r in results)) == len(results)
    
    def test_unicode_boundary_cases(self):
        """Test unicode characters at boundaries."""
        # Unicode variable names
        unicode_vars = ["α", "β", "γ", "δ", "ε"]
        
        for var in unicode_vars:
            result = parse_string(var)
            assert result == Atomic(var)
            
            # In compound expressions
            result = parse_string(f"{var} \\and B")
            assert isinstance(result, TwoSided)
            assert result.left == Atomic(var)
    
    def test_numeric_atomics_boundary(self):
        """Test numeric atomic variables."""
        numeric_cases = [
            "0", "1", "42", "123456789",
            "3.14", "1e10", "-5"
        ]
        
        for case in numeric_cases:
            result = parse_string(case)
            assert result == Atomic(case)
    
    @pytest.mark.slow
    def test_performance_regression(self):
        """Test for performance regressions with complex expressions."""
        import time
        
        # Create moderately complex expression
        expr = "A"
        for i in range(20):
            expr = f"((\\not {expr}) \\and B{i}) \\or (C{i} \\implies D{i})"
        
        start_time = time.time()
        result = parse_string(expr)
        end_time = time.time()
        
        # Should complete in reasonable time (< 1 second)
        assert end_time - start_time < 1.0
        assert result is not None