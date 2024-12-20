import pytest
from prefix import Prefix  # Предполагается, что ваш класс находится в файле prefix.py

class TestPrefix:

    def test_simple_expressions(self):
        converter = Prefix("+ - 13 4 55")
        assert converter.to_infix_notation() == "((13 - 4) + 55)"

        converter = Prefix("+ 2 * 2 - 2 1")
        assert converter.to_infix_notation() == "(2 + (2 * (2 - 1)))"

        converter = Prefix("+ + 10 20 30")
        assert converter.to_infix_notation() == "((10 + 20) + 30)"

        converter = Prefix("- - 1 2")
        assert converter.to_infix_notation() == "((1 - 2))"

        converter = Prefix("/ + 3 10 * + 2 3 - 3 5")
        assert converter.to_infix_notation() == "((3 + 10) / ((2 + 3) * (3 - 5)))"

    def test_empty_expression(self):
        converter = Prefix("")
        assert converter.to_infix_notation() == ""

    def test_invalid_expression(self):
        converter = Prefix("+ -")
        with pytest.raises(IndexError):
            converter.to_infix_notation()
