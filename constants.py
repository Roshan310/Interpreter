from enum import Enum


class TokenType(Enum):

    ASSIGN = "ASSIGN"
    BEGIN = "BEGIN"
    COLON = "COLON"
    COMMA = "COMMA"
    DOT = "DOT"
    END = "END"
    EOF = "EOF"
    FLOAT_DIV = "FLOAT_DIV"
    ID = "ID"
    INTEGER = "INTEGER"
    INTEGER_CONST = "INTEGER_CONST"
    INTEGER_DIV = "INTEGER_DIV"
    LPAREN = "LPAREN"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    PLUS = "PLUS"
    PROCEDURE = "PROCEDURE"
    PROGRAM = "PROGRAM"
    REAL = "REAL"
    REAL_CONST = "REAL_CONST"
    RPAREN = "RPAREN"
    SEMI = "SEMI"
    VAR = "VAR"
    # EOF represents end-of-file token which indicate
    # that there is no more input for Lexical Analysis
