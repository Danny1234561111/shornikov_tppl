from .token import Token


class Node:
    pass


class Number(Node):
    def __init__(self, token: Token):
        self.token = token

    # def __str__(self):
    #     return f"{self.__class__.__name__} ({self.token})"


class Variable(Node):
    def __init__(self, token: Token):
        self.token = token

    # def __str__(self):
    #     return f"{self.__class__.__name__} ({self.token})"


class BinOp(Node):
    def __init__(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    # def __str__(self):
    #     return f"{self.__class__.__name__} {self.op.value}({self.op.value}, {self.left}, {self.right})"


class UnaryOp(Node):
    def __init__(self, op: Token, expr: Node):
        self.op = op
        self.expr = expr

    # def __str__(self):
    #     return f"{self.__class__.__name__}{self.op.value}({self.expr})"


class Assignment(Node):
    def __init__(self, id: Token, expr: Node):
        self.variable = id
        self.expr = expr

    # def __str__(self):
    #     return f"{self.__class__.__name__}({self.variable}, {self.expr})"


class Statement(Node):
    def __init__(self, node: Node):
        self.node = node

    # def __str__(self):
    #     return f"{self.__class__.__name__}({self.node})"


class StatementList(Node):
    def __init__(self, statement_list: Node, statement: Node):
        self.statement = statement
        self.statement_list = statement_list

    # def __str__(self):
    #     return f"{self.__class__.__name__}({self.statement}, {self.statement_list})"


class ComplexStatement(Node):
    def __init__(self, statement_list: Node):
        self.statement_list = statement_list

    # def __str__(self):
    #     return f"{self.__class__.__name__}({self.statement_list})"


class Program(Node):
    def __init__(self, complex_statement: Node):
        self.complex_statement = complex_statement

    # def __str__(self):
    #     return f"{self.__class__.__name__}({self.complex_statement})"


class CompoundStatement(Node):
    def __init__(self, statement_list: Node):
        self.statement_list = statement_list

    # def __str__(self):
    #     return f"{self.__class__.__name__}({self.statement_list})"


class Empty(Node):
    pass
    # def __str__(self):
    #     return f"{self.__class__.__name__}"