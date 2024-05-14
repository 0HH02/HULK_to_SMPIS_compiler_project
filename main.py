"""
"""

# pylint: disable=pointless-statement

from testers.grammar_tester import GrammarTester
from hulk_compiler.parser.grammar.grammar import Grammar, Sentence
from hulk_compiler.parser.grammar.grammar_utils import Item


grammar = Grammar()

eq, plus, num, eof = grammar.set_terminals(["=", "+", "i", "$"])
expr, a, init = grammar.set_non_terminals(["E", "A", "S"])

init <= expr
expr <= a + eq + a | num
a <= num + a | num


tester = GrammarTester(grammar)

# print(tester.run_first_tests())


items = {Item(head=init, body=Sentence([expr]), dot_position=0, lookahead=eof)}

print(
    tester.run_clousure(
        items,
        tester.run_first_tests(),
    )
)
