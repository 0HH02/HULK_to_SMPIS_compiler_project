"""
This module contains the abstract base class for parsing actions and its subclasses.
"""

import abc


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

    def __init__(self, production):
        self.production = production
