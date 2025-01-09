from .parser import Parser
from .ast import Number, BinOp, UnaryOp, Variable, Assignment, Statement, \
    StatementList, ComplexStatement, Program, CompoundStatement


class NodeVisitor:
    def visit(self):
        pass


class Interpreter(NodeVisitor):
    def __init__(self):
        self._parser = Parser()
        self.variables = [{}]
        self.answer_variables = [{}]
        self.scopes = 0

    def visit(self, node):
        if isinstance(node, Number):
            return self._visit_number(node)
        elif isinstance(node, BinOp):
            return self._visit_binop(node)
        elif isinstance(node, UnaryOp):
            return self._visit_unary(node)
        elif isinstance(node, Assignment):
            return self._visit_assignment(node)
        elif isinstance(node, Statement):
            return self._visit_statement(node)
        elif isinstance(node, StatementList):
            return self._visit_statementList(node)
        elif isinstance(node, Variable):
            return self._visit_variable(node)
        elif isinstance(node, ComplexStatement):
            return self._visit_сomplexStatement(node)
        elif isinstance(node, CompoundStatement):
            return self._visit_compoundStatement(node)
        elif isinstance(node, Program):
            return self._visit_program(node)


    def _visit_compoundStatement(self, node):
        self.scopes += 1
        self.variables.append({})
        self.visit(node.statement_list)
        self.answer_variables.insert(1, self.variables.pop(self.scopes))
        self.scopes -= 1

    def _visit_program(self, node):
        self.visit(node.complex_statement)

    def _visit_сomplexStatement(self, node):
        self.visit(node.statement_list)

    def _visit_variable(self, node):
        for scope in range(self.scopes, -1, -1):
            if node.token.value in self.variables[scope]:
                return self.variables[scope][node.token.value]

        raise RuntimeError("Invalid variable")

    def _visit_statement(self, node):
        self.visit(node.node)

    def _visit_statementList(self, node):
        self.visit(node.statement_list)
        self.visit(node.statement)

    def _visit_assignment(self, node):
        self.variables[self.scopes][node.variable.value] = self.visit(node.expr)

    def _visit_unary(self, node):
        match node.op.value:
            case "+":
                return +self.visit(node.expr)
            case "-":
                return -self.visit(node.expr)
            case "_":
                raise RuntimeError("Bad Unary op")

    def _visit_number(self, node: Number) -> float:
        return float(node.token.value)

    def _visit_binop(self, node: BinOp):
        match node.op.value:
            case "+":
                return self.visit(node.left) + self.visit(node.right)
            case "-":
                return self.visit(node.left) - self.visit(node.right)
            case "*":
                return self.visit(node.left) * self.visit(node.right)
            case "/":
                return self.visit(node.left) / self.visit(node.right)
            case _:
                raise RuntimeError("Invalid operator")

    def eval(self, code: str) -> float:
        self.variables = [{}]
        self.answer_variables = [{}]

        tree = self._parser.eval(code)
        self.visit(tree)

        self.answer_variables[0] = self.variables[0]
        return self.answer_variables
