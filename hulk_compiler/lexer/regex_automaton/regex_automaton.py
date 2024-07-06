"""
"""

from collections import deque
from multipledispatch import dispatch
from .regex_grammar import get_regex_grammar
from ..token import Token, RegexTokenType
from ...parser.parser_lr1 import ParserLR1
from .regex_ast import (
    AnyCharNode,
    ConcatNode,
    GroupNode,
    LiteralCharNode,
    EpsilonNode,
    OrNode,
    PlusNode,
    RepeatNode,
)

# pylint: disable=function-redefined

VOCABULARY_ASCII: list[str] = [chr(v) for v in range(32, 126)]


class RegexAutomaton:

    def __init__(self, regex_pattern: str) -> None:
        self.initial_state: AutomatonState = self._compile_regex_pattern(regex_pattern)

    def match(self, string: str):
        actual_state: AutomatonState = self.initial_state

        for char in string:
            if char in actual_state.transitions:
                actual_state = actual_state.transitions[char]
            else:
                break

        return actual_state.final

    def _compile_regex_pattern(self, regex_pattern: str) -> "AutomatonState":

        tokens: list[Token] = self._tokenize_regex_pattern(regex_pattern)
        grammar, mapping = get_regex_grammar()
        parser = ParserLR1(grammar, mapping)
        regex_ast = parser.parse(tokens)
        start_state = AutomatonState(0)
        NFAStateBuilder.build_state(regex_ast, set([start_state]))
        self._search_final_states(set([start_state]))
        return self._to_deterministic(start_state)

    def _search_final_states(self, states: set["AutomatonState"]):

        for state in states:
            self._search_final_states(state.epsilon_transitions)
            for t_set in state.transitions.values():
                for transition in t_set:
                    if transition != state:
                        self._search_final_states(t_set)

            if self._is_final_state(state):
                state.set_as_final()

    def _is_final_state(self, state: "AutomatonState") -> bool:

        transition: bool = True
        for transition_set in state.transitions.values():
            for transition in transition_set:
                if transition is not state:
                    transition = False

        for epsilon_node in state.epsilon_transitions:
            if epsilon_node.final:
                return True

        return len(state.epsilon_transitions) == 0 and transition

    def _to_deterministic(self, initial_state: "AutomatonState"):

        num_state = 0
        initial_clousure: set[AutomatonState] = initial_state.epsilon_clousure()
        initial_state = AutomatonState(
            num_state, any(state.final for state in initial_clousure)
        )

        clousures = [initial_clousure]
        states = [initial_state]
        pending = [initial_state]

        while pending:
            state: AutomatonState = pending.pop()
            symbols: set[str] = {symbol for symbol in state.transitions}
            for symbol in symbols:
                clousure = state.epsilon_clousure()
                for st in state.move_to_states(symbol):
                    clousure = clousure.union(st.epsilon_clousure())

                if clousure not in clousures:
                    new_state = AutomatonState(
                        num_state, any(st.final for st in clousure)
                    )
                    num_state += 1
                    clousures.append(clousure)
                    states.append(new_state)
                    pending.append(new_state)
                else:
                    index = clousures.index(clousure)
                    new_state = states[index]

                state.add_transition(symbol, new_state)

        return initial_state

    def _tokenize_regex_pattern(self, regex_pattern: str) -> list[Token]:

        tokens: list[Token] = []
        special: bool = False

        for char in regex_pattern:

            if special:
                special = False
                if char == "d":
                    tokens.extend(self._tokenize_regex_pattern("[0-9]")[:-1])
                elif char == "w":
                    tokens.extend(self._tokenize_regex_pattern("[A-Za-z0-9]")[:-1])
                else:
                    tokens.append(Token(char, RegexTokenType.SYMBOL))
                continue

            if char == "\\":
                special = True
                continue

            match char:

                case "^":
                    if tokens[-1].token_type == RegexTokenType.LBRACKET:
                        next_token = Token(char, RegexTokenType.NOT)
                    else:
                        next_token = Token(char, RegexTokenType.LINE_START)

                case "{":
                    next_token = Token(char, RegexTokenType.LBRACE)
                case "}":
                    next_token = Token(char, RegexTokenType.RBRACE)
                case "$":
                    next_token = Token(char, RegexTokenType.STRING_END)
                case "+":
                    next_token = Token(char, RegexTokenType.PLUS)
                case "|":
                    next_token = Token(char, RegexTokenType.OR)
                case "?":
                    next_token = Token(char, RegexTokenType.OPTIONAL)
                case "-":
                    next_token = Token(char, RegexTokenType.RANGE)
                case ".":
                    next_token = Token(char, RegexTokenType.DOT)
                case "(":
                    next_token = Token(char, RegexTokenType.LPAREN)
                case ")":
                    next_token = Token(char, RegexTokenType.RPAREN)
                case "[":
                    next_token = Token(char, RegexTokenType.LBRACKET)
                case "]":
                    next_token = Token(char, RegexTokenType.RBRACKET)
                case _:
                    if char.isdigit():
                        next_token = Token(char, RegexTokenType.NUMBER)
                    elif char.isalpha():
                        next_token = Token(char, RegexTokenType.LETTER)
                    else:
                        next_token = Token(char, RegexTokenType.SYMBOL)

            tokens.append(next_token)

        tokens.append(Token("$", RegexTokenType.EOF))
        return tokens


class AutomatonState:

    def __init__(self, id_: int, final: bool = False) -> None:
        self.id = id_
        self.final: bool = final
        self.transitions: dict[str, set[AutomatonState]] = {}
        self.epsilon_transitions: set[AutomatonState] = set()

    def set_as_final(self):
        self.final = True

    def add_epsilon_transition(self, state: "AutomatonState"):
        if state not in self.epsilon_transitions:
            self.epsilon_transitions.add(state)
        else:
            print("An state can't hace two epsilon transition to the same node")

    def add_transition(self, char: str, state: "AutomatonState"):
        if char not in self.transitions:
            self.transitions[char] = set([state])
        else:
            self.transitions[char].add(state)

    def epsilon_clousure(self):
        pendings = deque([self])
        epsilon_clousure = set([self])

        while len(pendings) > 0:
            actual_state = pendings.pop()
            for epsilon_t in actual_state.epsilon_transitions:
                pendings.append(epsilon_t)
                epsilon_clousure.add(epsilon_t)

        return epsilon_clousure

    def move_to_states(self, symbol: str):
        states: set[AutomatonState] = set()
        for key, transition in self.transitions.items():
            if key == symbol:
                states = states.union(transition)

        return states

    def __hash__(self) -> int:
        return self.id.__hash__()


class NFAStateBuilder:

    @staticmethod
    @dispatch(LiteralCharNode, set)
    def build_state(
        node: LiteralCharNode, previous_states: set[AutomatonState]
    ) -> set[AutomatonState]:
        new_state = AutomatonState(max([state.id for state in previous_states]) + 1)
        for previous in previous_states:
            previous.add_transition(node.value, new_state)

        return set([new_state])

    @staticmethod
    @dispatch(GroupNode, set)
    def build_state(
        node: GroupNode, previous_states: set[AutomatonState]
    ) -> set[AutomatonState]:
        new_state = AutomatonState(max([state.id for state in previous_states]) + 1)
        if node.negative:
            for char in VOCABULARY_ASCII:
                if char not in node.values:
                    for previous in previous_states:
                        previous.add_transition(char, new_state)
        else:
            for value in node.values:
                for previous in previous_states:
                    previous.add_transition(value, new_state)

        return set([new_state])

    @staticmethod
    @dispatch(OrNode, set)
    def build_state(
        node: OrNode, previous_states: set[AutomatonState]
    ) -> set[AutomatonState]:

        start_state = AutomatonState(max([state.id for state in previous_states]) + 1)
        next_states: set[AutomatonState] = set()

        for previous in previous_states:
            previous.add_epsilon_transition(start_state)

        for nod in node.nodes:
            next_states = next_states.union(
                NFAStateBuilder.build_state(nod, set([start_state]))
            )

        return next_states

    @staticmethod
    @dispatch(ConcatNode, set)
    def build_state(node: ConcatNode, previous_states: set[AutomatonState]):
        actual_states: set[AutomatonState] = NFAStateBuilder.build_state(
            node.expressions[0], previous_states
        )
        states: list[set[AutomatonState]] = [actual_states]

        for nod in node.expressions[1:]:
            actual_states = NFAStateBuilder.build_state(nod, actual_states)
            states.append(actual_states)

        return states[-1]

    @staticmethod
    @dispatch(PlusNode, set)
    def build_state(node: PlusNode, previous_states: set[AutomatonState]):
        actual_states: set[AutomatonState] = NFAStateBuilder.build_state(
            node.child, previous_states
        )
        for state in previous_states:
            for transition in state.transitions:
                for state in actual_states:
                    state.add_transition(transition, state)

        return actual_states

    @staticmethod
    @dispatch(EpsilonNode, set)
    def build_state(_: EpsilonNode, previous_states: set[AutomatonState]):

        new_state = AutomatonState(max([state.id for state in previous_states]) + 1)
        for state in previous_states:
            state.add_epsilon_transition(new_state)

        return set([new_state])
