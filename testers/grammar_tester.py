from parser.grammar.grammar import Grammar

grammar = Grammar()

plus, mul, minus, div = grammar.set_terminals(["+", "*", "-", "/"])
