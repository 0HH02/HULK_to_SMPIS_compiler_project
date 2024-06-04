"""

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
