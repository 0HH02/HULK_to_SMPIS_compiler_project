"""
This Module contains the Parser of the Hulk Compiler
"""

from collections import deque
from hulk_compiler.lexer.token import Token
from .grammar.grammar import Grammar, Symbol
from .grammar.grammar_utils import GrammarUtils, Item
from .ast.ast import ASTNode
from .parsing_action import ParsingAction, Shift, Reduce, Accept, GoTo
from .parser_exceptions import ConflictActionError, ParsingError


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

    def __init__(self, grammar: Grammar, mapping):
        self._grammar = grammar
        self._mapping = mapping
        self._action_table: dict[int, dict[Symbol, ParsingAction]] = (
            self._compile_grammar()
        )

    def __str__(self) -> str:
        string = ""
        for state, dct in self._action_table.items():
            string += f"State {state}\n"
            for symbol, action in dct.items():
                string += f"\t{symbol} -> {action}\n"
        return string

    def __repr__(self) -> str:
        return self.__str__()

    def parse(self, tokens: list[Token]) -> ASTNode:
        """
        #### Parses the input tokens and returns the generated Abstract Syntax Tree (AST).

        ### Args:
            automaton: The automaton used for parsing.
            tokens (list[Token]): The list of tokens to be parsed.

        ### Returns:
            AST: The generated Abstract Syntax Tree (AST).
        """
        tokens = [(self._mapping[token.token_type], token) for token in tokens]
        token_stack: deque[(Symbol, any)] = deque()
        state_stack: deque[int] = deque()
        state_stack.append(0)
        derivations: list[tuple] = []
        i = 0
        while True:
            state = state_stack[-1]
            token = tokens[i]
            action: ParsingAction = self._action_table[state][token[0]]
            if isinstance(action, Shift):
                token_stack.append(token)
                state_stack.append(action.next_state)
                i += 1
            elif isinstance(action, Reduce):
                derivations.append((action.head, action.body))
                body_token_values = [
                    token_stack.pop()[1] for _ in range(len(action.body))
                ]
                body_token_values.reverse()

                value = action.body.attributation(body_token_values)

                for _ in range(len(action.body)):
                    state_stack.pop()
                token_stack.append((action.head, value))

                state: int = state_stack[-1]
                go_to: ParsingAction = self._action_table[state][action.head]
                if isinstance(go_to, GoTo):
                    state_stack.append(go_to.next_state)
            elif isinstance(action, Accept):
                derivations.append((self._grammar.seed, action.body))
                body_token_values = [
                    token_stack.pop()[1] for _ in range(len(action.body))
                ]
                body_token_values.reverse()

                return action.body.attributation(body_token_values)
            else:
                raise ParsingError(
                    f"Invalid parsing-action in action table row : {state}, column : {token[0]}"
                )

    def _compile_grammar(self) -> dict[int, dict[Symbol, ParsingAction]]:
        """
        Compiles the grammar rules into an action table.

        Returns:
            list[dict[Symbol, ParsingAction]]: The compiled action table.
        """

        states, go_to_table = self._build_states()

        action_table: dict[int, dict[Symbol, ParsingAction]] = {}

        for num_state, state_items in states.items():
            action_table[num_state] = {}
            state = action_table[num_state]
            for item in state_items:
                if item.can_reduce:
                    if item.head == self._grammar.seed:
                        if self._grammar.eof not in state:
                            state[self._grammar.eof] = Accept(item.body)
                        else:
                            raise ConflictActionError(
                                num_state, self._grammar.eof, state[self._grammar.eof]
                            )

                    else:
                        if item.lookahead not in state:
                            state[item.lookahead] = Reduce(item.head, item.body)
                        else:
                            raise ConflictActionError(
                                num_state, item.lookahead, state[item.lookahead]
                            )
                else:
                    if item.next_symbol.is_terminal():
                        if item.next_symbol not in state:
                            state[item.next_symbol] = Shift(
                                go_to_table[num_state][item.next_symbol]
                            )

                    else:
                        if item.next_symbol not in state:
                            state[item.next_symbol] = GoTo(
                                go_to_table[num_state][item.next_symbol]
                            )

        return action_table

    def _build_states(self):
        firsts: dict[Symbol, set[Symbol]] = GrammarUtils.get_firsts(self._grammar)

        initial_items = {
            Item(self._grammar.seed, sentence, 0, self._grammar.eof)
            for sentence in self._grammar.productions[self._grammar.seed]
        }

        actual_state_items: set[Item] = GrammarUtils.get_clousure(
            self._grammar,
            initial_items,
            firsts,
        )

        num_states: int = 1

        states: dict[int, set[Item]] = {0: actual_state_items}

        states_kernels: dict[frozenset[Item], int] = {frozenset(initial_items): 0}

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

                frozen_new_kernel = frozenset(new_kernel)

                if frozen_new_kernel in states_kernels:
                    if count in go_to:
                        go_to[count][symbol] = states_kernels[frozen_new_kernel]
                    else:
                        go_to[count] = {symbol: states_kernels[frozen_new_kernel]}
                    continue

                new_items: set[Item] = GrammarUtils.get_clousure(
                    self._grammar,
                    {item.move_dot() for item in frozen_new_kernel},
                    firsts,
                )
                states[num_states] = new_items
                if count in go_to:
                    go_to[count][symbol] = num_states
                else:
                    go_to[count] = {symbol: num_states}

                states_kernels[frozen_new_kernel] = num_states

                num_states += 1

            count += 1

        return states, go_to
