from enum import Enum


class TokenType(Enum):

    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    BEGIN = "BEGIN"
    END = "END"
    ID = "ID"
    DOT = "DOT"
    SEMI = "SEMI"
    ASSIGN = "ASSIGN"
    COLON = "COLON"
    PROGRAM = "PROGRAM"
    VAR = "VAR"
    COMMA = "COMMA"
    INTEGER_CONST = "INTEGER_CONST"
    REAL_CONST = "REAL_CONST"
    INTEGER_DIV = "INTEGER_DIV"
    FLOAT_DIV = "FLOAT_DIV"
    REAL = "REAL"
    EOF = "EOF"
    # EOF represents end-of-file token which indicate
    # that there is no more input for Lexical Analysis
