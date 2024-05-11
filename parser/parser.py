"""
"""

from grammar.grammar import Grammar
from core.classes.ast import AST
from lexer.token_class.token import Token


class Parser:
    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        self.action_table = self._compile_grammar()

    def parse(self, tokens: list[Token]) -> AST:
        pass

    def _compile_grammar(self):
        raise NotImplementedError()
