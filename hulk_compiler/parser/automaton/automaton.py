"""
"""

from .automaton_exceptions import (
    TransitionAlreadyExistsException,
    StateNotInAutomatonException,
    StuckAutomatonException,
)


class AutomatonState:
    """
    Represents a state in an automaton.

    Attributes:
        value (any): The value associated with the state.
        transitions (dict[str, AutomatonState]): A dictionary of transitions from the state
            to other states in the automaton.
    """

    def __init__(self, value, transitions):
        self.value = value
        self.transitions: dict[str, AutomatonState] = transitions


class Automaton:
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

    def __init__(
        self,
        states: list[AutomatonState],
        initial_state: AutomatonState,
        final_states: list[AutomatonState],
    ) -> None:
        self.states: list[AutomatonState] = states
        self.initial_state: AutomatonState = initial_state
        self.final_states: list[AutomatonState] = final_states
        self.current_state: AutomatonState = initial_state
        self.states_stack: list[AutomatonState] = []

    def reset(self):
        """
        Resets the automaton to its initial state.
        """
        self.current_state = self.initial_state
        self.states_stack.clear()

    def consume(self, char: str) -> AutomatonState:
        """
        Consumes a character and transitions to the next state based on thecurrent state and the
        character.

        Args:
            char (str): The character to consume.

        Returns:
            AutomatonState: The next state after consuming the character.

        Raises:
            StuckAutomatonException: If there is no transition available for thecurrent state and
            the character.
        """
        if char in self.current_state.transitions:
            self.current_state = self.current_state.transitions[char]
            self.states_stack.append(self.current_state)
            return self.current_state
        else:
            raise StuckAutomatonException(self.current_state, char)

    def go_back(self, value: int) -> None:
        """
        Goes back a specified number of states in the automaton's execution history.

        Args:
            value (int): The number of states to go back.

        Raises:
            IndexError: If the value is greater than the number of states in the execution history.
        """
        for _ in range(value):
            self.states_stack.pop()
        self.current_state = self.states_stack[-1]

    def has_transition(self, char: str) -> bool:
        """
        Checks if there is a transition available for the current state and the character.

        Args:
            char (str): The character to check for a transition.

        Returns:
            bool: True if there is a transition available, False otherwise.
        """
        return char in self.current_state.transitions

    def add_transition(
        self, state: AutomatonState, char: str, next_state: AutomatonState
    ) -> None:
        """
        Adds a transition from a state to the next state for a given character.

        Args:
            state (AutomatonState): The current state.
            char (str): The character triggering the transition.
            next_state (AutomatonState): The next state after the transition.

        Raises:
            StateNotInAutomatonException: If the current state is not in the automaton.
            TransitionAlreadyExistsException: If a transition already exists for the current
            state and the character.
        """
        if state not in self.states:
            raise StateNotInAutomatonException(state)

        if char in self.states[char]:
            raise TransitionAlreadyExistsException(state, char, next_state)

        self.states[char] = next_state

    @property
    def get_current_state(self) -> AutomatonState:
        """
        Returns the current state of the automaton.
        """
        return self.current_state
