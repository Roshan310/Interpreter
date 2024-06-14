INTEGER, PLUS, MINUS, DIVIDE, MULTIPLY, EOF = (
    "INTEGER",
    "PLUS",
    "MINUS",
    "DIV",
    "MUL",
    "EOF",
)


class Token:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f"Token({self.type}, {self.value})"

    def __repr__(self) -> str:
        return self.__str__()


class Lexer:
    def __init__(self, text) -> None:
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid character!!!!")

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)

    def get_next_token(self):

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
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

            self.error()

        return Token(EOF, None)


class Interpreter:
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

    def factor(self):
        """factor: INTEGER"""
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def term(self):
        """term: factor ((MUL | DIV) factor)*"""
        result = self.factor()
        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result = result * self.factor()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result = result / self.factor()
        return result

    def expr(self):
        """Parser/Interpreter

        expr: term((PLUS | MINUS) term)*
        term: factor((MUL | DIV) factor)*
        factor: INTEGER
        """
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()

        return result


def main():
    while True:
        try:
            text = input("calc> ")

        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
