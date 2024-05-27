"""
This Module contains the Automaton for compile the grammar for the parser,
Build the Action Table and the Goto Table
"""

from hulk_compiler.parser.grammar.grammar import Symbol


from ..grammar.grammar_utils import Item, GrammarUtils
from ..grammar.grammar import Grammar, Sentence
from ..parsing_action import ParsingAction, Shift, Accept, Reduce


class ParserAutomatonState:
    """
    Represents a state in an automaton.

    Attributes:
        value (any): The value associated with the state.
        transitions (dict[str, AutomatonState]): A dictionary of transitions from the state
            to other states in the automaton.
    """

    def __init__(self, items: set[Item]):
        self.items: set[Item] = items

    def __len__(self) -> int:
        return len(self.items)

    def __str__(self) -> str:
        return f"""Items : {self.items} """

    def __repr__(self) -> str:
        return self.__str__()


class ParserAutomaton:
    """
    Represents an automaton with states, transitions, and current state.

    Attributes:
        states (list[AutomatonState]): The list of states in the automaton.
        initial_state (AutomatonState): The initial state of the automaton.
        final_states (list[AutomatonState]): The list of final states in the automaton.
        current_state (AutomatonState): The current state of the automaton.
        states_stack (list[AutomatonState]): The stack of states visited during the automaton
        execution.
    """

    def __init__(self, grammar: Grammar) -> None:
        self._grammar: Grammar = grammar
        self._firsts: dict[Symbol, set[Symbol]] = GrammarUtils.get_firsts(grammar)
        self._states: dict[int, ParserAutomatonState] = {}
        self._go_to: dict[int, dict[Symbol, int]] = {}
        self._action_table: dict[int, dict[Symbol, ParsingAction]] = {}
        self._build_action_table()

    def _build_states(self) -> None:
        """
        ### Builds the states of the parser automaton.

        This method constructs the states of the parser automaton by iteratively
        expanding the kernel items and computing the closure of each state.

        ## Returns:
            None
        """
        init_item = Item(
            self._grammar.special_seed,
            Sentence([self._grammar.seed]),
            0,
            self._grammar.eof,
        )

        actual_state = ParserAutomatonState(
            GrammarUtils.get_clousure(
                self._grammar,
                {init_item},
                self._firsts,
            ),
        )

        num_states: int = 1

        self._states[0] = actual_state

        kernels: dict[frozenset[Item], int] = {init_item: 0}

        count: int = 0

        while count < num_states:
            actual_state: ParserAutomatonState = self._states[count]

            for symbol in self._grammar.symbols:
                new_kernel: set[Item] = set()
                for item in actual_state.items:
                    if item.next_symbol == symbol:
                        new_kernel.add(item)

                if len(new_kernel) == 0:
                    continue

                f_new_kernel = frozenset(new_kernel)

                if f_new_kernel in kernels:

                    if count in self._go_to:
                        self._go_to[count][symbol] = kernels[f_new_kernel]
                    else:
                        self._go_to[count] = {symbol: kernels[f_new_kernel]}

                    continue

                kernels[f_new_kernel] = num_states

                new_state = ParserAutomatonState(
                    GrammarUtils.get_clousure(
                        self._grammar,
                        {item.move_dot() for item in new_kernel},
                        self._firsts,
                    ),
                )

                self._states[num_states] = new_state

                if count in self._go_to:
                    self._go_to[count][symbol] = num_states
                else:
                    self._go_to[count] = {symbol: num_states}

                num_states += 1

            count += 1

    def _build_action_table(self) -> None:

        pass

    @property
    def states_count(self) -> int:
        """
        Returns the number of states in the automaton.

        Returns:
            int: The number of states in the automaton.
        """
        return len(self._states)
