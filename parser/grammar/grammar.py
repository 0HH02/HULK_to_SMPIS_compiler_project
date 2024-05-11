"""
This Module define the Grammar class and its related classes used in parsing.
"""


class Grammar:
    """
    Represents a grammar used in parsing.

    Attributes:
        start_symbol: The start symbol of the grammar.
        terminals: A list of terminal symbols in the grammar.
        non_terminals: A list of non-terminal symbols in the grammar.
        productions: A dictionary mapping non-terminal symbols
        to their corresponding production rules.
    """

    def __init__(self):
        self.start_symbol = None
        self.terminals = []
        self.non_terminals = []
        self.productions: dict[NonTerminal, SentenceList] = {}


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
        return Sentence([self, other])

    def is_terminal(self):
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

    def __rshift__(self, other):
        """
        Defines a production for the non-terminal symbol.

        Args:
            other (Symbol or Sentence): The symbol or sentence to be added to the production.

        Raises:
            TypeError: If the `other` argument is not an instance of `Symbol` or `Sentence`.
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
            return self
        if isinstance(other, Sentence):
            self._symbols.extend(other._symbols)
            return self
        raise TypeError("Invalid type for Sentence addition")

    def __or__(self, other):
        if isinstance(other, Symbol):
            return SentenceList([self, Sentence([other])])
        if isinstance(other, Sentence):
            return SentenceList([self, other])

        raise TypeError("Invalid type for Sentence or")

    def __len__(self) -> int:
        return len(self._symbols)


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

    def __or__(self, other):
        self._sentences.append(other)
        return self

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
