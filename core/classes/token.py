from enum import Enum, auto


class Token:
    """
    Represents a token in the compiler.

    Attributes:
        lex (str): The lexeme of the token.
        token_type (str): The type of the token.
    """

    def __init__(self, lex, token_type, line_number, column_number):
        self.lex: str = lex
        self.token_type: TokenType = token_type
        self.line_number: int = line_number
        self.column_number: int = column_number

    def __str__(self):
        return f"Token( Lex:{self.lex}, Type:{self.token_type})"

    def __eq__(self, value: object) -> bool:
        return self.lex == value.lex and self.token_type == value.token_type


class TokenType(Enum):
    """
    Enumeration class representing the different token types used in the compiler.
    """

    # Logical Operators
    AND = auto()
    OR = auto()
    NOT = auto()

    # Conditional Statements
    IF = auto()
    ELSE = auto()
    ELIF = auto()

    # Loop Statements
    WHILE = auto()
    FOR = auto()

    # Variable Declaration
    LET = auto()
    IN = auto()
    ASSIGNMENT = auto()
    DESTRUCTIVE_ASSIGNMENT = auto()
    NEW = auto()
    AS = auto()
    IDENTIFIER = auto()

    # Data Types
    STRING = auto()
    NUMBER = auto()
    BOOL = auto()
    FUNCTION = auto()
    TYPE = auto()
    INHERITS = auto()
    PROTOCOL = auto()
    EXTENDS = auto()

    # Literals
    STRING_LITERAL = auto()
    NUMBER_LITERAL = auto()
    TRUE_LITERAL = auto()
    FALSE_LITERAL = auto()

    # Arithmetic Operators
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    MOD = auto()
    POWER = auto()

    # Relational Operators
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_THAN_EQUAL = auto()
    GREATER_THAN_EQUAL = auto()
    IS = auto()

    # Punctuation
    DOT = auto()
    COLON = auto()
    COMMA = auto()
    SEMI_COLON = auto()
    LEFT_PARENTHESIS = auto()
    RIGHT_PARENTHESIS = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    # Mathematical constants
    PI = auto()
    E = auto()

    # Special Operators
    CONCAT_OPERATOR = auto()
    DOUBLE_CONCAT_OPERATOR = auto()
    ARROW_OPERATOR = auto()

    # Others
    LINE_COMMENT = auto()
    MULTI_LINE_COMMENT_START = auto()
    MULTI_LINE_COMMENT_END = auto()
    EOF = auto()
