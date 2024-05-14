"""
"""

from .automaton import AutomatonState


class AutomatonException(Exception):
    """
    Base exception class for automaton-related errors.
    """

    def __init__(self, *args):
        super().__init__(*args)


class TransitionAlreadyExistsException(AutomatonException):
    """
    Exception raised when a transition already exists in an automaton.

    Args:
        state (AutomatonState): The state where the transition already exists.
        char (str): The character associated with the transition.
        transition_next_state (AutomatonState): The state that the transition leads to.
        args: Additional arguments to be passed to the base class constructor.
    """

    def __init__(
        self,
        state: AutomatonState,
        char: str,
        transition_next_state: AutomatonState,
        *args,
    ):
        print(
            f"""Transition already exists at state {state.value} 
            with char {char} to state {transition_next_state.value}"""
        )
        super().__init__(*args)


class StateNotInAutomatonException(AutomatonException):
    """
    Exception raised when a state is not present in the automaton.

    Attributes:
        state (AutomatonState): The state that is not present in the automaton.
    """

    def __init__(self, state: AutomatonState, *args):
        print(f"State {state.value} not in automaton")
        super().__init__(*args)


class StuckAutomatonException(AutomatonException):
    """
    Exception raised when the automaton gets stuck.

    Attributes:
        state (AutomatonState): The state where the automaton got stuck.
        char (str): The character that caused the automaton to get stuck.
    """

    def __init__(self, state: AutomatonState, char: str, *args):
        print(f"Automaton got stuck at state {state.value} with char {char}")
        super().__init__(*args)
