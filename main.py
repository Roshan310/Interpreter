# EOF represents end-of-file token which indicate
# that there is no more input for Lexical Analysis
from tokenizer import Token
from constants import TokenType
from ast_ import *

RESERVED_KEYWORDS = {
    "PROGRAM": Token(TokenType.PROGRAM.value, "PROGRAM"),
    "VAR": Token(TokenType.VAR.value, "VAR"),
    "DIV": Token(TokenType.INTEGER_DIV.value, "DIV"),
    "INTEGER": Token(TokenType.INTEGER.value, "INTEGER"),
    "REAL": Token(TokenType.REAL.value, "REAL"),
    "BEGIN": Token(TokenType.BEGIN.value, "BEGIN"),
    "END": Token(TokenType.END.value, "END")
    
}

##############################
#                            #
#         LEXER              #
#                            #
##############################

class Lexer:
    def __init__(self, text) -> None:
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid character!!!!")

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[self.peek_pos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()

    def number(self) -> int:
        """Return a multidigit integer or float consumed from the input"""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            token = Token("REAL_CONST", float(result))

        else:
            token = Token("INTEGER_CONST", int(result))

        return token

    def _id(self):
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(TokenType.ID.value, result))
        return token

    def get_next_token(self):

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == "{":
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.number()
            
            if self.current_char == ":":
                self.advance()
                return Token(TokenType.COLON.value, ":")

            if self.current_char == ",":
                self.advance()
                return Token(TokenType.COMMA.value, ",")
            
            if self.current_char == ":" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(TokenType.ASSIGN.value, ":=")
            
            if self.current_char == ";":
                self.advance()
                return Token(TokenType.SEMI.value, ";")
            
            if self.current_char == ".":
                self.advance()
                return Token(TokenType.DOT.value, ".")
            
            if self.current_char.isdigit():
                return Token(TokenType.INTEGER.value, self.integer())
            
            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS.value, "+")
            
            if self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS.value, "-")
            
            if self.current_char == "/":
                self.advance()
                return Token(TokenType.FLOAT_DIV.value, "/")
            
            if self.current_char == "*":
                self.advance()
                return Token(TokenType.MULTIPLY.value, "*")
            
            if self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAREN.value, "(")
            
            if self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAREN.value, ")")

            self.error()

        return Token(TokenType.EOF.value, None)


##############################
#                            #
#           PARSER           #
#                            #
##############################


class Parser:
    def __init__(self, lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Error parsing Input")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        """program: PROGRAM variable SEMI block DOT"""
        self.eat(TokenType.PROGRAM.value)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(TokenType.SEMI.value)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(TokenType.DOT.value)
        return program_node

    def block(self):
        """block: declarations compound_statement"""
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node

    def declarations(self):
        """declarations: VAR (variable declaration SEMI)+ | empty"""
        declarations = []
        if self.current_token.type == TokenType.VAR.value:
            self.eat(TokenType.VAR.value)
            while self.current_token.type == TokenType.ID.value:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(TokenType.SEMI.value)

        return declarations

    def variable_declaration(self):
        """variable_declaration: ID (COMMA ID)* COLON type_spec"""
    
        var_nodes = [Var(self.current_token)]
        self.eat(TokenType.ID.value)

        while self.current_token.type == TokenType.COMMA.value:
            self.eat(TokenType.COMMA.value)
            var_nodes.extend(Var(self.current_token))
            self.eat(TokenType.ID.value)
        self.eat(TokenType.COLON.value)

        type_node = self.type_spec()
        var_declarations = [VarDecl(var_node, type_node) for var_node in var_nodes]
        return var_declarations
    
    def type_spec(self):
        """type_spec: INTEGER | REAL"""
        token = self.current_token
        if self.current_token.type == TokenType.INTEGER.value:
            self.eat(TokenType.INTEGER.value)
        else:
            self.eat(TokenType.REAL.value)
        node = Type(token)
        return node

    def compound_statement(self):
        """compound_statement: BEGIN statement_list END"""
        self.eat(TokenType.BEGIN.value)
        nodes = self.statement_list()
        self.eat(TokenType.END.value)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list: statement | statement SEMI statement_list
        """
        node = self.statement()
        results = [node]

        while self.current_token.type == TokenType.SEMI.value:
            self.eat(TokenType.SEMI.value)
            results.append(self.statement())

        if self.current_token.type == TokenType.ID.value:
            self.error()

        return results

    def statement(self):
        """
        statement: compound_statement | assignment_statement | empty
        """
        if self.current_token.type == TokenType.BEGIN.value:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.ID.value:
            node = self.assginment_statement()
        else:
            node = self.empty()

        return node

    def assginment_statement(self):
        """assignment: variable ASSIGN expr"""
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN.value)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """variable: ID"""
        node = Var(self.current_token)
        self.eat(TokenType.ID.value)
        return node

    def empty(self):
        """An empty production rule"""
        return NoOp()

    def factor(self):
        """factor: PLUS factor
                 | MINUS factor
                 | INTEGER_CONST
                 | REAL_CONST
                 | LPAREN expr RPAREN
                 | variable
        """
        token = self.current_token
        if token.type == TokenType.PLUS.value:
            self.eat(TokenType.PLUS.value)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.MINUS.value:
            self.eat(TokenType.MINUS.value)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.INTEGER_CONST.value:
            self.eat(TokenType.INTEGER_CONST.value)
            return Num(token)
        elif token.type == TokenType.REAL_CONST.value:
            self.eat(TokenType.REAL_CONST.value)
            return Num(token)
        elif token.type == TokenType.LPAREN.value:
            self.eat(TokenType.LPAREN.value)
            node = self.expr()
            self.eat(TokenType.RPAREN.value)
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        """term: factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY.value, TokenType.INTEGER_DIV.value, TokenType.FLOAT_DIV.value):
            token = self.current_token
            if token.type == TokenType.MULTIPLY.value:
                self.eat(TokenType.MULTIPLY.value)
            elif token.type == TokenType.INTEGER_DIV:
                self.eat(TokenType.INTEGER_DIV)
            elif token.type == TokenType.FLOAT_DIV.value:
                self.eat(TokenType.FLOAT_DIV.value)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """Parser/Interpreter

        expr: term((PLUS | MINUS) term)*
        term: factor((MUL | DIV) factor)*
        factor: INTEGER
        """
        node = self.term()
        while self.current_token.type in (TokenType.PLUS.value, TokenType.MINUS.value):
            token = self.current_token
            if token.type == TokenType.PLUS.value:
                self.eat(TokenType.PLUS.value)
            elif token.type == TokenType.MINUS.value:
                self.eat(TokenType.MINUS.value)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != TokenType.EOF.value:
            self.error()

        return node


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
