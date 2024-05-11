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

from lexer.token_class.token import TokenPattern, TokenType


TOKEN_PATTERNS = [
    TokenPattern("/\\*", TokenType.MULTI_LINE_COMMENT_START),
    TokenPattern("\\*/", TokenType.MULTI_LINE_COMMENT_END),
    TokenPattern("\\|\\|", TokenType.DOUBLE_PIPE),
    TokenPattern("\\|", TokenType.OR),
    TokenPattern("&", TokenType.AND),
    TokenPattern("if", TokenType.IF, "[^a-zA-Z_]"),
    TokenPattern("else", TokenType.ELSE, "[^a-zA-Z_]"),
    TokenPattern("elif", TokenType.ELIF, "[^a-zA-Z_]"),
    TokenPattern("while", TokenType.WHILE, "[^a-zA-Z_]"),
    TokenPattern("for", TokenType.FOR, "[^a-zA-Z_]"),
    TokenPattern("let", TokenType.LET, "[^a-zA-Z_]"),
    TokenPattern("in", TokenType.IN, "[^a-zA-Z_]"),
    TokenPattern("=>", TokenType.ARROW_OPERATOR),
    TokenPattern("==", TokenType.EQUAL),
    TokenPattern("=", TokenType.ASSIGNMENT, "[^(=|>)]"),
    TokenPattern(":=", TokenType.DESTRUCTIVE_ASSIGNMENT),
    TokenPattern("new", TokenType.NEW, "[^a-zA-Z_]"),
    TokenPattern("as", TokenType.AS, "[^a-zA-Z_]"),
    TokenPattern("String", TokenType.STRING, "[^a-zA-Z_]"),
    TokenPattern('\\"([^\\"]*)\\"', TokenType.STRING_LITERAL),
    TokenPattern("Number", TokenType.NUMBER, "[^a-zA-Z_]"),
    TokenPattern("(0\\.[0-9]+)|([1-9][0-9]*\\.?[0-9]*)|(0)", TokenType.NUMBER_LITERAL),
    TokenPattern("Bool", TokenType.BOOLEAN, "[^a-zA-Z_]"),
    TokenPattern("function", TokenType.FUNCTION, "[^a-zA-Z_]"),
    TokenPattern("type", TokenType.TYPE, "[^a-zA-Z_]"),
    TokenPattern("inherits", TokenType.INHERITS, "[^a-zA-Z_]"),
    TokenPattern("protocol", TokenType.PROTOCOL, "[^a-zA-Z_]"),
    TokenPattern("extends", TokenType.EXTENDS, "[^a-zA-Z_]"),
    TokenPattern("(\\^ | \\*\\*)", TokenType.POWER),
    TokenPattern("\\+", TokenType.PLUS),
    TokenPattern("\\-", TokenType.MINUS),
    TokenPattern("\\*", TokenType.TIMES, "^\\*"),
    TokenPattern("\\/", TokenType.DIVIDE),
    TokenPattern("%", TokenType.MOD),
    TokenPattern("!=", TokenType.NOT_EQUAL),
    TokenPattern("!", TokenType.NOT, "[^=]"),
    TokenPattern("<=", TokenType.LESS_THAN_EQUAL),
    TokenPattern(">=", TokenType.GREATER_THAN_EQUAL),
    TokenPattern("<", TokenType.LESS_THAN, "[^=]"),
    TokenPattern(">", TokenType.GREATER_THAN, "[^=]"),
    TokenPattern("is", TokenType.IS, "[^a-zA-Z_]"),
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
    TokenPattern("PI", TokenType.PI, "[^a-zA-Z_]"),
    TokenPattern("E", TokenType.E, "[^a-zA-Z_]"),
    TokenPattern("true", TokenType.TRUE_LITERAL, "[^a-zA-Z_]"),
    TokenPattern("false", TokenType.FALSE_LITERAL, "[^a-zA-Z_]"),
    TokenPattern("//", TokenType.LINE_COMMENT),
    TokenPattern("@@", TokenType.DOUBLE_CONCAT_OPERATOR),
    TokenPattern("@", TokenType.CONCAT_OPERATOR, "^@"),
    TokenPattern("[a-zA-Z_]([a-zA-Z_0-9])*", TokenType.IDENTIFIER),
]
