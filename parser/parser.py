"""
This Module contains the Parser of the Hulk Compiler
"""

from parsing_action import ParsingAction
from grammar.grammar import Grammar
from core.classes.ast import AST
from lexer.token_class.token import Token, TokenType


class Parser:
    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        self.action_table: list[dict[TokenType, ParsingAction]] = (
            self._compile_grammar()
        )

    def parse(self, tokens: list[Token]) -> AST:
        pass

    def _compile_grammar(self) -> list[dict[TokenType, ParsingAction]]:
        raise NotImplementedError()
