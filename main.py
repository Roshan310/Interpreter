# EOF represents end-of-file token which indicate
# that there is no more input for Lexical Analysis

(
    INTEGER,
    PLUS,
    MINUS,
    DIVIDE,
    MULTIPLY,
    LPAREN,
    RPAREN,
    BEGIN,
    END,
    ID,
    DOT,
    SEMI,
    ASSIGN,
    EOF,
) = (
    "INTEGER",
    "PLUS",
    "MINUS",
    "DIV",
    "MUL",
    "(",
    ")",
    "BEGIN",
    "END",
    "ID",
    "DOT",
    "SEMI",
    "ASSIGN",
    "EOF",
)


##############################
#                            #
#         LEXER              #
#                            #
##############################


class Token:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f"Token({self.type}, {self.value})"

    def __repr__(self) -> str:
        return self.__str__()


RESERVED_KEYWORDS = {"BEGIN": Token(BEGIN, "BEGIN"), "END": Token(END, "END")}


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

    def integer(self) -> int:
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)

    def _id(self):
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                return self._id()
            if self.current_char == ":" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(ASSIGN, ":=")
            if self.current_char == ";":
                self.advance()
                return Token(SEMI, ";")
            if self.current_char == ".":
                self.advance()
                return Token(DOT, ".")
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")
            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")
            if self.current_char == "/":
                self.advance()
                return Token(DIVIDE, "/")
            if self.current_char == "*":
                self.advance()
                return Token(MULTIPLY, "*")
            if self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")
            if self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            self.error()

        return Token(EOF, None)


##############################
#                            #
#           PARSER           #
#                            #
##############################


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
        """program: compound_statement DOT"""
        node = self.compound_statement()
        self.eat(DOT)
        return node

    def compound_statement(self):
        """compound_statement: BEGIN statement_list END"""
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

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

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()
        
        return results

    def statement(self):
        """
        statement: compound_statement | assignment_statement | empty
        """
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assginment_statement()
        else:
            node = self.empty()

        return node

    def assginment_statement(self):
        """assignment: variable ASSIGN expr"""
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """variable: ID"""
        node = Var(self.current_token)
        self.eat(ID)
        return node
    
    def empty(self):
        """An empty production rule"""
        return NoOp()
    
    def factor(self):
        """factor: INTEGER"""
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
            return node
    def term(self):
        """term: factor ((MUL | DIV) factor)*"""
        node = self.factor()
        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
            elif token.type == DIVIDE:
                self.eat(DIVIDE)

            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """Parser/Interpreter

        expr: term((PLUS | MINUS) term)*
        term: factor((MUL | DIV) factor)*
        factor: INTEGER
        """
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
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

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIVIDE:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

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
