from constants import TokenType
from ast_ import *
from lexer import Lexer
from parser import Parser
from symbol import SymbolTable, VarSymbol

##############################
#                            #
#         INTERPRETER        #
#                            #
##############################


class NodeVisitor:

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")


class SymbolTableBuilder(NodeVisitor):
    def __init__(self) -> None:
        self.symtab = SymbolTable()

        def visit_Block(self, node):
            for declaration in node.declarations:
                self.visit(declaration)
            self.visit(node.compound_statement)

        def visit_Program(self, node):
            self.visit(node.block)

        def visit_BinOp(self, node):
            self.visit(node.left)
            self.visit(node.right)

        def visit_Num(self, node):
            pass

        def visit_UnaryOp(self, node):
            self.visit(node.expr)

        def visit_Compound(self, node):
            for child in self.children:
                self.visit(child)

        def visit_NoOp(self, node):
            pass

        def visit_VarDecl(self, node):
            type_name = node.type_node.value
            type_symbol = self.symtab.lookup(type_name)
            var_name = node.var_node.value
            var_symbol = VarSymbol(var_name, type_symbol)
            self.symtab.define(var_symbol)


class Interpreter(NodeVisitor):

    def __init__(self, parser) -> None:
        self.parser = parser
        # SYMBOL TABLE
        # that tracks various symbols
        # like variable name and it's value
        # for example, a:=3, here 'a' will be stored as key and 3 as value of the key
        self.GLOBAL_SCOPE = {}

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == TokenType.PLUS.value:
            return +self.visit(node.expr)
        elif op == TokenType.MINUS.value:
            return -self.visit(node.expr)

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS.value:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS.value:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MULTIPLY.value:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.INTEGER_DIV.value:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == TokenType.FLOAT_DIV.value:
            return self.visit(node.left) / self.visti(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        pass

    def visit_Type(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    while True:
        try:
            text = input("calc> ")

        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == "__main__":
    main()
