from lexer.lexer import Lexer
from core.classes.token import Token, TokenType

TESTS: dict[str:Token] = {
    'let a = 42 in if (a % 2 == 0) print("Even") else print("odd");': [
        Token("let", TokenType.LET, 1, 1),
        Token("a", TokenType.IDENTIFIER, 1, 5),
        Token("=", TokenType.ASSIGNMENT, 1, 7),
        Token("42", TokenType.NUMBER_LITERAL, 1, 9),
        Token("in", TokenType.IN, 1, 12),
        Token("if", TokenType.IF, 1, 15),
        Token("(", TokenType.LEFT_PARENTHESIS, 1, 18),
        Token("a", TokenType.IDENTIFIER, 1, 19),
        Token("%", TokenType.MOD, 1, 21),
        Token("2", TokenType.NUMBER_LITERAL, 1, 23),
        Token("==", TokenType.EQUAL, 1, 26),
        Token("0", TokenType.NUMBER_LITERAL, 1, 29),
        Token(")", TokenType.RIGHT_PARENTHESIS, 1, 30),
        Token("print", TokenType.IDENTIFIER, 1, 32),
        Token("(", TokenType.LEFT_PARENTHESIS, 1, 37),
        Token('"Even"', TokenType.STRING_LITERAL, 1, 38),
        Token(")", TokenType.RIGHT_PARENTHESIS, 1, 45),
        Token("else", TokenType.ELSE, 1, 47),
        Token("print", TokenType.IDENTIFIER, 1, 52),
        Token("(", TokenType.LEFT_PARENTHESIS, 1, 57),
        Token('"odd"', TokenType.STRING_LITERAL, 1, 58),
        Token(")", TokenType.RIGHT_PARENTHESIS, 1, 64),
    ],
    """
    let iterable = range(0, 10) in
        while (iterable.next())
            let x = iterable.current() in
                print(x);'
    """: [
        Token("let", TokenType.LET, 1, 1),
        Token("iterable", TokenType.IDENTIFIER, 1, 5),
        Token("=", TokenType.ASSIGNMENT, 1, 14),
        Token("range", TokenType.IDENTIFIER, 1, 16),
        Token("(", TokenType.LEFT_PARENTHESIS, 1, 21),
        Token("0", TokenType.NUMBER_LITERAL, 1, 22),
        Token(",", TokenType.COMMA, 1, 23),
        Token("10", TokenType.NUMBER_LITERAL, 1, 25),
        Token(")", TokenType.RIGHT_PARENTHESIS, 1, 27),
        Token("in", TokenType.IN, 1, 29),
        Token("while", TokenType.WHILE, 2, 5),
        Token("(", TokenType.LEFT_PARENTHESIS, 2, 11),
        Token("iterable", TokenType.IDENTIFIER, 2, 12),
        Token(".", TokenType.DOT, 2, 21),
        Token("next", TokenType.IDENTIFIER, 2, 22),
        Token("(", TokenType.LEFT_PARENTHESIS, 2, 26),
        Token(")", TokenType.RIGHT_PARENTHESIS, 2, 27),
        Token(")", TokenType.RIGHT_PARENTHESIS, 2, 28),
        Token("let", TokenType.LET, 3, 9),
        Token("x", TokenType.IDENTIFIER, 3, 13),
        Token("=", TokenType.ASSIGNMENT, 3, 15),
        Token("iterable", TokenType.IDENTIFIER, 3, 17),
        Token(".", TokenType.DOT, 3, 26),
        Token("current", TokenType.IDENTIFIER, 3, 27),
        Token("(", TokenType.LEFT_PARENTHESIS, 3, 34),
        Token(")", TokenType.RIGHT_PARENTHESIS, 3, 35),
        Token("in", TokenType.IN, 3, 37),
        Token("print", TokenType.IDENTIFIER, 4, 9),
        Token("(", TokenType.LEFT_PARENTHESIS, 4, 14),
        Token("x", TokenType.IDENTIFIER, 4, 15),
        Token(")", TokenType.RIGHT_PARENTHESIS, 4, 16),
    ],
}


class LexerTester:
    """
    A class for testing the Lexer class.

    Attributes:
        lexer (Lexer): The Lexer object to be tested.
    """

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer

    def run_tests(self) -> None:
        """
        Runs the tests for the lexer.

        This method iterates over the TESTS dictionary and tokenizes each test case using the lexer.
        It then compares the generated tokens with the expected tokens from the TESTS dictionary.
        If any token does not match the expected token, an assertion error is raised.

        Raises:
            AssertionError: If any token does not match the expected token.

        Returns:
            None
        """
        for i, test in enumerate(TESTS):
            tokens = self.lexer.tokenize()
            for j, token in enumerate(tokens):
                assert (
                    token == TESTS[test][j]
                ), f"Test {i} failed. Expected {TESTS[test][j]}, got {token}"
