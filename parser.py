
##############################
#                            #
#           PARSER           #
#                            #
##############################
from constants import TokenType
from ast_ import *

class Parser:
    def __init__(self, lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Error parsing Input")

    def eat(self, token_type):
        print(f"Current token: {self.current_token}, Expected: {token_type}")
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            print("SORRY BROTHER NO TOKEN MATCHED!!")
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
        """declarations: VAR (variable declaration SEMI)+ | 
        (PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI)* | empty"""
        declarations = []

        while True:
            if self.current_token.type == TokenType.VAR.value:
                self.eat(TokenType.VAR.value)
                while self.current_token.type == TokenType.ID.value:
                    var_decl = self.variable_declaration()
                    declarations.extend(var_decl)
                    self.eat(TokenType.SEMI.value)

            elif self.current_token.type == TokenType.PROCEDURE.value:
                self.eat(TokenType.PROCEDURE.value)
                proc_name = self.current_token.value
                self.eat(TokenType.ID.value)
                self.eat(TokenType.SEMI.value)
                block_node = self.block()
                proc_decl = ProcedureDecl(proc_name, block_node)
                declarations.append(proc_decl)
                self.eat(TokenType.SEMI.value)
            
            else:
                break

        return declarations

    def formal_parameter_list(self):
        """formal_parameter_list: formal_parameters | formal_parameters SEMI formal_parameter_list """
        pass

    def formal_parameters(self):
        """formal_parameters: ID (COMMA ID)* COLON type_spec"""
        param_nodes = []
        
    def variable_declaration(self):
        """variable_declaration: ID (COMMA ID)* COLON type_spec"""
    
        var_nodes = [Var(self.current_token)]
        self.eat(TokenType.ID.value)

        while self.current_token.type == TokenType.COMMA.value:
            self.eat(TokenType.COMMA.value)
            var_nodes.append(Var(self.current_token))
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
