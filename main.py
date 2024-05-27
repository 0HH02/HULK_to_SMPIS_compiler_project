"""
"""

# pylint: disable=pointless-statement

from hulk_compiler.parser.grammar.grammar import Grammar
from hulk_compiler.parser.automaton.automaton import ParserAutomaton

# from hulk_compiler.parser.parser_lr1 import ParserLR1

grammar = Grammar()

equal, plus, num = grammar.set_terminals(["=", "+", "i"])
S, E, A = grammar.set_non_terminals(["S", "E", "A"])

S <= E
E <= A + equal + A | num
A <= num + plus + A | num

grammar.set_seed(S)

automaton = ParserAutomaton(grammar)
