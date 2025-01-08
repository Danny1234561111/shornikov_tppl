from .token import TokenType
from .lexer import Lexer
from .ast import BinOp, Number, UnaryOp, Variable, Assignment, Statement, StatementList, \
    ComplexStatement, Program, Empty, CompoundStatement

class Parser():
    def __init__(self) -> None:
        self._lexer = Lexer()
        self._current_token = None

    def __check_token(self, type_: TokenType) -> None:
        if self._current_token.type_ == type_:
            self._current_token = self._lexer.next()
        else:
            raise SyntaxError('invalid token order')

    def __factor(self):
        token = self._current_token

        if token.value == "+":
            self.__check_token(TokenType.OPERATOR)
            return UnaryOp(token, self.__factor())

        if token.value == "-":
            self.__check_token(TokenType.OPERATOR)
            return UnaryOp(token, self.__factor())

        if token.type_ == TokenType.NUMBER:
            self.__check_token(TokenType.NUMBER)
            return Number(token)
        if token.type_ == TokenType.LPAREN:
            self.__check_token(TokenType.LPAREN)
            result = self.__expr()
            self.__check_token(TokenType.RPAREN)
            return result
        if token.type_ == TokenType.ID:
            self.__check_token(TokenType.ID)
            return Variable(token)

        raise SyntaxError("Invalid factor")

    def __term(self):
        result = self.__factor()

        while self._current_token and (self._current_token.type_ == TokenType.OPERATOR):
            if self._current_token.value not in ["*", "/"]:
                break
            token = self._current_token
            self.__check_token(TokenType.OPERATOR)

            result = BinOp(result, token, self.__factor())

        return result

    def __expr(self) -> BinOp:
        result = self.__term()

        while self._current_token and (self._current_token.type_ == TokenType.OPERATOR):
            token = self._current_token
            self.__check_token(TokenType.OPERATOR)

            result = BinOp(result, token, self.__term())

        return result

    def __assignment(self):
        token = self._current_token
        self._current_token = self._lexer.next()

        if not(self._current_token.value == ':='):
            raise SyntaxError('bad token')

        self._current_token = self._lexer.next()

        result = Assignment(token, self.__expr())
        return result

    def __statement_list_without_begins(self):
        result = Empty()

        while self._current_token:
            result = StatementList(result, Statement(self.__assignment()))

            if self._current_token is not None and not (self._current_token.value == ';'):
                raise SyntaxError('Missed SEMI sign')

            self._current_token = self._lexer.next()

        self._current_token = self._lexer.next()

        return result

    def __compound_statement(self):
        self._current_token = self._lexer.next()

        if self._current_token.value == 'END':
            self._current_token = self._lexer.next()
            return Empty()

        result = Empty()
        compound_stack=[]
        while self._current_token:
            if self._current_token.value == 'BEGIN':
                compound_stack.append(result)
                result = self.__compound_statement()  # Рекурсивный вызов
                result = StatementList(compound_stack.pop(), Statement(result))
            else:
                result = StatementList(result, Statement(self.__assignment()))

            if self._current_token is not None and not (self._current_token.value == ';'):
                if self._current_token.value == 'END':
                    self._current_token = self._lexer.next()

                    if self._current_token is not None and self._current_token.value == ';':
                        return CompoundStatement(result)

                raise SyntaxError('Missed SEMI sign')

            self._current_token = self._lexer.next()

    def __program(self):
        self._current_token = self._lexer.next()

        result = Empty()

        while self._current_token:
            if self._current_token.value == 'END':
                self._current_token = self._lexer.next()

                if self._current_token is not None and self._current_token.value == '.':
                    return Program(ComplexStatement(result))

                raise SyntaxError('Missed DOT sign')

            if self._current_token.value == 'BEGIN':
                result = StatementList(result, Statement(self.__compound_statement()))
            else:
                result = StatementList(result, Statement(self.__assignment()))

            if self._current_token is not None and not (self._current_token.value == ';'):
                raise SyntaxError('Missed SEMI sign')

            self._current_token = self._lexer.next()


    def eval(self, s: str) -> StatementList | BinOp | Statement | ComplexStatement | UnaryOp:
        self._lexer.init(s)
        self._current_token = self._lexer.next()

        if self._current_token.value == "BEGIN":
            return self.__program()
        elif self._current_token.value[0].isalpha():
            return self.__statement_list_without_begins()
        else:
            return self.__expr()

