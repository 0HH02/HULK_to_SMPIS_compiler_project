"""
This Module is for define Lexer Exceptions
"""


class UnrecognizedTokenException(Exception):
    """
    Exception raised when an unrecognized token is encountered during lexing.

    Attributes:
        token (str): The error message associated with the exception.
    """

    def __init__(self, token, line, column, *args: object) -> None:
        print(f"Unrecognized token {token} at line {line}, column {column}.")
        super().__init__(*args)
