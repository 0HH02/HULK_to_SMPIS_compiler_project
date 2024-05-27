"""
This module contains the exceptions that are raised during parsing.
"""

from .parsing_action import ParsingAction, Reduce


class ParsingError(Exception):
    """
    Exception raised for errors that occur during parsing.

    Attributes:
        args -- the error message(s) passed to the exception
    """

    def __init__(self, *args):
        super().__init__(*args)


class AmbigousGrammarError(ParsingError):
    """
    Exception raised when an ambiguous grammar is encountered during parsing.

    Attributes:
        state (AutomatonState): The state at which the ambiguous grammar was encountered.
        char (str): The character that caused the ambiguity.
        *args: Additional arguments to be passed to the base class constructor.
    """

    def __init__(self, state: int, char: str, *args):
        print(f"Ambiguous grammar at state {state} with char {char}")
        super().__init__(*args)


class ConflictActionError(ParsingError):
    """Exception raised for conflict actions during parsing.

    Attributes:
        state (int): The state where the conflict occurred.
        char (str): The symbol causing the conflict.
        action (ParsingAction): The type of parsing action causing the conflict.
        args: Additional arguments to be passed to the base class constructor.
    """

    def __init__(self, state: int, char: str, action: ParsingAction, *args):
        conflict = "Reduce-Reduce" if action is Reduce else "Shift-Reduce"
        print(f"{conflict} conflict at state {state} with symbol {char}")
        super().__init__(*args)
