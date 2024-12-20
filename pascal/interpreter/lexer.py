from .token import Token, TokenType

class Lexer:
    def __init__(self):
        self._pos = 0
        self._text = ""
        self._current_char = None

    def __forward(self):
        self._pos += 1
        if self._pos > len(self._text) - 1:
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def __skip(self):
        while self._current_char is not None and self._current_char.isspace():
            self.__forward()

    def __number(self):
        result = ""
        while self._current_char is not None and (self._current_char.isdigit() or self._current_char == '.'):
            result += self._current_char
            if result.count('.') > 1:
                raise SyntaxError("Invalid number: more than one decimal point")
            self.__forward()
        if result == "":
            raise SyntaxError("Invalid number: no digits found")
        return result

    def __id(self):
        result = ""
        while self._current_char is not None and (self._current_char.isalnum() or self._current_char == '_'):
            result += self._current_char
            self.__forward()
        return result

    def __assign(self):
        result = ":="
        self.__forward()  # Пропускаем ':'
        self.__forward()  # Пропускаем '='
        return result

    def init(self, s: str):
        self._text = s
        self._pos = 0
        self._current_char = self._text[self._pos] if self._text else None

    def next(self) -> Token:
        while self._current_char is not None:
            if self._current_char.isspace():
                self.__skip()
                continue
            if self._current_char.isdigit():
                return Token(TokenType.NUMBER, self.__number())
            if self._current_char in ["+", "-", "*", "/"]:
                op = self._current_char
                self.__forward()
                return Token(TokenType.OPERATOR, op)
            if self._current_char == "(":
                val = self._current_char
                self.__forward()
                return Token(TokenType.LPAREN, val)
            if self._current_char == ")":
                val = self._current_char
                self.__forward()
                return Token(TokenType.RPAREN, val)
            if self._current_char == ';':
                val = self._current_char
                self.__forward()
                return Token(TokenType.SEMI, val)
            if self._current_char == ':':
                return Token(TokenType.ASSIGN, self.__assign())
            if self._current_char == '.':
                self.__forward()
                return Token(TokenType.DOT, '.')
            if self._current_char.isalpha():
                val = self.__id()
                if val == 'BEGIN':
                    return Token(TokenType.BEGIN, val)
                if val == 'END':
                    return Token(TokenType.END, val)
                return Token(TokenType.ID, val)
            else:
                raise SyntaxError(f'Invalid character: {self._current_char}')
        return None  # Конец ввода
