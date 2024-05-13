"""
"""

from modules.parser.grammar.grammar import Grammar, Symbol


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
                    for firsts in first_set[sentence.first]:
                        new_first.add(firsts)
                    first_set[head].update(new_first)
                    has_changed = (
                        True if len(first_set[head]) == old_len else has_changed
                    )

        return first_set
