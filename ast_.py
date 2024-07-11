class AST:
    pass


class Compound(AST):
    """Represents a 'BEGIN ... END' block"""

    def __init__(self) -> None:
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    def __init__(self, token) -> None:
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class UnaryOp(AST):
    def __init__(self, op, expr) -> None:
        self.token = self.op = op
        self.expr = expr


class BinOp(AST):
    def __init__(self, left, op, right) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token) -> None:
        self.token = token
        self.value = token.value


class Program(AST):

    def __init__(self, name, block) -> None:
        self.name = name
        self.block = block


class Block(AST):

    def __init__(self, declarations, compound_statement) -> None:
        self.declarations = declarations
        self.compound_statement = compound_statement


class VarDecl(AST):

    def __init__(self, var_node, type_node) -> None:
        self.var_node = var_node
        self.type_node = type_node


class Type(AST):

    def __init__(self, token) -> None:
        self.token = token
        self.value = token.value
