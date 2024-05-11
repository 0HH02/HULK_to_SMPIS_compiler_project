"""
This is a module for the purpose of testing the lexer class
"""

from lexer.lexer import Lexer
from core.classes.token import Token, TokenType

TESTS: dict[str:Token] = {
    'let a= 42 in if(a %2 ==0) print( "   Even") else print("odd") ;': [
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
        Token('"   Even"', TokenType.STRING_LITERAL, 1, 38),
        Token(")", TokenType.RIGHT_PARENTHESIS, 1, 45),
        Token("else", TokenType.ELSE, 1, 47),
        Token("print", TokenType.IDENTIFIER, 1, 52),
        Token("(", TokenType.LEFT_PARENTHESIS, 1, 57),
        Token('"odd"', TokenType.STRING_LITERAL, 1, 58),
        Token(")", TokenType.RIGHT_PARENTHESIS, 1, 64),
        Token(";", TokenType.SEMI_COLON, 1, 65),
        Token("", TokenType.EOF, 1, 65),
    ],
    """
    let iterable= range(  0,10)in
        while(iterable.next ( ) )
            let x= iterable.current()in
                print( x ) ;
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
        Token(";", TokenType.SEMI_COLON, 4, 17),
        Token("", TokenType.EOF, 4, 16),
    ],
    """
    type Range(min:   Number,max:Number){
        min=min     ;
        max = max;
        current=min-1;

        next(  )   : Bool => (self.current := self.current+ 1 )< max;
        current(  ):Number => self.    current;
    """: [
        Token("type", TokenType.TYPE, 1, 1),
        Token("Range", TokenType.IDENTIFIER, 1, 6),
        Token("(", TokenType.LEFT_PARENTHESIS, 1, 11),
        Token("min", TokenType.IDENTIFIER, 1, 12),
        Token(":", TokenType.COLON, 1, 15),
        Token("Number", TokenType.NUMBER, 1, 17),
        Token(",", TokenType.COMMA, 1, 23),
        Token("max", TokenType.IDENTIFIER, 1, 25),
        Token(":", TokenType.COLON, 1, 28),
        Token("Number", TokenType.NUMBER, 1, 30),
        Token(")", TokenType.RIGHT_PARENTHESIS, 1, 36),
        Token("{", TokenType.LEFT_BRACE, 1, 38),
        Token("min", TokenType.IDENTIFIER, 2, 9),
        Token("=", TokenType.ASSIGNMENT, 2, 13),
        Token("min", TokenType.IDENTIFIER, 2, 15),
        Token(";", TokenType.SEMI_COLON, 2, 18),
        Token("max", TokenType.IDENTIFIER, 3, 9),
        Token("=", TokenType.ASSIGNMENT, 3, 13),
        Token("max", TokenType.IDENTIFIER, 3, 15),
        Token(";", TokenType.SEMI_COLON, 3, 18),
        Token("current", TokenType.IDENTIFIER, 4, 9),
        Token("=", TokenType.ASSIGNMENT, 4, 17),
        Token("min", TokenType.IDENTIFIER, 4, 19),
        Token("-", TokenType.MINUS, 4, 23),
        Token("1", TokenType.NUMBER_LITERAL, 4, 25),
        Token(";", TokenType.SEMI_COLON, 4, 26),
        Token("next", TokenType.IDENTIFIER, 6, 9),
        Token("(", TokenType.LEFT_PARENTHESIS, 6, 13),
        Token(")", TokenType.RIGHT_PARENTHESIS, 6, 14),
        Token(":", TokenType.COLON, 6, 16),
        Token("Bool", TokenType.BOOL, 6, 19),
        Token("=>", TokenType.ARROW_OPERATOR, 6, 26),
        Token("(", TokenType.LEFT_PARENTHESIS, 6, 29),
        Token("self", TokenType.IDENTIFIER, 6, 30),
        Token(".", TokenType.DOT, 6, 34),
        Token("current", TokenType.IDENTIFIER, 6, 35),
        Token(":=", TokenType.DESTRUCTIVE_ASSIGNMENT, 6, 43),
        Token("self", TokenType.IDENTIFIER, 6, 46),
        Token(".", TokenType.DOT, 6, 50),
        Token("current", TokenType.IDENTIFIER, 6, 51),
        Token("+", TokenType.PLUS, 6, 58),
        Token("1", TokenType.NUMBER_LITERAL, 6, 60),
        Token(")", TokenType.RIGHT_PARENTHESIS, 6, 61),
        Token("<", TokenType.LESS_THAN, 6, 63),
        Token("max", TokenType.IDENTIFIER, 6, 65),
        Token(";", TokenType.SEMI_COLON, 6, 68),
        Token("current", TokenType.IDENTIFIER, 7, 9),
        Token("(", TokenType.LEFT_PARENTHESIS, 7, 16),
        Token(")", TokenType.RIGHT_PARENTHESIS, 7, 17),
        Token(":", TokenType.COLON, 7, 19),
        Token("Number", TokenType.NUMBER, 7, 21),
        Token("=>", TokenType.ARROW_OPERATOR, 7, 28),
        Token("self", TokenType.IDENTIFIER, 7, 31),
        Token(".", TokenType.DOT, 7, 35),
        Token("current", TokenType.IDENTIFIER, 7, 36),
        Token(";", TokenType.SEMI_COLON, 7, 43),
        Token("", TokenType.EOF, 7, 43),
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
            tokens = self.lexer.tokenize(test)
            for j, token in enumerate(tokens):
                expected_token = TESTS[test][j]

                assert (
                    token == expected_token
                ), f"Test {i} failed. Expected {TESTS[test][j]}, got {token}"

            print(f"passed testers [{i+1} / {len(TESTS)}]")
