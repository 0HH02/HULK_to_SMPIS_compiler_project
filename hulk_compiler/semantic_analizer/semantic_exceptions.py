"""
This module contains the exceptions raised by the semantic analyzer.
"""


class RedefineException(Exception):
    """
    Exception raised when attempting to redefine a type with the same name in the context.

    Attributes:
        type_t (str): The type being redefined.
        name (str): The name of the type being redefined.
    """

    def __init__(self, type_t, name):
        print(type_t, " with the same name (", name, ") already in context.")
        super().__init__()


class NotDeclaredTypeException(Exception):
    """
    Exception raised when attempting to use a type that has not been declared.

    Attributes:
        name (str): The name of the type being used.
    """

    def __init__(self, name):
        print("Type ", name, " has not been declared.")
        super().__init__()


class NotDeclaredVariableException(Exception):
    """
    Exception raised when attempting to use a variable that has not been declared.

    Attributes:
        name (str): The name of the variable being used.
    """

    def __init__(self, name):
        print("Variable ", name, " has not been declared.")
        super().__init__()


class InvalidDeclarationException(Exception):
    """
    Exception raised when attempting to declare a variable with an invalid type.

    Attributes:
        name (str): The name of the variable being declared.
    """

    def __init__(self, name):
        print("Variable ", name, " has an invalid type.")
        super().__init__()


class InferTypeException(Exception):
    """
    Exception raised when the type of a expression cannot be inferred.
    """
