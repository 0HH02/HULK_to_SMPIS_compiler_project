"""
"""

from hulk_compiler.parser.grammar.grammar import Grammar
from hulk_compiler.parser.grammar.grammar_utils import GrammarUtils


class GrammarTester:
    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar

    def run_first_tests(self):
        return GrammarUtils.get_firsts(self.grammar)

    def run_clousure(self, items, first):
        return GrammarUtils.get_clousure(self.grammar, items, first)
