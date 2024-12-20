import pytest
from interpreter import Token, TokenType  # Убедитесь, что у вас есть правильный импорт
from interpreter import Lexer  # Импортируйте ваш класс Lexer из соответствующего модуля


@pytest.fixture
def lexer():
    return Lexer()


def test_single_number(lexer):
    lexer.init("123")
    token = lexer.next()
    assert token.type_ == TokenType.NUMBER
    assert token.value == "123"


def test_float_number(lexer):
    lexer.init("123.456")
    token = lexer.next()
    assert token.type_ == TokenType.NUMBER
    assert token.value == "123.456"


def test_operator(lexer):
    lexer.init("+")
    token = lexer.next()
    assert token.type_ == TokenType.OPERATOR
    assert token.value == "+"


def test_parentheses(lexer):
    lexer.init("()")
    token = lexer.next()
    assert token.type_ == TokenType.LPAREN
    assert token.value == "("

    token = lexer.next()
    assert token.type_ == TokenType.RPAREN
    assert token.value == ")"


def test_semi_colon(lexer):
    lexer.init(";")
    token = lexer.next()
    assert token.type_ == TokenType.SEMI
    assert token.value == ";"


def test_assignment(lexer):
    lexer.init(":=")
    token = lexer.next()
    assert token.type_ == TokenType.ASSIGN
    assert token.value == ":="


def test_identifier(lexer):
    lexer.init("myVariable")
    token = lexer.next()
    assert token.type_ == TokenType.ID
    assert token.value == "myVariable"


def test_begin_end_keywords(lexer):
    lexer.init("BEGIN END")
    token = lexer.next()
    assert token.type_ == TokenType.BEGIN
    assert token.value == "BEGIN"

    token = lexer.next()
    assert token.type_ == TokenType.END
    assert token.value == "END"


def test_invalid_character(lexer):
    lexer.init("@")
    with pytest.raises(SyntaxError):
        lexer.next()


def test_multiple_tokens(lexer):
    lexer.init("BEGIN x := 10; END.")
    tokens = []
    while True:
        token = lexer.next()
        if token is None:  # Если токен None, значит, конец ввода
            break
        tokens.append(token)

    assert len(tokens) == 7  # Проверяем количество токенов