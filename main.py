from constants import TokenType
from ast_ import *
from lexer import Lexer
from parser import Parser
from symbol import ScopedSymbolTable, VarSymbol, ProcedureSymbol

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


class SemanticAnalyzer(NodeVisitor):
    def __init__(self) -> None:
        self.current_scope = None

        def visit_Block(self, node):
            for declaration in node.declarations:
                self.visit(declaration)
            self.visit(node.compound_statement)

        def visit_Program(self, node):
            print("ENTER scope: global")
            global_scope = ScopedSymbolTable(scope_name="global", scope_level=1, enclosing_scpe=self.current_scope)
            self.current_scope = global_scope
            self.visit(node.block)
            print(global_scope)
            self.current_scope = self.current_scope.enclosing_scope
            print("LEAVE scope: global")

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
            type_symbol = self.current_scope.lookup(type_name)
            var_name = node.var_node.value
            var_symbol = VarSymbol(var_name, type_symbol)
            if self.symtab.lookup(var_name) is not None:
                raise Exception(f"Error: Duplicate identifier {var_name} found")
            self.current_scope.insert(var_symbol)

        def visit_Assign(self, node):
            self.visit(node.right)
            self.visit(node.left)

        def visit_Var(self, node):
            var_name = node.value
            var_symbol = self.current_scope.lookup(var_name)
            if var_symbol is None:
                raise NameError(repr(var_name))

        def visit_ProcedureDecl(self, node):
            proc_name = node.proc_name
            proc_symbol = ProcedureSymbol(proc_name)
            self.current_scope.insert(proc_symbol)
            print(f"ENTER scope: {proc_name}")

            procedure_scope = ScopedSymbolTable(proc_name, self.current_scope.scope_level+1, self.current_scope    )
            self.current_scope = procedure_scope

            for param in node.params:
                param_type = self.current_scope.lookup(param.type_node.value)
                param_name = param.var_node.value
                var_symbol = VarSymbol(param_name, param_type)
                self.current_scope.insert(var_symbol)
                proc_symbol.params.append(var_symbol)
            
            self.visit(node.block_node)
            print(procedure_scope)
            self.current_scope = self.current_scope.enclosing_scope
            print(f"LEAVE scope: {proc_name}")


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

    def visit_ProcedureDecl(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    while True:
        try:
            text = """
            PROGRAM first;
            VAR
                a, b : INTEGER;
            BEGIN
                a := 10;
                b := a+20;
            END.
        """

        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)
        print("Gloabl scope", interpreter.GLOBAL_SCOPE)


if __name__ == "__main__":
    main()
