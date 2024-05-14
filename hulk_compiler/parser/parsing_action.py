"""
This module contains the abstract base class for parsing actions and its subclasses.
"""

import abc
from .grammar.grammar_utils import Item


class ParsingAction(abc.ABC):
    """
    Abstract base class for parsing actions.
    """

    @abs.abstractmethod
    def __init__(self):
        pass


class Shift(ParsingAction):
    """
    Represents a shift action in the parsing table.

    Attributes:
        next_state (AutomatonState): The state to shift to.
    """

    def __init__(self, next_state):
        self.next_state = next_state


class Reduce(ParsingAction):
    """
    Represents a reduce action in the parsing table.

    Attributes:
        production (Production): The production to reduce by.
    """

    def __init__(self, item: Item, next_state: int):
        self.production = item
        self.next_state: int = next_state


class Accept(ParsingAction):
    """
    Represents an accept action in the parsing table.
    """

    def __init__(self):
        pass
