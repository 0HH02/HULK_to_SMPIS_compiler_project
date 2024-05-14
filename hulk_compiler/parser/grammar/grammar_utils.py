"""
"""

from .grammar import Grammar, NonTerminal, Sentence, Symbol


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


class GrammarUtils:
    """
    Utility class for working with grammars.
    """

    @staticmethod
    def get_firsts(grammar: Grammar) -> dict[Symbol, set[Symbol]]:
        """
        Computes the FIRST sets for all symbols in the given grammar.

        Args:
            grammar (Grammar): The grammar for which to compute the FIRST sets.

        Returns:
            dict[Symbol, set[Symbol]]: A dictionary mapping symbols to their FIRST sets.
        """
        first_set: dict[Symbol, set[Symbol]] = {}

        for terminal in grammar.terminals:
            first_set[terminal] = {terminal}

        has_changed = True

        while has_changed:
            has_changed = False
            for head, body in grammar.productions.items():
                for sentence in body:
                    old_len = len(first_set[head])
                    new_first: set = set()

                    for first in first_set[sentence.first]:
                        new_first.add(first)

                    first_set[head].update(new_first)
                    has_changed = (
                        True if len(first_set[head]) == old_len else has_changed
                    )

        return first_set

    @staticmethod
    def get_clousure(
        gramar: Grammar,
        items: set[Item],
        firsts: dict[Symbol, set[Symbol]],
    ) -> set[Item]:
        """
        Computes the closure of a set of items in a grammar.

        Args:
            gramar (Grammar): The grammar object.
            items (set[Item]): The set of items to compute the closure for.
            firsts (dict[Symbol, set[Symbol]]): The first sets of symbols in the grammar.

        Returns:
            set[Item]: The closure of the input set of items.
        """

        has_changed = True
        while has_changed:
            old_len = len(items)
            has_changed = False
            for item in items:
                item_next_production = item.body[item.dot_position]
                if not item_next_production.is_terminal():
                    for head, body in gramar.productions.items():
                        if head == item_next_production:
                            for first in firsts[
                                (
                                    item.body[item.dot_position + 1]
                                    if item.dot_position < len(item.body) - 1
                                    else item.lookahead
                                )
                            ]:
                                items.add(
                                    Item(
                                        head=item_next_production,
                                        body=body,
                                        dot_position=0,
                                        lookahead=first,
                                    )
                                )
            has_changed = True if len(items) != old_len else has_changed
