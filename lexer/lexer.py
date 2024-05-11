"""
This Module define the Lexer class of the Hulk Compiler

The Lexer class is kind of generic because just recive the patterns of the language
and tokenize any string
"""

from token_class.token import TokenPattern, TokenType, Token
from core.exceptions.lexer_exceptions import UnrecognizedTokenException


class Lexer:
    """
    The Lexer class tokenizes input strings based on predefined patterns.

    Args:
        patterns (dict[str:TokenType]): A dictionary mapping patterns to token types.

    """

    def __init__(self, patterns: list[TokenPattern]) -> None:
        self.patterns: list[TokenPattern] = patterns

    def tokenize(self, text: str) -> list[Token]:
        """
        Tokenizes the given string based on the patterns provided.

        Args:
            text: A string of a language to tokenize.

        Returns:
            A list of tokens representing the input string.
        """
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

            for pattern in self.patterns:
                match = pattern.regex_pattern.match(text, i)

                if match:
                    if pattern.follow and match.end() < len(text):
                        if not pattern.follow.match(text, match.end()):
                            continue

                    i = match.end()
                    column = match.end()
                    tokens.append(
                        Token(
                            match.group(),
                            pattern.token_type,
                            line_number=line,
                            column_number=column,
                        )
                    )

                    break
            else:
                raise UnrecognizedTokenException(
                    token=text[i : i + 20], line=line, column=column
                )

        tokens.append(Token("", TokenType.EOF, line, column))
        return tokens
