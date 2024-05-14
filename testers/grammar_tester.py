"""
"""

from modules.parser.grammar.grammar_utils import GrammarUtils
from modules.parser.grammar.grammar import Grammar

grammar = Grammar()

plus, mul, minus, div = grammar.set_terminals(["+", "*", "-", "/"])
expr, term, factor = grammar.set_non_terminal(["E", "T", "F"])


firsts = GrammarUtils.get_firsts(grammar)
print(firsts)
