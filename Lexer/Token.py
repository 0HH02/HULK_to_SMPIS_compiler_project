from enum import Enum, auto
import re

class Token:
    """
    Basic token class.

    Parameters
    ----------
    lex : str
        Token's lexeme.
    token_type : Enum
        Token's type.
    """
    
    def __init__(self, lex: str, token_type: Enum, line: int, column: int):
        self.lex = lex
        self.token_type = token_type
        self.line = line
        self.column = column

    def __str__(self):
        return f'{self.token_type}: {self.lex}'

    def __repr__(self):
        return str(self)
 
class TokenPattern:
    """
    Token pattern class.

    Parameters
    ----------
    pattern : str
        Token's pattern.
    follow : str
        Token's follow pattern.
    token_type : Enum
        Token's type.
    """
 
    def __init__(self, token_type: Enum, pattern: str, follow = None):
        self.token_type = token_type
        self.pattern = re.compile(pattern) 
        self.follow = re.compile(follow) if follow else None
      
    def __str__(self):
        return f'{self.token_type}: {self.pattern}'

    def __repr__(self):
        return str(self)

class TokenType(Enum):
    # expressions
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # arithmetic operations
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    POWER_V2 = auto()
    MOD = auto()

    # symbols
    OPEN_BRACES = auto()
    CLOSE_BRACES = auto()
    SEMICOLON = auto()
    OPEN_PARENTHESIS = auto()
    CLOSE_PARENTHESIS = auto()
    ARROW = auto()
    COMMA = auto()
    ASSIGNMENT = auto()
    DESTRUCTIVE_ASSIGNMENT = auto()
    DOT = auto()
    COLON = auto()
    OPEN_BRACKETS = auto()
    CLOSE_BRACKETS = auto()
    DOUBLE_PIPE = auto()
    CONCAT = auto()
    DOUBLE_CONCAT = auto()
    LINEBREAK = auto()
    SPACE = auto()
    TAB = auto()
    ESCAPED_QUOTE = auto()

    # keywords
    FUNCTION = auto()
    LET = auto()
    IN = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    TRUE = auto()
    FALSE = auto()
    WHILE = auto()
    FOR = auto()
    TYPE = auto()
    NEW = auto()
    INHERITS = auto()
    IS = auto()
    AS = auto()
    PROTOCOL = auto()
    EXTENDS = auto()

    # relational
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    EQUAL = auto()
    DIFFERENT = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    EOF = auto()
    
    def __str__(self):
        return self.name
       

    # End of File