"""
This Module contains the Parser of the Hulk Compiler
"""

from collections import deque
from hulk_compiler.lexer.token import Token
from .grammar.grammar import Grammar, Symbol, Sentence
from .grammar.grammar_utils import GrammarUtils, Item
from .ast.ast import AST
from .parsing_action import ParsingAction, Shift, Reduce, Accept, GoTo
from .parser_exceptions import AmbigousGrammarError, ConflictActionError


class ParserLR1:
    """
    The Parser class is responsible for parsing the input tokens and generating an
    Abstract Syntax Tree (AST)based on the given grammar rules.

    Attributes:
        _grammar (Grammar): The grammar object that defines the production rules.
        action_table (list[dict[Symbol, ParsingAction]]): The action table used for parsing.

    Methods:
        parse(automaton, tokens): Parses the input tokens and returns the generated AST.
        _compile_grammar(): Compiles the grammar rules into an action table.
    """

    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        self._action_table: dict[int, dict[Symbol, ParsingAction]] = (
            self._compile_grammar()
        )

    def parse(self, automaton, tokens: list[Token]) -> AST:
        """
        #### Parses the input tokens and returns the generated Abstract Syntax Tree (AST).

        ### Args:
            automaton: The automaton used for parsing.
            tokens (list[Token]): The list of tokens to be parsed.

        ### Returns:
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

    def _compile_grammar(self) -> dict[int, dict[Symbol, ParsingAction]]:
        """
        Compiles the grammar rules into an action table.

        Returns:
            list[dict[Symbol, ParsingAction]]: The compiled action table.
        """

        states, go_to_table = self._build_states()

        action_table: dict[int, dict[Symbol, ParsingAction]] = []

        for num_state, state_items in states.items():
            action_table[num_state] = {}
            state = action_table[num_state]
            for item in state_items:
                if item.can_reduce:
                    if item.head == self._grammar.special_seed:
                        if not self._grammar.eof in state:
                            state[self._grammar.eof] = Accept()
                        else:
                            raise ConflictActionError(
                                num_state, self._grammar.eof, state[self._grammar.eof]
                            )

                    else:
                        if not item.lookahead in state:
                            state[item.lookahead] = Reduce(item.head, item.body)
                        else:
                            raise ConflictActionError(
                                num_state, item.lookahead, state[item.lookahead]
                            )
                else:
                    if item.next_symbol.is_terminal():
                        if not item.next_symbol in state:
                            state[item.next_symbol] = Shift(
                                go_to_table[num_state][item.next_symbol]
                            )
                        else:
                            raise AmbigousGrammarError(num_state, item.next_symbol)
                    else:
                        if not item.next_symbol in state:
                            state[item.next_symbol] = GoTo(
                                go_to_table[num_state][item.next_symbol]
                            )
                        else:
                            raise AmbigousGrammarError(num_state, item.next_symbol)

        return action_table

    def _build_states(self):
        firsts: dict[Symbol, set[Symbol]] = GrammarUtils.get_firsts(self._grammar)

        init_item = Item(
            self._grammar.special_seed,
            Sentence([self._grammar.seed]),
            0,
            self._grammar.eof,
        )

        actual_state_items: set[Item] = GrammarUtils.get_clousure(
            self._grammar,
            {init_item},
            firsts,
        )

        num_states: int = 1

        states: dict[int, set[Item]] = {0: actual_state_items}

        states_kernels: dict[frozenset[Item], int] = {frozenset([init_item]): 0}

        go_to: dict[int, dict[Symbol, int]] = {}

        count: int = 0

        while count < num_states:
            actual_state_items = states[count]

            for symbol in self._grammar.symbols:
                new_kernel: set[Item] = set()
                for item in actual_state_items:
                    if item.next_symbol == symbol:
                        new_kernel.add(item)

                if len(new_kernel) == 0:
                    continue

                new_kernel = frozenset(new_kernel)

                if new_kernel in states_kernels:
                    if count in go_to:
                        go_to[count][symbol] = states_kernels[new_kernel]
                    else:
                        go_to[count] = {symbol: states_kernels[new_kernel]}
                    continue

                new_items: set[Item] = GrammarUtils.get_clousure(
                    self._grammar,
                    {item.move_dot() for item in new_kernel},
                    firsts,
                )
                states[num_states] = new_items
                if count in go_to:
                    go_to[count][symbol] = num_states
                else:
                    go_to[count] = {symbol: num_states}

                states_kernels[new_kernel] = num_states

                num_states += 1

            count += 1

        return states, go_to
