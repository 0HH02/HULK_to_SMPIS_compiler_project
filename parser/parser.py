"""
"""

from grammar.grammar import Grammar
from core.classes.ast import AST
from lexer.token_class.token import Token


class Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    def parse(self, tokens: list[Token]) -> AST:
        pass
