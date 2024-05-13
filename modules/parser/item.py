"""
"""

from modules.parser.grammar.grammar import NonTerminal, Symbol, Sentence


class Item:
    """
    Represents an item in the parser.
    Args:
        head (NonTerminal): The head of the production rule.
        body (Sentence): The body of the production rule.
        dot_position (int): The position of the dot in the body.
    Raises:
        AssertionError: If the dot position is not within the bounds of the body.
    """

    def __init__(
        self, head: NonTerminal, body: Sentence, dot_position: int, lookahead: Symbol
    ):
        assert 0 <= dot_position <= len(body)
        self.head: NonTerminal = head
        self.body: Sentence = body
        self.dot_position: int = dot_position
        self.lookahead: Symbol = lookahead

    def __eq__(self, other) -> bool:
        return (
            self.head == other.head
            and self.body == other.body
            and self.dot_position == other.dot_position
            and self.lookahead == other.lookahead
        )

    def can_reduce(self) -> bool:
        """
        Determines whether the current production rule can be reduced.

        Returns:
            bool: True if the dot position is at the end of the body, indicating that the rule
            can be reduced.
        """
        return self.dot_position == len(self.body)
