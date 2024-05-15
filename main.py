"""
"""

# pylint: disable=pointless-statement

from testers.grammar_tester import GrammarTester
from hulk_compiler.parser.grammar.grammar import Grammar, Sentence
from hulk_compiler.parser.grammar.grammar_utils import Item


grammar = Grammar()

plus, semicolon = grammar.set_terminals(["+", ";"])
expr, term = grammar.set_non_terminals(["E", "T"])

expr <= term + plus + ~term + ~semicolon

print(grammar.productions)
