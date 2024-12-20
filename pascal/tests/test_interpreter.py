import pytest
from interpreter import Interpreter


@pytest.fixture(scope="function")  # Если указать score, то Interpreter для каждого теста будет уникальным
def interpreter():
    return Interpreter()


class TestInterpreter:
    def test_factor(self, interpreter):
        assert interpreter.eval("-5;") == [{}]
        assert interpreter.eval("+5;") == [{}]
        assert interpreter.eval("5+6;") == [{}]
        assert interpreter.eval("(5+6);") == [{}]

    def test_bad_factor(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("a := *5;")

    def test_missed_semi(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("a := 5 ^ 6")

    def test_simple_assigment(self, interpreter):
        assert interpreter.eval("a := -5") == [{'a': -5.0}]
        assert interpreter.eval("a := 5 * 4 + 6 * 5;") == [{'a': 50.0}]

    def test_statement(self, interpreter):
        assert interpreter.eval("a := 5;") == [{'a': 5.0}]
        assert interpreter.eval("a := 5 * 4 + 6 * 5;") == [{'a': 50.0}]

    def test_statement_list(self, interpreter):
        assert interpreter.eval("a := 5; b := 6; c := a + b;") == [{'a': 5.0, 'b': 6.0, 'c': 11.0}]
        assert interpreter.eval("sum := 5; counter := sum; counter := counter + 1;") == [{'sum': 5.0, 'counter': 6.0}]

    def test_incorrect_assign_sign(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("a := 5; b = c + 1;")

    def test_no_semi_sign(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("a := 5; b = c + 1;")

    def test_invalid_variable(self, interpreter):
        with pytest.raises(RuntimeError):
            interpreter.eval("a := 5; b := c + 1;")

    def test_bad_program(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval(
                """
                BEGIN
                    BEGIN
                    END
                    x:= 2 + 3 * (2 + 3);
                    y:= 2 / 2 - 2 + 3 * ((1 + 1) + (1 + 1));
                END.
                """)

        with pytest.raises(SyntaxError):
            interpreter.eval(
                """
                BEGIN
                    y:= 2 / 2 - 2 + 3 * ((1 + 1) + (1 + 1));
                END
                """)

    def test_program(self, interpreter):
        assert interpreter.eval(
            """
            BEGIN
                BEGIN
                END;
                x:= 2 + 3 * (2 + 3);
                y:= 2 / 2 - 2 + 3 * ((1 + 1) + (1 + 1));
            END.
            """) == [{'x': 17.0, 'y': 11.0}]

        assert interpreter.eval(
            """
            BEGIN
                BEGIN
                    a := 5;
                    BEGIN
                        b := a + 8
                    END;
                    t := 11
                END;
                x:= 2 + 3 * (2 + 3);
                y:= 2 / 2 - 2 + 3 * ((1 + 1) + (1 + 1));
            END.
            """) == [{'x': 17.0, 'y': 11.0}, {'a': 5.0, 't': 11}, {'b': 13.0}]


        assert interpreter.eval(
            """
            BEGIN
                y := 2;
                BEGIN
                    a := 3;
                    a := a;
                    b := 10 + a + 10 * y / 4;
                    c := a - b
                END;
                x := 11;
            END.
            """) == [{'y': 2.0, 'x': 11.0}, {'a': 3.0, 'b': 18.0, 'c': -15.0}]

        assert interpreter.eval(
            """
            BEGIN
            END.
            """) == [{}]
        assert interpreter.eval(
        """
        BEGIN 
            a := 5; 
            b := 6; 
            c := a + b;
        END.
        """) == [{'a': 5.0, 'b': 6.0, 'c': 11.0}]

        assert interpreter.eval(
        """
        BEGIN 
	        x:= 2 + 3 * (2 + 3);
            y:= 2 / 2 - 2 + 3 * ((1 + 1) + (1 + 1));
        END.
        """) == [{'x': 17.0, 'y': 11.0}]

