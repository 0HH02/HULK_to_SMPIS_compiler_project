"""
"""

from grammar import Grammar, Symbol


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
        first: dict[Symbol, set[Symbol]] = {}

        for terminal in grammar.terminals:
            first[terminal] = {terminal}

        for head, body in grammar.productions.items():
            for sentence in body:
                if not first[head]:
                    first[head] = sentence[0]

        return first
