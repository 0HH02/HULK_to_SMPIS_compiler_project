from Token import Token, TokenPattern, TokenType

def lexer(token_patterns: list[TokenPattern], text: str) -> list[Token]:
    tokens = []
    line = 0
    column = 0

    i = 0
    while i < len(text):
        if text[i] == "\n":
            i += 1
            line += 1
            column = 0
            continue

        if text[i] == " ":
            i += 1
            column += 1
            continue

        if text[i] == "\t":
            i += 1
            column += 4
            continue

        for token_pattern in token_patterns:
            match = token_pattern.pattern.match(text, i)

            if match:
                if token_pattern.follow and match.end() < len(text):
                    if not token_pattern.follow.match(text, match.end()):
                        continue

                i = match.end()
                column = match.end()
                tokens.append(Token(match.group(), token_pattern.token_type, line, column))

                break
        else:
            raise Exception(f"Unrecognized token at line {line}, column {column}.")

    tokens.append(Token("", TokenType.EOF, line, column))
    return tokens

non_letter = r"[^a-zA-Z_]"
patterns = [
    TokenPattern(TokenType.FUNCTION, r"function", non_letter),
    TokenPattern(TokenType.LET, r"let", non_letter),
    TokenPattern(TokenType.IN, r"in", non_letter),
    TokenPattern(TokenType.IF, r"if", non_letter),
    TokenPattern(TokenType.ELIF, r"elif", non_letter),
    TokenPattern(TokenType.ELSE, r"else", non_letter),
    TokenPattern(TokenType.TRUE, r"true", non_letter),
    TokenPattern(TokenType.FALSE, r"false", non_letter),
    TokenPattern(TokenType.WHILE, r"while", non_letter),
    TokenPattern(TokenType.FOR, r"for", non_letter),
    TokenPattern(TokenType.TYPE, r"type", non_letter),
    TokenPattern(TokenType.NEW, r"new", non_letter),
    TokenPattern(TokenType.INHERITS, r"inherits", non_letter),
    TokenPattern(TokenType.IS, r"is", non_letter),
    TokenPattern(TokenType.AS, r"as", non_letter),
    TokenPattern(TokenType.PROTOCOL, r"protocol", non_letter),
    TokenPattern(TokenType.EXTENDS, r"extends", non_letter),
    TokenPattern(TokenType.NUMBER, r"(0\.[0-9]+)|([1-9][0-9]*\.?[0-9]*)"),
    TokenPattern(TokenType.STRING, r"\"([^\"]*)\""),
    TokenPattern(TokenType.IDENTIFIER, r"[a-zA-Z_]([a-zA-Z_0-9])*"),
    TokenPattern(TokenType.PLUS, r"\+"),
    TokenPattern(TokenType.MINUS, r"\-"),
    TokenPattern(TokenType.MULTIPLY, r"\*"),
    TokenPattern(TokenType.DIVIDE, r"\/"),
    TokenPattern(TokenType.POWER, r"\^"),
    TokenPattern(TokenType.POWER_V2, r"\*\*"),
    TokenPattern(TokenType.MOD, r"%"),
    TokenPattern(TokenType.OPEN_BRACES, r'\{'),
    TokenPattern(TokenType.CLOSE_BRACES, r'\}'),
    TokenPattern(TokenType.SEMICOLON, r";"),
    TokenPattern(TokenType.OPEN_PARENTHESIS, r"\("),
    TokenPattern(TokenType.CLOSE_PARENTHESIS, r"\)"),
    TokenPattern(TokenType.ARROW, r"=>"),
    TokenPattern(TokenType.COMMA, r","),
    TokenPattern(TokenType.ASSIGNMENT, r"="),
    TokenPattern(TokenType.DESTRUCTIVE_ASSIGNMENT, r":="),
    TokenPattern(TokenType.DOT, r"\."),
    TokenPattern(TokenType.COLON, r":"),
    TokenPattern(TokenType.OPEN_BRACKETS, r"\["),
    TokenPattern(TokenType.CLOSE_BRACKETS, r"\]"),
    TokenPattern(TokenType.DOUBLE_PIPE, r"\|\|"),
    TokenPattern(TokenType.CONCAT, r"@"),
    TokenPattern(TokenType.DOUBLE_CONCAT, r"@@"),
    TokenPattern(TokenType.GREATER, r">"),
    TokenPattern(TokenType.GREATER_EQUAL, r">="),
    TokenPattern(TokenType.LESS, r"<"),
    TokenPattern(TokenType.LESS_EQUAL, r"<="),
    TokenPattern(TokenType.EQUAL, r"=="),
    TokenPattern(TokenType.DIFFERENT, r"!="),
    TokenPattern(TokenType.AND, r"&"),
    TokenPattern(TokenType.OR, r"\|"),
    TokenPattern(TokenType.NOT, r"!")
]

# test
text = "function 1 2.2 2.03 15.25 0.5255 0.001 let in if elif else true false while for type new inherits is as protocol extends"
tokens = lexer(patterns, text)
print(tokens)
print(len(tokens))