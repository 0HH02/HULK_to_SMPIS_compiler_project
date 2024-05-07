from core.classes.token import TokenType, Token


class Lexer:
    """
    The Lexer class tokenizes input strings based on predefined patterns.

    Args:
        patterns (dict[str:TokenType]): A dictionary mapping patterns to token types.

    Attributes:
        patterns (dict[str:TokenType]): A dictionary mapping patterns to token types.

    """

    def __init__(self, patterns: dict[str:TokenType]) -> None:
        self.patterns: dict[str:TokenType] = patterns

    def tokenize(self, text: str) -> list[Token]:
        """
        Tokenizes the given string based on the patterns provided.

        Args:
            text: A string of a language to tokenize.

        Returns:
            A list of tokens representing the input string.
        """
