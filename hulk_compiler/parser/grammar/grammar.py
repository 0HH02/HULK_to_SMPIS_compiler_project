"""
This Module define the Grammar class and its related classes like 
Symbol : Represents a symbol in a grammar.
NonTerminal : Represents a non-terminal symbol in a grammar.
Terminal : Represents a terminal symbol in a grammar
Sentence : Represents a list of Symbols
used in parsing.
"""

from copy import deepcopy
from typing import Iterator


class Grammar:
    """
    Represents a grammar used in parsing, this grammar don't have epsilon symbol.

    Attributes:
        start_symbol: The start symbol of the grammar.
        terminals: A list of terminal symbols in the grammar.
        non_terminals: A list of non-terminal symbols in the grammar.
        productions: A dictionary mapping non-terminal symbols
        to their corresponding production rules.
    """

    def __init__(self):
        eof = Symbol("$", self)
        self.special_seed = Symbol("S'", self)
        self.eof = eof
        self.seed: NonTerminal = None
        self.terminals: list[Symbol] = [eof]
        self.non_terminals: list[NonTerminal] = []
        self.productions: dict[NonTerminal, SentenceList] = {}

    def set_terminals(self, values: list[str]):
        """
        Add a terminal symbol to the grammar.

        Args:
            value (str): The value of the terminal symbol.
        """

        new_terminals: list[Symbol] = [Symbol(value, self) for value in values]
        self.terminals.extend(new_terminals)

        return tuple(new_terminals)

    def set_non_terminals(self, values: list[str]):
        """
        Add a non-terminal symbol to the grammar.

        Args:
            value (str): The value of the non-terminal symbol.
        """
        new_non_terminals: list[NonTerminal] = [
            NonTerminal(value, self) for value in values
        ]
        self.non_terminals.extend(new_non_terminals)

        return tuple(new_non_terminals)

    def set_seed(self, seed):
        """
        Sets the seed  or the distinguished for the grammar.

        Parameters:
        - seed: The NonTerminal distinguished to set for the grammar.
        """
        if not self.seed is None and not seed in self.non_terminals:
            self.non_terminals.append(seed)
        self.seed = seed

    @property
    def symbols(self):
        """
        Returns a list of all symbols in the grammar, including terminals and non-terminals.
        """
        return [*self.terminals, *self.non_terminals]

    @property
    def num_symbols(self) -> int:
        """
        Returns the total amount of symbols in the grammar.
        """
        return len(self.terminals) + len(self.non_terminals)


class Symbol:
    """
    Represents a symbol in a grammar.

    Args:
        value (str): The value of the symbol.
        grammar (Grammar): The grammar to which this symbol belongs.
    """

    def __init__(self, value: str, grammar: Grammar):
        self.value: str = value
        self.grammar = grammar

    def __add__(self, other):
        return Sentence([self]).__add__(other)

    def __or__(self, other):
        return SentenceList([Sentence([self])]).__or__(other)

    def __invert__(self):
        return SentenceList([Sentence([self]), Sentence([])])

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Symbol):
            return self.value == other.value

        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__()

    def is_terminal(self) -> bool:
        """
        Check if the current grammar symbol is a terminal.

        Returns:
            bool : True if the grammar symbol is a terminal, False otherwise.
        """
        return self in self.grammar.terminals


class NonTerminal(Symbol):
    """
    Represents a non-terminal symbol in a grammar.

    Non-terminal symbols are symbols that can be expanded into one or more
    sentences in a grammar. This class provides methods to define productions
    for non-terminal symbols.
    """

    def __le__(self, other):
        """
        Defines a production for the non-terminal symbol.

        Args:
            other (Symbol or Sentence): The symbol or sentence to be added to the production.

        Raises:
            TypeError: If the `other` argument is not an instance of `Symbol`,`Sentence` or
            `SentenceList`.
        """
        if isinstance(other, Symbol):
            if not self.grammar.productions.__contains__(self):
                self.grammar.productions[self] = SentenceList([Sentence([other])])
            else:
                self.grammar.productions[self].append(Sentence([other]))

        if isinstance(other, Sentence):
            if not self.grammar.productions.__contains__(self):
                self.grammar.productions[self] = SentenceList([other])
            else:
                self.grammar.productions[self].append(other)

        if isinstance(other, SentenceList):
            if not self.grammar.productions.__contains__(self):
                self.grammar.productions[self] = other
            else:
                self.grammar.productions[self].append(other)


class Sentence:
    """
    Represents a sentence in the grammar.

    A sentence is a sequence of symbols.

    Attributes:
        _symbols (list[Symbol]): The list of symbols in the sentence.
    """

    def __init__(self, symbols: list[Symbol]):
        self._symbols: list[Symbol] = symbols

    def __add__(self, other):
        if isinstance(other, Symbol):
            self._symbols.append(other)
        elif isinstance(other, Sentence):
            self._symbols.extend(other._symbols)
        elif isinstance(other, SentenceList):
            sentence_list = SentenceList([])
            for sentence in other:
                self_sentence = deepcopy(self)
                sentence_list.append(self_sentence.extend(sentence._symbols))
            return sentence_list
        return self

    def __invert__(self):
        return SentenceList([self, Sentence([])])

    def __eq__(self, other: object) -> bool:
        return self._symbols == other._symbols

    def __or__(self, other) -> "SentenceList":
        return SentenceList([self]).__or__(other)

    def __iter__(self) -> Iterator[Symbol]:
        return iter(self._symbols)

    def __len__(self) -> int:
        return len(self._symbols)

    def __getitem__(self, key: int) -> Symbol:
        return self._symbols[key]

    def __str__(self) -> str:
        return self._symbols.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def append(self, item):
        """
        Appends the given object to the list of symbols in the sentence.

        Args:
            item: The object to be appended.

        Returns:
            self: The Sentence object after appending the object.
        """
        self._symbols.append(item)

    def extend(self, items):
        """
        Extends the list of symbols in the sentence with the given list of items.

        Args:
            items (list[Symbol]): The list of items to be appended.

        Returns:
            self: The Sentence object after extending the list of symbols.
        """
        self._symbols.extend(items)
        return self

    @property
    def first(self) -> Symbol:
        """
        Returns the first Symbol of the Sentence
        """
        return self._symbols[0]


class SentenceList:
    """
    Represents a list of sentences.

    Args:
        sentences (list[Sentence]): The list of sentences.

    Attributes:
        _sentences (list[Sentence]): The internal list of sentences.

    """

    def __init__(self, sentences: list[Sentence]):
        self._sentences: list[Sentence] = sentences

    def __len__(self) -> int:
        return len(self._sentences)

    def __iter__(self):
        return iter(self._sentences)

    def __add__(self, other):
        if isinstance(other, Sentence):
            for sentence in self._sentences:
                sentence.extend(other)
        elif isinstance(other, Symbol):
            for sentence in self._sentences:
                sentence.append(other)
        elif isinstance(other, SentenceList):
            new_sentence_list = SentenceList([])
            for sentence in self._sentences:
                for other_sentence in other:
                    self_sentence = deepcopy(sentence)
                    new_sentence_list.append(self_sentence.extend(other_sentence))
            return new_sentence_list

        return self

    def __or__(self, other):
        if isinstance(other, Sentence):
            self._sentences.append(other)
        elif isinstance(other, Symbol):
            self._sentences.append(Sentence([other]))
        return self

    def __str__(self) -> str:
        return self._sentences.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def append(self, other):
        """
        Appends the given object to the list of sentences in the grammar.

        Args:
            other: The object to be appended.

        Returns:
            self: The Grammar object after appending the object.
        """
        self._sentences.append(other)
        return self
