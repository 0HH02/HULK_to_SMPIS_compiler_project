"""
This Module contains the Parser of the Hulk Compiler
"""
from collections import deque
from hulk_compiler.lexer.token import Token, TokenType
from .grammar.grammar import Grammar
from .ast.ast import AST
from .parsing_action import ParsingAction, Item, Shift, Reduce, Accept


class Parser:
    """
    The Parser class is responsible for parsing the input tokens and generating an Abstract Syntax Tree (AST)
    based on the given grammar rules.

    Attributes:
        _grammar (Grammar): The grammar object that defines the production rules.
        action_table (list[dict[TokenType, ParsingAction]]): The action table used for parsing.

    Methods:
        parse(automaton, tokens): Parses the input tokens and returns the generated AST.
        _compile_grammar(): Compiles the grammar rules into an action table.
    """

    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        self.action_table: list[dict[TokenType, ParsingAction]] = (
            self._compile_grammar()
        )

    def parse(self, automaton, tokens: list[Token]) -> AST:
        """
        Parses the input tokens and returns the generated Abstract Syntax Tree (AST).

        Args:
            automaton: The automaton used for parsing.
            tokens (list[Token]): The list of tokens to be parsed.

        Returns:
            AST: The generated Abstract Syntax Tree (AST).
        """
        token_stack: deque[Token] = deque()
        state_stack: deque[int] = deque()
        state_stack.append(0)
        derivations: list[Item] = []
        i = 0
        while True:
            state = state_stack[-1]
            token = tokens[i]
            action: ParsingAction = automaton[state][token]
            if isinstance(action, Shift):
                token_stack.append(token)
                state_stack.append(action.next_state)
                i += 1
            elif isinstance(action, Reduce):
                derivations.append(action.production)
                for _ in range(len(action.production.body)):
                    token_stack.pop()
                    state_stack.pop()
                state = state_stack[-1]
                state_stack.append(action.production.head)
                state_stack.append(automaton[state][action[1]])
            elif isinstance(action, Accept):
                return True
            else:
                return False

    def _compile_grammar(self) -> list[dict[TokenType, ParsingAction]]:
        """
        Compiles the grammar rules into an action table.

        Returns:
            list[dict[TokenType, ParsingAction]]: The compiled action table.
        """
        raise NotImplementedError()
