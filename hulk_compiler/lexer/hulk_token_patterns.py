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

from .token import TokenPattern, TokenType

_NOT_LETTER_OR_UNDERSCORE = "[^a-zA-Z_]"


TOKEN_PATTERNS = [
    TokenPattern("/\\*", TokenType.MULTI_LINE_COMMENT_START),
    TokenPattern("\\*/", TokenType.MULTI_LINE_COMMENT_END),
    TokenPattern("\\|\\|", TokenType.DOUBLE_PIPE),
    TokenPattern("\\|", TokenType.OR),
    TokenPattern("&", TokenType.AND),
    TokenPattern("if", TokenType.IF, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("else", TokenType.ELSE, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("elif", TokenType.ELIF, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("while", TokenType.WHILE, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("for", TokenType.FOR, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("let", TokenType.LET, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("in", TokenType.IN, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("=>", TokenType.ARROW_OPERATOR),
    TokenPattern("==", TokenType.EQUAL),
    TokenPattern("=", TokenType.ASSIGNMENT, "[^=>]"),
    TokenPattern(":=", TokenType.DESTRUCTIVE_ASSIGNMENT),
    TokenPattern("new", TokenType.NEW, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("as", TokenType.AS, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("String", TokenType.STRING, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern('\\"([^\\"]*)\\"', TokenType.STRING_LITERAL),
    TokenPattern("Number", TokenType.NUMBER, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("(0\\.[0-9]+)|([1-9][0-9]*\\.?[0-9]*)|(0)", TokenType.NUMBER_LITERAL),
    TokenPattern("Bool", TokenType.BOOLEAN, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("function", TokenType.FUNCTION, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("type", TokenType.TYPE, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("inherits", TokenType.INHERITS, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("protocol", TokenType.PROTOCOL, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("extends", TokenType.EXTENDS, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("(\\^|\\*\\*)", TokenType.POWER),
    TokenPattern("\\+", TokenType.PLUS),
    TokenPattern("\\-", TokenType.MINUS),
    TokenPattern("\\*", TokenType.TIMES, "[^\\*]"),
    TokenPattern("\\/", TokenType.DIVIDE),
    TokenPattern("%", TokenType.MOD),
    TokenPattern("!=", TokenType.NOT_EQUAL),
    TokenPattern("!", TokenType.NOT, "[^=]"),
    TokenPattern("<=", TokenType.LESS_THAN_EQUAL),
    TokenPattern(">=", TokenType.GREATER_THAN_EQUAL),
    TokenPattern("<", TokenType.LESS_THAN, "[^=]"),
    TokenPattern(">", TokenType.GREATER_THAN, "[^=]"),
    TokenPattern("is", TokenType.IS, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("\\.", TokenType.DOT),
    TokenPattern(":", TokenType.COLON, "[^=]"),
    TokenPattern(",", TokenType.COMMA),
    TokenPattern(";", TokenType.SEMI_COLON),
    TokenPattern("\\(", TokenType.LEFT_PARENTHESIS),
    TokenPattern("\\)", TokenType.RIGHT_PARENTHESIS),
    TokenPattern("\\[", TokenType.LEFT_BRACKET),
    TokenPattern("\\]", TokenType.RIGHT_BRACKET),
    TokenPattern("\\{", TokenType.LEFT_BRACE),
    TokenPattern("\\}", TokenType.RIGHT_BRACE),
    TokenPattern("PI", TokenType.PI, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("E", TokenType.E, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("true", TokenType.TRUE_LITERAL, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("false", TokenType.FALSE_LITERAL, _NOT_LETTER_OR_UNDERSCORE),
    TokenPattern("//", TokenType.LINE_COMMENT),
    TokenPattern("@@", TokenType.DOUBLE_CONCAT_OPERATOR),
    TokenPattern("@", TokenType.CONCAT_OPERATOR, "[^@]"),
    TokenPattern("[a-zA-Z_]([a-zA-Z_0-9])*", TokenType.IDENTIFIER),
]
