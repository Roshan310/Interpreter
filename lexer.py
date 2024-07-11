##############################
#                            #
#         LEXER              #
#                            #
##############################
from constants import TokenType
from tokenizer import Token

RESERVED_KEYWORDS = {
    "PROGRAM": Token(TokenType.PROGRAM.value, "PROGRAM"),
    "VAR": Token(TokenType.VAR.value, "VAR"),
    "DIV": Token(TokenType.INTEGER_DIV.value, "DIV"),
    "INTEGER": Token(TokenType.INTEGER.value, "INTEGER"),
    "REAL": Token(TokenType.REAL.value, "REAL"),
    "BEGIN": Token(TokenType.BEGIN.value, "BEGIN"),
    "END": Token(TokenType.END.value, "END")
    
}


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

