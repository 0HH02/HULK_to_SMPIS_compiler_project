from Lexer.Token import Token, TokenPattern

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

    tokens.append(Token("", 'EOF', line, column))
    return tokens
