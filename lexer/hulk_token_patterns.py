"""
This Module Contains the Hulk language Token Patterns

Important:
    Patterns are made in such a way that there is a hierarchy,
    so the most important patterns or patterns that contain other 
    patterns come first.

    Example :
        if the pattern = come first than the pattern == ,
        the lexer will recognize a == lexema as = lexema

"""

from core.classes.token import TokenType

TOKEN_PATTERNS: dict[str:TokenType] = {
    "/\\*": TokenType.MULTI_LINE_COMMENT_START,
    "\\*/": TokenType.MULTI_LINE_COMMENT_END,
    "\\|\\|": TokenType.DOUBLE_PIPE,
    "\\|": TokenType.OR,
    "&": TokenType.AND,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "elif": TokenType.ELIF,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "let": TokenType.LET,
    "in": TokenType.IN,
    "=>": TokenType.ARROW_OPERATOR,
    "==": TokenType.EQUAL,
    "=": TokenType.ASSIGNMENT,
    ":=": TokenType.DESTRUCTIVE_ASSIGNMENT,
    "new": TokenType.NEW,
    "as": TokenType.AS,
    "String": TokenType.STRING,
    '\\"([^\\"]*)\\"': TokenType.STRING_LITERAL,
    "Number": TokenType.NUMBER,
    "(0\\.[0-9]+)|([1-9][0-9]*\\.?[0-9]*)|(0)": TokenType.NUMBER_LITERAL,
    "Bool": TokenType.BOOL,
    "function": TokenType.FUNCTION,
    "type": TokenType.TYPE,
    "inherits": TokenType.INHERITS,
    "protocol": TokenType.PROTOCOL,
    "extends": TokenType.EXTENDS,
    "\\+": TokenType.PLUS,
    "\\-": TokenType.MINUS,
    "\\*": TokenType.TIMES,
    "\\/": TokenType.DIVIDE,
    "%": TokenType.MOD,
    "\\^": TokenType.POWER,
    "!=": TokenType.NOT_EQUAL,
    "!": TokenType.NOT,
    "<=": TokenType.LESS_THAN_EQUAL,
    ">=": TokenType.GREATER_THAN_EQUAL,
    "<": TokenType.LESS_THAN,
    ">": TokenType.GREATER_THAN,
    "is": TokenType.IS,
    "\\.": TokenType.DOT,
    ":": TokenType.COLON,
    ",": TokenType.COMMA,
    ";": TokenType.SEMI_COLON,
    "\\(": TokenType.LEFT_PARENTHESIS,
    "\\)": TokenType.RIGHT_PARENTHESIS,
    "\\[": TokenType.LEFT_BRACKET,
    "\\]": TokenType.RIGHT_BRACKET,
    "\\{": TokenType.LEFT_BRACE,
    "\\}": TokenType.RIGHT_BRACE,
    "PI": TokenType.PI,
    "E": TokenType.E,
    "true": TokenType.TRUE_LITERAL,
    "false": TokenType.FALSE_LITERAL,
    "//": TokenType.LINE_COMMENT,
    "@@": TokenType.DOUBLE_CONCAT_OPERATOR,
    "@": TokenType.CONCAT_OPERATOR,
    "[a-zA-Z_]([a-zA-Z_0-9])*": TokenType.IDENTIFIER,
}
