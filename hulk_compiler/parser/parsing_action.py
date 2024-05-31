"""
This module contains the abstract base class for parsing actions and its subclasses.
"""

from abc import ABC
from dataclasses import dataclass
from .grammar.grammar import NonTerminal, Sentence


class ParsingAction(ABC):
    """
    Abstract base class for parsing actions.
    """

    def __init__(self):
        pass


@dataclass
class Shift(ParsingAction):
    """
    Represents a shift action in the parsing table.

    Attributes:
        next_state (AutomatonState): The state to shift to.
    """

    next_state: int


@dataclass
class Reduce(ParsingAction):
    """
    Represents a reduce action in the parsing table.

    Attributes:
        production (Production): The production to reduce by.
    """

    head: NonTerminal
    body: Sentence


@dataclass
class GoTo(ParsingAction):
    """
    Represents a parsing action that transitions to the next state.

    Attributes:
        next_state (int): The next state to transition to.
    """

    next_state: int


@dataclass
class Accept(ParsingAction):
    """
    Represents an accept action in the parsing table.
    """

    body: Sentence
